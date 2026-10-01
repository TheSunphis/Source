#!/usr/bin/env python3
"""Germinal deterministic structural validator and packager. Standard library only."""
from __future__ import annotations
import argparse,base64,gzip,hashlib,io,json,os,sys,tarfile,urllib.error,urllib.request,subprocess,shutil
VERSION="germinal-tool-v7"
VALK_FORMAT="germinal-valkyrie-output-v1"
CROW_FORMAT="germinal-crow-review-v1"
VALK_CHECKPOINT_FORMAT="germinal-valkyrie-checkpoint-v2"
CROW_CHECKPOINT_FORMAT="germinal-crow-checkpoint-v2"
STATUSES={"submitted","abstained","failed"}
SEVERITIES={"critical","major","minor"}
class Problems:
 def __init__(self):self.items=[]
 def add(self,path,msg):self.items.append(f"{path}: {msg}")
 def need(self,cond,path,msg):
  if not cond:self.add(path,msg)
def canonical(obj):return (json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def sha(data):return hashlib.sha256(data).hexdigest()
def read_json(path):
 with open(path,"rb") as f:return json.load(f)
def read_ndjson(path):
 out=[]
 with open(path,"rb") as f:
  for n,b in enumerate(f,1):
   try:out.append(json.loads(b))
   except Exception as e:raise ValueError(f"line {n}: invalid JSON: {e}")
 return out
def records_bytes(records):return b"".join(canonical(x) for x in records)
def evidence_ok(x):
 return isinstance(x,dict) and all(isinstance(x.get(k),str) and x[k] for k in ("sourceId","artifact","locator","claimScope"))
def required_strings(p,obj,keys,problems):
 for k in keys:problems.need(isinstance(obj.get(k),str) and bool(obj[k]),f"{p}/{k}","required non-empty string")
def validate_line(p,line,problems):
 if not isinstance(line,dict):problems.add(p,"must be object");return
 required_strings(p,line,["lineId","japanese","reading","meaning"],problems)
 problems.need(isinstance(line.get("ttsEligible"),bool),p+"/ttsEligible","must be boolean")
 ev=line.get("evidence");problems.need(isinstance(ev,list) and ev and all(evidence_ok(x) for x in ev),p+"/evidence","requires evidence locators")
 segs=line.get("segments");problems.need(isinstance(segs,list) and bool(segs),p+"/segments","requires segments")
 if not isinstance(segs,list):return
 js=line.get("japanese","");rd=line.get("reading","");jparts=[];rparts=[];jpos=rpos=0
 for i,s in enumerate(segs):
  q=f"{p}/segments/{i}"
  if not isinstance(s,dict):problems.add(q,"must be object");continue
  required_strings(q,s,["segmentId","surface","reading","contextualMeaning","grammaticalRole","vocabularyDisposition"],problems)
  for k in ("japaneseStart","japaneseEnd","readingStart","readingEnd"):problems.need(isinstance(s.get(k),int),q+"/"+k,"must be integer")
  a,b=s.get("japaneseStart"),s.get("japaneseEnd");c,d=s.get("readingStart"),s.get("readingEnd")
  if all(isinstance(x,int) for x in (a,b)):
   problems.need(a==jpos,q+"/japaneseStart","segments must be contiguous")
   problems.need(0<=a<=b<=len(js),q,"Japanese span out of range")
   if 0<=a<=b<=len(js):problems.need(js[a:b]==s.get("surface"),q+"/surface","surface/span mismatch")
   jpos=b;jparts.append(s.get("surface", ""))
  if all(isinstance(x,int) for x in (c,d)):
   problems.need(c==rpos,q+"/readingStart","reading segments must be contiguous")
   problems.need(0<=c<=d<=len(rd),q,"reading span out of range")
   if 0<=c<=d<=len(rd):problems.need(rd[c:d]==s.get("reading"),q+"/reading","reading/span mismatch")
   rpos=d;rparts.append(s.get("reading", ""))
  for k in ("lemma","inflection"):problems.need(k in s,q+"/"+k,"required; use null when not applicable")
  vc=s.get("vocabularyCandidates");problems.need(isinstance(vc,list),q+"/vocabularyCandidates","must be list")
  selected=s.get("selectedVocabularyId");problems.need(selected is None or isinstance(selected,str),q+"/selectedVocabularyId","must be string or null")
  reason=s.get("unlinkedReason")
  if selected is None:problems.need(isinstance(reason,str) and bool(reason),q+"/unlinkedReason","required when no selected destination")
  sev=s.get("evidence");problems.need(isinstance(sev,list) and sev and all(evidence_ok(x) for x in sev),q+"/evidence","requires evidence locators")
 problems.need("".join(jparts)==js,p+"/segments","Japanese reconstruction failed")
 problems.need("".join(rparts)==rd,p+"/segments","reading reconstruction failed")
 problems.need(jpos==len(js),p+"/segments","Japanese spans do not cover line")
 problems.need(rpos==len(rd),p+"/segments","reading spans do not cover line")
def collect_line_refs(obj,path=""):
 refs=[]
 if isinstance(obj,dict):
  for k,v in obj.items():
   q=path+"/"+k
   if k.endswith("LineId") and isinstance(v,str):refs.append((q,v))
   elif k.endswith("LineIds") and isinstance(v,list):refs.extend((q+f"/{i}",x) for i,x in enumerate(v) if isinstance(x,str))
   elif k!="japaneseLines":refs.extend(collect_line_refs(v,q))
 elif isinstance(obj,list):
  for i,v in enumerate(obj):refs.extend(collect_line_refs(v,path+f"/{i}"))
 return refs
def validate_expression(p,e,problems):
 if not isinstance(e,dict):problems.add(p,"must be object");return
 required_strings(p,e,["expressionId","primaryLineId","category","usageSummary","verificationState"],problems)
 problems.need(e.get("verificationState")=="candidate",p+"/verificationState","must be candidate")
 problems.need(isinstance(e.get("kotoDifficulty"),int) and 1<=e.get("kotoDifficulty",0)<=5,p+"/kotoDifficulty","must be integer 1..5")
 for k in ("intentions","useWhen","takeCare","relationships","forms","responses","followUps","sources"):
  problems.need(isinstance(e.get(k),list) and bool(e[k]),p+"/"+k,"required non-empty list")
 for k in ("dialogue","patterns","distinctions","library","provenance"):
  problems.need(isinstance(e.get(k),dict),p+"/"+k,"required object")
 lines=e.get("japaneseLines");problems.need(isinstance(lines,dict) and bool(lines),p+"/japaneseLines","required non-empty map")
 if not isinstance(lines,dict):return
 for key,line in lines.items():
  validate_line(p+"/japaneseLines/"+str(key),line,problems)
  if isinstance(line,dict):problems.need(line.get("lineId")==key,p+"/japaneseLines/"+str(key)+"/lineId","must equal map key")
 refs=collect_line_refs(e,p)
 referenced=set()
 for q,r in refs:problems.need(r in lines,q,"unknown line reference");referenced.add(r)
 problems.need(e.get("primaryLineId") in lines,p+"/primaryLineId","unknown primary line")
 referenced.add(e.get("primaryLineId"))
 problems.need(set(lines)==referenced,p+"/japaneseLines","orphan or unreferenced lines exist")
 for s in e.get("sources",[]):problems.need(evidence_ok(s),p+"/sources","invalid source locator")
def validate_valkyrie(manifest,records):
 p=Problems();p.need(isinstance(manifest,dict),"/manifest","must be object")
 if not isinstance(manifest,dict):return p.items
 fmt=manifest.get("formatVersion")
 p.need(fmt in (VALK_FORMAT,VALK_CHECKPOINT_FORMAT),"/manifest/formatVersion","wrong format")
 p.need(manifest.get("agent")=="Valkyrie1","/manifest/agent","must be Valkyrie1")
 if fmt==VALK_FORMAT:
  p.need(manifest.get("assignment")=="germinal-wave001-valkyrie1-50","/manifest/assignment","wrong assignment")
  expected=[f"V1-W001-{i:03d}" for i in range(1,51)]
 else:
  p.need(manifest.get("assignment")=="germinal-wave002-valkyrie1-checkpoint01-5","/manifest/assignment","wrong checkpoint assignment")
  expected=[f"V1-W002-C01-{i:03d}" for i in range(1,6)]
  p.need(manifest.get("expectedSlotIds")==expected,"/manifest/expectedSlotIds","checkpoint slot identity mismatch")
 p.need(len(records)==len(expected),"/records",f"must contain exactly {len(expected)} records")
 p.need([x.get("slotId") if isinstance(x,dict) else None for x in records]==expected,"/records","slot IDs/order mismatch")
 counts={x:0 for x in STATUSES}
 for i,r in enumerate(records):
  q=f"/records/{i}"
  if not isinstance(r,dict):p.add(q,"must be object");continue
  st=r.get("status");p.need(st in STATUSES,q+"/status","invalid status")
  if st in counts:counts[st]+=1
  if st=="submitted":p.need("expression" in r,q+"/expression","required");validate_expression(q+"/expression",r.get("expression"),p)
  else:
   p.need(isinstance(r.get("reasonCode"),str) and bool(r["reasonCode"]),q+"/reasonCode","required")
   p.need("expression" not in r,q+"/expression","forbidden for non-submitted slot")
 p.need(manifest.get("attempted")==len(expected),"/manifest/attempted",f"must be {len(expected)}")
 for k,v in counts.items():p.need(manifest.get(k)==v,f"/manifest/{k}","count mismatch")
 p.need(sum(counts.values())==len(expected),"/manifest","count conservation failed")
 p.need(manifest.get("recordsSha256")==sha(records_bytes(records)),"/manifest/recordsSha256","digest mismatch")
 for k in ("inputAsset","evidenceBuild","candidateBuild"):p.need(k in manifest,"/manifest/"+k,"required")
 return p.items
def validate_crow(manifest,records):
 p=Problems();p.need(isinstance(manifest,dict),"/manifest","must be object")
 if not isinstance(manifest,dict):return p.items
 fmt=manifest.get("formatVersion")
 p.need(fmt in (CROW_FORMAT,CROW_CHECKPOINT_FORMAT),"/manifest/formatVersion","wrong format")
 p.need(manifest.get("agent")=="Crow1","/manifest/agent","must be Crow1")
 if fmt==CROW_FORMAT:
  p.need(manifest.get("assignment")=="germinal-wave001-crow1-review-50","/manifest/assignment","wrong assignment")
  expected=[f"V1-W001-{i:03d}" for i in range(1,51)]
 else:
  p.need(manifest.get("assignment")=="germinal-wave002-crow1-checkpoint01-review-5","/manifest/assignment","wrong checkpoint assignment")
  expected=[f"V1-W002-C01-{i:03d}" for i in range(1,6)]
  p.need(manifest.get("expectedSlotIds")==expected,"/manifest/expectedSlotIds","checkpoint slot identity mismatch")
 p.need(len(records)==len(expected),"/records",f"must contain exactly {len(expected)} records")
 p.need([x.get("slotId") if isinstance(x,dict) else None for x in records]==expected,"/records","slot IDs/order mismatch")
 counts={"pass":0,"quarantine":0}
 for i,r in enumerate(records):
  q=f"/records/{i}"
  if not isinstance(r,dict):p.add(q,"must be object");continue
  rec=r.get("recommendation");p.need(rec in counts,q+"/recommendation","invalid recommendation")
  if rec in counts:counts[rec]+=1
  checks=r.get("checks");findings=r.get("findings")
  p.need(isinstance(checks,dict) and bool(checks),q+"/checks","required non-empty object")
  p.need(isinstance(findings,list),q+"/findings","must be list")
  if rec=="pass":
   p.need(findings==[],q+"/findings","pass requires zero findings")
   if isinstance(checks,dict):p.need(all(v is True for v in checks.values()),q+"/checks","pass requires all true")
  if rec=="quarantine":p.need(isinstance(findings,list) and bool(findings),q+"/findings","quarantine requires finding")
  if isinstance(findings,list):
   for j,f in enumerate(findings):
    z=q+f"/findings/{j}"
    if not isinstance(f,dict):p.add(z,"must be object");continue
    required_strings(z,f,["severity","code","pointer","evidenceLocator","explanation","gate"],p)
    p.need(f.get("severity") in SEVERITIES,z+"/severity","invalid severity")
 p.need(manifest.get("attempted")==len(expected) and manifest.get("reviewed")==len(expected),"/manifest",f"attempted/reviewed must be {len(expected)}")
 p.need(manifest.get("pass")==counts["pass"],"/manifest/pass","count mismatch")
 p.need(manifest.get("quarantine")==counts["quarantine"],"/manifest/quarantine","count mismatch")
 p.need(sum(counts.values())==len(expected),"/manifest","count conservation failed")
 p.need(manifest.get("recordsSha256")==sha(records_bytes(records)),"/manifest/recordsSha256","digest mismatch")
 for k in ("evidenceAsset","valkyrieAsset","evidenceBuild","candidateBuild"):p.need(k in manifest,"/manifest/"+k,"required")
 return p.items
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):return None
def github_token():
 for name in ("GH_TOKEN","GITHUB_TOKEN"):
  value=os.environ.get(name)
  if value:return value.strip()
 try:
  return subprocess.check_output(["gh","auth","token"],text=True,stderr=subprocess.DEVNULL,timeout=10).strip()
 except Exception as e:raise RuntimeError("GitHub credential unavailable") from e
