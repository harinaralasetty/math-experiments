# Verification report

Math Experiments including OEIS stage 4 is generated locally from pinned committed source snapshots. The OEIS stages together supply 1,456 new terms across 15 sequences. No commit, push, publication or OEIS submission was performed.

The generator and stylesheet provide the announcement copy, per-sequence pages, two-significant-digit historical timings, complete downloads with 20-row previews, author credit, a visible FAQ and matching FAQPage, Article, WebSite, Dataset and breadcrumb JSON-LD, a refreshed social image, llms.txt and a sitemap. The README and all totals use the same combined sequence data. The stage 4 import preserves the earlier pinned files and adds the manager-specified committed snapshot. Its programs and b-files remain byte-identical; the report's machine-home paths are redacted and its original hash is retained. The verification runner and site checks respect each sequence's original first index.

## Source revisions

- `oeis`: `05ce39322c21fd37febd55601fbb27d7f92bc8fe`
- `bb6`: `228ba5559d062ca1f8fb5f6a21285fb9e80a6eb6`
- `hm-batchA`: `b969a3c1429b2946ea10c3b365086d39bcc60ac7`
- `hm-batchB`: `87d65db8e5b58a3e741c0bcfc3143bd44ce2609f`
- `hm-batchC`: `302ff69a016406034ec43024639c6536890a5f30`

## Verification scope and limitations

The mathematical command below recomputes every distributed OEIS row with both independent methods and checks the published overlap. It also verifies the BB(6) local proof objects, corruption controls, concrete replays and certificate fixtures, and runs the exact record-search construction verifiers with invalid controls. It does not repeat the full historical search campaigns or claim a new Busy Beaver decision or a new mathematical record. Source timings on the pages remain the separately identified historical measurements, rounded for display; actual recomputation timings appear below. Mathematical checks use this repository alone; the full site provenance check also requires the pinned sibling source workspaces. Building the site requires Git history for dates, Pillow and lxml.

Site validation uses the strict local validator for this generator's HTML5 subset, rather than the Nu HTML Checker. It checks nesting, supported attributes and content models, exactly one h1 and one initial lead sentence per page, links, unique titles and descriptions, canonical URLs, Open Graph, Twitter cards, schema author and creator identities, breadcrumbs, date consistency, sitemap and llms.txt coverage, imported hashes and source-backed numeric claims. New tests parse FAQ JSON-LD and compare it with the visible questions and answers; mutations of either the visible answer or schema answer must fail. Other mutation tests cover changed research numbers, missing leads, broken links, duplicate titles, invalid JSON-LD and sitemap omissions.

Page modification dates use each imported file's last-change date from the pinned source git revision and the relevant generator/style dates. Uncommitted generator/style changes use filesystem modification dates. The dates are repeated consistently in the byline, structured data and sitemap. Dates therefore follow each page's dependencies rather than one fixed publication date.

Responsive CSS wraps long numbers and inline code, keeps tables in scrollable boxes, lets navigation and cards wrap, and limits b-file previews to the first 20 rows. The 1200-by-630 social image was inspected directly. No rendered 390 px viewport or physical-phone test was performed. The checks verify the relevant CSS and viewport rules.

Only allowlisted first-party source programs, evidence and text were imported; third-party papers, web snapshots, archives and implementations remain excluded. All complete b-files are byte-identical to the pinned source blobs. sources.json and docs/PROVENANCE.md record hashes, transformations and dates. The privacy scan below includes hidden and ignored working-tree files, excludes git history and skips binary content.

## Build

Command: `make build`

```text
python3 tools/build_site.py
Generated 20 HTML pages, provenance, sitemap, README and social image.
```

## Site, FAQ, provenance, metadata, links and privacy

Command: `make verify-site`

