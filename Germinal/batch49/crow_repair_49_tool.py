#!/usr/bin/env python3
import argparse,gzip,hashlib,io,json,os,tarfile
VERSION="germinal-crow-repair-49-tool-v1";FORMAT="germinal-crow-repair-49-output-v1";ASSIGNMENT="germinal-crow1-review-repair-49-1"
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def lines(f):return [f.get("primary")]+list(f.get("forms",[]))+list(f.get("responses",[]))+list(f.get("followUps",[]))+list(f.get("dialogue",[]))+[e for p in f.get("patterns",[]) for e in p.get("examples",[])]
def validate_line(x,p):
 e=[]
 def need(ok,q,m):
  if not ok:e.append(p+q+": "+m)
 need(isinstance(x,dict),"","line must be object")
 if not isinstance(x,dict):return e
 for k in ("japanese","reading","meaning"):need(isinstance(x.get(k),str) and x[k].strip(),"/"+k,"required")
 need(x.get("deviceTts") is True,"/deviceTts","must be true")
 ss=x.get("segments");need(isinstance(ss,list) and ss,"/segments","complete segments required")
 if isinstance(ss,list):
  surfaces=[]
  for i,s in enumerate(ss):
   q=f"/segments/{i}";need(isinstance(s,dict),q,"must be object")
   if not isinstance(s,dict):continue
   for k in ("surface","reading","kind","contextualMeaning","grammaticalRole"):need(isinstance(s.get(k),str) and s[k].strip(),q+"/"+k,"required")
   need(s.get("selectedVocabularyId") is None,q+"/selectedVocabularyId","Valkyrie must not assign canonical IDs");surfaces.append(str(s.get("surface","")))
  need("".join(surfaces)==x.get("japanese"),"/segments","surfaces must exactly cover Japanese line")
 return e
def validate(material,manifest,records):
 e=[]
 def need(ok,p,m):
  if not ok:e.append(p+": "+m)
 need(material.get("formatVersion")=="germinal-49-material-v1","/material/formatVersion","wrong material");need(manifest.get("formatVersion")==FORMAT,"/manifest/formatVersion","wrong format");need(manifest.get("assignment")==ASSIGNMENT,"/manifest/assignment","wrong assignment");need(manifest.get("attempted")==49 and manifest.get("submitted")+manifest.get("quarantined")==49,"/manifest","counts must conserve 49");need(manifest.get("recordsSha256")==sha(b"".join(canon(x) for x in records)),"/manifest/recordsSha256","mismatch")
 expected=material.get("expectedIds",[]);need(len(records)==49,"/records","exactly 49 required");need([x.get("id") for x in records]==expected,"/records","exact ordered seed IDs required");seeds={x["id"]:x for x in material.get("drafts",[])};summaries=[]
 for i,f in enumerate(records):
  p=f"/records/{i}";seed=seeds.get(f.get("id"),{});need(f.get("publicationStatus") in ("candidate-complete","quarantined"),p+"/publicationStatus","invalid");need(f.get("previewStatus") in ("candidate","quarantined"),p+"/previewStatus","invalid");need(isinstance(f.get("difficulty"),int) and 1<=f["difficulty"]<=5,p+"/difficulty","Koto Difficulty required");need(isinstance(f.get("category"),str) and bool(f["category"].strip()),p+"/category","required");need(isinstance(f.get("intentions"),list) and len(f["intentions"])>=2,p+"/intentions","two specific intentions required")
  usage=f.get("usage");need(isinstance(usage,dict),p+"/usage","required")
  if isinstance(usage,dict):
   need(isinstance(usage.get("summary"),str) and len(usage["summary"])>=80,p+"/usage/summary","specific summary required");summaries.append(usage.get("summary"));
   for k in ("useWhen","avoidWhen","suitableRelationships"):need(isinstance(usage.get(k),list) and len(usage[k])>=2 and all(isinstance(z,str) and len(z)>=30 for z in usage[k]),p+"/usage/"+k,"two concrete items required")
  need(isinstance(f.get("forms"),list) and len(f["forms"])>=1,p+"/forms","required");need(isinstance(f.get("responses"),list) and len(f["responses"])>=2,p+"/responses","two required");need(isinstance(f.get("followUps"),list) and len(f["followUps"])>=2,p+"/followUps","two required");need(isinstance(f.get("dialogue"),list) and len(f["dialogue"])>=3,p+"/dialogue","three turns required")
  for j,x in enumerate(lines(f)):e+=validate_line(x,p+f"/displayedLines/{j}")
  src=f.get("sources");anchors={(x.get("sourceId"),x.get("locator")) for x in src or [] if isinstance(x,dict)};seedanchors={(x.get("sourceId"),x.get("locator")) for x in seed.get("sources",[]) if isinstance(x,dict)};need(seedanchors<=anchors,p+"/sources","seed source anchor must be preserved");need(any(x.get("sourceId")=="original-editorial" for x in src or [] if isinstance(x,dict)),p+"/sources","editorial provenance required")
  rat=f.get("editorialRationales");need(isinstance(rat,dict) and set(rat)=={"forms","responses","followUps","dialogue","segments"},p+"/editorialRationales","exact rationales required")
  if isinstance(rat,dict):
   for k,v in rat.items():need(isinstance(v,str) and len(v)>=80,p+"/editorialRationales/"+k,"specific rationale required")
  policy=f.get("analysisPolicy");need(isinstance(policy,dict) and isinstance(policy.get("segmentationPolicy"),str) and len(policy["segmentationPolicy"])>=30,p+"/analysisPolicy","declared segmentation policy required")
 need(len(summaries)==len(set(summaries)),"/records","usage summaries must be independently specific")
 return e