def signed_asset_url(owner,repo,asset_id,token):
 url=f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{asset_id}"
 req=urllib.request.Request(url,headers={"Authorization":f"Bearer {token}","Accept":"application/octet-stream","X-GitHub-Api-Version":"2022-11-28","User-Agent":"Germinal-Agent"})
 opener=urllib.request.build_opener(NoRedirect)
 try:
  r=opener.open(req,timeout=30);code=r.status;location=r.headers.get("Location");r.close()
 except urllib.error.HTTPError as e:
  code=e.code;location=e.headers.get("Location");e.close()
 if code not in (301,302,303,307,308) or not location:raise RuntimeError(f"asset redirect unavailable: HTTP {code}")
 return location
def fetch_release_asset(owner,repo,asset_id,expected_bytes,expected_sha,output,chunk_bytes=4*1024*1024,retries=5):
 if expected_bytes<1 or chunk_bytes<65536 or retries<1:raise ValueError("invalid bounded transfer parameters")
 token=github_token();part=output+".part"
 if os.path.exists(output):
  with open(output,"rb") as f:data=f.read()
  if len(data)==expected_bytes and sha(data)==expected_sha:return len(data),expected_sha
  os.remove(output)
 offset=os.path.getsize(part) if os.path.exists(part) else 0
 if offset>expected_bytes:os.remove(part);offset=0
 while offset<expected_bytes:
  end=min(expected_bytes-1,offset+chunk_bytes-1);need=end-offset+1;payload=None;last=None
  for _ in range(retries):
   try:
    location=signed_asset_url(owner,repo,asset_id,token)
    try:
     req=urllib.request.Request(location,headers={"Range":f"bytes={offset}-{end}","User-Agent":"Germinal-Agent"})
     with urllib.request.urlopen(req,timeout=60) as r:
      cr=r.headers.get("Content-Range","")
      if r.status!=206 or not cr.startswith(f"bytes {offset}-{end}/"):raise RuntimeError(f"unexpected range response: HTTP {r.status}")
      data=r.read(need)
      if len(data)!=need or r.read(1):raise EOFError(f"range length mismatch at byte {offset}")
     payload=data
    except Exception as python_tls_error:
     if not shutil.which("curl"):raise RuntimeError("Python TLS failed and curl fallback is unavailable") from python_tls_error
     cmd=["curl","--http1.1","--tlsv1.2","--fail","--silent","--show-error","--connect-timeout","30","--max-time","90","--range",f"{offset}-{end}",location]
     run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=100)
     if run.returncode!=0 or len(run.stdout)!=need:raise RuntimeError(f"curl range fallback failed at byte {offset}") from python_tls_error
     payload=run.stdout
    break
   except Exception as e:last=e;payload=None
  if payload is None:raise RuntimeError(f"bounded range transfer failed at byte {offset}: {type(last).__name__}") from last
  with open(part,"ab") as f:f.write(payload);f.flush();os.fsync(f.fileno())
  offset+=len(payload)
  print(json.dumps({"transfer":"progress","bytes":offset,"total":expected_bytes},sort_keys=True))
 z=hashlib.sha256();n=0
 with open(part,"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):z.update(b);n+=len(b)
 digest=z.hexdigest()
 if n!=expected_bytes or digest!=expected_sha:
  os.remove(part);raise RuntimeError("completed asset identity mismatch")
 os.replace(part,output);return n,digest
def fetch_release_body_bundle(owner,repo,release_ids,expected_bytes,expected_sha,output,retries=5):
 token=github_token();ids=[int(x) for x in release_ids.split(",") if x.strip()]
 if not ids or expected_bytes<1 or retries<1:raise ValueError("invalid private body-bundle parameters")
 parts={};bundle_name=None;declared_count=None
 for release_id in ids:
  obj=None;last=None
  for _ in range(retries):
   try:
    url=f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    req=urllib.request.Request(url,headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"Germinal-Agent"})
    with urllib.request.urlopen(req,timeout=60) as r:obj=json.loads(r.read())
    break
   except Exception as e:last=e;obj=None
  if obj is None:raise RuntimeError(f"private release metadata unavailable for release {release_id}: {type(last).__name__}") from last
  if not obj.get("draft"):raise RuntimeError(f"release {release_id} is not private draft metadata")
  try:chunk=json.loads(obj.get("body") or "")
  except Exception as e:raise RuntimeError(f"release {release_id} has invalid private chunk body") from e
  if chunk.get("format")!="germinal-private-body-chunk-v1":raise RuntimeError(f"release {release_id} has wrong chunk format")
  try:data=base64.b64decode(chunk["payloadBase64"],validate=True)
  except Exception as e:raise RuntimeError(f"release {release_id} has invalid base64") from e
  index=chunk.get("index");count=chunk.get("count")
  if not isinstance(index,int) or not isinstance(count,int) or not 1<=index<=count:raise RuntimeError(f"release {release_id} has invalid chunk index")
  if len(data)!=chunk.get("chunkBytes") or sha(data)!=chunk.get("chunkSha256"):raise RuntimeError(f"release {release_id} chunk identity mismatch")
  if chunk.get("bundleBytes")!=expected_bytes or chunk.get("bundleSha256")!=expected_sha:raise RuntimeError(f"release {release_id} bundle identity mismatch")
  if declared_count is None:declared_count=count;bundle_name=chunk.get("bundle")
  if count!=declared_count or chunk.get("bundle")!=bundle_name or index in parts:raise RuntimeError("inconsistent or duplicate private chunks")
  parts[index]=data;print(json.dumps({"privateChunk":"verified","index":index,"count":count},sort_keys=True))
 if declared_count!=len(ids) or set(parts)!=set(range(1,declared_count+1)):raise RuntimeError("private chunk set incomplete")
 payload=b"".join(parts[i] for i in range(1,declared_count+1))
 if len(payload)!=expected_bytes or sha(payload)!=expected_sha:raise RuntimeError("reconstructed private bundle identity mismatch")
 part=output+".part"
 with open(part,"wb") as f:f.write(payload);f.flush();os.fsync(f.fileno())
 os.replace(part,output);return len(payload),sha(payload),bundle_name
