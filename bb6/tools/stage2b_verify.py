#!/usr/bin/env python3
"""Fresh-process local-proof checks, mutation controls, and exact tape comparisons.

No local lemma, frontier experiment, or accelerated run counts as a decision.
"""
import copy
import gzip
import hashlib
import functools
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def invoke(certificate, accepted, label=''):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
        json.dump(certificate, f)
        f.flush()
        p = subprocess.run([sys.executable, 'tools/check_symbolic.py', f.name],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert p.returncode == (0 if accepted else 1), (label,p.stdout,p.stderr)
    assert p.stdout.strip() == ('ACCEPT local lemmas only' if accepted else 'REJECT')


def mutations(c):
    for i, rule in enumerate(c['rules']):
        bad = copy.deepcopy(c)
        target = bad['rules'][i]['target']['tape']
        # Change an actual written symbol in the claimed endpoint.
        changed=False
        for j, term in enumerate(target):
            if isinstance(term, str) and term:
                target[j] = ('1' if term[0] == '0' else '0') + term[1:]
                changed=True
                break
            if isinstance(term,dict) and any(term['count'].values()):
                target[j]['bit']=1-term['bit'];changed=True
                break
        assert changed, (rule['id'],'no nonempty endpoint term to mutate')
        yield f"{rule['id']}: wrong endpoint symbol", bad
        bad = copy.deepcopy(c)
        steps = bad['rules'][i]['steps']
        if type(steps) is int:
            bad['rules'][i]['steps'] += 1
        else:
            steps['constant'] = steps.get('constant', 0) + 1
        yield f"{rule['id']}: off-by-one count", bad
        bad = copy.deepcopy(c)
        del bad['rules'][i]
        yield f"{rule['id']}: dropped case", bad
    bad = copy.deepcopy(c)
    bad['machine'] = '1RZ' + bad['machine'][3:]
    yield 'machine contains out-of-range target state', bad
    for i, rule in enumerate(c['rules']):
        for j, op in enumerate(rule['proof']):
            if 'scan' in op:
                bad = copy.deepcopy(c)
                del bad['rules'][i]['proof'][j]['scan']['induction']['base']
                yield f"{rule['id']}: missing scan base case", bad
    for i, t in enumerate(c.get('word_transducers', [])):
        bad = copy.deepcopy(c)
        del bad['word_transducers'][i]['cases'][0]
        yield f"{t['id']}: dropped transducer case", bad
        bad = copy.deepcopy(c)
        if t['kind'] == 'right_word_transducer':
            current = t['cases'][0]['to_state']
            alternative = next((s for s in t['head_offsets'] if s != current), 'invalid_parser_state')
            bad['word_transducers'][i]['cases'][0]['to_state'] = alternative
        else:
            bad['word_transducers'][i]['cases'][0]['to_buffer'] = 'z5'
        yield f"{t['id']}: wrong successor state", bad
        bad = copy.deepcopy(c)
        bad['word_transducers'][i]['base'] = 'unchecked'
        yield f"{t['id']}: missing word induction base", bad
    for i, sweep in enumerate(c.get('periodic_sweeps', [])):
        bad = copy.deepcopy(c)
        bad['periodic_sweeps'][i]['steps']['n'] += 1
        yield f"{sweep['rule']}: wrong periodic count coefficient", bad
        bad = copy.deepcopy(c)
        bad['periodic_sweeps'][i]['base'] = 'unchecked'
        yield f"{sweep['rule']}: dropped periodic base case", bad
    for i, guard in enumerate(c.get('entry_guards', [])):
        for field, value in [('bit',1-guard['bit']),('offset',-guard['offset'])]:
            bad=copy.deepcopy(c);bad['entry_guards'][i][field]=value
            yield f"{guard['id']}: wrong {field}",bad
        bad=copy.deepcopy(c);del bad['entry_guards'][i]['incoming'][0]
        yield f"{guard['id']}: missing incoming case",bad
    for i, shortcut in enumerate(c.get('machine_shortcuts', [])):
        bad=copy.deepcopy(c);del bad['machine_shortcuts'][i]['cases'][0]
        yield f"{shortcut['id']}: dropped replacement case",bad
        bad=copy.deepcopy(c);bad['machine_shortcuts'][i]['cases'][0]['rule']=c['rules'][0]['id']
        yield f"{shortcut['id']}: wrong supporting rule",bad
        bad=copy.deepcopy(c);bad['machine_shortcuts'][i]['target_machine']=c['machine']
        yield f"{shortcut['id']}: wrong replacement machine",bad


def integer(expression, env):
    if type(expression) is int:
        return expression
    return expression.get('constant', 0) + sum(env[v] * expression.get(v, 0) for v in env)


def instantiate(expr, env):
    result = ''
    for term in expr:
        result += term if isinstance(term, str) else str(term['bit']) * integer(term['count'], env)
    return result


def concrete_checks(c):
    """Separate sparse-tape implementation, including arbitrary outside context."""
    rng = random.Random(20261021)
    tests = 0
    for rule in c['rules']:
        if len(rule['variables']) == 2:
            cases = [dict(zip(rule['variables'], (n, m))) for n in range(9) for m in range(9)]
            cases += [dict(zip(rule['variables'], (1000, 1000)))]
        elif rule['variables']:
            cases = [{rule['variables'][0]: n} for n in [*range(33), 1000, 10000]]
        else:
            cases = [{}]
        for env in cases:
            source = instantiate(rule['source']['tape'], env)
            expected = instantiate(rule['target']['tape'], env)
            assert len(source) == len(expected)
            background = {x for x in [*range(-17, 0), *range(len(source), len(source) + 17)]
                          if rng.getrandbits(1)}
            tape = background | {x for x, bit in enumerate(source) if bit == '1'}
            target = background | {x for x, bit in enumerate(expected) if bit == '1'}
            head = integer(rule['source']['head'], env)
            q = ord(rule['source']['state']) - 65
            rows = c['machine'].split('_')
            for _ in range(integer(rule['steps'], env)):
                assert 0 <= q < len(rows)
                code = rows[q][3 * (head in tape):3 * (head in tape) + 3]
                if code == '---':
                    tape.add(head)
                    head += 1
                    q = 25
                else:
                    if code[0] == '1':
                        tape.add(head)
                    else:
                        tape.discard(head)
                    head += {'L': -1, 'R': 1}[code[1]]
                    q = ord(code[2]) - 65
            assert tape == target, (rule['id'], env, 'tape')
            assert head == integer(rule['target']['head'], env), (rule['id'], env, 'head')
            assert q == ord(rule['target']['state']) - 65, (rule['id'], env, 'state')
            tests += 1
    return tests


def read_checkpoint(path):
    lines = path.read_text().splitlines()
    m, w, t, h, q, lo, hi = lines[0].split()
    return dict(machine=m, width=int(w), steps=int(t), head=int(h), state=int(q),
                min_head=int(lo), max_head=int(hi),
                boundaries=[tuple(map(int, line.split())) for line in lines[1:]])


def checkpoint_runs(c):
    result = []
    lo, hi, width = c['min_head'], c['max_head'], c['width']

    def emit(start, bit, length):
        end = min(start + length, hi + 1)
        start = max(start, lo)
        if end <= start:
            return
        length = end - start
        if result and result[-1][1] == bit:
            assert result[-1][0] + result[-1][2] == start
            result[-1][2] += length
        else:
            result.append([start, bit, length])

    bounds = c['boundaries']
    if not bounds:
        return [[lo, 0, hi - lo + 1]]
    emit(lo, 0, bounds[0][0] * width - lo)
    for i, (block, word) in enumerate(bounds):
        end = bounds[i + 1][0] if i + 1 < len(bounds) else (hi // width + 1)
        if word in (0, (1 << width) - 1):
            emit(block * width, int(bool(word)), (end - block) * width)
        else:
            assert end - block < 1000000, 'periodic output too large for this comparison'
            for index in range(block, end):
                for bit in range(width):
                    emit(index * width + bit, (word >> bit) & 1, 1)
    assert result[0][0] == lo and result[-1][0] + result[-1][2] == hi + 1
    return result


def compare_saved_block_runs(index=24):
    count = 0
    for name in (f'{index:03d}-block-billion', f'{index:03d}-block16-billion'):
        path = ROOT / f'data/stage2b/{name}.checkpoint'
        if not path.exists():
            continue
        c = read_checkpoint(path)
        with gzip.open(ROOT / f'data/stage2/attempts/{index:03d}.rle.gz', 'rt') as f:
            expected = [list(map(int, line.split())) for line in f if not line.startswith('#')]
        assert checkpoint_runs(c) == expected, name
        record = json.loads((ROOT / f'logs/stage2/{index:03d}-direct-sim.log').read_text())['samples'][-1]
        assert c['steps'] == 1000000000
        for key in ('steps', 'head', 'state', 'min_head', 'max_head'):
            assert c[key] == record[key], (name, key)
        count += 1
    return count


def hypothetical_witnesses():
    cases = []
    for line in (ROOT / 'logs/stage2b/024-family-sign.jsonl').read_text().splitlines():
        row = json.loads(line)
        if row.get('reason') == 'halt-from-hypothetical-family-not-blank':
            cases.append(dict(prefix_ones=64, input_runs=row['input_runs'],
                              steps=row['steps'], visits=row['visits'],
                              shift=row['shift'], minimum_head=row['minimum_head'], halted=True))
    unary = ROOT / 'logs/stage2b/024-unary-reset.jsonl'
    if unary.exists():
        for line in unary.read_text().splitlines():
            row = json.loads(line)
            if row['halted'] or row['prefix_ones'] in (1, 4, 300):
                cases.append(row)
    machine = '1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA'
    rows = machine.split('_')
    verified = []
    for case in cases:
        word = '1' * case['prefix_ones'] + '00' + ''.join('1' * r + '0' for r in case['input_runs']) + '1'
        tape = {i for i, bit in enumerate(word) if bit == '1'}
        head = len(word); initial = head; state = 2; minimum = head; visits = 0
        first_halt = None
        for step in range(1, case['steps'] + 1):
            assert state >= 0, 'expected witness runs beyond its first halt'
            bit = int(head in tape)
            code = rows[state][3 * bit:3 * bit + 3]
            if code == '---':
                tape.add(head); head += 1; state = -1; first_halt = step
            else:
                if code[0] == '1':
                    tape.add(head)
                else:
                    tape.discard(head)
                head += 1 if code[1] == 'R' else -1
                state = ord(code[2]) - 65
            minimum = min(minimum, head)
            if state == 2 and head > max(tape, default=-10**9):
                visits += 1
        assert (state == -1) == case['halted']
        assert first_halt == (case['steps'] if case['halted'] else None)
        assert head - initial == case['shift'] and minimum == case['minimum_head']
        assert visits == case['visits']
        value = 0
        for r in case['input_runs']:
            value = -2 * value + r - 2
        verified.append(dict(source='hypothetical nonblank configuration; blank reachability not established',
                             prefix_ones=case['prefix_ones'], input_runs=case['input_runs'],
                             encoded_value=value, steps=case['steps'], halted=case['halted']))
    (ROOT / 'data/stage2b/hypothetical-witness-verification.json').write_text(json.dumps(verified, indent=2) + '\n')
    return len(verified), sum(r['halted'] and r['encoded_value'] < 0 for r in verified)


def signed_grammar_witnesses():
    path = ROOT / 'data/stage2b/024-signed-grammar.json'
    if not path.exists():
        return 0
    record = json.loads(path.read_text())
    compressed = ROOT / record['raw_gzip']
    assert hashlib.sha256(compressed.read_bytes()).hexdigest() == record['raw_gzip_sha256']
    with gzip.open(compressed, 'rb') as f:
        assert hashlib.sha256(f.read()).hexdigest() == record['raw_sha256']
    verified = []
    for name, case in record['witnesses'].items():
        word = '1' * 64 + '00' + ''.join('1' * r + '0' for r in case['input_runs']) + '1'
        tape = {i for i, bit in enumerate(word) if bit == '1'}
        head = len(word); initial = head; state = 2; minimum = head; visits = 0
        for step in range(1, case['steps'] + 1):
            assert state >= 0
            row = record['machine'].split('_')[state]
            tr = row[3 * int(head in tape):3 * int(head in tape) + 3]
            if tr == '---':
                tape.add(head); head += 1; state = -1
            else:
                if tr[0] == '1':
                    tape.add(head)
                else:
                    tape.discard(head)
                head += {'L': -1, 'R': 1}[tr[1]]; state = ord(tr[2]) - 65
            minimum = min(minimum, head)
            if state == 2 and head > max(tape):
                visits += 1
        assert (state == -1) == case['halted']
        assert (minimum < 64) == case['prefix_touched']
        if not case['halted']:
            assert visits == 2 and state == 2 and head > max(tape)
            marker = max((i for i in range(head - 1) if i not in tape and i + 1 not in tape), default=-1)
            final = ''.join('1' if i in tape else '0' for i in range(marker + 2, head))
            actual = [len(s) for s in final.split('0')[:-1]] if marker >= 0 else []
            assert actual == case['output_runs']
        verified.append(dict(name=name, input_runs=case['input_runs'], steps=case['steps'],
                             halted=case['halted'], minimum_head=minimum,
                             shift=head - initial, visits=visits,
                             final_state=state, final_head=head,
                             tape_word=''.join('1' if i in tape else '0'
                                               for i in range(min(tape), max(tape) + 1))))
    dest = ROOT / 'data/stage2b/signed-witness-verification.json'
    dest.write_text(json.dumps(verified, indent=2) + '\n')
    return len(verified)


def configured_source_check():
    path = ROOT / 'data/stage2b/024-configured-blank-billion-b7.json'
    if not path.exists():
        return 0
    record = json.loads(path.read_text()); origin = record['initial_left_word']
    source = ROOT / origin['source_checkpoint']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == origin['source_sha256']
    checkpoint = read_checkpoint(source); runs = checkpoint_runs(checkpoint)
    low, high = checkpoint['min_head'], checkpoint['max_head']
    tape = bytearray(high - low + 1001)
    for start, bit, length in runs:
        if bit:
            tape[start - low:start - low + length] = bytes([1]) * length
    rightmost = len(tape) - 1
    while not tape[rightmost]:
        rightmost -= 1
    head = checkpoint['head'] - low; state = checkpoint['state']
    for extra in range(100001):
        if state == 2 and head > rightmost:
            break
        assert extra < 100000 and 0 <= head < len(tape)
        tr = checkpoint['machine'].split('_')[state][3 * tape[head]:3 * tape[head] + 3]
        assert tr != '---'
        tape[head] = int(tr[0])
        if tape[head]:
            rightmost = max(rightmost, head)
        elif head == rightmost:
            while not tape[rightmost]:
                rightmost -= 1
        head += {'L': -1, 'R': 1}[tr[1]]; state = ord(tr[2]) - 65
    leftmost = tape.index(1)
    word = bytes(tape[leftmost:head]).translate(bytes.maketrans(bytes([0, 1]), b'01'))
    with gzip.open(ROOT / origin['initial_word_file'], 'rb') as f:
        assert word == f.read()
    assert hashlib.sha256(word).hexdigest() == origin['word_sha256']
    assert extra == origin['replay_steps']
    assert checkpoint['steps'] + extra == origin['absolute_frontier_steps']
    assert head + low == origin['absolute_head'] and leftmost + low == origin['source_leftmost_one']
    result = dict(scope='finite starting configuration only; no decision', status='PASS',
                  source=str(source.relative_to(ROOT)), steps=checkpoint['steps'] + extra,
                  replay_steps=extra, word_sha256=origin['word_sha256'])
    (ROOT / 'data/stage2b/configured-source-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return 1


def guarded_countdown_check():
    path = ROOT / 'logs/stage2b/024-guarded-100returns.jsonl'
    if not path.exists():
        return 0
    case = next(json.loads(line) for line in path.read_text().splitlines()
                if json.loads(line)['kind'] == 'witness')
    word = '1' * 64 + '00' + ''.join('1' * r + '0' for r in case['input_runs']) + '1'
    tape = {i for i, bit in enumerate(word) if bit == '1'}
    head = len(word); state = 2; minimum = head; visits = 0; phases = []
    rows = '1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA'.split('_')

    def phase(step):
        marker = max((i for i in range(head - 1) if i not in tape and i + 1 not in tape), default=-1)
        tail = ''.join('1' if i in tape else '0' for i in range(marker + 2, head)) if marker >= 0 else ''
        valid = marker >= 0 and len(tail.split('0')[-1]) == 1
        runs = [len(s) for s in tail.split('0')[:-1]] if valid else []
        value = 0
        for r in runs:
            value = -2 * value + r - 2
        phases.append(dict(steps=step, frontier_returns=visits, valid_frame=valid,
                           runs=runs, value=value if valid else None, head=head))

    phase(0)
    for step in range(1, case['steps'] + 1):
        tr = rows[state][3 * int(head in tape):3 * int(head in tape) + 3]
        assert tr != '---'
        if tr[0] == '1':
            tape.add(head)
        else:
            tape.discard(head)
        head += {'L': -1, 'R': 1}[tr[1]]; state = ord(tr[2]) - 65
        minimum = min(minimum, head)
        if state == 2 and head > max(tape):
            visits += 1
            if visits % 2 == 0:
                phase(step)
    assert visits == 100 and minimum == 64
    assert len(phases) == 51 and all(r['valid_frame'] for r in phases[:-1])
    assert all(r['value'] == 100 - r['frontier_returns'] for r in phases[:-1])
    assert phases[-2]['runs'] == [3, 3, 2] and not phases[-1]['valid_frame']
    assert phases[-1]['steps'] - phases[-2]['steps'] == 111
    result = dict(scope='one finite hypothetical countdown; no global recurrence claimed',
                  source=str(path.relative_to(ROOT)), input_runs=case['input_runs'],
                  steps=case['steps'], halted=False, minimum_head=minimum, phases=phases)
    (ROOT / 'data/stage2b/guarded-countdown-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return 1


def guarded_enumeration_check():
    path = ROOT / 'data/stage2b/024-guarded-all.json'
    if not path.exists():
        return 0
    campaign = json.loads(path.read_text())
    assert campaign['status'] == 'finished'
    assert hashlib.sha256((ROOT / campaign['source']).read_bytes()).hexdigest() == campaign['source_sha256']
    log = ROOT / campaign['log']
    assert hashlib.sha256(log.read_bytes()).hexdigest() == campaign['log_sha256']
    records = [json.loads(line) for line in log.read_text().splitlines()]
    completed = [r for r in records if r['kind'] == 'completed_length']
    counts = []
    for record in completed:
        k = record['digits']

        @functools.lru_cache(None)
        def suffix(position):
            if position >= k - 1:
                return 1
            count = 2 * suffix(position + 1)
            if (k - 1 - position) % 2 and position + 2 < k:
                count += suffix(position + 3)
            return count

        expected = suffix(1) + (suffix(3) if k % 2 == 0 else 0)
        assert record['checked'] == expected
        if k <= 10:
            brute = 0
            for middle in itertools.product((2, 3, 4), repeat=k - 2):
                for first in (3, 4):
                    word = (first, *middle, 2)
                    if all(x != 4 or ((k - 1 - i) % 2 and i + 2 < k
                                     and word[i + 1:i + 3] == (3, 2))
                           for i, x in enumerate(word)):
                        brute += 1
            assert brute == expected
        counts.append(dict(digits=k, count=expected))
    assert completed[-1]['digits'] == campaign['completed_through']
    result = dict(status='PASS', scope='enumeration counts only; simulations remain finite evidence',
                  completed_lengths_checked=len(counts), brute_force_max_digits=10, counts=counts,
                  complete_plus_partial_trials=campaign['total_checked'])
    (ROOT / 'data/stage2b/guarded-enumeration-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return len(counts)


def entry_guard_controls():
    control=dict(type='local_affine_run_lemmas',machine='0RA0RA',
                 scope='local transitions only; no global decision',required_rules=[],rules=[],
                 entry_guards=[dict(id='A-left-zero',state='A',offset=-1,bit=0,
                                    incoming=[dict(state='A',read=0),dict(state='A',read=1)])])
    invoke(control,True)
    # All incoming writes establish one, but the standard blank A base does not.
    bad=copy.deepcopy(control);bad['machine']='1RA1RA';bad['entry_guards'][0]['bit']=1
    invoke(bad,False,'entry-guard blank-base regression')
    bad=copy.deepcopy(control);bad['entry_guards'][0]['incoming'].append(dict(state='A',read=0))
    invoke(bad,False,'entry-guard duplicate incoming case')
    machine=json.loads((ROOT/'data/stage2b/444-local-lemmas.json').read_text())
    bad=copy.deepcopy(machine);bad['machine_shortcuts'][0]['cases'].append(copy.deepcopy(bad['machine_shortcuts'][0]['cases'][0]))
    invoke(bad,False,'machine-shortcut duplicate replacement case')
    return dict(authentic=1,corrupted_variants_rejected=3)


def main():
    if sys.flags.optimize:
        raise SystemExit('verification requires assertions enabled')
    c = json.loads((ROOT / 'data/stage2b/024-local-lemmas.json').read_text())
    invoke(c, True)
    rejected = []
    for label, bad in mutations(c):
        assert bad != c, (label,'mutation did not change certificate')
        invoke(bad, False,label)
        rejected.append(label)
    concrete = concrete_checks(c)
    block_runs = compare_saved_block_runs()
    other_block_runs = compare_saved_block_runs(444)
    witnesses, negative_halters = hypothetical_witnesses()
    signed_witnesses = signed_grammar_witnesses()
    configured_sources = configured_source_check()
    guarded_countdowns = guarded_countdown_check()
    guarded_lengths = guarded_enumeration_check()
    guard_controls = entry_guard_controls()
    additional = []
    for path in sorted((ROOT / 'data/stage2b').glob('*-local-lemmas.json')):
        if path.name == '024-local-lemmas.json':
            continue
        other = json.loads(path.read_text())
        invoke(other, True)
        corruptions = []
        for label, bad in mutations(other):
            assert bad != other, (label,'mutation did not change certificate')
            invoke(bad, False,label); corruptions.append(label)
        record = dict(machine=other['machine'], scope='local lemmas only; no new decision',
                      certificate=str(path.relative_to(ROOT)), rules=len(other['rules']),
                      corrupted_variants_rejected=len(corruptions), rejected=corruptions,
                      concrete_instantiations=concrete_checks(other))
        destination = path.with_name(path.name.replace('-local-lemmas.json', '-local-verification.json'))
        destination.write_text(json.dumps(record, indent=2) + '\n')
        additional.append(str(path.relative_to(ROOT)))
        print(f"LOCAL PROOFS {path.stem}: lemmas={record['rules']}; corrupted variants rejected={len(corruptions)}; concrete instantiations={record['concrete_instantiations']}")
    optimized = 0
    for checker, path in [('tools/check_symbolic.py', 'data/stage2b/024-local-lemmas.json'),
                          ('tools/check_far.py', 'data/stage2b/024-far-control-m1-c0-normal.candidate.json'),
                          ('tools/check_phase_cps.py', 'data/stage2b/control-phase-uniform6.json')]:
        p = subprocess.run([sys.executable, '-O', checker, path], cwd=ROOT, capture_output=True, text=True)
        assert p.returncode == 1 and p.stdout.strip() == 'REJECT'
        optimized += 1
    report = dict(scope='local lemmas only; no new decision',
                  rules=len(c['rules']), corrupted_variants_rejected=len(rejected),
                  rejected=rejected, concrete_instantiations=concrete,
                  exact_billion_step_block_tapes_matched=block_runs,
                  candidate444_exact_billion_step_block_tapes_matched=other_block_runs,
                  hypothetical_configurations_replayed=witnesses,
                  signed_grammar_witnesses_replayed=signed_witnesses,
                  additional_local_certificates_checked=additional,
                  exact_configured_source_words_checked=configured_sources,
                  guarded_countdowns_replayed=guarded_countdowns,
                  guarded_enumeration_lengths_checked=guarded_lengths,
                  entry_guard_controls=guard_controls,
                  hypothetical_negative_value_halters=negative_halters,
                  optimized_python_rejections=optimized)
    (ROOT / 'data/stage2b/local-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"LOCAL PROOFS candidate 24: lemmas={len(c['rules'])}; corrupted variants rejected={len(rejected)}; concrete instantiations={concrete}")
    print(f"DISCOVERY SIMULATOR: exact billion-step tapes matched={block_runs}")
    print(f"CANDIDATE444 SIMULATOR: exact billion-step tapes matched={other_block_runs}")
    print(f"HYPOTHETICAL CONFIGURATIONS: independently replayed={witnesses}; negative-value halters={negative_halters}; none claimed blank-reachable")
    print(f"SIGNED-GRAMMAR WITNESSES: independently replayed={signed_witnesses}; no blank-start claims")
    print(f"CONFIGURED PROVER SOURCE: exact finite starting words checked={configured_sources}")
    print(f"GUARDED COUNTDOWN: finite hypothetical trajectories checked={guarded_countdowns}")
    print(f"GUARDED ENUMERATION: completed-length counts independently checked={guarded_lengths}")
    print(f"ENTRY-GUARD KERNEL: synthetic controls accepted={guard_controls['authentic']}; corrupted variants rejected={guard_controls['corrupted_variants_rejected']}")
    print(f"PROOF CHECKERS: optimized Python rejected={optimized}")
    print('PASS stage2b checks (local proofs and discovery runs are not decisions)')


if __name__ == '__main__':
    main()
