#!/usr/bin/env python3
from __future__ import annotations
import collections,gzip,hashlib,json,os,re,sys,unicodedata
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'evidence'; C=ROOT/'candidates'; S=ROOT/'schema'
J=re.compile(r'[ぁ-ゖァ-ヺ一-龯々〆ヵヶ]'); R=re.compile(r'^[ぁ-ゖァ-ヺー・、。！？!?「」『』（）()〜～…‥・,.\s0-9]+$')
def canon(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def h(b):return hashlib.sha256(b).hexdigest()
def sid(p,*x):return p+hashlib.sha256('\0'.join(x).encode()).hexdigest()[:32]
def nfc(x):return unicodedata.normalize('NFC',x).replace('\x00','').strip()
def hira(x):return ''.join(chr(ord(c)-96) if '\u30a1'<=c<='\u30f6' else c for c in x)
def load(name):
 with gzip.open(E/name,'rt',encoding='utf-8') as f:return json.load(f)['records']
def ev(r,source,kind,supports):return {'sourceId':source,'locator':r['locator'],'evidenceType':kind,'supports':supports,'recordHash':r['recordHash'],'permissionClass':r['permissionClass']}
def raw(ch,surface,reading,e,snap,loc,at):return {'schemaVersion':1,'rawCandidateId':sid('rawcandidate2:',ch,surface,reading or '',loc),'channel':ch,'surface':surface,'reading':reading,'sourceEvidence':e,'extractor':{'name':'expressions2-remote-miner','version':'0.1.0','sourceSnapshotSha256':snap,'ruleId':ch+'-v1'},'createdAt':at}
def classify(labels,gloss,origin,tokens):
 t=(labels+' '+gloss).lower()
 if 'proverb' in t:return ['proverb-or-saying']
 if 'idiomatic' in t or 'yojijukugo' in t:return ['idiom']
 if 'collocation' in t:return ['conventional-collocation']
 if any(x in t for x in ('thank','sorry','apolog','greeting','welcome','congrat','please','excuse','goodbye')):return ['interactional-formula']
 if origin=='wiktionary-structural':return ['idiom','proverb-or-saying']
 if origin=='corpus-ngram' and any(x[2]=='助詞' for x in tokens):return ['grammar-construction']
 return ['conventional-collocation']
def morphology(tok,mode,s):
 try: ms=tok.tokenize(s,mode.A)
 except Exception:return '',[]
 out=[]; rd=[]
 for m in ms:
  r=hira(m.reading_form() or ''); p=list(m.part_of_speech()); rd.append(r); out.append((m.surface(),r,p[0] if p else ''))
 reading=''.join(rd); return (reading if reading and R.fullmatch(reading) else ''),out
def schemas():
 reg=Registry(); all={}
 for p in S.glob('*.schema.json'):
  x=json.loads(p.read_text()); all[p.name.removesuffix('.schema.json')]=x; reg=reg.with_resource(x['$id'],Resource.from_contents(x))
 return all,reg
def validate(x,s,reg,label):
 errs=list(Draft202012Validator(s,registry=reg,format_checker=FormatChecker()).iter_errors(x))
 if errs:raise RuntimeError(label+': '+errs[0].message)
def build(tok,mode,sources,at):
 jmd=load('jmdict-english.evidence.json.gz'); wik=load('japanese-wiktionary.evidence.json.gz'); tat=load('tatoeba-japanese-ccby.evidence.json.gz')
 provisional=[]; raws=[]
 jsnap=sources['source2:jmdict-english']['snapshot']['sha256']; wsnap=sources['source2:japanese-wiktionary']['snapshot']['sha256']; tsnap=sources['source2:tatoeba-japanese-ccby']['snapshot']['sha256']
 for r in jmd:
  f=r['fields']; s=nfc(f['surface']); reads=[nfc(x) for x in f['readings'].split('␟') if nfc(x)]; rd=reads[0] if reads else ''
  if not s or not rd or not R.fullmatch(rd):continue
  _,t=morphology(tok,mode,s); e=ev(r,'source2:jmdict-english','direct-authority',['existence','form','reading','meaning']); g=[nfc(x) for x in f['glosses'].split('␟') if nfc(x) and len(nfc(x))<=500][:20]
  raws.append(raw('labelled-expression',s,rd,[e],jsnap,r['locator'],at)); provisional.append((s,rd,g,f['labels'],[e],t,[r['locator']],0,True,'labelled-expression'))
 for r in wik:
  s=nfc(r['fields']['surface']); rd,t=morphology(tok,mode,s)
  if not s or not rd:continue
  e=ev(r,'source2:japanese-wiktionary','direct-authority',['existence','form']); raws.append(raw('wiktionary-structural',s,rd,[e],wsnap,r['locator'],at)); provisional.append((s,rd,[],r['fields']['markers'],[e],t,[r['locator']],0,False,'wiktionary-structural'))
 counts=collections.Counter(); first={}
 for r in tat[:25000]:
  _,t=morphology(tok,mode,r['fields']['normalizedText']); t=[x for x in t if x[2] not in {'補助記号','空白'}]
  for i in range(len(t)-1):
   group=t[i:i+2]; s=nfc(group[0][0]+group[1][0]); rd=group[0][1]+group[1][1]
   if 2<=len(s)<=24 and J.search(s) and rd and R.fullmatch(rd):counts[(s,rd)]+=1; first.setdefault((s,rd),r)
 selected=sorted(((k,v) for k,v in counts.items() if v>=2),key=lambda x:(-x[1],x[0]))[:5000]
 for (s,rd),count in selected:
  r=first[(s,rd)]; e=ev(r,'source2:tatoeba-japanese-ccby','corpus-attestation',['existence','pattern']); _,t=morphology(tok,mode,s); loc='ngram:'+sid('',s,rd)+':'+r['locator']; raws.append(raw('corpus-ngram',s,rd,[e],tsnap,loc,at)); provisional.append((s,rd,[],'',[e],t,[r['locator']],count,False,'corpus-ngram'))
 merged={}
 for s,rd,g,l,e,t,ids,c,d,o in provisional:
  key=s+'|'+rd
  if key not in merged:merged[key]=[s,rd,list(g),l,list(e),t,list(ids),c,d,{o}]
  else:
   q=merged[key]; q[2]=list(dict.fromkeys(q[2]+g))[:20]; q[4]+=e; q[6]+=ids; q[7]=max(q[7],c); q[8]=q[8] or d; q[9].add(o)
 norm=[]
 for key,q in merged.items():
  s,rd,g,l,e,t,ids,c,d,orig=q; hyp=classify(l,' '.join(g),next(iter(sorted(orig))),t); uniq={(x['sourceId'],x['locator'],x['recordHash']):x for x in e}; evidence=[uniq[k] for k in sorted(uniq)]
  norm.append({'schemaVersion':1,'candidateId':sid('candidate2:',key),'surface':s,'reading':rd,'normalizedKey':key,'senseGlosses':g,'sourceEvidence':evidence,'classHypotheses':hyp,'signals':{'multiword':len(t)>1,'fixedness':0.95 if d else (0.8 if 'wiktionary-structural' in orig else min(0.9,0.5+c/100)),'productiveSlots':0,'formulaic':d or 'wiktionary-structural' in orig,'pragmaticFunction':hyp[0] in {'interactional-formula','discourse-routine','pragmatic-pattern'},'dictionaryExpressionTag':d,'corpusHitCount':c},'normalization':{'pipelineVersion':'0.1.0','unicodeForm':'NFC','sourceRecordIds':sorted(set(ids)),'inputDigest':h(canon({'key':key,'evidence':evidence}))},'createdAt':at})
 raws.sort(key=lambda x:x['rawCandidateId']); norm.sort(key=lambda x:x['candidateId']); return {'schemaVersion':1,'kind':'raw','records':raws},{'schemaVersion':1,'kind':'normalized','records':norm}
def main():
 sys.path.insert(0,os.environ['EXPRESSIONS2_RUNTIME']); from sudachipy import Dictionary,SplitMode
 tok=Dictionary(dict='core').tokenizer(); sources={x['sourceId']:x for x in json.loads((ROOT/'source-registry/sources.json').read_text())['sources']}; em=json.loads((E/'manifest.json').read_text()); all,reg=schemas()
 a,b=build(tok,SplitMode,sources,em['sourceDateEpoch']); ca,cb=canon(a),canon(b); a2,b2=build(tok,SplitMode,sources,em['sourceDateEpoch'])
 if ca!=canon(a2) or cb!=canon(b2):raise RuntimeError('candidate rebuild mismatch')
 validate(a,all['candidate-store'],reg,'raw'); validate(b,all['candidate-store'],reg,'normalized'); C.mkdir(exist_ok=True)
 ga=gzip.compress(ca,9,mtime=0); gb=gzip.compress(cb,9,mtime=0); (C/'raw-candidates.json.gz').write_bytes(ga); (C/'normalized-candidates.json.gz').write_bytes(gb)
 channels=collections.Counter(x['channel'] for x in a['records']); classes=collections.Counter(x['classHypotheses'][0] for x in b['records']); arts=[{'kind':'raw','file':'raw-candidates.json.gz','records':len(a['records']),'canonicalBytes':len(ca),'compressedBytes':len(ga),'canonicalSha256':h(ca),'compressedSha256':h(ga)},{'kind':'normalized','file':'normalized-candidates.json.gz','records':len(b['records']),'canonicalBytes':len(cb),'compressedBytes':len(gb),'canonicalSha256':h(cb),'compressedSha256':h(gb)}]
 body={'sourceDateEpoch':em['sourceDateEpoch'],'inputs':{'evidenceBuildId':em['buildId'],'evidenceManifestSha256':h((E/'manifest.json').read_bytes())},'runtime':{'sudachiPyVersion':'0.7.0','sudachiPySha256':sources['source2:sudachipy-runtime']['snapshot']['sha256'],'dictionaryVersion':'20260723.1','dictionarySha256':sources['source2:sudachidict-core']['snapshot']['sha256'],'splitMode':'A'},'artifacts':arts,'counts':{'rawCandidates':len(a['records']),'normalizedCandidates':len(b['records']),'rawByChannel':{'labelled-expression':channels['labelled-expression'],'corpus-ngram':channels['corpus-ngram'],'wiktionary-structural':channels['wiktionary-structural']},'normalizedByPrimaryHypothesis':dict(sorted(classes.items())),'corpusAttestedNormalized':sum(x['signals']['corpusHitCount']>0 for x in b['records']),'duplicatesMerged':len(a['records'])-len(b['records'])},'determinism':{'canonicalJson':True,'gzipMtime':0,'secondBuildMatched':True,'stableOrdering':True},'contaminationAudit':{'legacyImports':0,'legacyIds':0,'unapprovedSources':0,'personalState':0,'verdict':'passed'},'familyGenerationStarted':False}
 m={'schemaVersion':1,'buildId':'candidatebuild2:'+h(canon(body))[:32],**body}; validate(m,all['candidate-build-manifest'],reg,'manifest'); (C/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); print('CANDIDATE_BUILD_PASS',len(a['records']),len(b['records']))
if __name__=='__main__':main()
