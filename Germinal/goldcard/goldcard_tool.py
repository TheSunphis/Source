#!/usr/bin/env python3
import argparse,gzip,hashlib,io,json,os,tarfile
import germinal_tool as core
VERSION="germinal-goldcard-tool-v1"
FORMAT="germinal-goldcard-valkyrie-v1"
SLOT="V1-GOLD-001"
ASSIGNMENT="germinal-goldcard-ii-yo-valkyrie1-1"
GENERIC_PHRASES=("dossier-anchored","immediate context calls for","relationship permits the candidate register","other acknowledges the contribution")
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def required_text(o,k,p,problems,n=20):problems.need(isinstance(o.get(k),str) and len(o[k].strip())>=n,p+"/"+k,f"requires at least {n} characters")
def validate_expression(e,p):
 core.validate_expression("/record/expression",e,p)
 if not isinstance(e,dict):return
 lines=e.get("japaneseLines",{});primary=lines.get(e.get("primaryLineId"),{}) if isinstance(lines,dict) else {}
 p.need(isinstance(primary,dict) and primary.get("japanese")=="いいよ" and primary.get("reading")=="いいよ","/record/expression/primaryLineId","must be exact target")
 segs=primary.get("segments",[]) if isinstance(primary,dict) else []
 p.need([x.get("surface") for x in segs if isinstance(x,dict)]==["いい","よ"],"/record/expression/primaryLineId","target must separate adjective and final particle")
 p.need([x.get("kind") for x in segs if isinstance(x,dict)]==["content-or-idiom","particle-or-grammar"],"/record/expression/primaryLineId","target segment kinds mismatch")
 p.need(isinstance(lines,dict) and len(lines)>=7,"/record/expression/japaneseLines","requires at least seven analysed lines")
 turns=e.get("dialogue",{}).get("turns",[]) if isinstance(e.get("dialogue"),dict) else []
 p.need(isinstance(turns,list) and len(turns)>=3,"/record/expression/dialogue/turns","requires at least three turns")
 if isinstance(turns,list):p.need(len({x.get("lineId") for x in turns if isinstance(x,dict)})>=3,"/record/expression/dialogue/turns","requires three distinct lines")
 text=json.dumps({k:v for k,v in e.items() if k not in ("japaneseLines","sources")},ensure_ascii=False).lower()
 for phrase in GENERIC_PHRASES:p.need(phrase not in text,"/record/expression","rejected generic Wave 002 boilerplate detected")
 audit=e.get("specificityAudit");p.need(isinstance(audit,dict),"/record/expression/specificityAudit","required object")
 if not isinstance(audit,dict):return
 for k in ("concreteSituation","targetPragmatics","dialogueRationale","alternateFormDecision","patternDecision","distinctionDecision"):required_text(audit,k,"/record/expression/specificityAudit",p,30)
 for module in ("responses","followUps"):
  key=module+"Rationales";items=audit.get(key);p.need(isinstance(items,list) and len(items)==len(e.get(module,[])),"/record/expression/specificityAudit/"+key,"must cover every item")
  if isinstance(items,list):
   expected=[x.get("lineId") for x in e.get(module,[]) if isinstance(x,dict)];actual=[]
   for i,x in enumerate(items):
    q=f"/record/expression/specificityAudit/{key}/{i}";p.need(isinstance(x,dict),q,"must be object")
    if isinstance(x,dict):actual.append(x.get("lineId"));required_text(x,"rationale",q,p,30)
   p.need(actual==expected,"/record/expression/specificityAudit/"+key,"line identity/order mismatch")
