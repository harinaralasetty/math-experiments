# Verification report

Math Experiments v2 is generated locally from pinned committed source snapshots. The OEIS stages together supply 1,350 new terms across 10 sequences. No commit, push, publication or OEIS submission was performed.

The generator and stylesheet provide the announcement copy, per-sequence pages, two-significant-digit historical timings, complete downloads with 20-row previews, author credit, a visible FAQ and matching FAQPage, Article, WebSite, Dataset and breadcrumb JSON-LD, a refreshed social image, llms.txt and a sitemap. The README and all totals use the same combined sequence data.

## Source revisions

- `oeis`: `3504def3c80d31ce2cacb94b9fa67843812518db`
- `bb6`: `228ba5559d062ca1f8fb5f6a21285fb9e80a6eb6`
- `hm-batchA`: `b969a3c1429b2946ea10c3b365086d39bcc60ac7`
- `hm-batchB`: `87d65db8e5b58a3e741c0bcfc3143bd44ce2609f`
- `hm-batchC`: `302ff69a016406034ec43024639c6536890a5f30`

## Verification scope and limitations

The mathematical command below recomputes every distributed OEIS row with both independent methods and checks the published overlap. It also verifies the BB(6) local proof objects, corruption controls, concrete replays and certificate fixtures, and runs the exact record-search construction verifiers with invalid controls. It does not repeat the full historical search campaigns or claim a new Busy Beaver decision or a new mathematical record. Source timings on the pages remain the separately identified historical measurements, rounded for display; actual recomputation timings appear below. Mathematical checks use this repository alone; the full site provenance check also requires the pinned sibling source workspaces. Building the site requires Git history for dates, Pillow and lxml.

Site validation uses the strict local validator for this generator's HTML5 subset, rather than the Nu HTML Checker. It checks nesting, supported attributes and content models, exactly one h1 and one initial lead sentence per page, links, unique titles and descriptions, canonical URLs, Open Graph, Twitter cards, schema author and creator identities, breadcrumbs, date consistency, sitemap and llms.txt coverage, imported hashes and source-backed numeric claims. New tests parse FAQ JSON-LD and compare it with the visible questions and answers; mutations of either the visible answer or schema answer must fail. Other mutation tests cover changed research numbers, missing leads, broken links, duplicate titles, invalid JSON-LD and sitemap omissions.

Page modification dates use each imported file's last-change date from the pinned source git revision and the relevant generator/style dates. Uncommitted generator/style changes use filesystem modification dates. The dates are repeated consistently in the byline, structured data and sitemap. Dates therefore follow each page's dependencies rather than one fixed publication date.

Responsive CSS wraps long numbers and inline code, keeps tables in scrollable boxes, lets navigation and cards wrap, and limits b-file previews to the first 20 rows. The 1200-by-630 social image was inspected directly. Browser automation was unavailable, so no rendered 390 px viewport or physical-phone test is claimed. The checks verify the relevant CSS and viewport rules.

Only allowlisted first-party source programs, evidence and text were imported; third-party papers, web snapshots, archives and implementations remain excluded. All complete b-files are byte-identical to the pinned source blobs. sources.json and docs/PROVENANCE.md record hashes, transformations and dates. The privacy scan below includes hidden and ignored working-tree files, excludes git history and skips binary content.

## Build

Command: `make build`

```text
python3 tools/build_site.py
Generated 15 HTML pages, provenance, sitemap, README and social image.
```

## Site, FAQ, provenance, metadata, links and privacy

Command: `make verify-site`

```text
python3 -m unittest discover -s tools -p 'test_*.py'
...............
----------------------------------------------------------------------
Ran 15 tests in 1.105s

OK
python3 tools/check_site.py
PASS imported source hashes and pinned source bytes: 163 files
PASS final stage2c summary: rule, corruption and concrete totals match source certificates; decision registry empty
PASS numeric claim ledger: 51 source-backed sections; derived totals and ranges checked
c8254c6946c5081c7a98bef5db1c49ee7274a5b1c9db25b316af740fcb8e212a  docs/data/A391646.txt  SOURCE BYTE MATCH
cb6407dce9262780347ede1f01552c286ba7f69f8cdf393df1ae17625df50607  docs/data/A383533.txt  SOURCE BYTE MATCH
0cae08d930abb2f7a9c27690792e6da326a323b1804dd6dee0c3fa173a962fc3  docs/data/A374679.txt  SOURCE BYTE MATCH
2364ef7e0888ebae32183640258713c25e4e38459fd4f077a245eefed35c1599  docs/data/A353390.txt  SOURCE BYTE MATCH
62ac5f2df048c873dcc53af7a9bf7891d1bfab75387505262d913b4e5ee15415  docs/data/A335457.txt  SOURCE BYTE MATCH
3d75a9aee887565f0e61d50aed7ef80ac12ce6324ef9f55de30dbc1c40cba338  docs/data/A374680.txt  SOURCE BYTE MATCH
0e20b1f08d9c44f9e83dd2bf63bbaf50523051d12b9143a69c2829db8778275c  docs/data/A374681.txt  SOURCE BYTE MATCH
c723aac27e7467e8bcf65eee9dd2c467697f81def286f2093ee5e0018a3fc7ff  docs/data/A374682.txt  SOURCE BYTE MATCH
38e674a6ecc63b74c8b468dd02200b3d51d31c53efa3c45ccfa8f0b8803d7e6e  docs/data/A383710.txt  SOURCE BYTE MATCH
8c7ab3d49b82270d9a010ddbee632cf6a829f18352ecf3fc4a79f6d89a80e816  docs/data/A383711.txt  SOURCE BYTE MATCH
PASS local HTML5 subset validator: 15 pages, strict nesting, attributes, content models, one h1 and semantic structure
PASS internal link checker: 198 links and assets, including fragments
PASS unique titles/descriptions, canonical URLs, Open Graph, Twitter cards and parsed JSON-LD: 15 pages
PASS sitemap exact coverage: 15 pages; robots sitemap reference
PASS visible FAQ matches parsed FAQPage JSON-LD; author, Article, Dataset and breadcrumbs; per-page modification dates and llms.txt coverage
PASS responsive viewport and CSS; no runtime scripts, remote fonts, trackers or large page assets
PASS social image: 1200x630; results table drawn from the shared source model
PASS repository Markdown internal links: 16 targets
PASS no vendored papers, PDFs, source archives or copied web pages; imported code is byte-identical allowlisted first-party code; batch C sources folder excluded
COMMAND: python regex scan of every file under the repo root (hidden and ignored files included; .git excluded)
scan output: (no matches)
PASS privacy grep: no personal home paths, email addresses, known token/key patterns or private-key headers in distributable files
Privacy scan covers the whole working tree, including hidden and ignored files, and skips binary content and .git history. No private sprint log or third-party implementation imported.
PASS all site checks
```