def github_api_json(owner,repo,path,token,method="GET",payload=None,retries=5):
 data=None if payload is None else json.dumps(payload,separators=(",",":")).encode();last=None
 for _ in range(retries):
  try:
   req=urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}{path}",data=data,method=method,headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","Content-Type":"application/json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"Germinal-Agent"})
   with urllib.request.urlopen(req,timeout=60) as r:
    body=r.read();return json.loads(body) if body else None
  except Exception as e:last=e
 raise RuntimeError(f"GitHub API {method} failed for safe endpoint: {type(last).__name__}") from last
def private_chunk_body(bundle_name,bundle,part,index,count):
 obj={"format":"germinal-private-body-chunk-v1","bundle":bundle_name,"index":index,"count":count,"chunkBytes":len(part),"chunkSha256":sha(part),"bundleBytes":len(bundle),"bundleSha256":sha(bundle),"payloadBase64":base64.b64encode(part).decode()}
 return json.dumps(obj,sort_keys=True,separators=(",",":"))
def upload_release_body_bundle(owner,repo,assignment,bundle_path,chunk_bytes=70000,retries=5):
 if chunk_bytes<16384 or chunk_bytes>80000:raise ValueError("private metadata chunk size out of bounds")
 token=github_token()
 with open(bundle_path,"rb") as f:bundle=f.read()
 if not bundle:raise ValueError("private output bundle is empty")
 digest=sha(bundle);parts=[bundle[i:i+chunk_bytes] for i in range(0,len(bundle),chunk_bytes)];slug="".join(ch if ch.isalnum() or ch=="-" else "-" for ch in assignment.lower()).strip("-")
 existing={};page=1
 while page<=10:
  rels=github_api_json(owner,repo,f"/releases?per_page=100&page={page}",token,retries=retries)
  for rel in rels:existing[rel.get("tag_name")]=rel
  if len(rels)<100:break
  page+=1
 ids=[]
 for i,part in enumerate(parts,1):
  tag=f"germinal-private-{slug}-{digest[:16]}-{i:03d}";body=private_chunk_body(os.path.basename(bundle_path),bundle,part,i,len(parts));rel=existing.get(tag)
  if rel:
   if not rel.get("draft") or rel.get("body")!=body:raise RuntimeError(f"existing private output chunk conflict at index {i}")
  else:
   rel=github_api_json(owner,repo,"/releases",token,"POST",{"tag_name":tag,"target_commitish":"Germinal","name":f"Germinal private output {i}/{len(parts)}","body":body,"draft":True,"prerelease":True,"generate_release_notes":False},retries)
  ids.append(rel["id"]);print(json.dumps({"privateOutputChunk":"stored","index":i,"count":len(parts),"releaseId":rel["id"]},sort_keys=True))
 return len(bundle),digest,ids
