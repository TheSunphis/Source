#!/usr/bin/env python3
import argparse,hashlib,json
VERSION="germinal-compiled-card-tool-v1"
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def ndjson(xs):return b"".join(canon(x) for x in xs)
def sha(b):return hashlib.sha256(b).hexdigest()
def loadj(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def loadn(p):
 with open(p,encoding="utf-8") as f:return [json.loads(x) for x in f if x.strip()]
def validate(manifest,card,links,records):
 e=[];reg={x.get("vocabularyId"):x for x in records};lines=card.get("japaneseLines",{}) if isinstance(card,dict) else {};segs=[]
 for lid,line in lines.items():
  for i,s in enumerate(line.get("segments",[])):segs.append((f"/japaneseLines/{lid}/segments/{i}",s))
 if manifest.get("formatVersion")!="germinal-compiled-goldcard-v1":e.append("/manifest/formatVersion: wrong format")
 if manifest.get("cardSha256")!=sha(canon(card)):e.append("/manifest/cardSha256: mismatch")
 if manifest.get("linksSha256")!=sha(ndjson(links)):e.append("/manifest/linksSha256: mismatch")
 if manifest.get("segmentCount")!=len(segs) or manifest.get("linkCount")!=len(links):e.append("/manifest: count mismatch")
 by={x.get("segmentPointer"):x for x in links}
 if len(by)!=len(links):e.append("/links: duplicate pointer")
 linked=unlinked=0
 for pointer,s in segs:
  x=by.get(pointer)
  if not x:e.append(pointer+": missing link");continue
  if x.get("surface")!=s.get("surface") or x.get("reading")!=s.get("reading"):e.append(pointer+": surface/reading mismatch")
  cl=s.get("canonicalVocabularyLink")
  if x.get("status")=="linked":
   linked+=1;vid=x.get("vocabularyId");r=reg.get(vid)
   if not r:e.append(pointer+": unknown vocabulary ID");continue
   if s.get("selectedVocabularyId")!=vid or s.get("vocabularyDisposition")!="linked-zero-canonical-index-v1":e.append(pointer+": compiled fields mismatch")
   if not isinstance(cl,dict) or cl.get("status")!="linked" or cl.get("vocabularyId")!=vid or cl.get("reverseChecked") is not True:e.append(pointer+": canonical link object mismatch")
   if not any(f.get("surface")==s.get("surface") and f.get("reading")==s.get("reading") for f in r.get("forms",[])):e.append(pointer+": no exact form in canonical record")
  elif x.get("status")=="unlinked":
   unlinked+=1
   if s.get("kind")!="punctuation" or s.get("selectedVocabularyId") is not None or s.get("vocabularyDisposition")!="unlinked-punctuation":e.append(pointer+": only punctuation may be unlinked")
   if not isinstance(cl,dict) or cl.get("status")!="unlinked" or cl.get("reasonCode")!="punctuation" or cl.get("reverseChecked") is not True:e.append(pointer+": unlinked object mismatch")
  else:e.append(pointer+": invalid link status")
 if manifest.get("linkedCount")!=linked or manifest.get("unlinkedCount")!=unlinked:e.append("/manifest: link disposition counts mismatch")
 return e
def self_test():
 r={"vocabularyId":"vocabulary2:"+"a"*32,"forms":[{"surface":"語","reading":"ご"}]};s={"surface":"語","reading":"ご","kind":"content-or-idiom","selectedVocabularyId":r["vocabularyId"],"vocabularyDisposition":"linked-zero-canonical-index-v1","canonicalVocabularyLink":{"status":"linked","vocabularyId":r["vocabularyId"],"reverseChecked":True}};c={"japaneseLines":{"l":{"segments":[s]}}};links=[{"segmentPointer":"/japaneseLines/l/segments/0","surface":"語","reading":"ご","status":"linked","vocabularyId":r["vocabularyId"]}];m={"formatVersion":"germinal-compiled-goldcard-v1","cardSha256":sha(canon(c)),"linksSha256":sha(ndjson(links)),"segmentCount":1,"linkCount":1,"linkedCount":1,"unlinkedCount":0};assert not validate(m,c,links,[r]);return True
def main(argv=None):
 a=argparse.ArgumentParser();sub=a.add_subparsers(dest="cmd");sub.add_parser("self-test");p=sub.add_parser("validate");[p.add_argument(x) for x in ("manifest","card","links","registry")];x=a.parse_args(argv)
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed"}));return 0
 if x.cmd=="validate":
  e=validate(loadj(x.manifest),loadj(x.card),loadn(x.links),loadn(x.registry));print(json.dumps({"valid":not e,"problems":e}));return 0 if not e else 2
 a.error("command required")
if __name__=="__main__":raise SystemExit(main())