def package(material,manifest,records,path):
 e=validate(material,manifest,records)
 if e:raise ValueError(e[0])
 fs={"manifest.json":json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n","records.ndjson":b"".join(canon(x) for x in records)};o=io.BytesIO()
 with gzip.GzipFile(fileobj=o,mode="wb",mtime=0,filename="") as gz:
  with tarfile.open(fileobj=gz,mode="w") as tf:
   for n,d in sorted(fs.items()):ti=tarfile.TarInfo(n);ti.size=len(d);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644;tf.addfile(ti,io.BytesIO(d))
 with open(path,"wb") as f:f.write(o.getvalue());f.flush();os.fsync(f.fileno())
 return len(o.getvalue()),sha(o.getvalue())
def loadj(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def loadn(p):
 with open(p,encoding="utf-8") as f:return [json.loads(x) for x in f if x.strip()]
def self_test():
 line={"japanese":"TEST","reading":"test","meaning":"test meaning","deviceTts":True,"segments":[{"surface":"TEST","reading":"test","kind":"content-or-idiom","contextualMeaning":"test context","grammaticalRole":"fixed expression","selectedVocabularyId":None}]};f={"id":"expression:test","publicationStatus":"candidate-complete","previewStatus":"candidate","difficulty":1,"category":"Test","intentions":["specific intention one","specific intention two"],"primary":line,"usage":{"summary":"A deliberately long and independently specific usage summary for deterministic validator self testing only.","useWhen":["Concrete use condition long enough for validation.","Another concrete use condition long enough."],"avoidWhen":["Concrete caution long enough for validation here.","Another concrete caution long enough here."],"suitableRelationships":["Concrete relationship guidance long enough here.","Another relationship guidance long enough here."]},"forms":[line],"responses":[line,line],"followUps":[line,line],"dialogue":[line,line,line],"patterns":[],"sources":[{"sourceId":"test","locator":"test"},{"sourceId":"original-editorial","locator":"test"}],"editorialRationales":{k:"A concrete and deliberately long rationale explaining this editorial choice for validator self testing without claiming source attestation." for k in ("forms","responses","followUps","dialogue","segments")},"analysisPolicy":{"segmentationPolicy":"A declared segmentation policy long enough for testing."}};m={"formatVersion":"germinal-49-material-v1","expectedIds":[f["id"]],"drafts":[{"id":f["id"],"sources":[{"sourceId":"test","locator":"test"}]}]};mf={"formatVersion":FORMAT,"assignment":ASSIGNMENT,"attempted":49,"submitted":49,"quarantined":0,"recordsSha256":sha(canon(f))};assert not [x for x in validate(m,mf,[f]) if not x.startswith('/records: exactly 49')];return True
def main():
 a=argparse.ArgumentParser();s=a.add_subparsers(dest="cmd");s.add_parser("self-test");p=s.add_parser("validate");p.add_argument("material");p.add_argument("manifest");p.add_argument("records");p=s.add_parser("package");p.add_argument("material");p.add_argument("manifest");p.add_argument("records");p.add_argument("output");x=a.parse_args()
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed"}));return
 if x.cmd=="validate":e=validate(loadj(x.material),loadj(x.manifest),loadn(x.records));print(json.dumps({"valid":not e,"problems":e},ensure_ascii=False));raise SystemExit(0 if not e else 2)
 if x.cmd=="package":n,d=package(loadj(x.material),loadj(x.manifest),loadn(x.records),x.output);print(json.dumps({"bytes":n,"sha256":d}));return
 a.error("command required")
if __name__=="__main__":main()
