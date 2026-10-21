#!/usr/bin/env python3
"""Independent exact check over integer pairs, including x=y."""
import json
import sys


def verify(solution):
    if type(solution) is not list or len(solution) < 2:
        return {'valid': False, 'reason': 'expected bare coloring list'}
    if type(solution[0]) is not int or solution[0] != 0:
        return {'valid': False, 'reason': 'bad sentinel'}
    if any(type(c) is not int or not 0 <= c < 6 for c in solution[1:]):
        return {'valid': False, 'reason': 'invalid color'}
    n = len(solution) - 1
    pairs_checked = 0
    for x in range(1, n // 2 + 1):
        for y in range(x, n - x + 1):
            pairs_checked += 1
            if solution[x] == solution[y] == solution[x+y]:
                return {'valid': False, 'N': n, 'reason': 'monochromatic sum', 'witness': [x,y,x+y]}
    return {'valid': True, 'N': n, 'pairs_checked': pairs_checked, 'color_sizes': [solution[1:].count(c) for c in range(6)]}

if __name__ == '__main__':
    result = verify(json.load(open(sys.argv[1])))
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result['valid'] else 1)
