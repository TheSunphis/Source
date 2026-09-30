#!/usr/bin/env python3
from __future__ import annotations
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args,env=None):subprocess.run(args,cwd=ROOT,env=env,check=True)
def main():
 if not os.environ.get('GITHUB_ACTIONS'):raise SystemExit('GitHub Actions only')
 env=dict(os.environ); runtime=Path('/tmp/expressions2-runtime'); run(sys.executable,'-m','pip','install','--disable-pip-version-check','--no-deps','--require-hashes','--target',str(runtime),'-r','runtime/requirements-linux-x86_64.lock'); env['PYTHONPATH']=str(runtime); env['EXPRESSIONS2_RUNTIME']=str(runtime)
 run(sys.executable,'tools/build_evidence_stores.py',env=env); run(sys.executable,'remote/build_candidates.py',env=env); run(sys.executable,'tools/guard_clean_room.py','--self-test',env=env)
 bundle=Path('/tmp/expressions2-batch001-candidates.tar.gz'); run('tar','-czf',str(bundle),'evidence','candidates','snapshots','source-registry')
 tag='expressions2-0.1.0-development-shadow'; token=os.environ['GH_TOKEN']; gh=dict(env); gh['GH_TOKEN']=token
 view=subprocess.run(['gh','release','view',tag,'--repo',os.environ['EXPRESSIONS2_REPOSITORY']],env=gh,cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 if view.returncode:run('gh','release','create',tag,'--repo',os.environ['EXPRESSIONS2_REPOSITORY'],'--target',os.environ['EXPRESSIONS2_BRANCH'],'--title','Expressions2 0.1.0-development shadow','--notes','Private commissioning artifacts. Not production.','--draft',str(bundle),env=gh)
 else:run('gh','release','upload',tag,str(bundle),'--repo',os.environ['EXPRESSIONS2_REPOSITORY'],'--clobber',env=gh)
 print('REMOTE_CANDIDATE_STAGE_PASS')
 return 0
if __name__=='__main__':raise SystemExit(main())
