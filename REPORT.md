# Verification report

The repository and static site were refreshed locally from the final committed batch C and BB6 stage 2c source snapshots. No commit, push, publication or OEIS submission was performed. Only allowlisted committed source blobs and the authorized record-status note were imported.

## Source revisions

- `oeis`: `77efe9549b8ced52bf7bec16acb93e794872379c`
- `bb6`: `228ba5559d062ca1f8fb5f6a21285fb9e80a6eb6`
- `hm-batchA`: `b969a3c1429b2946ea10c3b365086d39bcc60ac7`
- `hm-batchB`: `87d65db8e5b58a3e741c0bcfc3143bd44ce2609f`
- `hm-batchC`: `302ff69a016406034ec43024639c6536890a5f30`

## Scope

The full OEIS run below recomputes all distributed extended rows with both original methods. Its wall seconds are actual measurements of this build. Page timing tables retain the separately identified historical source run. The BB6 portable target replays the local proof objects, corruption controls and concrete instances, plus authentic small-machine certificate fixtures. It does not rerun the full historical simulator campaign or claim a global decision. HorizonMath runs exact positive and negative construction checks, without vendoring the upstream benchmark.

HTML validation uses the repository's strict local validator for the HTML5 subset used by this generator. It checks explicit nesting, supported elements/attributes and content models, plus metadata, links and structure. It is not the Nu HTML Checker. Mutation tests exercise malformed nesting, invalid paragraph contents, unknown elements, missing alt text and duplicate attributes. Further tests alter real generated pages to check rejection of a changed research number, broken link, duplicate title, malformed JSON-LD and omitted sitemap entry.

The final BB6 stage 2c result is no global decision after the six-hour interval, with 118 additional local rules, 470 rejected corruptions and 3973 concrete instantiations. These are additional to the earlier 48 lemmas and 198 corruption controls. Batch C retained W(7,2) colouring length 3703 and an A(21,10) code of size 42 with minimum distance 10, matching published lower bounds. The full source reports contain the historical verification output; fresh portable checks below replay the distributed claims without modifying the read-only sibling workspaces.

Responsive CSS keeps tables and b-file rows in scrollable containers and wraps navigation on narrow viewports. A physical phone was not used. The refreshed social image was inspected directly. The refreshed sitemap covers every HTML page and has last-modified dates taken from pinned source commits. JSON-LD on the home and project pages describes the final outcomes.

No third-party source folder, paper, PDF, source archive or copied web page was imported. The file audit below checks forbidden archive/document extensions and import paths; sources.json and PROVENANCE.md enumerate every imported file with its original hash. Batch C research references remain upstream links.

## Site, provenance, hashes, links, sitemap, JSON-LD and privacy

Command: `make verify-site`

```text
python3 -m unittest discover -s tools -p 'test_*.py'
...........
----------------------------------------------------------------------
Ran 11 tests in 0.220s

OK
python3 tools/check_site.py
PASS imported source hashes and pinned source bytes: 144 files
PASS final stage2c summary: rule, corruption and concrete totals match source certificates; decision registry empty
PASS numeric claim ledger: 30 source-backed sections; derived totals and ranges checked
c8254c6946c5081c7a98bef5db1c49ee7274a5b1c9db25b316af740fcb8e212a  docs/data/A391646.txt  SOURCE BYTE MATCH
cb6407dce9262780347ede1f01552c286ba7f69f8cdf393df1ae17625df50607  docs/data/A383533.txt  SOURCE BYTE MATCH
0cae08d930abb2f7a9c27690792e6da326a323b1804dd6dee0c3fa173a962fc3  docs/data/A374679.txt  SOURCE BYTE MATCH
2364ef7e0888ebae32183640258713c25e4e38459fd4f077a245eefed35c1599  docs/data/A353390.txt  SOURCE BYTE MATCH
62ac5f2df048c873dcc53af7a9bf7891d1bfab75387505262d913b4e5ee15415  docs/data/A335457.txt  SOURCE BYTE MATCH
PASS local HTML5 subset validator: 10 pages, strict nesting, attributes, content models, one h1 and semantic structure
PASS internal link checker: 113 links and assets, including fragments
PASS unique titles/descriptions, canonical URLs, Open Graph, Twitter cards and parsed JSON-LD: 10 pages
PASS sitemap exact coverage: 10 pages; robots sitemap reference
PASS responsive viewport and CSS; no runtime scripts, remote fonts, trackers or large page assets
PASS social image: 1200x630; results table drawn from the shared source model
PASS repository Markdown internal links: 16 targets
PASS no vendored papers, PDFs, source archives or copied web pages; imported code is byte-identical allowlisted first-party code; batch C sources folder excluded
COMMAND: rg --hidden --no-ignore -n -I -e '[/]Users[/][^\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk[-](?:proj[-])?[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----' .
grep output: (no matches); exit status 1
PASS privacy grep: no personal home paths, email addresses, known token/key patterns or private-key headers in distributable files
Privacy grep covers the whole tree, including hidden and ignored files and git metadata; rg skips binary content. No private sprint log or third-party implementation imported.
PASS all site checks
```

## Full OEIS recomputation

Command: `make -C oeis verify`

```text
clang++ -O3 -std=c++17 -Wall -Wextra code/new_powerful.cpp -o code/new_powerful
clang++ -O3 -std=c++17 -Wall -Wextra code/new_patterns.cpp -o code/new_patterns
clang++ -O3 -std=c++17 -Wall -Wextra code/cut_runs.cpp -o code/cut_runs
clang++ -O3 -std=c++17 -Wall -Wextra code/new_runs.cpp -o code/new_runs
python3 -u verify.py
A391646 reference indices=0..37 PASS wall_seconds=0.040153
A391646 independent indices=0..37 PASS wall_seconds=0.376238
A374679 independent indices=0..512 PASS wall_seconds=1.829949
A374679 reference indices=0..512 PASS wall_seconds=12.751165
A383533 reference indices=0..75 PASS wall_seconds=60.821322
A335457 reference indices=0..26 PASS wall_seconds=62.993270
A353390 reference indices=0..32 PASS wall_seconds=205.606470
A353390 independent indices=0..32 PASS wall_seconds=280.949909
A383533 independent indices=0..75 PASS wall_seconds=533.871905
A335457 independent indices=0..26 PASS wall_seconds=953.571814
PASS all extended b-files recomputed by both methods
```

## BB6 local proofs and checker controls

Command: `make -C bb6 verify`

```text
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
```

## HorizonMath exact verifiers

Command: `make -C horizonmath verify`

```text
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

The README and site share the same result model. Every research number has a section-level source mapping in docs/PROVENANCE.md and tools/claims.json. sources.json records hashes and extraction transformations. Five distributed b-files are byte-identical to their pinned source results. The licence split is MIT for original code and CC BY 4.0 for original data/text, with source attribution retained for quotations and published constructions. Repository description, topics and Pages configuration suggestions are in docs/github-topics.md.
