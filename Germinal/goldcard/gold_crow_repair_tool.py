#!/usr/bin/env python3
import argparse,gzip,hashlib,io,json,os,tarfile
VERSION="germinal-goldcard-crow-repair-tool-v2";FORMAT="germinal-goldcard-crow-repair-v2";SLOT="V1-GOLD-001";ASSIGNMENT="germinal-goldcard-ii-yo-crow1-review-repair-1"
CHECKS={
"reassuranceBoundaryExcludesPermission":("/boundaryLock",("reassur","permission")),
"minorApologyTriggerIsConcrete":("/dialogue/situation",("apolog","minor")),
"primaryAdjectiveFinalParticleSegmentation":("/japaneseLines/",("adjective","particle")),
"finalParticleForceIsSubstantive":("/japaneseLines/",("sentence-final","reassur")),
"casualContractionAnalysisIsAccurate":("/japaneseLines/",("contract","past")),
"declaredSegmentationPolicyIsConsistent":("/analysisPolicy",("policy","consistent")),
"repeatedFormsUseCompatibleAnalysis":("/japaneseLines/",("repeat","consistent")),
"socialClosureAndPracticalCleanupCoexist":("/dialogue",("apology","cleanup")),
"allDisplayedLinesAreNaturalAndComplete":("/japaneseLines",("natural","complete")),
"readingsAndMeaningsAreContextAccurate":("/japaneseLines",("reading","meaning")),
"responsesFitReassuranceContext":("/responses",("response","reassur")),
"followUpsFitMinorAccidentContext":("/followUps",("follow","minor")),
"registerRelationshipAndSafetyAreAligned":("/relationships",("casual","formal")),
"canonicalLinksReverseCheckExactly":("/japaneseLines",("reverse","exact")),
"expressionClaimsDoNotExceedEvidence":("/sources",("source","expression")),
"patternsAndDistinctionsAreHonestlyDeferred":("/patterns",("pattern","defer")),
}
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def validate(m,r):
 e=[]
 def need(ok,p,msg):
  if not ok:e.append(p+": "+msg)
 need(m.get("formatVersion")==FORMAT,"/manifest/formatVersion","wrong format");need(m.get("agent")=="Crow1","/manifest/agent","wrong agent");need(m.get("assignment")==ASSIGNMENT,"/manifest/assignment","wrong assignment");need(m.get("expectedSlotIds")==[SLOT],"/manifest/expectedSlotIds","wrong slot");need(m.get("attempted")==1 and m.get("reviewed")==1,"/manifest","counts must be one");need(m.get("recordSha256")==sha(canon(r)),"/manifest/recordSha256","mismatch")
 for k in ("compiledCardAsset","vocabularyAsset","clarifiedProposalAsset","originalDossierAsset"):need(isinstance(m.get(k),dict),"/manifest/"+k,"required")
 need(r.get("slotId")==SLOT,"/record/slotId","wrong slot");rec=r.get("recommendation");need(rec in ("pass","quarantine"),"/record/recommendation","invalid");checks=r.get("checks");need(isinstance(checks,dict) and set(checks)==set(CHECKS),"/record/checks","exact issue-specific checks required")
 rats=[]
 if isinstance(checks,dict):
  for k,(prefix,tokens) in CHECKS.items():
   x=checks.get(k);p="/record/checks/"+k;need(isinstance(x,dict),p,"must be object")
   if not isinstance(x,dict):continue
   need(type(x.get("passed")) is bool,p+"/passed","must be boolean");rat=x.get("rationale");need(isinstance(rat,str) and len(rat.strip())>=100,p+"/rationale","requires substantive issue-specific rationale");low=rat.lower() if isinstance(rat,str) else ""
   for tok in tokens:need(tok in low,p+"/rationale","missing issue token: "+tok)
   ptr=x.get("pointer");need(isinstance(ptr,str) and ptr.startswith(prefix),p+"/pointer","must point to issue anchor "+prefix);loc=x.get("evidenceLocator");need(isinstance(loc,str) and len(loc.strip())>=16,p+"/evidenceLocator","requires concrete evidence locator");sp=x.get("supportingPointers");need(isinstance(sp,list) and len(sp)>=2 and all(isinstance(z,str) and z.startswith("/") for z in sp),p+"/supportingPointers","requires at least two concrete pointers");rats.append(rat)
  need(len(rats)==len(set(rats)),"/record/checks","rationales must be distinct")
 findings=r.get("findings");need(isinstance(findings,list),"/record/findings","must be list")
 if rec=="pass":need(findings==[],"/record/findings","pass requires none");need(isinstance(checks,dict) and all(x.get("passed") is True for x in checks.values()),"/record/checks","pass requires every issue check true");need(m.get("pass")==1 and m.get("quarantine")==0,"/manifest","pass counts mismatch")
 if rec=="quarantine":need(bool(findings),"/record/findings","quarantine requires findings");need(m.get("pass")==0 and m.get("quarantine")==1,"/manifest","quarantine counts mismatch")
 if isinstance(findings,list):
  for i,x in enumerate(findings):
   p=f"/record/findings/{i}";need(isinstance(x,dict),p,"must be object")
   if isinstance(x,dict):
    for q in ("severity","code","pointer","evidenceLocator","explanation","gate"):need(isinstance(x.get(q),str) and bool(x[q].strip()),p+"/"+q,"required")
    need(x.get("gate") in CHECKS,p+"/gate","must name issue-specific check")
 return e