def validate_safe_report_text(text):
 if len(text.encode())>32768:raise ValueError("safe report exceeds 32 KiB")
 forbidden=("payloadBase64","Authorization: Bearer","oauth_token","<token>")
 if any(x in text for x in forbidden):raise ValueError("safe report contains forbidden material")
 for ch in text:
  o=ord(ch)
  if 0x3040<=o<=0x30ff or 0x3400<=o<=0x9fff:raise ValueError("safe report contains Japanese payload text")
 return True
def publish_safe_report(owner,repo,branch,path,report_file,message,retries=5):
 token=github_token()
 with open(report_file,"r",encoding="utf-8") as f:text=f.read()
 validate_safe_report_text(text)
 current=github_api_json(owner,repo,f"/contents/{path}?ref={branch}",token,retries=retries)
 result=github_api_json(owner,repo,f"/contents/{path}",token,"PUT",{"message":message,"content":base64.b64encode(text.encode()).decode(),"sha":current["sha"],"branch":branch},retries)
 return result["commit"]["sha"]
def deterministic_archive(manifest,records,records_name,out_path):
 members={"manifest.json":canonical(manifest),records_name:records_bytes(records)}
 raw=io.BytesIO()
 with gzip.GzipFile(fileobj=raw,mode="wb",filename="",mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode="w",format=tarfile.PAX_FORMAT) as tf:
   for name in sorted(members):
    data=members[name];ti=tarfile.TarInfo(name);ti.size=len(data);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644
    tf.addfile(ti,io.BytesIO(data))
 with open(out_path,"wb") as f:f.write(raw.getvalue())
 return len(raw.getvalue()),sha(raw.getvalue())
