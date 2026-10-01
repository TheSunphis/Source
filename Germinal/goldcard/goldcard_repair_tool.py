#!/usr/bin/env python3
import argparse,copy,gzip,hashlib,io,json,os,tarfile
import goldcard_tool as base
VERSION="germinal-goldcard-repair-tool-v2";FORMAT="germinal-goldcard-valkyrie-v2";ASSIGNMENT="germinal-goldcard-ii-yo-valkyrie1-repair-1"
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def sha(b):return hashlib.sha256(b).hexdigest()
def boundary_problems(e):
 p=[]
 def need(ok,path,msg):
  if not ok:p.append(path+": "+msg)
 if not isinstance(e,dict):return ["/record/expression: must be object"]
 lock=e.get("boundaryLock");need(isinstance(lock,dict),"/record/expression/boundaryLock","required")
 if isinstance(lock,dict):
  need(lock.get("dialogueAct")=="casual-reassurance-after-minor-apology","/record/expression/boundaryLock/dialogueAct","must preserve reassurance act")
  need(lock.get("excludedDialogueActs")==["affirmative-permission"],"/record/expression/boundaryLock/excludedDialogueActs","must exclude permission")
  need(lock.get("sourceConstraint")=="frozen-candidate-reassurance-boundary","/record/expression/boundaryLock/sourceConstraint","wrong source constraint")
 policy=e.get("analysisPolicy");need(isinstance(policy,dict),"/record/expression/analysisPolicy","required")
 if isinstance(policy,dict):
  need(policy.get("targetSegmentation")=="ii-adjective-plus-yo-final-particle","/record/expression/analysisPolicy/targetSegmentation","wrong target policy")
  need(policy.get("suruTakingNounPolicy")=="split-noun-and-support-verb","/record/expression/analysisPolicy/suruTakingNounPolicy","canonical support-verb policy required")
 reduced={k:v for k,v in e.items() if k not in ("sources","japaneseLines","boundaryLock")};need("permission" not in json.dumps(reduced,ensure_ascii=False).lower(),"/record/expression","permission dialogue-act drift forbidden")
 lines=e.get("japaneseLines",{});primary=lines.get(e.get("primaryLineId"),{}) if isinstance(lines,dict) else {};meaning=str(primary.get("meaning","")).lower();need("worry" in meaning or "problem" in meaning,"/record/expression/primaryLineId","meaning must preserve reassurance/no-problem boundary")
 situation=str(e.get("dialogue",{}).get("situation","")).lower();need(any(x in situation for x in ("apolog","minor mistake","minor inconvenience")),"/record/expression/dialogue/situation","requires concrete minor-apology situation")
 return p
def validate(m,r):
 x=copy.deepcopy(m);x["formatVersion"]=base.FORMAT;x["assignment"]=base.ASSIGNMENT;x["recordSha256"]=base.sha(base.canon(r));p=base.validate(x,r);p+=boundary_problems(r.get("expression",{}) if isinstance(r,dict) else {})
 if m.get("formatVersion")!=FORMAT:p.append("/manifest/formatVersion: wrong repair format")
 if m.get("assignment")!=ASSIGNMENT:p.append("/manifest/assignment: wrong repair assignment")
 if m.get("recordSha256")!=sha(canon(r)):p.append("/manifest/recordSha256: mismatch")
 return p
def package(m,r,path):
 p=validate(m,r)
 if p:raise ValueError(p[0])
 f={"manifest.json":json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n","record.json":canon(r)};o=io.BytesIO()
 with gzip.GzipFile(fileobj=o,mode="wb",mtime=0,filename="") as gz:
  with tarfile.open(fileobj=gz,mode="w") as tf:
   for n,d in sorted(f.items()):ti=tarfile.TarInfo(n);ti.size=len(d);ti.mtime=0;ti.uid=ti.gid=0;ti.uname=ti.gname="";ti.mode=0o644;tf.addfile(ti,io.BytesIO(d))
 with open(path,"wb") as q:q.write(o.getvalue());q.flush();os.fsync(q.fileno())
 return len(o.getvalue()),sha(o.getvalue())
def self_test():
 e={"boundaryLock":{"dialogueAct":"casual-reassurance-after-minor-apology","excludedDialogueActs":["affirmative-permission"],"sourceConstraint":"frozen-candidate-reassurance-boundary"},"analysisPolicy":{"targetSegmentation":"ii-adjective-plus-yo-final-particle","suruTakingNounPolicy":"split-noun-and-support-verb"},"primaryLineId":"p","japaneseLines":{"p":{"meaning":"Do not worry; it is not a problem."}},"dialogue":{"situation":"A familiar peer apologizes for a minor inconvenience."}};assert not boundary_problems(e);b=copy.deepcopy(e);b["dialogue"]["situation"]="A asks permission.";assert boundary_problems(b);return True
def load(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def main():
 a=argparse.ArgumentParser();s=a.add_subparsers(dest="cmd");s.add_parser("self-test");p=s.add_parser("validate");p.add_argument("manifest");p.add_argument("record");p=s.add_parser("package");p.add_argument("manifest");p.add_argument("record");p.add_argument("output");x=a.parse_args()
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"base":base.VERSION,"selfTest":"passed"}));return
 if x.cmd=="validate":p=validate(load(x.manifest),load(x.record));print(json.dumps({"valid":not p,"problems":p},ensure_ascii=False));raise SystemExit(0 if not p else 2)
 if x.cmd=="package":n,d=package(load(x.manifest),load(x.record),x.output);print(json.dumps({"bytes":n,"sha256":d}));return
 a.error("command required")
if __name__=="__main__":main()
