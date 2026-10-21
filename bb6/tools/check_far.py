#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent finite-automata backward-closure certificate checker.

Prefix DFA state q and TM state s select NFA state n*q+s. The extra sink
accepts every suffix. Every halting configuration reaches it; the checked
transition inclusions make that language closed backwards under TM steps.
A zero-closed safe set contains the blank-start NFA state and excludes the
sink, proving that no finite zero suffix of blank start reaches the sink.
Thus blank start cannot lead to a halting configuration. No solver imported.
"""
import json
import re
import sys


def check(c):
    if sys.flags.optimize:
        raise ValueError('FAR verification requires Python assertions enabled')
    assert c['type'] == 'finite_automata_backward'
    assert type(c.get('mirror', False)) is bool
    machine = c['machine']
    if c.get('mirror', False):
        machine = machine.translate(str.maketrans('LR', 'RL'))
    rows = machine.split('_')
    assert 1 <= len(rows) <= 6
    assert all(re.fullmatch(r'(?:[01][LR][A-F]|---){2}', r) for r in rows)
    n = len(rows)
    dfa = c['dfa']; m = len(dfa)
    assert 1 <= m <= 128
    assert all(len(r) == 2 and all(type(x) is int and 0 <= x < m for x in r) for r in dfa)
    assert dfa[0][0] == 0
    size = n * m + 1; sink = size - 1
    raw = c['nfa']
    assert len(raw) == size
    assert all(len(r) == 2 for r in raw)
    assert all(type(x) is int and 0 <= x < size for r in raw for dest in r for x in dest)
    assert all(len(dest) == len(set(dest)) for r in raw for dest in r)
    edges = [[set(dest) for dest in row] for row in raw]
    assert all(sink in edges[sink][b] for b in (0, 1))
    safe = set(c['zero_safe'])
    assert len(safe) == len(c['zero_safe']) and 0 in safe and sink not in safe
    assert all(type(x) is int and 0 <= x < size for x in safe)
    assert all(edges[x][0] <= safe for x in safe)
    for s, row in enumerate(rows):
        for r in (0, 1):
            tr = row[3 * r:3 * r + 3]
            for q in range(m):
                if tr == '---':
                    assert sink in edges[n * q + s][r]
                    continue
                w, d, t = int(tr[0]), tr[1], ord(tr[2]) - 65
                assert 0 <= t < n
                if d == 'R':
                    assert n * dfa[q][w] + t in edges[n * q + s][r]
                else:
                    for b in (0, 1):
                        after_two = set()
                        for k in edges[n * q + t][b]:
                            after_two |= edges[k][w]
                        assert after_two <= edges[n * dfa[q][b] + s][r]
    return True


def main():
    try:
        with open(sys.argv[1]) as f:
            check(json.load(f))
    except (AssertionError, KeyError, IndexError, TypeError, ValueError, OSError):
        print('REJECT')
        return 1
    print('ACCEPT')
    return 0


if __name__ == '__main__':
    sys.exit(main())
