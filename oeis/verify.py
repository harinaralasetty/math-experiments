"""Recompute the distributed b-files with both original independent methods."""
import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='Check published overlap only, not extensions')
    args = parser.parse_args()
    data = {'sequences': [seq for name in ['verification.json', 'stage3-verification.json', 'stage4-verification.json']
                          for seq in json.loads((ROOT/'data'/name).read_text())['sequences']]}
    stage3_ids = {s['id'] for s in json.loads((ROOT/'data/stage3-verification.json').read_text())['sequences']}
    stage4_ids = {s['id'] for s in json.loads((ROOT/'data/stage4-verification.json').read_text())['sequences']}
    def run(seq, method):
        limit = seq['listed_last'] if args.quick else seq['last']
        first = seq.get('first', 0)
        if seq['id'] in stage4_ids:
            if seq['id'] == 'A325549':
                command = (['code/stage4/necklaces', str(limit)] if method == 'reference' else
                           [sys.executable, 'code/stage4/necklace_independent.py', str(first), str(limit)])
            else:
                program = ([sys.executable, 'code/stage4/reference.py'] if method == 'reference' else
                           ['code/stage4/independent'])
                command = [*program, seq['id'], str(first), str(limit)]
        else:
            program = 'code/stage3/compute.py' if seq['id'] in stage3_ids else 'code/compute_new.py'
            command = [sys.executable, program, seq['id'], method, str(limit)]
        started = time.perf_counter()
        p = subprocess.run(command,
                           cwd=ROOT, check=True, capture_output=True, text=True, timeout=7150)
        elapsed = time.perf_counter() - started
        if seq['id'] in stage4_ids:
            computed = [json.loads(line) for line in p.stdout.splitlines()]
            value_key = 'circular' if seq['id'] == 'A325549' and method == 'reference' else 'value'
            result = dict(values=[row[value_key] for row in computed],
                          wall_seconds=elapsed)
            assert [row['n'] for row in computed] == list(range(first, limit+1))
        else:
            result = json.loads(p.stdout)
        rows = [list(map(int, line.split())) for line in (ROOT.parent/'docs/data'/f"{seq['id']}.txt").read_text().splitlines() if line and not line.startswith('#')]
        assert rows[:limit-first+1] == [[i, value] for i, value in enumerate(result['values'], first)]
        assert len(result['values']) == limit-first+1
        assert result['values'][:seq['listed_last']-first+1] == list(map(int, json.loads((ROOT/'data'/f"{seq['id']}.json").read_text())['data'].split(',')))
        print(f"{seq['id']} {method} indices={first}..{limit} PASS wall_seconds={result['wall_seconds']:.6f}", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run, seq, method) for seq in data['sequences'] for method in ['reference', 'independent']]
        for job in as_completed(jobs):
            job.result()
    print('PASS published overlap only' if args.quick else 'PASS all extended b-files recomputed by both methods', flush=True)


if __name__ == '__main__':
    main()