def package(m,r,path):
 e=validate(m,r)
 if e:raise ValueError(e[0])
 fs={"manifest.json":json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n","review.json":canon(r)};o=io.BytesIO()
 with gzip.GzipFile(fileobj=o,mode="wb",mtime=0,filename="") as gz:
  with tarfile.open(fileobj=gz,mode="w") as tf:
   for n,d in sorted(fs.items()):ti=tarfile.TarInfo(n);ti.size=len(d);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644;tf.addfile(ti,io.BytesIO(d))
 with open(path,"wb") as f:f.write(o.getvalue());f.flush();os.fsync(f.fileno())
 return len(o.getvalue()),sha(o.getvalue())
def self_test():
 checks={k:{"passed":True,"rationale":f"This substantive {t[0]} and {t[1]} assessment addresses {k} directly, compares the relevant fields, and explains why the issue-specific condition is satisfied without relying on structural validation alone.","pointer":p,"evidenceLocator":"compiled-card:bounded-test","supportingPointers":[p,"/verificationState"]} for k,(p,t) in CHECKS.items()};r={"slotId":SLOT,"recommendation":"pass","checks":checks,"findings":[]};m={"formatVersion":FORMAT,"agent":"Crow1","assignment":ASSIGNMENT,"expectedSlotIds":[SLOT],"attempted":1,"reviewed":1,"pass":1,"quarantine":0,"recordSha256":sha(canon(r)),"compiledCardAsset":{},"vocabularyAsset":{},"clarifiedProposalAsset":{},"originalDossierAsset":{}};assert not validate(m,r);return True
def load(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def main():
 a=argparse.ArgumentParser();s=a.add_subparsers(dest="cmd");s.add_parser("self-test");p=s.add_parser("validate");p.add_argument("manifest");p.add_argument("review");p=s.add_parser("package");p.add_argument("manifest");p.add_argument("review");p.add_argument("output");x=a.parse_args()
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed","checkCount":len(CHECKS)}));return
 if x.cmd=="validate":e=validate(load(x.manifest),load(x.review));print(json.dumps({"valid":not e,"problems":e}));raise SystemExit(0 if not e else 2)
 if x.cmd=="package":n,d=package(load(x.manifest),load(x.review),x.output);print(json.dumps({"bytes":n,"sha256":d}));return
 a.error("command required")
if __name__=="__main__":main()
