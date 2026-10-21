"""Import an explicit allowlist from committed source trees. Never import vendors."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = []
revisions = {}


def source(repo, path):
    base = ROOT.parent / repo
    rev = revisions.setdefault(repo, subprocess.check_output(
        ['git', '-C', str(base), 'rev-parse', 'HEAD'], text=True).strip())
    return subprocess.check_output(['git', '-C', str(base), 'show', f'{rev}:{path}'])


def write(repo, path, target, transform=None):
    original = source(repo, path)
    data = transform(original) if transform else original
    out = ROOT / target
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    modified = subprocess.check_output(['git', '-C', str(ROOT.parent/repo), 'log', '-1', '--format=%cs', revisions[repo], '--', path], text=True).strip()
    manifest.append(dict(workspace=repo, revision=revisions[repo], source=path, last_modified=modified,
                         target=target, source_sha256=hashlib.sha256(original).hexdigest(),
                         sha256=hashlib.sha256(data).hexdigest(), transformed=bool(transform)))


def encode(obj):
    return (json.dumps(obj, indent=2) + '\n').encode()


if __name__ == '__main__':
    ids = ['A391646', 'A383533', 'A374679', 'A353390', 'A335457']
    for name in ['compute_new.py', 'reference.py', 'independent.py', 'new_reference.py',
                 'new_independent.py', 'new_powerful.cpp', 'new_patterns.cpp',
                 'cut_runs.cpp', 'new_runs.cpp']:
        write('oeis', f'code/{name}', f'oeis/code/{name}')
    for a in ids:
        write('oeis', f'results/{a}.txt', f'docs/data/{a}.txt')
        write('oeis', f'data/{a}.json', f'oeis/data/{a}.json',
              lambda b: encode({k: json.loads(b)[k] for k in ['number', 'name', 'data', 'offset', 'keyword']}))
    write('oeis', 'data/runs/new-verification.json', 'oeis/data/verification.json',
          lambda b: encode({**{k: json.loads(b)[k] for k in ['started_utc', 'limits', 'sequences']},
                            'methods': [{k: x[k] for k in ['id', 'method', 'wall_seconds', 'cpu_seconds']}
                                        for x in json.loads(b)['methods']]}))
    write('oeis', 'data/STATUS-stage2.md', 'oeis/data/STATUS-stage2.txt')
    stage3_ids = ['A374680', 'A374681', 'A374682', 'A383710', 'A383711']
    for name in ['compute.py', 'anti_dp.py', 'anti_series.py',
                 'partition_reference.py', 'partition_independent.py']:
        write('oeis', 'stage3/code/'+name, 'oeis/code/stage3/'+name)
    for a in stage3_ids:
        write('oeis', f'stage3/results/b{a[1:]}.txt', f'docs/data/{a}.txt')
        write('oeis', f'stage3/data/{a}.json', f'oeis/data/{a}.json',
              lambda b: encode({k: json.loads(b)[k] for k in ['number', 'name', 'data', 'offset', 'keyword']}))
    def stage3_verification(b):
        data = json.loads(b)
        return encode(dict(started_utc=data['started_utc'],
            sequences=[dict(id=x['id'], listed_last=x['previous_last'], last=x['last'],
                            new_count=x['new_terms']) for x in data['results']],
            methods=[dict(id=x['id'], method=m, wall_seconds=r['wall_seconds'], cpu_seconds=r['cpu_seconds'])
                     for x in data['results'] for m,r in x['methods'].items()]))
    write('oeis', 'stage3/data/verification.json', 'oeis/data/stage3-verification.json', stage3_verification)
    for source_path, target in [('REPORT.md', 'REPORT.txt'), ('STATUS.md', 'STATUS.txt'),
                           ('results/SUBMISSION-DRAFTS.md', 'SUBMISSION-DRAFTS.txt')]:
        write('oeis', 'stage3/'+source_path, 'oeis/data/stage3-'+target)
    # Original first-party checker and proof objects; no external simulator code.
    write('bb6', 'tools/check_symbolic.py', 'bb6/tools/check_symbolic.py')
    write('bb6', 'tools/stage2b_verify.py', 'bb6/tools/stage2b_verify.py')
    for p in ['check_tc.py', 'check_ngram.py', 'check_far.py', 'fast_sim.cpp']:
        write('bb6', 'tools/'+p, 'bb6/tools/'+p)
    write('bb6', 'tools/CERTIFICATES.md', 'bb6/tools/CERTIFICATES.txt')
    write('bb6', 'README.md', 'bb6/SOURCE-README.txt')
    write('bb6', 'tools/LICENSE', 'bb6/tools/LICENSE')
    fixtures = json.loads(source('bb6', 'data/certificate-verification.json'))
    write('bb6', 'data/certificate-verification.json', 'bb6/data/certificate-verification.json')
    for group in fixtures.values():
        for item in group:
            for key in ['certificate', 'corrupt_certificate']:
                write('bb6', item[key], 'bb6/'+item[key])
    paths = subprocess.check_output(['git', '-C', str(ROOT.parent/'bb6'), 'ls-files'], text=True).splitlines()
    for p in paths:
        if p.startswith('data/stage2b/') and ('symbolic' in p or 'local-verification' in p or 'local-lemmas' in p):
            write('bb6', p, 'bb6/'+p)
    for p in ['decisions/registry.json', 'REPORT.md', 'data/STATUS-stage2b.md']:
        write('bb6', p, 'bb6/'+p.replace('.md','.txt'))
    for p in ['notes/024-attempt.md', 'data/STATUS-stage2c.md']:
        write('bb6', p, 'bb6/'+p.replace('.md', '.txt'))
    for name in ['024-carry-lemmas.json', '024-boundary-lemmas.json',
                 '024-hypothetical-halt-lemmas.json', 'local-verification.json',
                 'time-discipline.json']:
        write('bb6', 'data/stage2c/'+name, 'bb6/data/stage2c/'+name)
    write('bb6', 'data/stage2c/summary.json', 'bb6/data/stage2c/summary.json',
          lambda b: encode({**{k: json.loads(b)[k] for k in
                            ['utc', 'scope', 'final', 'start_utc', 'elapsed_seconds',
                             'target_decisions', 'local_totals']},
                            'searches': {k: {field: value[field] for field in ['queries', 'outcomes']}
                                         for k, value in json.loads(b)['searches'].items()}}))
    for repo, names in [('hm-batchA', ['dts_7_5_min_scope', 'cwcode_29_8_5']),
                        ('hm-batchB', ['covering_C13_k7_t4', 'schur_6']),
                        ('hm-batchC', ['vdw_W72_ap7', 'A21_10_binary_code'])]:
        for name in names:
            write(repo, f'verify_{name}.py', f'horizonmath/{repo}/verify_{name}.py')
            write(repo, f'solutions/{name}.json', f'horizonmath/{repo}/solutions/{name}.json')
        write(repo, 'REPORT.md', f'horizonmath/{repo}/REPORT.txt')
    # This note is an explicitly authorized non-git source. It has no private sprint log.
    p = ROOT.parent/'notes/horizonmath-records.md'
    data = p.read_bytes()
    out = ROOT/'horizonmath/record-status.md'
    out.write_bytes(data)
    manifest.append(dict(workspace='notes', source='horizonmath-records.md', last_modified=datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).date().isoformat(), target='horizonmath/record-status.md',
                         source_sha256=hashlib.sha256(data).hexdigest(), sha256=hashlib.sha256(data).hexdigest(), transformed=False))
    revision_dates = {repo: subprocess.check_output(
        ['git', '-C', str(ROOT.parent/repo), 'show', '-s', '--format=%cs', rev], text=True).strip()
        for repo, rev in revisions.items()}
    (ROOT/'sources.json').write_bytes(encode(dict(revisions=revisions, revision_dates=revision_dates, files=manifest,
        exclusions={'third-party': 'External papers, PDFs, copied web pages, source archives and implementations are not imported; cite their upstream links only.'})))
    print(f'Imported {len(manifest)} allowlisted files from pinned sources.')
