#!/usr/bin/env python3
import argparse,gzip,hashlib,io,json,os,re,tarfile
VERSION="germinal-goldcard-crow-correction-tool-v3";FORMAT="germinal-goldcard-crow-correction-v3";SLOT="V1-GOLD-001";ASSIGNMENT="germinal-goldcard-ii-yo-crow1-correction-1"
CHECKS={
"reassuranceBoundaryExcludesPermission":("/boundaryLock",("reassur","permission")),"minorApologyTriggerIsConcrete":("/dialogue/situation",("apolog","minor")),"primaryAdjectiveFinalParticleSegmentation":("/japaneseLines/",("adjective","particle")),"finalParticleForceIsSubstantive":("/japaneseLines/",("sentence-final","reassur")),"casualContractionAnalysisIsAccurate":("/japaneseLines/",("contract","past")),"declaredSegmentationPolicyIsConsistent":("/analysisPolicy",("policy","applicable")),"repeatedFormsUseCompatibleAnalysis":("/japaneseLines/",("repeat","consistent")),"socialClosureAndPracticalCleanupCoexist":("/dialogue",("apology","cleanup")),"allDisplayedLinesAreNaturalAndComplete":("/japaneseLines",("line","natural")),"readingsAndMeaningsAreContextAccurate":("/japaneseLines",("reading","meaning")),"responsesFitReassuranceContext":("/responses",("response","reassur")),"followUpsFitMinorAccidentContext":("/followUps",("follow","minor")),"registerRelationshipAndSafetyAreAligned":("/relationships",("casual","formal")),"canonicalLinksReverseCheckExactly":("/japaneseLines",("reverse","exact")),"expressionClaimsDoNotExceedEvidence":("/sources",("editorial","source")),"patternsAndDistinctionsAreHonestlyDeferred":("/patterns",("pattern","defer"))}
LINES=("repair-l01","repair-l02","repair-l03","repair-l04","repair-l05","repair-l06","repair-l07")
LINKS=tuple([f"/japaneseLines/repair-l01/segments/{i}" for i in (0,1)]+[f"/japaneseLines/repair-l02/segments/0"]+[f"/japaneseLines/repair-l03/segments/{i}" for i in range(6)]+[f"/japaneseLines/repair-l04/segments/{i}" for i in range(5)]+[f"/japaneseLines/repair-l05/segments/{i}" for i in range(4)]+[f"/japaneseLines/repair-l06/segments/{i}" for i in (0,2,3,4,5,6)]+[f"/japaneseLines/repair-l07/segments/{i}" for i in (0,2,3,4)])
PUNCT=("/japaneseLines/repair-l06/segments/1","/japaneseLines/repair-l06/segments/7","/japaneseLines/repair-l07/segments/1","/japaneseLines/repair-l07/segments/5")
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def concrete(x):return isinstance(x,str) and bool(re.fullmatch(r"(?:release:[0-9]+/(?:card\.json|links\.ndjson|records\.ndjson|record\.json|manifest\.json)(?:#/.+)?|source:(?:JMdict|Tatoeba)/.+)",x))
def validate(m,r):
 e=[]
 def need(ok,p,msg):
  if not ok:e.append(p+": "+msg)
 need(m.get("formatVersion")==FORMAT,"/manifest/formatVersion","wrong format");need(m.get("agent")=="Crow1","/manifest/agent","wrong agent");need(m.get("assignment")==ASSIGNMENT,"/manifest/assignment","wrong assignment");need(m.get("expectedSlotIds")==[SLOT],"/manifest/expectedSlotIds","wrong slot");need(m.get("attempted")==1 and m.get("reviewed")==1,"/manifest","counts must be one");need(m.get("recordSha256")==sha(canon(r)),"/manifest/recordSha256","mismatch")
 for k in ("compiledCardAsset","vocabularyAsset","clarifiedProposalAsset","originalDossierAsset","rejectedReviewAsset"):need(isinstance(m.get(k),dict),"/manifest/"+k,"required")
 need(r.get("slotId")==SLOT,"/record/slotId","wrong slot");rec=r.get("recommendation");need(rec in ("pass","quarantine"),"/record/recommendation","invalid")
 checks=r.get("checks");need(isinstance(checks,dict) and set(checks)==set(CHECKS),"/record/checks","exact issue checks required");rats=[]
 if isinstance(checks,dict):
  for k,(pref,toks) in CHECKS.items():
   x=checks.get(k);p="/record/checks/"+k;need(isinstance(x,dict),p,"must be object")
   if not isinstance(x,dict):continue
   rat=x.get("rationale");low=rat.lower() if isinstance(rat,str) else "";need(type(x.get("passed")) is bool,p+"/passed","boolean required");need(isinstance(rat,str) and len(rat)>=120,p+"/rationale","requires substantive rationale")
   for t in toks:need(t in low,p+"/rationale","missing issue token "+t)
   need(isinstance(x.get("pointer"),str) and x["pointer"].startswith(pref),p+"/pointer","wrong issue anchor");sp=x.get("supportingPointers");need(isinstance(sp,list) and len(sp)>=2 and all(isinstance(z,str) and z.startswith("/") for z in sp),p+"/supportingPointers","two pointers required");loc=x.get("evidenceLocators");need(isinstance(loc,list) and len(loc)>=2 and all(concrete(z) for z in loc),p+"/evidenceLocators","two concrete release/source locators required");rats.append(rat)
  need(len(rats)==len(set(rats)),"/record/checks","rationales must be distinct")
 la=r.get("lineAudit");need(isinstance(la,dict) and set(la)==set(LINES),"/record/lineAudit","all seven exact lines required")
 if isinstance(la,dict):
  for lid in LINES:
   x=la.get(lid);p="/record/lineAudit/"+lid;need(isinstance(x,dict),p,"must be object")
   if isinstance(x,dict):need(x.get("pointer")=="/japaneseLines/"+lid,p+"/pointer","wrong line");[need(x.get(q) is True,p+"/"+q,"must be true for pass record") for q in ("natural","readingAccurate","meaningAccurate","analysisComplete")];need(isinstance(x.get("rationale"),str) and len(x["rationale"])>=100,p+"/rationale","line-specific rationale required");loc=x.get("evidenceLocators");need(isinstance(loc,list) and len(loc)>=2 and all(concrete(z) for z in loc),p+"/evidenceLocators","concrete locators required")
 lka=r.get("linkAudit");need(isinstance(lka,list) and len(lka)==len(LINKS),"/record/linkAudit","all 28 links required")
 if isinstance(lka,list):
  need([x.get("segmentPointer") for x in lka if isinstance(x,dict)]==list(LINKS),"/record/linkAudit","exact ordered pointers required")
  for i,x in enumerate(lka):
   p=f"/record/linkAudit/{i}";need(isinstance(x,dict),p,"must be object")
   if isinstance(x,dict):need(re.fullmatch(r"vocabulary2:[0-9a-f]{32}",str(x.get("vocabularyId",""))) is not None,p+"/vocabularyId","invalid");[need(x.get(q) is True,p+"/"+q,"must be true") for q in ("exactSurfaceReading","exactLemmaAlignment","senseFit")];need(isinstance(x.get("rationale"),str) and len(x["rationale"])>=80,p+"/rationale","specific link rationale required");need(concrete(x.get("registryLocator")) and x["registryLocator"].startswith("release:"),p+"/registryLocator","concrete registry locator required")
 pa=r.get("punctuationAudit");need(isinstance(pa,list) and len(pa)==4,"/record/punctuationAudit","four exclusions required")
 if isinstance(pa,list):need([x.get("segmentPointer") for x in pa if isinstance(x,dict)]==list(PUNCT) and all(x.get("reasonCode")=="punctuation" for x in pa if isinstance(x,dict)),"/record/punctuationAudit","exact punctuation pointers required")
 app=r.get("applicability",{}).get("suruTakingNounPolicy") if isinstance(r.get("applicability"),dict) else None;need(isinstance(app,dict) and app.get("applicable") is False,"/record/applicability/suruTakingNounPolicy","must explicitly be not applicable");need(isinstance(app,dict) and isinstance(app.get("rationale"),str) and len(app["rationale"])>=80 and "no" in app["rationale"].lower() and "instance" in app["rationale"].lower(),"/record/applicability/suruTakingNounPolicy/rationale","explain absent instance")
 eb=r.get("evidenceBoundary");need(isinstance(eb,dict) and set(eb or {})=={"lexicalAnchors","expressionAnchors","editorialTeaching"},"/record/evidenceBoundary","three evidence classes required")
 if isinstance(eb,dict):
  expected={"lexicalAnchors":"source-anchored","expressionAnchors":"source-anchored-bounded","editorialTeaching":"editorial-not-source-attestation"}
  for k,st in expected.items():
   x=eb.get(k);p="/record/evidenceBoundary/"+k;need(isinstance(x,dict) and x.get("status")==st,p+"/status","wrong status");need(isinstance(x,dict) and isinstance(x.get("rationale"),str) and len(x["rationale"])>=100,p+"/rationale","substantive boundary rationale required");loc=x.get("evidenceLocators") if isinstance(x,dict) else None;need(isinstance(loc,list) and len(loc)>=2 and all(concrete(z) for z in loc),p+"/evidenceLocators","concrete locators required")
 findings=r.get("findings");need(isinstance(findings,list),"/record/findings","list required")
 if rec=="pass":need(findings==[],"/record/findings","pass requires none");need(isinstance(checks,dict) and all(x.get("passed") is True for x in checks.values()),"/record/checks","all checks must pass");need(m.get("pass")==1 and m.get("quarantine")==0,"/manifest","counts mismatch")
 if rec=="quarantine":need(bool(findings),"/record/findings","quarantine requires finding");need(m.get("pass")==0 and m.get("quarantine")==1,"/manifest","counts mismatch")
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
 loc=["release:401125726/card.json#/japaneseLines","source:JMdict/entry[ent_seq=1]/sense[1]"];checks={k:{"passed":True,"rationale":f"This detailed {t[0]} and {t[1]} correction review for {k} compares concrete source and release fields, states the bounded conclusion, and avoids treating structural validation as independent linguistic proof.","pointer":p,"supportingPointers":[p,"/verificationState"],"evidenceLocators":loc} for k,(p,t) in CHECKS.items()};lines={x:{"pointer":"/japaneseLines/"+x,"natural":True,"readingAccurate":True,"meaningAccurate":True,"analysisComplete":True,"rationale":"This line-specific assessment checks naturalness, reading, contextual meaning, and complete segment analysis against the compiled line and clarified proposal without relying on an aggregate assertion.","evidenceLocators":loc} for x in LINES};links=[{"segmentPointer":p,"vocabularyId":"vocabulary2:"+"a"*32,"exactSurfaceReading":True,"exactLemmaAlignment":True,"senseFit":True,"rationale":"This individual link has an exact surface and reading form, exact canonical lemma alignment, and a context-appropriate bounded sense in the cited registry record.","registryLocator":"release:401125715/records.ndjson#/vocabulary2:test"} for p in LINKS];r={"slotId":SLOT,"recommendation":"pass","checks":checks,"lineAudit":lines,"linkAudit":links,"punctuationAudit":[{"segmentPointer":p,"reasonCode":"punctuation"} for p in PUNCT],"applicability":{"suruTakingNounPolicy":{"applicable":False,"rationale":"No instance of a suru-taking noun occurs in the reviewed card, so this declared policy is explicitly not applicable rather than falsely reported as exercised."}},"evidenceBoundary":{"lexicalAnchors":{"status":"source-anchored","rationale":"Lexical and grammatical identities are source anchored through concrete registry and JMdict locators, while the scope stays limited to the cited forms, classes, and senses.","evidenceLocators":loc},"expressionAnchors":{"status":"source-anchored-bounded","rationale":"Expression-level evidence is treated as a bounded anchor for the frozen candidate use only and is not generalized into unsupported productive claims or broad usage guarantees.","evidenceLocators":loc},"editorialTeaching":{"status":"editorial-not-source-attestation","rationale":"Teaching situations, relationship guidance, responses, follow-ups, and warnings are identified as editorial proposals rather than misrepresented as statements directly attested by a source.","evidenceLocators":loc}},"findings":[]};m={"formatVersion":FORMAT,"agent":"Crow1","assignment":ASSIGNMENT,"expectedSlotIds":[SLOT],"attempted":1,"reviewed":1,"pass":1,"quarantine":0,"recordSha256":sha(canon(r)),"compiledCardAsset":{},"vocabularyAsset":{},"clarifiedProposalAsset":{},"originalDossierAsset":{},"rejectedReviewAsset":{}};e=validate(m,r);assert not e,e;return True
def load(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def main():
 a=argparse.ArgumentParser();s=a.add_subparsers(dest="cmd");s.add_parser("self-test");p=s.add_parser("validate");p.add_argument("manifest");p.add_argument("review");p=s.add_parser("package");p.add_argument("manifest");p.add_argument("review");p.add_argument("output");x=a.parse_args()
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed","checks":16,"lines":7,"links":28}));return
 if x.cmd=="validate":e=validate(load(x.manifest),load(x.review));print(json.dumps({"valid":not e,"problems":e}));raise SystemExit(0 if not e else 2)
 if x.cmd=="package":n,d=package(load(x.manifest),load(x.review),x.output);print(json.dumps({"bytes":n,"sha256":d}));return
 a.error("command required")
if __name__=="__main__":main()
