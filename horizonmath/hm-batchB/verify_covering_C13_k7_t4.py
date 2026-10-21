#!/usr/bin/env python3
"""Independent exact verifier; score is derived solely from supplied blocks."""
import json
import sys
from itertools import combinations


def verify(solution):
    if type(solution) is not dict or type(solution.get('blocks')) is not list:
        return {'valid': False, 'reason': 'expected blocks list'}
    blocks = solution['blocks']
    if not blocks:
        return {'valid': False, 'reason': 'empty construction'}
    canonical = []
    covered = set()
    for b in blocks:
        if type(b) is not list or len(b) != 7 or any(type(x) is not int for x in b):
            return {'valid': False, 'reason': 'block must contain seven integers'}
        if len(set(b)) != 7 or any(x < 0 or x >= 13 for x in b):
            return {'valid': False, 'reason': 'block has repeated or out-of-range points'}
        b = tuple(sorted(b))
        canonical.append(b)
        covered.update(combinations(b, 4))
    if len(set(canonical)) != len(canonical):
        return {'valid': False, 'reason': 'duplicate blocks'}
    missing = set(combinations(range(13), 4)) - covered
    result = {'valid': not missing, 'num_blocks': len(blocks), 'covered': len(covered), 'uncovered': len(missing)}
    if missing:
        result['example_uncovered'] = min(missing)
    return result

if __name__ == '__main__':
    result = verify(json.load(open(sys.argv[1])))
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result['valid'] else 1)
