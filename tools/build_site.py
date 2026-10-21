"""Generate a small static site from pinned evidence, with a claim ledger."""
import hashlib
import html
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
AUTHOR = {'@type': 'Person', 'name': 'Hari Naralasetty', 'url': 'https://github.com/harinaralasetty', 'sameAs': ['https://github.com/harinaralasetty', 'https://www.linkedin.com/in/harinaralasetty']}
AUTHOR_LINKS = f"<a href=\"{AUTHOR['url']}\">{AUTHOR['name']}</a> (<a href=\"https://github.com/harinaralasetty\">GitHub</a> · <a href=\"https://www.linkedin.com/in/harinaralasetty\">LinkedIn</a>)"
BASE = 'https://harinaralasetty.github.io/math-experiments/'
REPO = 'https://github.com/harinaralasetty/math-experiments'
sources = json.loads((ROOT/'sources.json').read_text())
verification = json.loads((ROOT/'oeis/data/verification.json').read_text())
sequences = verification['sequences']
total = sum(s['new_count'] for s in sequences)
claims = []
pages = []


def esc(value):
    return html.escape(str(value), quote=True)


def claim(key, text, evidence):
    claims.append(dict(id=key, html=text, evidence=evidence))
    return f'<section id="{key}">{text}</section>'


def page(path, title, description, body, schema):
    depth = len(Path(path).parts)-1
    prefix = '../'*depth
    canonical = BASE + ('' if path == 'index.html' else path)
    nav = ' '.join(f'<a href="{prefix}{url}">{label}</a>' for url, label in [
        ('index.html','Results'), ('oeis/index.html','OEIS terms'), ('bb6.html','BB(6)'),
        ('horizonmath.html','HorizonMath'), ('reproduce.html','Reproduce')])
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="author" content="{AUTHOR['name']}">
<link rel="canonical" href="{canonical}"><link rel="stylesheet" href="{prefix}assets/style.css">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/results.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Results table: OEIS new terms, BB(6) partial progress, HorizonMath no improvement.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{BASE}assets/results.png">
<meta name="twitter:image:alt" content="Verified research sprint results table.">
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org', **schema, 'author':AUTHOR},ensure_ascii=False)}</script>
</head><body><a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="{prefix}index.html">math-experiments</a><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main"><h1>{esc(title)}</h1><p class="byline">By {AUTHOR_LINKS}</p>{body}</main>
<footer><p>By {AUTHOR_LINKS}. Snapshot of verified sprint work. <a href="{prefix}PROVENANCE.md">Claim provenance and source revisions</a> · <a href="{REPO}">Repository and code</a></p>
<p>Original code: <a href="{REPO}/blob/main/LICENSE">MIT</a>. Original data and text: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Attributed quotations retain their source terms.</p></footer></body></html>'''
    out = DOCS/path; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc)
    pages.append(path)


def main():
    table = f'''<div class="table-scroll"><table><caption>Results from the pinned source snapshots</caption>
