"""Replay the committed local proofs. Acceptance never means a global decision."""
import json
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent/'tools'))
from stage2b_verify import invoke, mutations, concrete_checks

root = Path(__file__).resolve().parent
assert not sys.flags.optimize
assert json.loads((root/'decisions/registry.json').read_text()) == [], 'New decisions require the full source decision verifier'
total = rejected = samples = 0
for path in sorted((root/'data/stage2b').glob('*-local-lemmas.json')):
    c = json.loads(path.read_text())
    invoke(c, True)
    bad_count = 0
    for label, bad in mutations(c):
        assert bad != c
        invoke(bad, False, label)
        bad_count += 1
    n = concrete_checks(c)
    total += len(c['rules']); rejected += bad_count; samples += n
    print(f'{path.name}: local lemmas={len(c["rules"])} corruptions_rejected={bad_count} concrete_replays={n} PASS', flush=True)
assert total == 48 and rejected == 198 and samples == 840
print('PASS local lemmas=48 corruptions_rejected=198 concrete_replays=840; registered decisions=0')
# Replay only the new local proof objects, with the same mutation selection as
# the source stage2c verifier. Simulator and global search campaigns stay external.
stage2c = dict(rules=0, corruptions=0, concrete=0)
expected = json.loads((root/'data/stage2c/local-verification.json').read_text())
for record in expected['certificates']:
    c = json.loads((root/record['path']).read_text())
    invoke(c, True, record['path'])
    if c.get('word_transducers'):
        variants = mutations(c)
    else:
        def isolated_variants():
            for rule in c['rules']:
                part = {**c, 'rules': [rule], 'required_rules': [rule['id']]}
                scan_tested = False
                for label, bad in mutations(part):
                    if label == 'machine contains out-of-range target state': continue
                    if 'missing scan base case' in label:
                        if scan_tested: continue
                        scan_tested = True
                    yield label, bad
        variants = isolated_variants()
    rejected = 0
    for label, bad in variants:
        invoke(bad, False, label)
        rejected += 1
    for i, transducer in enumerate(c.get('word_transducers', [])):
        if 'head_offset' in transducer:
            bad = copy.deepcopy(c)
            bad['word_transducers'][i]['head_offset'] += 1
            invoke(bad, False, 'wrong carry buffer head offset')
            rejected += 1
    concrete = concrete_checks(c)
    assert len(c['rules']) == record['local_rules']
    assert rejected == record['corrupted_variants_rejected']
    assert concrete == record['concrete_instantiations']
    stage2c['rules'] += len(c['rules'])
    stage2c['corruptions'] += rejected
    stage2c['concrete'] += concrete
    print(f"{Path(record['path']).name}: local lemmas={len(c['rules'])} corruptions_rejected={rejected} concrete_replays={concrete} PASS", flush=True)
assert stage2c == dict(rules=118, corruptions=470, concrete=3973)
print('PASS stage2c local lemmas=118 corruptions_rejected=470 concrete_replays=3973; registered decisions=0')
from check_tc import check as tc
from check_ngram import check as cps
fixtures = json.loads((root/'data/certificate-verification.json').read_text())
for kind, checker in [('translated_cycler',tc),('ngram_cps',cps)]:
    accepted = rejected = 0
    for entry in fixtures[kind]:
        c = json.loads((root/entry['certificate']).read_text())
        assert checker(c)
        assert not checker(json.loads((root/entry['corrupt_certificate']).read_text()))
        accepted += 1; rejected += 1
        bad = copy.deepcopy(c)
        bad['machine'] = '---' + c['machine'][3:]
        assert not checker(bad)
        rejected += 1
    print(f'PASS {kind} source fixtures accepted={accepted}; corruptions and halting-transition variants rejected={rejected}; controls only, no new decisions')
