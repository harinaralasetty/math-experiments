"""One clean-process method run. Stdout is a machine-readable checkpoint."""
import argparse
import json
import resource
import subprocess
import time
from pathlib import Path

import independent
import new_independent
import new_reference
import reference

ROOT = Path(__file__).resolve().parents[1]


def compute(a, method, limit, cap):
    details = {}
    if a == 'A391646':
        if method == 'reference':
            values = new_reference.prime_minima(limit, cap)
        else:
            p = subprocess.run([str(ROOT/'code/new_powerful'), str(limit), str(cap)],
                check=True, capture_output=True, text=True, timeout=7100)
            details = json.loads(p.stdout)
            values = details.pop('values')
        assert max(values) <= cap, 'search cap did not enclose all minima'
        details['cap'] = cap
    elif a == 'A374679':
        fn = new_reference.anti_leaders if method == 'reference' else new_independent.anti_leaders
        values = fn(limit)
    elif a == 'A383533':
        fn = (lambda n: reference.partition_count(n, True)) if method == 'reference' else independent.feasible_partition_counts
        values, rows = [], []
        for n in range(limit+1):
            t = time.perf_counter()
            values.append(fn(n))
            rows.append(dict(n=n, seconds=time.perf_counter()-t))
        details['timings'] = rows
    elif a == 'A335457' and method == 'independent':
        values = new_independent.pattern_totals(limit)
        details['normalization_cache'] = new_independent.normal.cache_info()._asdict()
    else:
        if a == 'A335457':
            cmd = [str(ROOT/'code/new_patterns'), str(limit)]
        elif method == 'reference':
            cmd = [str(ROOT/'code/new_runs'), str(limit)]
        else:
            cmd = [str(ROOT/'code/cut_runs'), str(limit)]
        p = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=7100)
        rows = [json.loads(line) for line in p.stdout.splitlines()]
        assert [r['n'] for r in rows] == list(range(limit+1))
        values = [r['value'] for r in rows]
        details['rows'] = rows
        details['command'] = cmd
    return values, details


def main():
    p = argparse.ArgumentParser()
    p.add_argument('id')
    p.add_argument('method', choices=['reference', 'independent'])
    p.add_argument('limit', type=int)
    p.add_argument('--cap', type=int, default=(1 << 128) - 2)
    args = p.parse_args()
    wall, cpu = time.perf_counter(), time.process_time()
    values, details = compute(args.id, args.method, args.limit, args.cap)
    child = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(json.dumps(dict(id=args.id, method=args.method, limit=args.limit,
        values=values, details=details, wall_seconds=time.perf_counter()-wall,
        cpu_seconds=time.process_time()-cpu+child.ru_utime+child.ru_stime,
        child_maxrss=child.ru_maxrss,
        self_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == '__main__':
    main()
