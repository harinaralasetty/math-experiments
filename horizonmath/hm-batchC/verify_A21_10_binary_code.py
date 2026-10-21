#!/usr/bin/env python3
"""Independent exact verifier, computing distance coordinate by coordinate."""
import json
import sys


def verify(solution):
    if not isinstance(solution, dict) or not isinstance(solution.get('codewords'), list):
        return {'valid': False, 'reason': 'expected codewords list'}
    vectors = []
    for w in solution['codewords']:
        if type(w) is int and 0 <= w < 2**21:
            vectors.append(tuple((w >> j) & 1 for j in range(21)))
        elif isinstance(w, str) and len(w) == 21 and set(w) <= {'0', '1'}:
            vectors.append(tuple(int(c) for c in reversed(w)))
        else:
            return {'valid': False, 'reason': 'word not an exact binary vector of length 21'}
    if not vectors:
        return {'valid': False, 'reason': 'empty code'}
    minimum = 21
    for i, x in enumerate(vectors):
        for j in range(i):
            distance = sum(a != b for a, b in zip(x, vectors[j]))
            if distance < 10:
                return {'valid': False, 'reason': 'distance violation', 'pair': [j, i], 'distance': distance}
            minimum = min(minimum, distance)
    return {'valid': True, 'number_of_codewords': len(vectors), 'min_distance': minimum}


if __name__ == '__main__':
    result = verify(json.load(open(sys.argv[1])))
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result['valid'] else 1)
