#!/usr/bin/env python3
"""Machine Economy Lab: reproducible single-agent baseline experiments.

Requires Python 3.10+; optionally the `codex` CLI for running an agent.
No third-party Python packages.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / 'runs'
RESULTS = ROOT / 'results.csv'
FIELDS = ['run_id','task_id','condition','model_name','codex_cli_version','run_status','tests_passed','tests_run',
          'input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens',
          'wall_seconds','actual_cash_cost_usd','estimated_api_cost_usd','hypothetical_contract_usd',
          'net_income_usd','notes']


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def manifest():
    return {x['task_id']:x for x in json.loads((ROOT/'tasks.json').read_text())}


def require_run_id(s: str):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', s):
        raise ValueError('run-id must contain only letters, digits, _ or - (max 64)')
    return s


def path_for_run(run_id: str):
    return RUNS / require_run_id(run_id)


def prepare(task_id: str, run_id: str | None = None) -> Path:
    if task_id not in manifest():
        raise ValueError(f'Unknown task {task_id!r}. Use `list`.')
    run_id = require_run_id(run_id or f'{task_id}-{utc_stamp()}')
    run_dir = path_for_run(run_id)
    if run_dir.exists():
        raise ValueError(f'Run already exists: {run_dir}')
    RUNS.mkdir(exist_ok=True)
    workspace = run_dir/'workspace'
    shutil.copytree(ROOT/'tasks'/task_id, workspace)
    metadata = {
        'run_id':run_id,'task_id':task_id,'condition':'single_agent',
        'created_at_utc':datetime.now(timezone.utc).isoformat(),
        'status':'prepared','notes':''
    }
    (run_dir/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return run_dir


def grader_result(task_id: str, solution_folder: Path) -> dict:
    grader = ROOT/'graders'/f'{task_id}_test.py'
    env=os.environ.copy()
    env['PYTHONPATH']=str(solution_folder)
    proc=subprocess.run([sys.executable,str(grader)],cwd=solution_folder,env=env,
                        capture_output=True,text=True,timeout=30)
    stdout=proc.stdout+'\n'+proc.stderr
    match=re.search(r'Ran (\d+) tests?',stdout)
    return {'tests_run':int(match.group(1)) if match else None,
            'tests_passed':proc.returncode == 0,
            'test_output':stdout[-16000:]}


def usage_from_events(event_file: Path) -> dict:
    usage={'input_tokens':None,'cached_input_tokens':None,
           'output_tokens':None,'reasoning_output_tokens':None}
    if not event_file.exists():
        return usage
    sums={k:0 for k in usage}
    completed=0
    for ln in event_file.read_text(encoding='utf-8',errors='replace').splitlines():
        try: e=json.loads(ln)
        except (json.JSONDecodeError,ValueError): continue
        if e.get('type') != 'turn.completed': continue
        u=e.get('usage') or {}
        completed+=1
        for k in sums:
            sums[k]+=int(u.get(k,0) or 0)
    if completed:
        return sums
    return usage


def refresh_csv():
    RUNS.mkdir(exist_ok=True)
    rows=[]
    for p in sorted(RUNS.glob('*/result.json')):
        try:
            r=json.loads(p.read_text())
            rows.append({k:r.get(k,'') if r.get(k) is not None else '' for k in FIELDS})
        except (ValueError,OSError):
            pass
    with RESULTS.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def evaluate(run_id: str, wall_seconds: float | None = None):
    run_dir=path_for_run(run_id)
    meta_path=run_dir/'metadata.json'
    if not meta_path.exists():
        raise ValueError(f'Run not found: {run_id}')
    meta=json.loads(meta_path.read_text())
    task_id=meta['task_id']
    status=meta.get('status','prepared')
    failed_to_execute = status.startswith('agent_failed_exit_') or status == 'agent_timeout'
    if failed_to_execute:
        # A Codex launch/auth/timeout error is NOT evidence of incorrect agent code.
        grades={'tests_run':None, 'tests_passed':None,
                'test_output':f'NOT GRADED: Codex did not complete successfully ({status}).\n'
                              'Inspect codex_stderr.txt and codex_events.jsonl for the underlying error.\n'}
    else:
        grades=grader_result(task_id, run_dir/'workspace')
    (run_dir/'grader_output.txt').write_text(grades['test_output'],encoding='utf-8')
    u=usage_from_events(run_dir/'codex_events.jsonl')
    record={k:None for k in FIELDS}
    record.update({'run_id':run_id,'task_id':task_id,'condition':meta.get('condition','single_agent'),
                   'model_name':meta.get('model_name'),'codex_cli_version':meta.get('codex_cli_version'),
                   'run_status':meta.get('status','prepared'),
                   'tests_passed':grades['tests_passed'],'tests_run':grades['tests_run'],
                   'wall_seconds':wall_seconds if wall_seconds is not None else meta.get('wall_seconds'),
                   'hypothetical_contract_usd':manifest()[task_id]['hypothetical_contract_usd'],
                   'notes':meta.get('notes','')})
    record.update(u)
    # These fields intentionally remain blank. They are not inferable from token counts
    # or hypothetical task prices. There is no revenue in this synthetic benchmark.
    (run_dir/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    refresh_csv()
    if failed_to_execute:
        print(f'{run_id}: AGENT EXECUTION ERROR ({status}); task was NOT graded')
        print(f'Diagnostics: {run_dir/"codex_stderr.txt"} and {run_dir/"codex_events.jsonl"}')
    else:
        print(f"{run_id}: {'PASS' if grades['tests_passed'] else 'FAIL'} "
              f"({grades['tests_run'] or 0} grader tests)")
    print(f"Grader: {run_dir/'grader_output.txt'}")
    print(f"Ledger: {RESULTS}")
    return grades['tests_passed']


def execute_with_codex(task_id: str, run_id: str | None, timeout: int, model: str | None = None):
    if not shutil.which('codex'):
        raise RuntimeError('`codex` not found on PATH. Install/login to Codex or use prepare + manual agent run.')
    run_dir=prepare(task_id,run_id)
    workspace=run_dir/'workspace'
    meta_path=run_dir/'metadata.json'
    meta=json.loads(meta_path.read_text())
    meta['model_name']=model or 'CLI configured default (record separately)'
    ver=subprocess.run(['codex','--version'],capture_output=True,text=True,timeout=15)
    meta['codex_cli_version']=ver.stdout.strip()
    spec=(workspace/'task.md').read_text(encoding='utf-8')
    prompt=f'''You are taking part in a controlled single-agent software benchmark.\n\n{spec}\n\nWork ONLY inside the current workspace. Edit solution.py, and you may run python example_check.py.\nDo not inspect any files outside this workspace, including grader or reference solutions.\nDo not use the internet, install packages, or access production credentials.\nYou may use the Python standard library.\nImplement the code as robustly as possible, then run the public example check.\n'''
    # The user deliberately invokes this command to authorize the agent run.
    cmd=['codex','exec','--json','--sandbox','workspace-write',
         '--skip-git-repo-check','--cd',str(workspace),'-']
    if model:
        cmd[2:2]=['--model',model]
    started=time.monotonic()
    try:
        proc=subprocess.run(cmd,input=prompt,text=True,capture_output=True,
                            cwd=workspace,timeout=timeout,check=False)
        meta['status']='agent_completed' if proc.returncode == 0 else f'agent_failed_exit_{proc.returncode}'
        (run_dir/'codex_events.jsonl').write_text(proc.stdout,encoding='utf-8')
        (run_dir/'codex_stderr.txt').write_text(proc.stderr,encoding='utf-8')
    except subprocess.TimeoutExpired as ex:
        meta['status']='agent_timeout'
        (run_dir/'codex_events.jsonl').write_text((ex.stdout or b'').decode('utf-8','replace') if isinstance(ex.stdout,bytes) else (ex.stdout or ''),encoding='utf-8')
        (run_dir/'codex_stderr.txt').write_text((ex.stderr or b'').decode('utf-8','replace') if isinstance(ex.stderr,bytes) else (ex.stderr or ''),encoding='utf-8')
    meta['wall_seconds']=round(time.monotonic()-started,2)
    meta_path.write_text(json.dumps(meta,indent=2)+'\n')
    evaluate(meta['run_id'],meta['wall_seconds'])


def self_test():
    passed=0
    for task_id in manifest():
        ref=ROOT/'references'/task_id
        check=grader_result(task_id,ref)
        if not check['tests_passed']:
            print(f'[FAIL] {task_id}: {check["test_output"]}')
        else:
            print(f'[PASS] {task_id}: {check["tests_run"]} tests')
            passed+=1
    print(f'Reference solutions pass: {passed}/{len(manifest())}')
    if passed != len(manifest()):
        raise SystemExit(1)


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('list',help='List the six coding tasks')
    sub.add_parser('self-test',help='Check independent graders against reference solutions')
    p=sub.add_parser('prepare',help='Create isolated workspace for a manual agent session')
    p.add_argument('task_id');p.add_argument('--run-id')
    p=sub.add_parser('run',help='Run one task using authenticated Codex CLI and grade it')
    p.add_argument('task_id');p.add_argument('--run-id');p.add_argument('--timeout',type=int,default=900);p.add_argument('--model')
    p=sub.add_parser('evaluate',help='Grade a prepared/manual experiment workspace')
    p.add_argument('run_id');p.add_argument('--wall-seconds',type=float)
    args=parser.parse_args()
    try:
        if args.command=='list':
            for t in manifest().values():
                print(f"{t['task_id']:25} {t['complexity']:7} {t['title']}")
        elif args.command=='self-test':self_test()
        elif args.command=='prepare':
            run_dir=prepare(args.task_id,args.run_id)
            print(f'Workspace: {run_dir/"workspace"}')
            print(f'After agent edits solution.py: python lab.py evaluate {run_dir.name}')
        elif args.command=='run':execute_with_codex(args.task_id,args.run_id,args.timeout,args.model)
        elif args.command=='evaluate':evaluate(args.run_id,args.wall_seconds)
    except (ValueError,RuntimeError,OSError) as exc:
        print(f'Error: {exc}',file=sys.stderr)
        raise SystemExit(2)

if __name__=='__main__':main()
