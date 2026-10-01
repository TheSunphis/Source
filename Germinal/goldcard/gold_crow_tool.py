#!/usr/bin/env python3
import argparse,gzip,hashlib,io,json,os,tarfile
VERSION="germinal-goldcard-crow-tool-v1";FORMAT="germinal-goldcard-crow-v1";SLOT="V1-GOLD-001";ASSIGNMENT="germinal-goldcard-ii-yo-crow1-review-1"
CHECKS=("targetEvidenceBoundary","japaneseNaturalness","readingMeaningAccuracy","segmentationLinguisticCorrectness","vocabularyLinkCorrectness","responsesContextFit","followUpsContextFit","dialogueCoherence","pragmaticsRegisterRelationship","formsPatternsDistinctions","libraryProvenance","noUnsupportedClaims")
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def validate(m,r):
 e=[]
 def need(ok,p,msg):
  if not ok:e.append(p+": "+msg)
 need(m.get("formatVersion")==FORMAT,"/manifest/formatVersion","wrong format");need(m.get("agent")=="Crow1","/manifest/agent","wrong agent");need(m.get("assignment")==ASSIGNMENT,"/manifest/assignment","wrong assignment");need(m.get("expectedSlotIds")==[SLOT],"/manifest/expectedSlotIds","wrong slot");need(m.get("attempted")==1 and m.get("reviewed")==1,"/manifest","counts must be 1");need(m.get("recordSha256")==sha(canon(r)),"/manifest/recordSha256","mismatch")
 for k in ("compiledCardAsset","vocabularyAsset","proposalAsset"):need(k in m,"/manifest/"+k,"required")
 need(r.get("slotId")==SLOT,"/record/slotId","wrong slot");rec=r.get("recommendation");need(rec in ("pass","quarantine"),"/record/recommendation","invalid");checks=r.get("checks");need(isinstance(checks,dict) and tuple(checks)==CHECKS,"/record/checks","exact ordered checks required")
 rationales=[]
 if isinstance(checks,dict):
  for k in CHECKS:
   x=checks.get(k);p="/record/checks/"+k;need(isinstance(x,dict),p,"must be object")
   if isinstance(x,dict):
    need(type(x.get("passed")) is bool,p+"/passed","must be boolean");need(isinstance(x.get("rationale"),str) and len(x["rationale"].strip())>=40,p+"/rationale","requires specific rationale");need(isinstance(x.get("pointer"),str) and x["pointer"].startswith("/"),p+"/pointer","requires JSON pointer");need(isinstance(x.get("evidenceLocator"),str) and len(x["evidenceLocator"].strip())>=10,p+"/evidenceLocator","required");rationales.append(x.get("rationale"))
  need(len(rationales)==len(set(rationales)),"/record/checks","rationales must be independently specific")
 findings=r.get("findings");need(isinstance(findings,list),"/record/findings","must be list")
 if rec=="pass":need(findings==[],"/record/findings","pass requires none");need(isinstance(checks,dict) and all(x.get("passed") is True for x in checks.values()),"/record/checks","pass requires all true");need(m.get("pass")==1 and m.get("quarantine")==0,"/manifest","pass counts mismatch")
 if rec=="quarantine":need(bool(findings),"/record/findings","quarantine requires findings");need(m.get("pass")==0 and m.get("quarantine")==1,"/manifest","quarantine counts mismatch")
 if isinstance(findings,list):
  for i,x in enumerate(findings):
   p=f"/record/findings/{i}";need(isinstance(x,dict),p,"must be object")
   if isinstance(x,dict):
    for k in ("severity","code","pointer","evidenceLocator","explanation","gate"):need(isinstance(x.get(k),str) and bool(x[k].strip()),p+"/"+k,"required")
 return e
def package(m,r,path):
 e=validate(m,r)
 if e:raise ValueError(e[0])
 files={"manifest.json":json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n","review.json":canon(r)};o=io.BytesIO()
 with gzip.GzipFile(fileobj=o,mode="wb",mtime=0,filename="") as gz:
  with tarfile.open(fileobj=gz,mode="w") as tf:
   for n,d in sorted(files.items()):ti=tarfile.TarInfo(n);ti.size=len(d);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644;tf.addfile(ti,io.BytesIO(d))
 with open(path,"wb") as f:f.write(o.getvalue());f.flush();os.fsync(f.fileno())
 return len(o.getvalue()),sha(o.getvalue())
def self_test():
 checks={k:{"passed":True,"rationale":f"Specific independent rationale for {k} with enough detail to support this judgment.","pointer":"/japaneseLines","evidenceLocator":"compiled-card:test"} for k in CHECKS};r={"slotId":SLOT,"recommendation":"pass","checks":checks,"findings":[]};m={"formatVersion":FORMAT,"agent":"Crow1","assignment":ASSIGNMENT,"expectedSlotIds":[SLOT],"attempted":1,"reviewed":1,"pass":1,"quarantine":0,"recordSha256":sha(canon(r)),"compiledCardAsset":{},"vocabularyAsset":{},"proposalAsset":{}};assert not validate(m,r);return True
def load(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def main(argv=None):
 a=argparse.ArgumentParser();sub=a.add_subparsers(dest="cmd");sub.add_parser("self-test");p=sub.add_parser("validate");p.add_argument("manifest");p.add_argument("review");p=sub.add_parser("package");p.add_argument("manifest");p.add_argument("review");p.add_argument("output");x=a.parse_args(argv)
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed"}));return 0
 if x.cmd=="validate":e=validate(load(x.manifest),load(x.review));print(json.dumps({"valid":not e,"problems":e}));return 0 if not e else 2
 if x.cmd=="package":n,d=package(load(x.manifest),load(x.review),x.output);print(json.dumps({"bytes":n,"sha256":d}));return 0
 a.error("command required")
if __name__=="__main__":raise SystemExit(main())