## Complete mathematical verification

Command: `make verify-math`

```text
/Library/Developer/CommandLineTools/usr/bin/make -C oeis verify
clang++ -O3 -std=c++17 -Wall -Wextra code/new_powerful.cpp -o code/new_powerful
clang++ -O3 -std=c++17 -Wall -Wextra code/new_patterns.cpp -o code/new_patterns
clang++ -O3 -std=c++17 -Wall -Wextra code/cut_runs.cpp -o code/cut_runs
clang++ -O3 -std=c++17 -Wall -Wextra code/new_runs.cpp -o code/new_runs
python3 -u verify.py
A391646 reference indices=0..37 PASS wall_seconds=0.062775
A391646 independent indices=0..37 PASS wall_seconds=0.735525
A374679 independent indices=0..512 PASS wall_seconds=3.338294
A374679 reference indices=0..512 PASS wall_seconds=17.497081
A383533 reference indices=0..75 PASS wall_seconds=83.054962
A335457 reference indices=0..26 PASS wall_seconds=57.928392
A353390 reference indices=0..32 PASS wall_seconds=190.461001
A374680 reference indices=0..256 PASS wall_seconds=1.861636
A374680 independent indices=0..256 PASS wall_seconds=0.978749
A374681 reference indices=0..256 PASS wall_seconds=1.897893
A374681 independent indices=0..256 PASS wall_seconds=1.404770
A374682 reference indices=0..256 PASS wall_seconds=1.875518
A374682 independent indices=0..256 PASS wall_seconds=1.976311
A353390 independent indices=0..32 PASS wall_seconds=255.390424
A383710 reference indices=0..65 PASS wall_seconds=83.903052
A383711 reference indices=0..65 PASS wall_seconds=12.255656
A383710 independent indices=0..65 PASS wall_seconds=71.512934
A383711 independent indices=0..65 PASS wall_seconds=68.046216
A383533 independent indices=0..75 PASS wall_seconds=501.919625
A335457 independent indices=0..26 PASS wall_seconds=874.489557
PASS all extended b-files recomputed by both methods
/Library/Developer/CommandLineTools/usr/bin/make -C bb6 verify
python3 -u verify.py
024-local-lemmas.json: local lemmas=27 corruptions_rejected=106 concrete_replays=372 PASS
444-local-lemmas.json: local lemmas=21 corruptions_rejected=92 concrete_replays=468 PASS
PASS local lemmas=48 corruptions_rejected=198 concrete_replays=840; registered decisions=0
024-carry-lemmas.json: local lemmas=6 corruptions_rejected=25 concrete_replays=155 PASS
024-boundary-lemmas.json: local lemmas=109 corruptions_rejected=436 concrete_replays=3815 PASS
024-hypothetical-halt-lemmas.json: local lemmas=3 corruptions_rejected=9 concrete_replays=3 PASS
PASS stage2c local lemmas=118 corruptions_rejected=470 concrete_replays=3973; registered decisions=0
PASS translated_cycler source fixtures accepted=20; corruptions and halting-transition variants rejected=40; controls only, no new decisions
PASS ngram_cps source fixtures accepted=20; corruptions and halting-transition variants rejected=40; controls only, no new decisions
/Library/Developer/CommandLineTools/usr/bin/make -C horizonmath verify
python3 verify.py
dts_7_5_min_scope: scope=112; valid witness accepted, invalid control rejected PASS
cwcode_29_8_5: num_blocks=36; valid witness accepted, invalid control rejected PASS
covering_C13_k7_t4: num_blocks=30; valid witness accepted, invalid control rejected PASS
schur_6: N=536; valid witness accepted, invalid control rejected PASS
vdw_W72_ap7: length=3703; valid witness accepted, invalid control rejected PASS
A21_10_binary_code: number_of_codewords=42; valid witness accepted, invalid control rejected PASS
PASS 15 exact verifier cases; no new record claimed
```

## Delivery

All 10 b-files and sequence pages are included. The licence holder remains Hari Naralasetty; original code is MIT and original data/text are CC BY 4.0, with existing attribution retained. The changes are left uncommitted for manager review.