def validate(manifest,record):
 p=core.Problems();p.need(isinstance(manifest,dict),"/manifest","must be object");p.need(isinstance(record,dict),"/record","must be object")
 if not isinstance(manifest,dict) or not isinstance(record,dict):return p.items
 p.need(manifest.get("formatVersion")==FORMAT,"/manifest/formatVersion","wrong format");p.need(manifest.get("agent")=="Valkyrie1","/manifest/agent","wrong agent");p.need(manifest.get("assignment")==ASSIGNMENT,"/manifest/assignment","wrong assignment");p.need(manifest.get("expectedSlotIds")==[SLOT],"/manifest/expectedSlotIds","wrong slot identity")
 st=record.get("status");p.need(record.get("slotId")==SLOT,"/record/slotId","wrong slot");p.need(st in core.STATUSES,"/record/status","invalid status")
 p.need(manifest.get("attempted")==1,"/manifest/attempted","must be 1")
 counts={x:int(st==x) for x in core.STATUSES}
 for k,v in counts.items():p.need(manifest.get(k)==v,"/manifest/"+k,"count mismatch")
 p.need(manifest.get("recordSha256")==sha(canon(record)),"/manifest/recordSha256","digest mismatch")
 for k in ("inputAsset","vocabularySeedAsset","evidenceBuild","candidateBuild"):p.need(k in manifest,"/manifest/"+k,"required")
 if st=="submitted":p.need("expression" in record,"/record/expression","required");validate_expression(record.get("expression"),p)
 else:p.need(isinstance(record.get("reasonCode"),str) and bool(record["reasonCode"]),"/record/reasonCode","required")
 return p.items