```text
python3 -m unittest discover -s tools -p 'test_*.py'
................
----------------------------------------------------------------------
Ran 16 tests in 2.011s

OK
python3 tools/check_site.py
PASS imported source hashes and pinned source bytes: 186 files
PASS final stage2c summary: rule, corruption and concrete totals match source certificates; decision registry empty
PASS numeric claim ledger: 71 source-backed sections; derived totals and ranges checked
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
e7a5b09c0e4997d36a7720e99577a6bf320ff95685cded26f753267615a9e3d9  docs/data/A325549.txt  SOURCE BYTE MATCH
a2319370409368857497b77e51976b43cbc41f97f865f280bd5f36b2e6f24aed  docs/data/A336131.txt  SOURCE BYTE MATCH
96e6a8128ed07c103e715961a19f2eea0fa3315c7ab42766c9050297e89c9188  docs/data/A353426.txt  SOURCE BYTE MATCH
42d701ff8b3cee8a13259a15d17f50497ce7b1a2bc88d207fd9dd9772d46d2cc  docs/data/A320052.txt  SOURCE BYTE MATCH
1453bc6f68e786674fafb074a728791e2b0d497bf558579e06ec7931145cb2db  docs/data/A304382.txt  SOURCE BYTE MATCH
PASS local HTML5 subset validator: 20 pages, strict nesting, attributes, content models, one h1 and semantic structure
PASS internal link checker: 268 links and assets, including fragments
PASS unique titles/descriptions, canonical URLs, Open Graph, Twitter cards and parsed JSON-LD: 20 pages
PASS sitemap exact coverage: 20 pages; robots sitemap reference
PASS visible FAQ matches parsed FAQPage JSON-LD; author, Article, Dataset and breadcrumbs; per-page modification dates and llms.txt coverage
PASS responsive viewport and CSS; no runtime scripts, remote fonts, trackers or large page assets
PASS social image: 1200x630; results table drawn from the shared source model
PASS repository Markdown internal links: 15 targets
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
clang++ -O3 -std=c++17 -Wall -Wextra code/stage4/necklaces.cpp -o code/stage4/necklaces
clang++ -O3 -std=c++17 -Wall -Wextra code/stage4/independent.cpp -o code/stage4/independent
python3 -u verify.py
A391646 reference indices=0..37 PASS wall_seconds=0.039561
A391646 independent indices=0..37 PASS wall_seconds=0.091883
A374679 independent indices=0..512 PASS wall_seconds=2.690731
A374679 reference indices=0..512 PASS wall_seconds=18.421017
A383533 reference indices=0..75 PASS wall_seconds=89.164565
A335457 reference indices=0..26 PASS wall_seconds=76.211564
A353390 reference indices=0..32 PASS wall_seconds=242.098546
A374680 reference indices=0..256 PASS wall_seconds=2.171452
A374680 independent indices=0..256 PASS wall_seconds=1.154800
A374681 reference indices=0..256 PASS wall_seconds=2.005922
A374681 independent indices=0..256 PASS wall_seconds=1.659203
A374682 reference indices=0..256 PASS wall_seconds=2.297736
A374682 independent indices=0..256 PASS wall_seconds=2.875411
A353390 independent indices=0..32 PASS wall_seconds=324.281159
A383710 reference indices=0..65 PASS wall_seconds=101.989617
A383711 reference indices=0..65 PASS wall_seconds=15.097380
A383710 independent indices=0..65 PASS wall_seconds=93.925655
A325549 reference indices=1..40 PASS wall_seconds=4.168812
A383711 independent indices=0..65 PASS wall_seconds=90.847697
A336131 reference indices=0..30 PASS wall_seconds=8.875611
A336131 independent indices=0..30 PASS wall_seconds=0.335943
A353426 reference indices=0..60 PASS wall_seconds=43.707569
A353426 independent indices=0..60 PASS wall_seconds=5.612912
A320052 reference indices=0..35 PASS wall_seconds=0.619107
A320052 independent indices=0..35 PASS wall_seconds=0.709744
A304382 reference indices=1..85 PASS wall_seconds=5.785781
A304382 independent indices=1..85 PASS wall_seconds=0.199566
A383533 independent indices=0..75 PASS wall_seconds=643.852526
A325549 independent indices=1..40 PASS wall_seconds=282.956249
A335457 independent indices=0..26 PASS wall_seconds=941.890301
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

All 15 b-files and sequence pages are included. The licence holder remains Hari Naralasetty; original code is MIT and original data/text are CC BY 4.0, with existing attribution retained. The changes are left uncommitted for manager review.