<thead><tr><th scope="col">Project</th><th scope="col">Status</th><th scope="col">Verified outcome</th></tr></thead><tbody>
<tr><th scope="row"><a href="oeis/index.html">OEIS extensions</a></th><td><span class="status new">New result</span></td><td>{total} new terms; not yet submitted to OEIS</td></tr>
<tr><th scope="row"><a href="bb6.html">BB(6) holdouts</a></th><td><span class="status partial">Partial progress</span></td><td>48 initial lemmas plus 118 new local rules; no global decision</td></tr>
<tr><th scope="row"><a href="horizonmath.html">HorizonMath A, B and C</a></th><td><span class="status none">No improvement</span></td><td>Published baselines retained, including colouring length 3703 and code size 42 with minimum distance 10; no new record</td></tr></tbody></table></div>'''
    body = '<p class="eyebrow">Machine-checkable mathematics · source snapshot</p><p class="lead">An AI coding agent, managed by another AI, worked on open problems whose proposed answers can be checked by programs.</p>'
    body += claim('results-table', table, ['oeis/data/verification.json','bb6/REPORT.txt','bb6/data/stage2c/summary.json','horizonmath/hm-batchA/REPORT.txt','horizonmath/hm-batchB/REPORT.txt','horizonmath/hm-batchC/REPORT.txt'])
    body += '<h2>The experiment</h2><p>Claude managed the tasks and reviewed staged work. Codex computed candidates and wrote independent checkers. Before search, the workers checked published problem status. The manager reran verification before accepting a result. A long computation or a checker accepting malformed input did not count as mathematical progress.</p><h2>What these results mean</h2><p>The OEIS extensions are exact computations beyond the cached published ranges. BB(6) local transition lemmas leave a global proof obligation open. The HorizonMath searches retained the known constructions. Failed bounded searches do not establish optimality.</p><p>Published status is a dated source-search snapshot, with no coverage of unpublished work. See <a href="reproduce.html">verification commands and limitations</a>.</p>'
    page('index.html','Verified mathematics experiments','Source-backed results from an AI-managed research sprint: OEIS term extensions, local BB(6) lemmas, and HorizonMath searches.',body,{'@type':'WebSite','name':'math-experiments','url':BASE,'description':f'{total} new OEIS terms, BB(6) stage 2c finished with 118 new local rules and no decision, and HorizonMath batches A, B and C with no new record.'})

    methods = {
        'A391646': ('Multiple-choice multiplicative knapsack over prime powers in Python.', 'C++ branch-and-bound over distinct prime factors, with optimistic suffix bounds.', 'Prime factors of exponent one contribute zero and can be removed. Both searches use a finite cap; the computed minima must lie inside it.'),
        'A383533': ('Partition generation without ones and backtracking over disjoint strict-partition masks.', 'Enumerate disjoint strict refinements and aggregate feasible part multiplicities.', 'The two searches approach the same feasibility condition in opposite directions.'),
        'A374679': ('Dynamic programming on weight, previous part and last anti-run leader.', 'Truncated generating functions for complete anti-runs.', 'An anti-run is split at equal adjacent parts; successive leaders must strictly increase.'),
        'A353390': ('Recursive composition enumeration, run-length extraction and forward greedy subsequence matching.', 'Independent binary cut-mask enumeration and run-length subsequence testing.', 'The extension uses separate C++ programs. Neither reads expected terms to construct its answer.'),
        'A335457': ('C++ composition enumeration with contiguous-subword normalization and pattern deduplication.', 'Python binary cut-mask compositions with separately cached rank normalization.', 'The empty composition and empty pattern follow the cached sequence conventions.'),
    }
    rows = []
    for seq in sequences:
        a = seq['id']; meta = json.loads((ROOT/'oeis/data'/f'{a}.json').read_text())
        rows.append(f'<tr><th scope="row"><a href="{a}.html">{a}</a></th><td>0 through {seq["listed_last"]}</td><td>{seq["listed_last"]+1} through {seq["last"]}</td><td>{seq["new_count"]}</td></tr>')
        evidence = ['oeis/data/'+a+'.json','oeis/data/verification.json','docs/data/'+a+'.txt']
        section = claim(a+'-definition',f'<h2>Definition</h2><blockquote><p>{esc(meta["name"])}</p></blockquote><p>Quoted from <a href="https://oeis.org/{a}">OEIS {a}</a>, as cached in the source workspace.</p>',evidence)
        section += claim(a+'-range',f'<h2>Published range and extension</h2><p>The cached published range was 0 through {seq["listed_last"]}. The extension adds indices {seq["listed_last"]+1} through {seq["last"]}, giving {seq["new_count"]} new terms. These terms have not yet been submitted to the OEIS.</p><p><a href="../data/{a}.txt">Download the complete {a} b-file, published and new rows</a>.</p>',evidence)
        m1,m2,note = methods[a]
        section += f'<h2>Two computation methods</h2><p>{m1}</p><p>{m2}</p><p>{note}</p>'
        times = [x for x in verification['methods'] if x['id']==a]
        section += claim(a+'-timings','<h2>Recorded timings</h2><p>Wall seconds from the committed source verification run, not a benchmark of this website build.</p><ul>'+''.join(f'<li>{x["method"]}: {x["wall_seconds"]} seconds</li>' for x in times)+'</ul>',['oeis/data/verification.json'])
        # Every new term is directly downloadable and readable without scripts.
        values = (DOCS/'data'/f'{a}.txt').read_text().splitlines()
        new_lines = [line for line in values if line and not line.startswith('#') and int(line.split()[0])>seq['listed_last']]
        section += claim(a+'-terms','<h2>New b-file rows</h2><pre class="terms">'+esc('\n'.join(new_lines))+'</pre>',evidence)
        section += f'<h2>Reproduce</h2><p>From the repository root, run <code>make -C oeis verify</code>. It recomputes all extensions with both methods and compares every row, including the published overlap. C++ and Python are required.</p><p><a href="{REPO}/tree/main/oeis/code">Read the OEIS computation programs</a> and <a href="{REPO}/blob/main/oeis/verify.py">the portable verification runner</a>. <a href="../reproduce.html">Verification scope and dependencies</a>.</p>'
        page('oeis/'+a+'.html',a+' verified term extension',f'{a} definition, published range, verified new b-file terms, two independent methods, recorded timings and reproduction commands.',section,{'@type':'Dataset','name':a+' computed term extension','description':meta['name'],'url':BASE+'oeis/'+a+'.html','license':'https://creativecommons.org/licenses/by/4.0/','isBasedOn':'https://oeis.org/'+a,'distribution':{'@type':'DataDownload','encodingFormat':'text/plain','contentUrl':BASE+'data/'+a+'.txt'},'creator':AUTHOR})
    body = claim('oeis-summary',f'<p class="lead">{total} new terms across {len(sequences)} sequences, with two independent methods agreeing on every row.</p><p>Terms are not yet submitted to the OEIS. The status gate checked the cached entries before extension and retained their requests for more terms. This is the source snapshot, not a live claim about today\'s OEIS listings.</p><div class="table-scroll"><table><caption>Sequence extensions</caption><thead><tr><th scope="col">Sequence</th><th scope="col">Previous indices</th><th scope="col">New indices</th><th scope="col">New terms</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>',['oeis/data/verification.json'])
    body += '<h2>Evidence and use</h2><p>Each sequence page includes the definition, new rows, method descriptions and measured timings. The <a href="../data/SHA256SUMS">b-file SHA-256 list</a> identifies the exact distributed bytes. <a href="../PROVENANCE.md">Source provenance</a> records the pinned revision and extraction fields.</p>'
    page('oeis/index.html','OEIS verified new terms','Verified extensions of five OEIS sequences, with complete b-files, independent programs, source hashes and reproduction instructions.',body,{'@type':'CollectionPage','name':'OEIS term extensions','url':BASE+'oeis/index.html'})

    body = claim('bb-status','<p class="lead">Partial progress. No new halting or non-halting decision.</p><h2>Status and exclusions</h2><p>The source snapshot starts with 663 published representatives and excludes 92, retaining 571 candidates. Exclusions cover published decisions, explicit blank-orbit equivalences, Cryptids and potential Cryptids, existing research claims and work in progress. Blank spreadsheet status alone is not proof that a machine is open.</p><p>The later status refresh retained candidates 24 and 444. Equivalence edges for 444 relate blank-start behavior; they do not decide it. Private and unpublished work is outside this status check.</p>',['bb6/REPORT.txt','bb6/data/STATUS-stage2b.txt'])
    body += claim('bb-tools','<h2>Certified tools and self-checks</h2><p>The source tools include a fast simulator, an independent reference simulator, translated-cycler and n-gram CPS certificate checkers, a FAR checker, and a symbolic local-proof kernel. The source self-check compared 500 random machines, reproduced known champion runs, and tested both certificate checkers against 1772 known halters with no false positives. Existing small-machine fixtures and corruptions exercise the checkers; they are not new holdout decisions.</p><p>These are custom checker certificates. No new decision has been certified with busycoq or Rocq. Third-party simulator implementations are linked from the source instructions rather than vendored here.</p>',['bb6/REPORT.txt'])
    body += claim('bb-lemmas','<h2>Local lemmas and the proof gap</h2><p>Candidate 24 has 27 checked local lemmas and candidate 444 has 21, giving 48 total. The fresh source verification rejected 198 corrupted variants. Local transition and word-parser statements do not establish global non-halting.</p><p>The missing argument is a closed configuration family reachable from blank tape, preserving the left context through carries, delimiter changes and rebuilding, together with the required word induction. Finite simulations and a counter decrement observed in sampled phases do not close this gap.</p>',['bb6/REPORT.txt','bb6/data/stage2b/local-verification.json','bb6/data/stage2b/444-local-verification.json'])
    body += claim('bb-stage2c','<h2>Final stage 2c outcome</h2><p>The six-hour investigation finished after 21600.08631 seconds. Candidate 24 remains undecided. The new local certificates contain 118 rules; verification rejected 470 corrupted variants and checked 3973 independent concrete instantiations. These are additional to the earlier 48 lemmas.</p><p>The carry and unary-prefix rules do not supply a closed blank-start configuration family through rebuilding. A proposed guarded family contains hypothetical halting starts, so it cannot establish global safety. Those starts are not asserted blank-reachable. A checked finite blank-start anchor also does not prove non-halting.</p><p>The final global blank-start search recorded 8 unknown outcomes. Conditional prefix-boundary searches recorded 10 unknown outcomes and 1 external wall cap; retained-context anchor searches recorded 10 unknown outcomes. No target certificate was accepted. The committed decision registry is empty. A decision may be reported only after the full source <code>make verify-decisions</code> accepts a registered certificate.</p>', ['bb6/REPORT.txt','bb6/notes/024-attempt.txt','bb6/data/stage2c/summary.json','bb6/data/stage2c/time-discipline.json','bb6/data/stage2c/local-verification.json','bb6/decisions/registry.json'])
    body += '<h2>Reproduce the distributed checks</h2><p>Run <code>make -C bb6 verify</code> to check the local proofs, reject corrupted variants, replay concrete instantiations and confirm the distributed registry is empty. This portable target does not rerun the entire source simulator campaign.</p><p><a href="'+REPO+'/tree/main/bb6">Read the local checker, proof objects and source report</a>. The <a href="https://wiki.bbchallenge.org/wiki/Holdouts_lists">bbchallenge holdout lists</a> explain the upstream lists.</p>'
    page('bb6.html','BB(6) local lemmas and unresolved proof gap','Final BB(6) stage 2c outcome: candidate 24 undecided after six hours, 118 new local rules, 470 rejected corruptions, and an unresolved global proof gap.',body,{'@type':'SoftwareSourceCode','name':'BB(6) local symbolic proof kernel','description':'Stage 2c finished with 118 new local rules, 470 rejected corruptions and no global decision for candidate 24.','codeRepository':REPO+'/tree/main/bb6','programmingLanguage':'Python','license':'https://opensource.org/license/mit','url':BASE+'bb6.html'})

    body = claim('hm-baselines','<p class="lead">No new record in any of the committed batches.</p><h2>Record-status gate</h2><p>Batch A retained DTS scope 112 and constant-weight code size 36. Batch B retained a covering with 30 blocks and a Schur coloring through 536. These are reproduced published constructions, not new sprint records.</p><p>The covering repository web entry could not be fetched. Batch B subsequently checked the maintainer\'s downloadable metadata and latest archive, which confirm a 30-block construction and lower bound 28. The Schur convention here is the largest colorable integer. A different smallest-uncolorable convention must not be read as an improvement.</p>',['horizonmath/hm-batchA/REPORT.txt','horizonmath/hm-batchB/REPORT.txt'])
    body += '<h2>Strict independent verification</h2><p>The DTS verifier computes exact positive differences and requires global distinctness. The constant-weight verifier computes pairwise Hamming distances. The covering verifier checks every required subset. The Schur verifier checks integer sums, including doubling. Each derives its score from the construction and ignores claimed scores.</p>'
    body += claim('hm-issues','<h2>Benchmark checker observations</h2><p>The status review identified boundary tolerances that can admit points outside the intended square or off the unit sphere, producing apparent floating-point gains. Approximate moment tests also do not establish an exact spherical design. These are observations about acceptance rules, not mathematical record improvements, and the sprint did not count them as results.</p><p>A separate Schur format mismatch was reproduced. The prompt requests a coloring object, while the benchmark validator accepts a bare list and rejects the wrapper. The published coloring passes in the accepted format and remains independently checked for its mathematical property.</p>',['horizonmath/record-status.md','horizonmath/hm-batchB/REPORT.txt'])
    body += claim('hm-effort','<h2>Search effort and negative results</h2><p>Batch A used CP-SAT, orbit models, neighborhood repair and tabu search. Its committed report discloses a campaign shorter than requested. For example, a code tabu run made 281591612 iterations in 600.001 seconds and ended with collision energy 1, an invalid near miss. A DTS run ended at collision energy 2 after 281303682 iterations in 600.000 seconds.</p><p>Batch B records covering wall time 14758.238 seconds and Schur wall time 14919.003 seconds. CP-SAT, SAT neighborhoods, weighted tabu search and restricted orbit/link models found no record. The saved covering near misses leave 3 subsets uncovered; Schur near misses retain 1 violation. Neither is a valid improvement. Timeouts and restricted infeasibility results do not prove the unrestricted problem unsatisfiable.</p>',['horizonmath/hm-batchA/REPORT.txt','horizonmath/hm-batchB/REPORT.txt'])
    body += claim('hm-batchc','<h2>Final batch C outcome</h2><p>The W(7,2) search retained a two-colour construction of length 3703 with no monochromatic seven-term arithmetic progression. The binary A(21,10) search retained 42 codewords with minimum distance 10. Both match the published lower bounds; neither is a new record. Colour-first sources write the progression problem as W(2,7). A valid length-3703 colouring proves W &gt; 3703, not the existence of a length-3704 colouring.</p><p>The code is a reconstruction in the published quasi-cyclic family with the published parameters. Isomorphism to the original certificate was not proved. The independent verifiers check every progression step or every pairwise distance using exact integers, and derive scores from the constructions.</p><p>Credited active wall time was 14675.648 seconds for progression search and 14610.090 seconds for code improvement search, excluding interruption gaps. SAT, local search, clique repair and restricted orbit searches found no valid improvement. Saved length-3704 colourings still have 1 progression violation; a code near miss has squared distance-deficit energy 4. These invalid candidates do not establish a new bound.</p><p>The source status review links <a href="https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/">Monroe\'s van der Waerden bound compilation</a>, <a href="https://aeb.win.tue.nl/codes/binary-1.html">Brouwer\'s binary code table</a> and <a href="https://doi.org/10.1109/18.45298">Kaikkonen\'s code construction reference</a>. Papers and downloaded source pages are linked, not copied here.</p>', ['horizonmath/hm-batchC/REPORT.txt','horizonmath/hm-batchC/solutions/vdw_W72_ap7.json','horizonmath/hm-batchC/solutions/A21_10_binary_code.json'])
    body += '<h2>Scope and reproduction</h2><p>All committed batches are included. Run <code>make -C horizonmath verify</code> for the distributed exact positive and negative checks. The original source targets also compare against upstream benchmark validators; those external implementations are not vendored here.</p><p><a href="'+REPO+'/tree/main/horizonmath">Read exact verifiers, constructions, record-status notes and campaign reports</a>.</p>'
    page('horizonmath.html','HorizonMath checks and negative results','Final HorizonMath batches A, B and C: no new record; exact checks retain W(7,2) colouring length 3703 and A(21,10) code size 42 with minimum distance 10.',body,{'@type':'SoftwareSourceCode','name':'HorizonMath independent exact verifiers','description':'Batches A, B and C found no new record. Batch C retained a length-3703 colouring and 42 binary codewords with minimum distance 10.','codeRepository':REPO+'/tree/main/horizonmath','programmingLanguage':'Python','license':'https://opensource.org/license/mit','url':BASE+'horizonmath.html'})

    body = '<p class="lead">Every reported result has a source artifact and an executable check.</p><h2>Run from the repository root</h2><pre>make verify-site\nmake verify-math</pre><p>Site verification checks imported hashes, b-file equality against the adjacent source workspace, HTML structure, internal links, metadata, sitemap coverage, JSON-LD and the privacy scan. Mathematical verification runs the OEIS extensions with both methods, BB(6) local proofs and HorizonMath exact construction checks.</p><p>Python and a C++ compiler are required for mathematical recomputation. The site generator additionally uses Pillow for its results-table image. The validator uses lxml. No browser-side framework, external font, tracker or runtime script is used.</p><h2>Check scope</h2><p>The OEIS full check recomputes the extended ranges. A separate quick command checks only published overlap. Recorded source timings are historical measurements, not promises about another machine. BB(6) portable verification checks local claims and an empty decision registry; the full simulator campaign remains in the source workspace. HorizonMath portable verification checks the exact mathematical conditions, with invalid controls.</p><h2>Source snapshots</h2><p><a href="PROVENANCE.md">Provenance and numeric claim ledger</a>, <a href="data/SHA256SUMS">b-file hashes</a>, and the <a href="'+REPO+'/blob/main/sources.json">import manifest</a> pin the evidence. Run <code>python3 tools/import_sources.py</code> only when deliberately refreshing sources, then rebuild and rerun all checks. It reads committed source blobs and never copies third-party code.</p><h2>Local report</h2><p><a href="'+REPO+'/blob/main/REPORT.md">Read actual verification output</a>. Publication, submission to OEIS and source refreshes remain separate owner actions.</p>'
    page('reproduce.html','Reproduce the verified sprint results','Commands, dependencies, source snapshots and verification boundaries for the OEIS extensions, BB(6) local proofs and HorizonMath constructions.',body,{'@type':'SoftwareSourceCode','name':'math-experiments verification tools','codeRepository':REPO,'programmingLanguage':['Python','C++'],'license':'https://opensource.org/license/mit','url':BASE+'reproduce.html'})

    sums = ''.join(f'{hashlib.sha256((DOCS/"data"/f"{s["id"]}.txt").read_bytes()).hexdigest()}  {s["id"]}.txt\n' for s in sequences)
    (DOCS/'data/SHA256SUMS').write_text(sums)
    updated = max(sources['revision_dates'].values())
    (DOCS/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+('' if p=='index.html' else p)+'</loc><lastmod>'+updated+'</lastmod></url>' for p in pages)+'</urlset>\n')
    (DOCS/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
    (DOCS/'.nojekyll').touch()
    (ROOT/'tools/claims.json').write_text(json.dumps(claims,indent=2)+'\n')
    provenance = '# Provenance\n\nAll research quantities in the rendered pages are copied from the pinned files below or computed as counts, sums and range endpoints from those files. Sequence identifiers are source labels. Technical metadata dimensions, schema versions, URLs, hashes and licence versions come from the worker brief or the file formats, not research measurements.\n\n'
    provenance += 'The total new-term count is the sum of `new_count` in `oeis/data/verification.json`. The initial 48 BB6 lemmas and 198 rejected corruptions are sums across the stage2b local verification files. The additional 118 rules, 470 rejected corruptions and 3973 concrete instantiations are sums across the certificates in bb6/data/stage2c/local-verification.json and match its final summary. The six-hour duration is the recorded 21600.08631 seconds in time-discipline.json; it is a rounded description, not a fresh timing measurement. Batch C scores, minimum distance and active wall seconds come from its REPORT.txt and exact construction files. New starting indices equal `listed_last + 1`. Timing decimals are copied exactly from the source verification manifest. The social image uses the same results table as the home page.\n\n'
    provenance += '## Pinned revisions\n\n'+''.join(f'- `{r}`: `{v}`\n' for r,v in sources['revisions'].items())
    provenance += '\n## Numeric claims by rendered section\n\n'
    for c in claims:
        nums = sorted(set(re.findall(r'\d+(?:\.\d+)?', re.sub('<[^>]+>',' ',c['html']))),key=lambda s:(len(s),s))
        provenance += f'### {c["id"]}\n\nNumbers and identifiers: '+', '.join('`'+x+'`' for x in nums)+'.\n\nEvidence: '+', '.join('`'+x+'`' for x in c['evidence'])+'.\n\n'
    provenance += '## Source files and byte identity\n\n| Source workspace and file | Distributed file | Source SHA-256 | Transformation |\n|---|---|---|---|\n'
    for f in sources['files']:
        provenance += f'| `{f["workspace"]}/{f["source"]}` | `{f["target"]}` | `{f["source_sha256"]}` | '+('Selected fields only; original hash retained' if f['transformed'] else 'None; byte-identical')+' |\n'
    provenance += '\n## Limitations and attribution\n\nBatch C and BB6 stage 2c are included from their final committed snapshots. The hm-batchC sources/ directory contains third-party research material and is excluded in full; upstream references remain links in its first-party report. Source reports are historical records; their descriptions of commits or posts apply to the source worker run. OEIS definitions are attributed quotations. Published baseline constructions retain the source attribution documented in the campaign reports. No third-party implementation is copied into this repository. Sprint management rules are drawn from the parent sprint README; private and unrelated project information is intentionally excluded.\n'
    (DOCS/'PROVENANCE.md').write_text(provenance)
    (DOCS/'github-topics.md').write_text('# Repository metadata suggestions\n\nDescription: Verified OEIS term extensions, BB(6) local proofs, and exact HorizonMath checks from an AI-managed research sprint.\n\nTopics: mathematics, oeis, busy-beaver, combinatorics, reproducible-research, computational-mathematics, github-pages, verification\n\nPages configuration: deploy from the main branch, /docs folder. The manager handles repository creation and publication.\n')
    (ROOT/'README.md').write_text(f'''# math-experiments

