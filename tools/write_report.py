"""Capture already completed verification output without inventing test results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    logs = {}
    for key, marker in [('site','PASS all site checks'),('oeis-full','PASS all extended b-files recomputed by both methods'),
                        ('bb6','controls only, no new decisions'),('horizonmath','PASS 15 exact verifier cases')]:
        text = (ROOT/'.verification'/f'{key}.log').read_text()
        assert marker in text, f'{key}: completion marker missing'
        assert 'Traceback' not in text
        logs[key] = text
    manifest = json.loads((ROOT/'sources.json').read_text())
    assert 'PASS stage2c local lemmas=118 corruptions_rejected=470 concrete_replays=3973; registered decisions=0' in logs['bb6']
    report = '# Verification report\n\nThe repository and static site were refreshed locally from the final committed batch C and BB6 stage 2c source snapshots. No commit, push, publication or OEIS submission was performed. Only allowlisted committed source blobs and the authorized record-status note were imported.\n\n'
    report += '## Source revisions\n\n'+''.join(f'- `{repo}`: `{rev}`\n' for repo,rev in manifest['revisions'].items())
    report += '\n## Scope\n\nThe full OEIS run below recomputes all distributed extended rows with both original methods. Its wall seconds are actual measurements of this build. Page timing tables retain the separately identified historical source run. The BB6 portable target replays the local proof objects, corruption controls and concrete instances, plus authentic small-machine certificate fixtures. It does not rerun the full historical simulator campaign or claim a global decision. HorizonMath runs exact positive and negative construction checks, without vendoring the upstream benchmark.\n\n'
    report += 'HTML validation uses the repository\'s strict local validator for the HTML5 subset used by this generator. It checks explicit nesting, supported elements/attributes and content models, plus metadata, links and structure. It is not the Nu HTML Checker. Mutation tests exercise malformed nesting, invalid paragraph contents, unknown elements, missing alt text and duplicate attributes. Further tests alter real generated pages to check rejection of a changed research number, broken link, duplicate title, malformed JSON-LD and omitted sitemap entry.\n\n'
    report += 'The final BB6 stage 2c result is no global decision after the six-hour interval, with 118 additional local rules, 470 rejected corruptions and 3973 concrete instantiations. These are additional to the earlier 48 lemmas and 198 corruption controls. Batch C retained W(7,2) colouring length 3703 and an A(21,10) code of size 42 with minimum distance 10, matching published lower bounds. The full source reports contain the historical verification output; fresh portable checks below replay the distributed claims without modifying the read-only sibling workspaces.\n\n'
    report += 'Responsive CSS keeps tables and b-file rows in scrollable containers and wraps navigation on narrow viewports. A physical phone was not used. The refreshed social image was inspected directly. The refreshed sitemap covers every HTML page and has last-modified dates taken from pinned source commits. JSON-LD on the home and project pages describes the final outcomes.\n\n'
    report += 'No third-party source folder, paper, PDF, source archive or copied web page was imported. The file audit below checks forbidden archive/document extensions and import paths; sources.json and PROVENANCE.md enumerate every imported file with its original hash. Batch C research references remain upstream links.\n\n'
    for title,command,key in [('Site, provenance, hashes, links, sitemap, JSON-LD and privacy','make verify-site','site'),
                              ('Full OEIS recomputation','make -C oeis verify','oeis-full'),
                              ('BB6 local proofs and checker controls','make -C bb6 verify','bb6'),
                              ('HorizonMath exact verifiers','make -C horizonmath verify','horizonmath')]:
        report += f'## {title}\n\nCommand: `{command}`\n\n```text\n{logs[key].rstrip()}\n```\n\n'
    report += '## Delivery\n\nThe README and site share the same result model. Every research number has a section-level source mapping in docs/PROVENANCE.md and tools/claims.json. sources.json records hashes and extraction transformations. Five distributed b-files are byte-identical to their pinned source results. The licence split is MIT for original code and CC BY 4.0 for original data/text, with source attribution retained for quotations and published constructions. Repository description, topics and Pages configuration suggestions are in docs/github-topics.md.\n'
    (ROOT/'REPORT.md').write_text(report)
    print('Wrote REPORT.md from completed verification logs.')


if __name__ == '__main__':
    main()
