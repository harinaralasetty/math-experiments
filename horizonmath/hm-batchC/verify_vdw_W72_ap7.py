#!/usr/bin/env python3
"""Independent exact verifier: intersections of shifted integer bit sets."""
import json
import sys


def verify(solution):
    if not isinstance(solution, dict) or not isinstance(solution.get('coloring'), list):
        return {'valid': False, 'reason': 'expected coloring list'}
    colors = solution['coloring']
    if not colors or any(type(c) is not int or c not in (0, 1) for c in colors):
        return {'valid': False, 'reason': 'nonempty exact binary integer list required'}
    n = len(colors)
    ones = sum(c << i for i, c in enumerate(colors))
    mask = (1 << n) - 1
    for bitset, color in [(ones, 1), (ones ^ mask, 0)]:
        for d in range(1, (n - 1) // 6 + 1):
            starts = bitset
            for k in range(1, 7):
                starts &= bitset >> (k * d)
            if starts:
                a = (starts & -starts).bit_length() - 1
                return {'valid': False, 'reason': 'monochromatic AP', 'a': a, 'd': d, 'color': color}
    return {'valid': True, 'length': n}


if __name__ == '__main__':
    result = verify(json.load(open(sys.argv[1])))
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result['valid'] else 1)