def self_test():
 if not shutil.which("curl"):raise RuntimeError("curl is required as the alternate TLS transport")
 probe=b"germinal-private-body-self-test"
 if base64.b64decode(base64.b64encode(probe),validate=True)!=probe:raise RuntimeError("base64 self-test failed")
 body=json.loads(private_chunk_body("probe.tar.gz",probe,probe,1,1))
 if base64.b64decode(body["payloadBase64"],validate=True)!=probe or body["bundleSha256"]!=sha(probe):raise RuntimeError("private output chunk self-test failed")
 validate_safe_report_text("# Safe report\n\n- Status: `submitted`\n")
 ev={"sourceId":"s","artifact":"a","locator":"l","claimScope":"c"}
 seg={"segmentId":"s1","surface":"x","reading":"y","japaneseStart":0,"japaneseEnd":1,"readingStart":0,"readingEnd":1,"contextualMeaning":"m","grammaticalRole":"r","lemma":None,"inflection":None,"vocabularyCandidates":[],"selectedVocabularyId":None,"vocabularyDisposition":"reviewed-unlinked","unlinkedReason":"none","evidence":[ev]}
 line={"lineId":"l1","japanese":"x","reading":"y","meaning":"m","ttsEligible":True,"evidence":[ev],"segments":[seg]}
 exp={"expressionId":"e","primaryLineId":"l1","category":"c","usageSummary":"u","verificationState":"candidate","kotoDifficulty":1,"intentions":["i"],"useWhen":["u"],"takeCare":["t"],"relationships":[{"context":"c","guidance":"g"}],"forms":[{"lineId":"l1"}],"responses":[{"lineId":"l1"}],"followUps":[{"lineId":"l1"}],"sources":[ev],"dialogue":{"targetLineId":"l1"},"patterns":{},"distinctions":{},"library":{},"provenance":{},"japaneseLines":{"l1":line}}
 rs=[{"slotId":f"V1-W001-{i:03d}","status":"submitted","expression":exp} for i in range(1,51)]
 m={"formatVersion":VALK_FORMAT,"agent":"Valkyrie1","assignment":"germinal-wave001-valkyrie1-50","attempted":50,"submitted":50,"abstained":0,"failed":0,"recordsSha256":sha(records_bytes(rs)),"inputAsset":{},"evidenceBuild":"e","candidateBuild":"c"}
 probs=validate_valkyrie(m,rs)
 if probs:raise RuntimeError("self-test failed: "+probs[0])
 crs=[]
 for i in range(1,6):
  item=json.loads(json.dumps(rs[i-1]));item["slotId"]=f"V1-W002-C01-{i:03d}";crs.append(item)
 cm={"formatVersion":VALK_CHECKPOINT_FORMAT,"agent":"Valkyrie1","assignment":"germinal-wave002-valkyrie1-checkpoint01-5","expectedSlotIds":[f"V1-W002-C01-{i:03d}" for i in range(1,6)],"attempted":5,"submitted":5,"abstained":0,"failed":0,"recordsSha256":sha(records_bytes(crs)),"inputAsset":{},"evidenceBuild":"e","candidateBuild":"c"}
 probs=validate_valkyrie(cm,crs)
 if probs:raise RuntimeError("checkpoint self-test failed: "+probs[0])
 return True
