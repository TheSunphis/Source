#!/usr/bin/env python3
import argparse,hashlib,json,re,sys
VERSION="koto-vocabulary-tool-v1"
BAD_KEYS={"commonness","cefr","jlpt","jfStandard","frequencyGrade"}
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
def ndjson(rows):return b"".join(canon(x) for x in rows)
def sha(b):return hashlib.sha256(b).hexdigest()
def vocabulary_id(identity):return "vocabulary2:"+hashlib.sha256(b"koto-vocabulary-v1\0"+json.dumps(identity,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:32]
def no_bad_keys(o,path=""):
 out=[]
 if isinstance(o,dict):
  for k,v in o.items():
   if k in BAD_KEYS:out.append(path+"/"+k+": prohibited grading field")
   out.extend(no_bad_keys(v,path+"/"+k))
 elif isinstance(o,list):
  for i,v in enumerate(o):out.extend(no_bad_keys(v,path+f"/{i}"))
 return out
def load_json(p):
 with open(p,encoding="utf-8") as f:return json.load(f)
def load_ndjson(p):
 with open(p,encoding="utf-8") as f:return [json.loads(x) for x in f if x.strip()]
def validate(manifest,records,ledger):
 e=[]
 if manifest.get("formatVersion")!="koto-vocabulary-build-v1":e.append("/manifest/formatVersion: wrong format")
 if not records:e.append("/records: empty")
 ids=[]
 for i,r in enumerate(records):
  p=f"/records/{i}";e.extend(no_bad_keys(r,p));identity=r.get("identity")
  if r.get("formatVersion")!="koto-vocabulary-record-v1":e.append(p+"/formatVersion: wrong format")
  if not isinstance(identity,dict) or set(identity)!={"canonicalLemma","canonicalReading","lexicalCategory","senseKey"}:e.append(p+"/identity: exact identity keys required")
  elif r.get("vocabularyId")!=vocabulary_id(identity):e.append(p+"/vocabularyId: deterministic identity mismatch")
  ids.append(r.get("vocabularyId"))
  if r.get("status") not in ("candidate","accepted","quarantined","redirected"):e.append(p+"/status: invalid")
  if not r.get("forms") or not r.get("senses") or not r.get("sourceRefs"):e.append(p+": forms, senses and sourceRefs required")
  for j,x in enumerate(r.get("sourceRefs",[])):
   if x.get("sourceId")!="JMdict" or not re.fullmatch(r"[0-9a-f]{64}",str(x.get("snapshotSha256",""))):e.append(p+f"/sourceRefs/{j}: invalid JMdict source")
 if len(ids)!=len(set(ids)):e.append("/records: duplicate IDs")
 if manifest.get("recordIds")!=ids:e.append("/manifest/recordIds: order or identity mismatch")
 if manifest.get("recordCount")!=len(records):e.append("/manifest/recordCount: mismatch")
 if manifest.get("recordsSha256")!=sha(ndjson(records)):e.append("/manifest/recordsSha256: mismatch")
 if manifest.get("ledgerEventCount")!=len(ledger) or manifest.get("ledgerSha256")!=sha(ndjson(ledger)):e.append("/manifest/ledger: count/digest mismatch")
 if [x.get("sequence") for x in ledger]!=list(range(1,len(ledger)+1)):e.append("/ledger: non-contiguous sequence")
 for i,x in enumerate(ledger):
  if x.get("action")=="admit" and x.get("vocabularyId") not in ids:e.append(f"/ledger/{i}: admitted unknown ID")
  if x.get("recordSha256") not in {sha(canon(r)) for r in records}:e.append(f"/ledger/{i}/recordSha256: unknown record")
 return e
def self_test():
 ident={"canonicalLemma":"いい","canonicalReading":"いい","lexicalCategory":"adjective","senseKey":"acceptable-all-right-no-problem"};assert vocabulary_id(ident)=="vocabulary2:9388217c802184c295872c8415e616c2";assert no_bad_keys({"commonness":1});return True
def main(argv=None):
 a=argparse.ArgumentParser();a.add_argument("--version",action="store_true");sub=a.add_subparsers(dest="cmd");sub.add_parser("self-test");p=sub.add_parser("canonical-id");p.add_argument("identity_json");p=sub.add_parser("validate-registry");p.add_argument("manifest");p.add_argument("records");p.add_argument("ledger");x=a.parse_args(argv)
 if x.version:print(VERSION);return 0
 if x.cmd=="self-test":self_test();print(json.dumps({"tool":VERSION,"selfTest":"passed"}));return 0
 if x.cmd=="canonical-id":print(vocabulary_id(load_json(x.identity_json)));return 0
 if x.cmd=="validate-registry":
  e=validate(load_json(x.manifest),load_ndjson(x.records),load_ndjson(x.ledger));print(json.dumps({"valid":not e,"problems":e},ensure_ascii=False));return 0 if not e else 2
 a.error("command required")
if __name__=="__main__":raise SystemExit(main())
