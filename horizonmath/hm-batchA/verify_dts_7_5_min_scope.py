#!/usr/bin/env python3
"""Independent exact checker. Claimed scores are never read."""
import json
import sys
from collections import Counter


def verify(solution):
    if not isinstance(solution, dict):
        raise ValueError('expected object')
    if type(solution.get('n')) is not int or solution['n'] != 7:
        raise ValueError('n must be integer 7')
    if type(solution.get('k')) is not int or solution['k'] != 5:
        raise ValueError('k must be integer 5')
    rows = solution.get('rows')
    if not isinstance(rows, list) or len(rows) != 7:
        raise ValueError('expected seven rows')
    differences = []
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 6:
            raise ValueError(f'row {i}: expected six marks')
        if any(type(x) is not int for x in row):
            raise ValueError(f'row {i}: marks must be integers, excluding bool')
        if row[0] != 0 or any(a >= b for a, b in zip(row, row[1:])):
            raise ValueError(f'row {i}: not normalized and strictly increasing')
        differences.extend(row[j] - row[k] for j in range(6) for k in range(j))
    counts = Counter(differences)
    repeated = sorted(d for d, count in counts.items() if count != 1)
    if repeated:
        raise ValueError(f'repeated positive differences: {repeated}')
    return {'scope': max(max(row) for row in rows),
            'num_differences': len(differences), 'distinct_differences': len(counts)}


def main():
    try:
        result = {'valid': True, **verify(json.load(open(sys.argv[1])))}
    except (ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'valid': False, 'reason': str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
