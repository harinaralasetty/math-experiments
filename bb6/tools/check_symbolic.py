#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent kernel for LOCAL affine-run transition lemmas, not decisions.

Counts are affine forms in independent natural variables. Coefficientwise
non-negativity is a sufficient, deliberately incomplete arithmetic solver.
Every read/write must fall inside a supplied homogeneous run for every value
of the variables. Outside tape contexts are arbitrary and are never read.

The sole induction principle accelerates a single-symbol TM self-loop. Its
zero case is the identity. Its successor case executes the transition on the
next cell, writes the stated symbol, and reuses the induction hypothesis on
the adjacent remaining cells. They are disjoint, so this proves all natural
counts and the exact linear time/displacement. No samples establish a lemma.

This file imports no discovery/simulation tool. ACCEPT means only the local
lemmas hold. It does NOT certify start reachability or global non-halting.
"""
import argparse
import json
import re
import sys


class Kernel:
    def __init__(self, machine, variables):
        if sys.flags.optimize:
            raise ValueError('symbolic verification requires Python assertions enabled')
        assert len(variables) == len(set(variables))
        assert all(re.fullmatch('[a-z][a-z0-9_]*', v) for v in variables)
        self.variables = variables
        self.zero = (0,) * (len(variables) + 1)
        self.one = (1,) + (0,) * len(variables)
        rows = machine.split('_')
        assert 1 <= len(rows) <= 6
        assert all(re.fullmatch(r'(?:[01][LR][A-F]|---){2}', row) for row in rows)
        assert all(tr == '---' or ord(tr[2]) - 65 < len(rows) for row in rows for tr in (row[:3], row[3:]))
        self.rows = rows
        self.runs = []
        self.head = self.zero
        self.steps = self.zero
        self.state = 'A'
        self.trace = []

    def form(self, obj):
        if type(obj) is int:
            return (obj,) + self.zero[1:]
        assert isinstance(obj, dict)
        assert set(obj) <= {'constant', *self.variables}
        result = (obj.get('constant', 0),) + tuple(obj.get(v, 0) for v in self.variables)
        assert all(type(x) is int for x in result)
        return result

    @staticmethod
    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    @staticmethod
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    @staticmethod
    def scale(a, n):
        return tuple(x * n for x in a)

    @staticmethod
    def natural(a):
        return all(x >= 0 for x in a)

    def normalize(self, runs):
        result = []
        for bit, count in runs:
            assert type(bit) is int and bit in (0, 1)
            assert self.natural(count)
            if count == self.zero:
                continue
            if result and result[-1][0] == bit:
                result[-1] = bit, self.add(result[-1][1], count)
            else:
                result.append((bit, count))
        return result

    def parse_tape(self, expr):
        runs = []
        for term in expr:
            if isinstance(term, str):
                assert set(term) <= {'0', '1'}
                runs.extend((int(bit), self.one) for bit in term)
            else:
                assert set(term) == {'bit', 'count'}
                runs.append((term['bit'], self.form(term['count'])))
        return self.normalize(runs)

    def transition(self, bit):
        assert self.state in 'ABCDEF'
        row = self.rows[ord(self.state) - ord('A')]
        code = row[3 * bit:3 * bit + 3]
        if code == '---':
            return 1, 1, 'Z'
        return int(code[0]), 1 if code[1] == 'R' else -1, code[2]

    def snapshot(self, instruction):
        self.trace.append(dict(instruction=instruction, state=self.state,
                               head=self.head, steps=self.steps, runs=self.runs))

    def microstep(self):
        start = self.zero
        for i, (bit, length) in enumerate(self.runs):
            before = self.sub(self.head, start)
            after = self.sub(self.sub(length, before), self.one)
            if self.natural(before) and self.natural(after):
                write, direction, state = self.transition(bit)
                changed = [(bit, before), (write, self.one), (bit, after)]
                self.runs = self.normalize(self.runs[:i] + changed + self.runs[i + 1:])
                self.head = self.add(self.head, self.scale(self.one, direction))
                self.steps = self.add(self.steps, self.one)
                self.state = state
                self.snapshot(dict(microstep=dict(read=bit, write=write,
                                                 direction=direction, next=state)))
                return
            start = self.add(start, length)
        raise AssertionError('read not proved inside a supplied run for all parameters')

    def scan(self, instruction):
        count = self.form(instruction['count'])
        bit = instruction['read']
        assert self.natural(count) and type(bit) is int and bit in (0, 1)
        write, direction, state = self.transition(bit)
        assert state == self.state, 'induction requires a TM self-loop'
        assert instruction['induction'] == {
            'base': 'zero steps; tape and head unchanged',
            'successor': 'one self-loop step; induction on adjacent remaining cells'}
        begin = self.head if direction == 1 else self.add(self.sub(self.head, count), self.one)
        start = self.zero
        for i, (symbol, length) in enumerate(self.runs):
            before = self.sub(begin, start)
            after = self.sub(self.sub(length, before), count)
            if symbol == bit and self.natural(before) and self.natural(after):
                self.runs = self.normalize(self.runs[:i] + [(bit, before),
                                           (write, count), (bit, after)] + self.runs[i + 1:])
                self.head = self.add(self.head, self.scale(count, direction))
                self.steps = self.add(self.steps, count)
                self.snapshot(dict(inductive_scan=dict(state=state, read=bit, write=write,
                                                       count=count, direction=direction)))
                return
            start = self.add(start, length)
        raise AssertionError('scan interval not proved to contain the stated symbol')

    def check_rule(self, rule):
        self.runs = self.parse_tape(rule['source']['tape'])
        self.head = self.form(rule['source']['head'])
        self.state = rule['source']['state']
        self.snapshot('initial')
        for op in rule['proof']:
            assert self.state != 'Z', 'cannot continue after halting'
            if set(op) == {'steps'}:
                assert type(op['steps']) is int and 0 <= op['steps'] <= 10000
                for _ in range(op['steps']):
                    self.microstep()
            else:
                assert set(op) == {'scan'}
                self.scan(op['scan'])
        final = rule['target']
        assert self.runs == self.parse_tape(final['tape']), ('wrong tape', self.runs)
        assert self.head == self.form(final['head']), ('wrong head', self.head)
        assert self.state == final['state'], ('wrong state', self.state)
        assert self.steps == self.form(rule['steps']), ('wrong count', self.steps)
        return self.trace


def check(certificate):
    if sys.flags.optimize:
        raise ValueError('symbolic verification requires Python assertions enabled')
    assert certificate['type'] == 'local_affine_run_lemmas'
    assert certificate['scope'] == 'local transitions only; no global decision'
    ids = [r['id'] for r in certificate['rules']]
    assert len(ids) == len(set(ids))
    assert set(ids) == set(certificate['required_rules'])
    assert len(ids) == len(certificate['required_rules'])
    # Reject malformed induction descriptions and inconsistent proof times
    # before replaying any rule. These are necessary syntactic/arithmetic
    # conditions; the full independent transition replay still follows.
    for rule in certificate['rules']:
        arithmetic = Kernel(certificate['machine'], rule['variables'])
        total = arithmetic.zero
        for op in rule['proof']:
            if set(op) == {'steps'}:
                assert type(op['steps']) is int and 0 <= op['steps'] <= 10000
                total = arithmetic.add(total, arithmetic.form(op['steps']))
            else:
                assert set(op) == {'scan'}
                scan = op['scan']
                assert set(scan) == {'read', 'count', 'induction'}
                assert type(scan['read']) is int and scan['read'] in (0, 1)
                assert scan['induction'] == {
                    'base': 'zero steps; tape and head unchanged',
                    'successor': 'one self-loop step; induction on adjacent remaining cells'}
                count = arithmetic.form(scan['count'])
                assert arithmetic.natural(count)
                total = arithmetic.add(total, count)
        assert total == arithmetic.form(rule['steps']), 'declared time differs from proof instruction total'
    traces = {}
    for rule in certificate['rules']:
        kernel = Kernel(certificate['machine'], rule['variables'])
        traces[rule['id']] = kernel.check_rule(rule)
    by_id = {r['id']: r for r in certificate['rules']}
    rows = Kernel(certificate['machine'], []).rows
    guards = {}

    def entry_guard(guard, machine_rows):
        assert set(guard) == {'id','state','offset','bit','incoming'}
        assert guard['state'] in 'ABCDEF'[:len(machine_rows)]
        assert type(guard['offset']) is int and guard['offset'] in (-1,1)
        assert type(guard['bit']) is int and guard['bit'] in (0,1)
        # Standard blank start is A. Other control states have a vacuous base.
        assert guard['state'] != 'A' or guard['bit'] == 0
        expected = []
        for q, row in zip('ABCDEF', machine_rows):
            for read in (0,1):
                tr = row[3*read:3*read+3]
                if tr != '---' and tr[2] == guard['state']:
                    direction = 1 if tr[1] == 'R' else -1
                    # The cell just written is at displacement -direction
                    # from the new head. No old-tape assumption is needed.
                    assert -direction == guard['offset'] and int(tr[0]) == guard['bit']
                    expected.append((q,read))
        actual = []
        for case in guard['incoming']:
            assert set(case) == {'state','read'}
            assert type(case['read']) is int and case['read'] in (0,1)
            actual.append((case['state'],case['read']))
        assert len(actual) == len(set(actual)) and set(actual) == set(expected)
        return expected

    for guard in certificate.get('entry_guards', []):
        assert guard['id'] not in guards
        incoming = entry_guard(guard, rows); guards[guard['id']] = guard
        traces['entry-'+guard['id']] = dict(scope='all finite blank-start executions',
            incoming=incoming, proof='blank A base; every incoming transition writes the required neighbor')
    shortcut_ids = set()
    for shortcut in certificate.get('machine_shortcuts', []):
        assert set(shortcut) == {'id','target_machine','cases'}
        assert shortcut['id'] not in shortcut_ids; shortcut_ids.add(shortcut['id'])
        target_rows = Kernel(shortcut['target_machine'], []).rows
        assert len(target_rows) == len(rows)
        differences = {(q,b) for q,(old,new) in zip('ABCDEF',zip(rows,target_rows)) for b in (0,1)
                       if old[3*b:3*b+3] != new[3*b:3*b+3]}
        cases = [(case['state'],case['read']) for case in shortcut['cases']]
        assert len(cases) == len(set(cases)) and set(cases) == differences
        bounds = []
        for case in shortcut['cases']:
            assert set(case) == {'state','read','rule','guard'}
            q,read = case['state'],case['read']; guard = guards[case['guard']]
            assert guard['state'] == q and guard['offset'] == 1
            entry_guard(guard, target_rows)
            tr = target_rows[ord(q)-65][3*read:3*read+3]
            assert tr != '---' and tr[1] == 'R'
            r = by_id[case['rule']]; bit = str(guard['bit'])
            assert not r['variables'] and type(r['steps']) is int and r['steps'] > 0
            assert r['source'] == dict(tape=[str(read)+bit],head=0,state=q)
            assert r['target'] == dict(tape=[tr[0]+bit],head=1,state=tr[2])
            bounds.append(r['steps'])
        traces['shortcut-'+shortcut['id']] = dict(target_machine=shortcut['target_machine'],
            replaced_cases=cases, positive_step_bounds=bounds,
            proof='entry guard in both machines; checked finite local replacements; induction on target steps',
            consequence='blank-start halting equivalence only; neither halting nor nonhalting is asserted')
    for sweep in certificate.get('periodic_sweeps', []):
        r = by_id[sweep['rule']]
        assert not r['variables']
        assert r['source']['state'] == r['target']['state']
        assert len(r['source']['tape']) == len(r['target']['tape']) == 1
        source, target = r['source']['tape'][0], r['target']['tape'][0]
        assert type(source) is str and type(target) is str
        assert source and len(source) == len(target)
        width = len(source)
        direction = sweep['direction']
        assert direction in (-1, 1)
        assert r['source']['head'] == (0 if direction == 1 else width - 1)
        assert r['target']['head'] == (width if direction == 1 else -1)
        assert sweep['base'] == 'zero blocks is identity'
        assert sweep['induction'] == 'checked first block; induction on remaining disjoint blocks'
        assert sweep['steps'] == {'n': r['steps']}
        assert sweep['displacement'] == {'n': width * direction}
        traces['repeat-' + r['id']] = dict(domain='all natural n, including zero',
                                          input_word=source, output_word=target,
                                          steps=sweep['steps'], displacement=sweep['displacement'],
                                          proof='identity base; checked block touches no other block; induction')
    for transducer in certificate.get('word_transducers', []):
        if transducer['kind'] == 'left_buffer_transducer':
            assert transducer['base'] == 'empty word is identity'
            assert transducer['induction'] == 'process last block; induction on remaining prefix'
            alphabet, buffers = transducer['alphabet'], transducer['buffers']
            head_offset = transducer.get('head_offset', 0)
            assert type(head_offset) is int and 0 <= head_offset < min(map(len, buffers.values()))
            assert alphabet and buffers
            assert all(word and set(word) <= {'0', '1'} for word in [*alphabet.values(), *buffers.values()])
            domain = {(buffer, letter) for buffer in buffers for letter in alphabet}
            actual = [(c['from_buffer'], c['letter']) for c in transducer['cases']]
            assert set(actual) == domain and len(actual) == len(domain)
            for case in transducer['cases']:
                assert set(case) == {'from_buffer', 'letter', 'to_buffer', 'output', 'rule', 'parameters', 'steps'}
                r = by_id[case['rule']]
                env = case['parameters']
                assert set(env) == set(r['variables'])
                assert all(type(x) is int and x >= 0 for x in env.values())
                assert case['to_buffer'] in buffers

                def evaluate(value):
                    if type(value) is int:
                        return value
                    return value.get('constant', 0) + sum(env[v] * value.get(v, 0) for v in env)

                def expand(tape):
                    return ''.join(term if isinstance(term, str) else str(term['bit']) * evaluate(term['count'])
                                   for term in tape)

                word = alphabet[case['letter']]
                assert r['source']['state'] == r['target']['state'] == transducer['state']
                assert expand(r['source']['tape']) == word + buffers[case['from_buffer']]
                assert evaluate(r['source']['head']) == len(word) + head_offset
                assert expand(r['target']['tape']) == buffers[case['to_buffer']] + case['output']
                assert evaluate(r['target']['head']) == head_offset
                assert evaluate(r['steps']) == case['steps']
            traces[transducer['id']] = dict(checked_cases=len(domain),
                                            proof='empty prefix identity; checked last block yields next buffer; structural induction')
            continue
        assert transducer['kind'] == 'right_word_transducer'
        assert transducer['base'] == 'empty word is identity'
        assert transducer['induction'] == 'process first block; induction on remaining word'
        alphabet = transducer['alphabet']
        offsets = transducer['head_offsets']
        lookahead = transducer['lookahead']
        assert lookahead and set(lookahead) <= {'0', '1'}
        assert alphabet and offsets
        assert all(word.startswith(lookahead) for word in alphabet.values())
        assert all(type(i) is int and 0 <= i < min(map(len, alphabet.values())) for i in offsets.values())
        domain = {(state, letter) for state in offsets for letter in alphabet}
        actual = [(c['from_state'], c['letter']) for c in transducer['cases']]
        assert set(actual) == domain and len(actual) == len(domain), 'dropped or duplicate transducer case'
        for case in transducer['cases']:
            assert set(case) == {'from_state', 'letter', 'to_state', 'output', 'rule'}
            r = by_id[case['rule']]
            assert not r['variables']
            word = alphabet[case['letter']]
            assert case['to_state'] in offsets
            assert len(case['output']) == len(word)
            assert r['source'] == dict(state=transducer['state'], tape=[word + lookahead],
                                       head=offsets[case['from_state']])
            assert r['target'] == dict(state=transducer['state'], tape=[case['output'] + lookahead],
                                       head=len(word) + offsets[case['to_state']])
            # The untouched lookahead is the next block's prefix. Thus checked
            # cases compose by induction on an arbitrary finite input word.
        traces[transducer['id']] = dict(checked_cases=len(domain),
                                        proof='empty word identity; checked cases preserve next prefix; structural induction')
    return traces


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate')
    parser.add_argument('--trace')
    args = parser.parse_args()
    try:
        with open(args.certificate) as f:
            traces = check(json.load(f))
        if args.trace:
            with open(args.trace, 'w') as f:
                json.dump(traces, f, indent=2)
                f.write('\n')
    except (AssertionError, KeyError, IndexError, TypeError, ValueError, OSError) as exc:
        print('REJECT', flush=True)
        print(str(exc), file=sys.stderr)
        return 1
    print('ACCEPT local lemmas only', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
