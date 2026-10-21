#!/usr/bin/env python3
"""Independent exact checker via pairwise Hamming distances, not pair ownership."""
import json
import sys
from itertools import combinations


def verify(solution):
    if not isinstance(solution, dict) or not isinstance(solution.get('blocks'), list):
        raise ValueError('expected object with blocks list')
    blocks = solution['blocks']
    supports = []
    for i, block in enumerate(blocks):
        if not isinstance(block, list) or len(block) != 5:
            raise ValueError(f'block {i}: expected five points')
        if any(type(x) is not int or x < 0 or x >= 29 for x in block):
            raise ValueError(f'block {i}: points must be integers in [0,28]')
        if len(set(block)) != 5:
            raise ValueError(f'block {i}: repeated point')
        supports.append(set(block))
    min_distance = 10
    for (i, a), (j, b) in combinations(enumerate(supports), 2):
        distance = len(a.symmetric_difference(b))
        if distance < 8:
            raise ValueError(f'blocks {i},{j}: Hamming distance {distance} < 8')
        min_distance = min(min_distance, distance)
    return {'num_blocks': len(blocks),
            'min_distance': min_distance if len(blocks) > 1 else None,
            'num_pairs_covered': len(blocks) * 10}


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