def main(argv=None):
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
 sub.add_parser("self-test")
 v=sub.add_parser("validate-valkyrie");v.add_argument("manifest");v.add_argument("records")
 c=sub.add_parser("validate-crow");c.add_argument("manifest");c.add_argument("records")
 g=sub.add_parser("package");g.add_argument("kind",choices=["valkyrie","crow"]);g.add_argument("manifest");g.add_argument("records");g.add_argument("output")
 s=sub.add_parser("sha256");s.add_argument("file")
 f=sub.add_parser("fetch-release-asset");f.add_argument("owner");f.add_argument("repo");f.add_argument("asset_id",type=int);f.add_argument("expected_bytes",type=int);f.add_argument("expected_sha");f.add_argument("output");f.add_argument("--chunk-bytes",type=int,default=4*1024*1024);f.add_argument("--retries",type=int,default=5)
 b=sub.add_parser("fetch-release-body-bundle");b.add_argument("owner");b.add_argument("repo");b.add_argument("release_ids");b.add_argument("expected_bytes",type=int);b.add_argument("expected_sha");b.add_argument("output");b.add_argument("--retries",type=int,default=5)
 u=sub.add_parser("upload-release-body-bundle");u.add_argument("owner");u.add_argument("repo");u.add_argument("assignment");u.add_argument("bundle");u.add_argument("--chunk-bytes",type=int,default=70000);u.add_argument("--retries",type=int,default=5)
 r=sub.add_parser("publish-safe-report");r.add_argument("owner");r.add_argument("repo");r.add_argument("branch");r.add_argument("path");r.add_argument("report_file");r.add_argument("message");r.add_argument("--retries",type=int,default=5)
 a=ap.parse_args(argv)
 if a.cmd=="self-test":self_test();print(VERSION+" self-test passed");return 0
 if a.cmd=="sha256":
  z=hashlib.sha256();n=0
  with open(a.file,"rb") as f:
   for b in iter(lambda:f.read(1024*1024),b""):z.update(b);n+=len(b)
  print(json.dumps({"bytes":n,"sha256":z.hexdigest()},sort_keys=True));return 0
 if a.cmd=="fetch-release-asset":
  n,d=fetch_release_asset(a.owner,a.repo,a.asset_id,a.expected_bytes,a.expected_sha,a.output,a.chunk_bytes,a.retries);print(json.dumps({"transfer":"complete","bytes":n,"sha256":d},sort_keys=True));return 0
 if a.cmd=="fetch-release-body-bundle":
  n,d,name=fetch_release_body_bundle(a.owner,a.repo,a.release_ids,a.expected_bytes,a.expected_sha,a.output,a.retries);print(json.dumps({"privateBodyBundle":"complete","bundle":name,"bytes":n,"sha256":d},sort_keys=True));return 0
 if a.cmd=="upload-release-body-bundle":
  n,d,ids=upload_release_body_bundle(a.owner,a.repo,a.assignment,a.bundle,a.chunk_bytes,a.retries);print(json.dumps({"privateOutputBundle":"stored","bytes":n,"sha256":d,"releaseIds":ids},sort_keys=True));return 0
 if a.cmd=="publish-safe-report":
  commit=publish_safe_report(a.owner,a.repo,a.branch,a.path,a.report_file,a.message,a.retries);print(json.dumps({"safeReport":"published","commit":commit},sort_keys=True));return 0
 m=read_json(a.manifest);r=read_ndjson(a.records);probs=validate_valkyrie(m,r) if (a.cmd=="validate-valkyrie" or getattr(a,"kind",None)=="valkyrie") else validate_crow(m,r)
 if probs:
  print(json.dumps({"status":"failed","problemCount":len(probs),"problems":probs[:200]},ensure_ascii=False,sort_keys=True));return 1
 if a.cmd=="package":
  name="slots.ndjson" if a.kind=="valkyrie" else "reviews.ndjson";n,d=deterministic_archive(m,r,name,a.output);print(json.dumps({"status":"packaged","bytes":n,"sha256":d},sort_keys=True))
 else:print(json.dumps({"status":"passed","records":len(r),"tool":VERSION},sort_keys=True))
 return 0
if __name__=="__main__":raise SystemExit(main())
