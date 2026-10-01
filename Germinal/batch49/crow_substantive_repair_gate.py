#!/usr/bin/env python3
import argparse,json,re,sys
sys.path.insert(0,__file__.rsplit('/',1)[0]);import complete_49_tool as core
VERSION="germinal-crow-substantive-repair-gate-v1";FORMAT="germinal-crow-substantive-repair-49-output-v1";ASSIGNMENT="germinal-crow1-substantive-repair-49-2"
ROOTS=("intentions","usage","forms","responses","followUps","dialogue","editorialRationales")
GATES=("meaningAndIntentions","usageAndRelationships","japaneseNaturalness","responseFit","followUpFit","dialogueCoherence","segmentAccuracy","evidenceBoundary","searchableForms")
FORBIDDEN=("source-anchored preview draft","has not received the accepted Card","Context-fitting response to","Alternative natural response after","Useful continuation following","Alternative continuation after","The familiar interlocutor","Help a learner recognize and produce","Communicate:")
def loadj(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def loadn(p):
 with open(p,encoding="utf-8") as f:return [json.loads(x) for x in f if x.strip()]
def validate(mat,base,man,rows):
 core.FORMAT=FORMAT;core.ASSIGNMENT=ASSIGNMENT;e=core.validate(mat,man,rows)
 def n(ok,p,m):
  if not ok:e.append(p+": "+m)
 n(len(base)==49,"/baseline","49 records required");n(man.get("submitted")==49 and man.get("quarantined")==0,"/manifest","all 49 must be candidate-complete after direct repair")
 for i,(b,r) in enumerate(zip(base,rows)):
  p=f"/records/{i}";t=json.dumps(r,ensure_ascii=False);n(r.get("id")==b.get("id"),p+"/id","baseline order mismatch");n(r.get("publicationStatus")=="candidate-complete",p+"/publicationStatus","must be candidate-complete");n(sum(r.get(k)!=b.get(k) for k in ROOTS)>=6,p,"fewer than six substantive roots changed");n(not any(x in t for x in FORBIDDEN),p,"forbidden boilerplate retained");n(not re.search(r"[.!?][.]",t),p,"doubled terminal punctuation retained");pr=r.get("primary",{}).get("japanese");n(any(x.get("japanese")!=pr for x in r.get("forms",[])),p+"/forms","requires genuine alternate form");n(all(x.get("japanese")!=pr for x in r.get("responses",[])),p+"/responses","response repeats target");n(sum(x.get("japanese")==pr for x in r.get("dialogue",[]))==1,p+"/dialogue","target must occur exactly once");v=r.get("crowReview");n(isinstance(v,dict),p+"/crowReview","required")
  if isinstance(v,dict):
   gs=v.get("gates");n(isinstance(gs,dict) and set(gs)==set(GATES) and all(x is True for x in gs.values()),p+"/crowReview/gates","exact post-repair passes required");ap=v.get("repairsApplied");n(isinstance(ap,list) and len(ap)>=5,p+"/crowReview/repairsApplied","five substantive repairs required")
   if isinstance(ap,list):n(len({x.get("pointer") for x in ap if isinstance(x,dict) and x.get("pointer")!="/crowReview"})>=5,p+"/crowReview/repairsApplied","five distinct substantive pointers required")
   n(isinstance(v.get("finalRationale"),str) and len(v["finalRationale"])>=120,p+"/crowReview/finalRationale","Card-specific rationale required")
 return e
def self_test():
 assert len(ROOTS)==7 and len(GATES)==9 and len(FORBIDDEN)==9;assert re.search(r"[.!?][.]","wrong?.")
def main():
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd");s.add_parser("self-test")
 for z in ("validate","package"):
  q=s.add_parser(z);q.add_argument("material");q.add_argument("baseline");q.add_argument("manifest");q.add_argument("records");
  if z=="package":q.add_argument("output")
 x=p.parse_args()
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed"}));return
 mat,base,man,rows=loadj(x.material),loadn(x.baseline),loadj(x.manifest),loadn(x.records);e=validate(mat,base,man,rows)
 if e:print(json.dumps({"valid":False,"problems":e}));raise SystemExit(2)
 if x.cmd=="validate":print(json.dumps({"valid":True,"problems":[]}));return
 core.FORMAT=FORMAT;core.ASSIGNMENT=ASSIGNMENT;n,d=core.package(mat,man,rows,x.output);print(json.dumps({"valid":True,"bytes":n,"sha256":d}))
if __name__=="__main__":main()
