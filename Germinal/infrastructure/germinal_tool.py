#!/usr/bin/env python3
"""Germinal deterministic structural validator and packager. Standard library only."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,sys,tarfile
VERSION="germinal-tool-v1"
VALK_FORMAT="germinal-valkyrie-output-v1"
CROW_FORMAT="germinal-crow-review-v1"
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
 p.need(manifest.get("formatVersion")==VALK_FORMAT,"/manifest/formatVersion","wrong format")
 p.need(manifest.get("agent")=="Valkyrie1","/manifest/agent","must be Valkyrie1")
 p.need(manifest.get("assignment")=="germinal-wave001-valkyrie1-50","/manifest/assignment","wrong assignment")
 p.need(len(records)==50,"/records","must contain exactly 50 records")
 expected=[f"V1-W001-{i:03d}" for i in range(1,51)]
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
 p.need(manifest.get("attempted")==50,"/manifest/attempted","must be 50")
 for k,v in counts.items():p.need(manifest.get(k)==v,f"/manifest/{k}","count mismatch")
 p.need(sum(counts.values())==50,"/manifest","count conservation failed")
 p.need(manifest.get("recordsSha256")==sha(records_bytes(records)),"/manifest/recordsSha256","digest mismatch")
 for k in ("inputAsset","evidenceBuild","candidateBuild"):p.need(k in manifest,"/manifest/"+k,"required")
 return p.items
def validate_crow(manifest,records):
 p=Problems();p.need(isinstance(manifest,dict),"/manifest","must be object")
 if not isinstance(manifest,dict):return p.items
 p.need(manifest.get("formatVersion")==CROW_FORMAT,"/manifest/formatVersion","wrong format")
 p.need(manifest.get("agent")=="Crow1","/manifest/agent","must be Crow1")
 p.need(manifest.get("assignment")=="germinal-wave001-crow1-review-50","/manifest/assignment","wrong assignment")
 p.need(len(records)==50,"/records","must contain exactly 50 records")
 expected=[f"V1-W001-{i:03d}" for i in range(1,51)]
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
 p.need(manifest.get("attempted")==50 and manifest.get("reviewed")==50,"/manifest","attempted/reviewed must be 50")
 p.need(manifest.get("pass")==counts["pass"],"/manifest/pass","count mismatch")
 p.need(manifest.get("quarantine")==counts["quarantine"],"/manifest/quarantine","count mismatch")
 p.need(sum(counts.values())==50,"/manifest","count conservation failed")
 p.need(manifest.get("recordsSha256")==sha(records_bytes(records)),"/manifest/recordsSha256","digest mismatch")
 for k in ("evidenceAsset","valkyrieAsset","evidenceBuild","candidateBuild"):p.need(k in manifest,"/manifest/"+k,"required")
 return p.items
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
 ev={"sourceId":"s","artifact":"a","locator":"l","claimScope":"c"}
 seg={"segmentId":"s1","surface":"x","reading":"y","japaneseStart":0,"japaneseEnd":1,"readingStart":0,"readingEnd":1,"contextualMeaning":"m","grammaticalRole":"r","lemma":None,"inflection":None,"vocabularyCandidates":[],"selectedVocabularyId":None,"vocabularyDisposition":"reviewed-unlinked","unlinkedReason":"none","evidence":[ev]}
 line={"lineId":"l1","japanese":"x","reading":"y","meaning":"m","ttsEligible":True,"evidence":[ev],"segments":[seg]}
 exp={"expressionId":"e","primaryLineId":"l1","category":"c","usageSummary":"u","verificationState":"candidate","kotoDifficulty":1,"intentions":["i"],"useWhen":["u"],"takeCare":["t"],"relationships":[{"context":"c","guidance":"g"}],"forms":[{"lineId":"l1"}],"responses":[{"lineId":"l1"}],"followUps":[{"lineId":"l1"}],"sources":[ev],"dialogue":{"targetLineId":"l1"},"patterns":{},"distinctions":{},"library":{},"provenance":{},"japaneseLines":{"l1":line}}
 rs=[{"slotId":f"V1-W001-{i:03d}","status":"submitted","expression":exp} for i in range(1,51)]
 m={"formatVersion":VALK_FORMAT,"agent":"Valkyrie1","assignment":"germinal-wave001-valkyrie1-50","attempted":50,"submitted":50,"abstained":0,"failed":0,"recordsSha256":sha(records_bytes(rs)),"inputAsset":{},"evidenceBuild":"e","candidateBuild":"c"}
 probs=validate_valkyrie(m,rs)
 if probs:raise RuntimeError("self-test failed: "+probs[0])
 return True
def main(argv=None):
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
 sub.add_parser("self-test")
 v=sub.add_parser("validate-valkyrie");v.add_argument("manifest");v.add_argument("records")
 c=sub.add_parser("validate-crow");c.add_argument("manifest");c.add_argument("records")
 g=sub.add_parser("package");g.add_argument("kind",choices=["valkyrie","crow"]);g.add_argument("manifest");g.add_argument("records");g.add_argument("output")
 s=sub.add_parser("sha256");s.add_argument("file")
 a=ap.parse_args(argv)
 if a.cmd=="self-test":self_test();print(VERSION+" self-test passed");return 0
 if a.cmd=="sha256":
  z=hashlib.sha256();n=0
  with open(a.file,"rb") as f:
   for b in iter(lambda:f.read(1024*1024),b""):z.update(b);n+=len(b)
  print(json.dumps({"bytes":n,"sha256":z.hexdigest()},sort_keys=True));return 0
 m=read_json(a.manifest);r=read_ndjson(a.records);probs=validate_valkyrie(m,r) if (a.cmd=="validate-valkyrie" or getattr(a,"kind",None)=="valkyrie") else validate_crow(m,r)
 if probs:
  print(json.dumps({"status":"failed","problemCount":len(probs),"problems":probs[:200]},ensure_ascii=False,sort_keys=True));return 1
 if a.cmd=="package":
  name="slots.ndjson" if a.kind=="valkyrie" else "reviews.ndjson";n,d=deterministic_archive(m,r,name,a.output);print(json.dumps({"status":"packaged","bytes":n,"sha256":d},sort_keys=True))
 else:print(json.dumps({"status":"passed","records":len(r),"tool":VERSION},sort_keys=True))
 return 0
if __name__=="__main__":raise SystemExit(main())