By [Hari Naralasetty](https://github.com/harinaralasetty) · [GitHub](https://github.com/harinaralasetty) · [LinkedIn](https://www.linkedin.com/in/harinaralasetty).

An AI coding agent managed by another AI worked on open problems whose answers can be checked by programs. Claude managed staged tasks; Codex computed candidates and wrote independent checkers. Published status was checked first. The manager reran verification, and no result was accepted without a check.

| Project | Status | Verified outcome |
|---|---|---|
| OEIS | New result | {total} new terms across {len(sequences)} sequences; not yet submitted to OEIS |
| BB(6) | Partial progress | 48 initial local lemmas for candidates 24 and 444, plus 118 new rules for candidate 24; undecided after six hours; 470 new corruption controls rejected |
| HorizonMath A, B and C | No improvement | Published baselines retained: DTS scope 112, constant-weight code size 36, covering size 30, Schur coloring through 536, W(7,2) colouring length 3703 and A(21,10) code size 42 with minimum distance 10 |

The [static site](docs/index.html) has per-sequence definitions, b-files, methods and recorded timings. The intended Pages URL is {BASE}. The manager handles publication.

Run `make verify-site` and `make verify-math`. The full OEIS check recomputes the extensions with both methods. BB(6) checks local proofs and rejects corruptions; its committed decision registry is empty. HorizonMath checks constructions with independent exact verifiers and invalid controls. See [verification output](REPORT.md), [provenance](docs/PROVENANCE.md) and [source hashes](sources.json).

Sources are pinned committed snapshots of sibling workspaces. Batch C and BB(6) stage 2c are included from their final committed snapshots. Neither produced a new record or global decision. Stage 2c added 118 local rules, with 470 rejected corruptions and 3973 concrete instantiations. Batch C credited 14675.648 seconds for progression search and 14610.090 seconds for code improvement search, excluding interruption gaps. Long finite simulation is not a decision. Failed bounded search is not an optimality proof. Benchmark tolerance effects and the Schur format mismatch are documented as checker observations, not record improvements.

The programs use Python and C++. Generating the site needs Pillow; site validation uses lxml. No third-party code is vendored. Source reports document external reference implementations. Code is [MIT](LICENSE); original data and text are [CC BY 4.0](LICENSE-DATA), with attributed quotations and baseline constructions retaining source attribution.
''')
    social_image()
    print(f'Generated {len(pages)} HTML pages, provenance, sitemap, README and social image.')


def social_image():
    image = Image.new('RGB',(1200,630),'#f4f2e9'); draw = ImageDraw.Draw(image)
    # Use a local platform font only at build time; the site loads no fonts.
    options = ['/System/Library/Fonts/Supplemental/Arial.ttf',
               '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
               '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
    fontpath = next((p for p in options if Path(p).is_file()), None)
    font = lambda n: ImageFont.truetype(fontpath,n) if fontpath else ImageFont.load_default(size=n)
    draw.rectangle((0,0,1200,12),fill='#195b46')
    draw.text((65,55),'math-experiments',font=font(46),fill='#172d26')
    draw.text((65,121),'Verified results from an AI-managed research sprint',font=font(25),fill='#43584f')
    xs=[65,400,710]; headers=['Project','Status','Verified outcome']
    for x,t in zip(xs,headers):draw.text((x,205),t,font=font(23),fill='#43584f')
    rows=[('OEIS','New result',f'{total} new terms'),('BB(6)','Partial progress','118 new local rules\n470 corruptions rejected'),('HorizonMath A/B/C','No improvement','3703 colouring\n42 codewords; distance 10')]
    for i,row in enumerate(rows):
        y=260+i*82;draw.line((65,y-14,1135,y-14),fill='#c9d1c8',width=2)
        for x,t in zip(xs,row):draw.text((x,y),t,font=font(24),fill='#172d26')
    draw.text((65,540),'OEIS terms not yet submitted. No new BB(6) decision.',font=font(24),fill='#43584f')
    (DOCS/'assets').mkdir(exist_ok=True)
    image.save(DOCS/'assets/results.png',optimize=True)


if __name__=='__main__':
    main()