def package(manifest,record,path):
 probs=validate(manifest,record)
 if probs:raise ValueError(probs[0])
 files={"manifest.json":json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n","record.json":canon(record)};out=io.BytesIO()
 with gzip.GzipFile(fileobj=out,mode="wb",mtime=0,filename="") as gz:
  with tarfile.open(fileobj=gz,mode="w") as tf:
   for name,data in sorted(files.items()):
    ti=tarfile.TarInfo(name);ti.size=len(data);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644;tf.addfile(ti,io.BytesIO(data))
 with open(path,"wb") as f:f.write(out.getvalue());f.flush();os.fsync(f.fileno())
 return len(out.getvalue()),sha(out.getvalue())
def self_test():
 ext={"sourceId":"source:test","artifact":"a","locator":"l","claimScope":"c"};ed={"sourceId":"editorial:Valkyrie1","artifact":"private-goldcard-output","locator":"line","claimScope":"editorial-proposal-not-source-attestation"}
 def line(lid,jp,external=False,primary=False):
  ev=ext if external else ed;parts=["いい","よ"] if primary else [jp[0],jp[1:]];segs=[];a=b=0
  for i,x in enumerate(parts,1):
   kind="content-or-idiom" if i==1 else "particle-or-grammar";segs.append({"segmentId":f"s{i:02d}","surface":x,"reading":x,"kind":kind,"contextualMeaning":"specific segment meaning","grammaticalRole":"specific lexical role" if i==1 else "specific grammatical role","lemma":x,"inflection":None,"japaneseStart":a,"japaneseEnd":a+len(x),"readingStart":b,"readingEnd":b+len(x),"vocabularyCandidates":[{"surface":x,"reading":x,"lemma":x}],"selectedVocabularyId":None,"vocabularyDisposition":"deferred-zero-canonical-index","unlinkedReason":"Zero canonical resolution required before final acceptance","evidence":[ev]});a+=len(x);b+=len(x)
  return {"lineId":lid,"japanese":jp,"reading":jp,"meaning":"specific meaning","ttsEligible":True,"evidence":[ev],"segments":segs}
 vals={"p":"いいよ","r1":"あい","r2":"うえ","f1":"おか","f2":"きく","d1":"けこ","d2":"さし"};lines={k:line(k,v,k=="p",k=="p") for k,v in vals.items()};exp={"expressionId":"gold:e","primaryLineId":"p","category":"interactional-formula","usageSummary":"A concrete familiar-person reassurance after a minor apology where no repair is needed.","verificationState":"candidate","kotoDifficulty":2,"intentions":["Reassure a familiar person that a minor issue is acceptable."],"useWhen":["Use after a minor apology when the speaker genuinely accepts the situation."],"takeCare":["Avoid when harm remains unresolved or a more formal response is required."],"relationships":[{"context":"familiar peers","guidance":"Casual reassurance between familiar peers after a minor inconvenience."}],"forms":[{"lineId":"p","kind":"primary","register":"casual","meaning":"specific meaning","ttsEligible":True}],"responses":[{"lineId":"r1","context":"specific response context","meaning":"specific meaning","ttsEligible":True},{"lineId":"r2","context":"second specific response context","meaning":"specific meaning","ttsEligible":True}],"followUps":[{"lineId":"f1","context":"specific follow-up context","meaning":"specific meaning","ttsEligible":True},{"lineId":"f2","context":"second specific follow-up context","meaning":"specific meaning","ttsEligible":True}],"sources":[ext],"dialogue":{"situation":"Two familiar friends resolve a minor delay before meeting, with no remaining practical repair needed.","relationship":"familiar peers","register":"casual target with context-matched replies","targetLineId":"p","turns":[{"speaker":"A","lineId":"d1","meaning":"specific meaning"},{"speaker":"B","lineId":"p","meaning":"specific meaning"},{"speaker":"A","lineId":"d2","meaning":"specific meaning"}]},"patterns":{"status":"none-supported","reason":"The source supports this fixed expression but not a productive substitution pattern."},"distinctions":{"status":"none-supported","reason":"No nearby expression has enough evidence for a safe contrast in this pilot."},"library":{"searchJapanese":["いいよ"],"searchKana":["いいよ"],"searchMeaning":["reassurance"],"searchIntentions":["reassure familiar peer"],"searchUsage":["minor apology accepted"],"alternateForms":[]},"provenance":{"candidateBuild":"c","candidateId":"id","creationDate":"2026-10-01","creator":"Valkyrie1","editorialStatus":"gold-proposal","evidenceBuild":"e"},"japaneseLines":lines,"specificityAudit":{"concreteSituation":"A familiar friend apologizes for a minor delay that causes no remaining problem.","targetPragmatics":"Casual acceptance and reassurance; the final particle presents that stance directly.","dialogueRationale":"The apology, reassurance, and acknowledgement form one concrete coherent exchange.","alternateFormDecision":"No alternate form is added because the dossier does not independently support one.","patternDecision":"No productive pattern is claimed because only the fixed target is externally anchored.","distinctionDecision":"No nearby distinction is claimed without independent contrastive evidence.","responsesRationales":[{"lineId":"r1","rationale":"The first reply acknowledges the specific reassurance in a familiar exchange."},{"lineId":"r2","rationale":"The second reply closes the accepted minor issue without reopening it."}],"followUpsRationales":[{"lineId":"f1","rationale":"This follow-up is useful only in the concrete minor-delay situation."},{"lineId":"f2","rationale":"This alternative follow-up preserves the familiar and resolved interaction."}]}}
 rec={"slotId":SLOT,"status":"submitted","expression":exp};man={"formatVersion":FORMAT,"agent":"Valkyrie1","assignment":ASSIGNMENT,"expectedSlotIds":[SLOT],"attempted":1,"submitted":1,"abstained":0,"failed":0,"recordSha256":sha(canon(rec)),"inputAsset":{},"vocabularySeedAsset":{},"evidenceBuild":"e","candidateBuild":"c"};p=validate(man,rec)
 if p:raise RuntimeError(p[0])
 bad=json.loads(json.dumps(rec,ensure_ascii=False));bad["expression"]["japaneseLines"]["p"]["segments"]=[bad["expression"]["japaneseLines"]["p"]["segments"][0]];man["recordSha256"]=sha(canon(bad));assert validate(man,bad)
 return True
def load(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def main(argv=None):
 a=argparse.ArgumentParser();a.add_argument("--version",action="store_true");sub=a.add_subparsers(dest="cmd");sub.add_parser("self-test");p=sub.add_parser("validate");p.add_argument("manifest");p.add_argument("record");p=sub.add_parser("package");p.add_argument("manifest");p.add_argument("record");p.add_argument("output");x=a.parse_args(argv)
 if x.version:print(VERSION);return 0
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"core":core.VERSION,"selfTest":"passed"}));return 0
 if x.cmd=="validate":
  probs=validate(load(x.manifest),load(x.record));print(json.dumps({"valid":not probs,"problems":probs},ensure_ascii=False));return 0 if not probs else 2
 if x.cmd=="package":
  n,d=package(load(x.manifest),load(x.record),x.output);print(json.dumps({"bytes":n,"sha256":d}));return 0
 a.error("command required")
if __name__=="__main__":raise SystemExit(main())
