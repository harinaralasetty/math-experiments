"""Capture completed verification logs without inventing results."""
import json
from pathlib import Path
from site_data import load_verification

ROOT = Path(__file__).resolve().parents[1]


def main():
    checks = [
        ('Build', 'make build', 'build', 'Generated'),
        ('Site, FAQ, provenance, metadata, links and privacy', 'make verify-site', 'site', 'PASS all site checks'),
        ('Complete mathematical verification', 'make verify-math', 'math', 'PASS 15 exact verifier cases'),
    ]
    logs = {}
    for _, _, key, marker in checks:
        logs[key] = (ROOT/'.verification'/f'{key}.log').read_text()
        assert marker in logs[key] and 'Traceback' not in logs[key], key
    assert 'PASS all extended b-files recomputed by both methods' in logs['math']
    assert 'PASS stage2c local lemmas=118 corruptions_rejected=470 concrete_replays=3973; registered decisions=0' in logs['math']
    manifest = json.loads((ROOT/'sources.json').read_text())
    sequences = load_verification()['sequences']
    total = sum(row['new_count'] for row in sequences)
    report = f'''# Verification report

Math Experiments including OEIS stage 4 is generated locally from pinned committed source snapshots. The OEIS stages together supply {total:,} new terms across {len(sequences)} sequences. No commit, push, publication or OEIS submission was performed.

The generator and stylesheet provide the announcement copy, per-sequence pages, two-significant-digit historical timings, complete downloads with 20-row previews, author credit, a visible FAQ and matching FAQPage, Article, WebSite, Dataset and breadcrumb JSON-LD, a refreshed social image, llms.txt and a sitemap. The README and all totals use the same combined sequence data. The stage 4 import preserves the earlier pinned files and adds the manager-specified committed snapshot. Its programs and b-files remain byte-identical; the report's machine-home paths are redacted and its original hash is retained. The verification runner and site checks respect each sequence's original first index.

## Source revisions

'''
    report += ''.join(f'- `{repo}`: `{rev}`\n' for repo, rev in manifest['revisions'].items())
    report += '''
## Verification scope and limitations

The mathematical command below recomputes every distributed OEIS row with both independent methods and checks the published overlap. It also verifies the BB(6) local proof objects, corruption controls, concrete replays and certificate fixtures, and runs the exact record-search construction verifiers with invalid controls. It does not repeat the full historical search campaigns or claim a new Busy Beaver decision or a new mathematical record. Source timings on the pages remain the separately identified historical measurements, rounded for display; actual recomputation timings appear below. Mathematical checks use this repository alone; the full site provenance check also requires the pinned sibling source workspaces. Building the site requires Git history for dates, Pillow and lxml.

Site validation uses the strict local validator for this generator's HTML5 subset, rather than the Nu HTML Checker. It checks nesting, supported attributes and content models, exactly one h1 and one initial lead sentence per page, links, unique titles and descriptions, canonical URLs, Open Graph, Twitter cards, schema author and creator identities, breadcrumbs, date consistency, sitemap and llms.txt coverage, imported hashes and source-backed numeric claims. New tests parse FAQ JSON-LD and compare it with the visible questions and answers; mutations of either the visible answer or schema answer must fail. Other mutation tests cover changed research numbers, missing leads, broken links, duplicate titles, invalid JSON-LD and sitemap omissions.

Page modification dates use each imported file's last-change date from the pinned source git revision and the relevant generator/style dates. Uncommitted generator/style changes use filesystem modification dates. The dates are repeated consistently in the byline, structured data and sitemap. Dates therefore follow each page's dependencies rather than one fixed publication date.

Responsive CSS wraps long numbers and inline code, keeps tables in scrollable boxes, lets navigation and cards wrap, and limits b-file previews to the first 20 rows. The 1200-by-630 social image was inspected directly. No rendered 390 px viewport or physical-phone test was performed. The checks verify the relevant CSS and viewport rules.

Only allowlisted first-party source programs, evidence and text were imported; third-party papers, web snapshots, archives and implementations remain excluded. All complete b-files are byte-identical to the pinned source blobs. sources.json and docs/PROVENANCE.md record hashes, transformations and dates. The privacy scan below includes hidden and ignored working-tree files, excludes git history and skips binary content.

'''
    for title, command, key, _ in checks:
        report += f'## {title}\n\nCommand: `{command}`\n\n```text\n{logs[key].rstrip()}\n```\n\n'
    report += f'''## Delivery

All {len(sequences)} b-files and sequence pages are included. The licence holder remains Hari Naralasetty; original code is MIT and original data/text are CC BY 4.0, with existing attribution retained. The changes are left uncommitted for manager review.
'''
    (ROOT/'REPORT.md').write_text(report)
    print('Wrote REPORT.md from completed build, site and mathematical verification logs.')


if __name__ == '__main__':
    main()
