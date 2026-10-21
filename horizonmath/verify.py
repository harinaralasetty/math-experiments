"""Run the distributed exact verifiers with valid and invalid constructions."""
import copy
import importlib.util
import json
from pathlib import Path

root = Path(__file__).resolve().parent
cases = 0
for batch, name, metric, score in [
    ('hm-batchA', 'dts_7_5_min_scope', 'scope', 112),
    ('hm-batchA', 'cwcode_29_8_5', 'num_blocks', 36),
    ('hm-batchB', 'covering_C13_k7_t4', 'num_blocks', 30),
    ('hm-batchB', 'schur_6', 'N', 536),
    ('hm-batchC', 'vdw_W72_ap7', 'length', 3703),
    ('hm-batchC', 'A21_10_binary_code', 'number_of_codewords', 42),
]:
    spec = importlib.util.spec_from_file_location(name, root/batch/f'verify_{name}.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    original = json.loads((root/batch/'solutions'/f'{name}.json').read_text())
    def valid(data):
        try:
            result = module.verify(data)
            return result.get('valid', True), result
        except ValueError:
            return False, {}
    ok, result = valid(original)
    assert ok and result[metric] == score
    bad = copy.deepcopy(original)
    if name.startswith('dts'): bad['rows'][1] = bad['rows'][0][:]
    elif name.startswith('cwcode'): bad['blocks'][1] = bad['blocks'][0][:]
    elif name.startswith('covering'): bad['blocks'] = bad['blocks'][:1]
    elif name == 'schur_6': bad[2] = bad[1]
    elif name == 'vdw_W72_ap7': bad['coloring'][:7] = [0]*7
    else: bad['codewords'][1] = bad['codewords'][0]
    assert not valid(bad)[0]
    cases += 2
    if name == 'schur_6':
        assert not valid({'coloring': original})[0]
        cases += 1
    if name == 'A21_10_binary_code':
        assert result['min_distance'] == 10
        mixed = copy.deepcopy(original)
        index = next(i for i, word in enumerate(original['codewords'])
                     if f'{word:021b}' != f'{word:021b}'[::-1])
        mixed['codewords'][index] = f"{mixed['codewords'][index]:021b}"
        assert valid(mixed)[0]
        mixed['codewords'].append(original['codewords'][index])
        assert not valid(mixed)[0]
        cases += 2
    print(f'{name}: {metric}={score}; valid witness accepted, invalid control rejected PASS')
print(f'PASS {cases} exact verifier cases; no new record claimed')
