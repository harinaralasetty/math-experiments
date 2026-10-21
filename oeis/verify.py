"""Recompute the distributed b-files with both original independent methods."""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='Check published overlap only, not extensions')
    args = parser.parse_args()
    data = json.loads((ROOT/'data/verification.json').read_text())
    def run(seq, method):
        limit = seq['listed_last'] if args.quick else seq['last']
        p = subprocess.run([sys.executable, 'code/compute_new.py', seq['id'], method, str(limit)],
                           cwd=ROOT, check=True, capture_output=True, text=True, timeout=7150)
        result = json.loads(p.stdout)
        rows = [list(map(int, line.split())) for line in (ROOT.parent/'docs/data'/f"{seq['id']}.txt").read_text().splitlines() if line and not line.startswith('#')]
        assert rows[:limit+1] == [[i, value] for i, value in enumerate(result['values'])]
        assert result['values'][:seq['listed_last']+1] == list(map(int, json.loads((ROOT/'data'/f"{seq['id']}.json").read_text())['data'].split(',')))
        print(f"{seq['id']} {method} indices=0..{limit} PASS wall_seconds={result['wall_seconds']:.6f}", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run, seq, method) for seq in data['sequences'] for method in ['reference', 'independent']]
        for job in as_completed(jobs):
            job.result()
    print('PASS published overlap only' if args.quick else 'PASS all extended b-files recomputed by both methods', flush=True)


if __name__ == '__main__':
    main()
