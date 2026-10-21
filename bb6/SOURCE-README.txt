# BB(6) stage-1 research workspace

Start with [REPORT.md](REPORT.md), then [SHORTLIST.md](SHORTLIST.md).
No machine is claimed newly decided in this stage.

Stage 2 status and bounded attempts are recorded in
[data/STATUS-stage2.md](data/STATUS-stage2.md) and the stage-2 section of
[REPORT.md](REPORT.md). Reproduce with:

```sh
python3 tools/stage2_status.py
python3 tools/stage2_attempt.py
make verify-decisions
python3 tools/stage2_report.py
```

The attempt runner checkpoints after every probe and resumes completed records.
It processes the shortlist in order with one child at a time; each probe has a
deadline. The status archive and extracted upstream proof tree are retained
locally and ignored by git; the saved manifest records their source and hash.
An empty `decisions/registry.json` means no checked decision is claimed.

Requires Python, Clang C++, curl and tar. Source selection additionally uses
BeautifulSoup (`bs4`), already present in the task environment. Verification
and triage use only the Python standard library and the vendored searcher.

```sh
make tools
make verify
make select
make triage
make shortlist
make audit
make report
```

`make triage` resumes matching completed machine records. To rerun every
computation from scratch while keeping source evidence, move `data/triage.jsonl`
out of the workspace first. Each simulation and search has a subprocess time
limit. Child computations share a four-slot lock pool, leaving room for the
Python coordinators under the requested CPU ceiling. Run the top-level targets
sequentially as shown.

Examples:

```sh
build/fast_sim 1RB1LB_1LA0LC_1RZ1LD_1RD0RA 1000 /tmp/bb4-tape.rle
build/reference_sim simulate 1RB1LB_1LA0LC_1RZ1LD_1RD0RA 1000
build/decider_tc decide 1RA---_------_------ 8192
python3 tools/ngram.py 1RA---_------_------ 2 5000
python3 tools/check_tc.py certificates/verification/translated_cycler-00.json
python3 tools/check_ngram.py certificates/verification/ngram_cps-00.json
```

The fast simulator's final argument writes the exact tape as absolute-start,
symbol, run-length rows, with zeros everywhere outside the rows. JSON reports
step count, state, head position, head span, ones, tape runs, writes that change
a symbol, direction changes, adjacent-symbol counts, and a positional tape hash.
Halting transitions count as one step; an undefined `---` is completed as
`1RZ`, matching the reference simulator's convention. Visited width includes
the final head position.

`data/SOURCES.md` contains download URLs, UTC completion timestamps and hashes.
The full upstream archives are retained in `data/`; `vendor/` contains the
unpacked sources. See [tools/CERTIFICATES.md](tools/CERTIFICATES.md) for the
certificate invariants and [REPORT.md](REPORT.md) for licences and limitations.
## Stage 2b reproduction

The focused attempt notes are `notes/024-attempt.md` and, after its scheduled
investigation begins, `notes/444-attempt.md`. Local symbolic lemmas are research
results only. The decision registry determines which global claims exist.

```sh
python3 tools/stage2_status.py --stage2b
python3 tools/stage2_status.py --stage2b --offline
python3 tools/stage2b_rules.py
python3 tools/check_symbolic.py data/stage2b/024-local-lemmas.json --trace data/stage2b/024-symbolic-proof-traces.json
make verify-decisions
clang++ -O3 -std=c++17 -Wall -Wextra tools/stage2b_block.cpp -o build/stage2b_block
clang++ -O3 -std=c++17 -Wall -Wextra tools/stage2b_family.cpp -o build/stage2b_family
clang++ -O3 -std=c++17 -Wall -Wextra tools/stage2b_frontier.cpp -o build/stage2b_frontier
clang++ -O3 -std=c++17 -Wall -Wextra tools/stage2b_tree.cpp -o build/stage2b_tree
```

The fixed-block and tree programs print their usage when invoked without
arguments. Their checkpoints store complete finite tapes with zero tails.
Tree macros stop at the last complete root transition before a requested step
limit; the printed step count is authoritative. Finite exploration is never a
non-halting proof. The family explorer starts from hypothetical nonblank
configurations and records that distinction in its witnesses.

The optional SAT search uses `z3-solver`, installed for this attempt in a
temporary virtual environment. Its version is recorded in each search result.
For example, after installing that dependency in a virtual environment:

```sh
python -m pip install -r tools/requirements-stage2b.txt
python tools/stage2b_far_sat.py --states 7 8 9 10 11 12 --seconds 180
python tools/stage2b_far_sat.py --states 8 12 16 --seconds 1200 --cycle 3
python tools/stage2b_far_cegis.py --states 12 --cycle 3 --seconds 1200
```

The solver saves compressed SMT-LIB queries before solving. SAT candidates
must pass `tools/check_far.py`, which needs only the standard Python library
and imports no search code. Solver `unsat` and timeout results are search
outcomes, not machine decisions. Known-machine controls have distinct tags
and contain their actual machine string; they are not decisions on candidate 24.

`stage2b_far_templates.py` checks fixed prefix automata derived from run residues
and the negative-base encoding. `stage2b_far_cegis.py` learns prefix-graph
constraints from failed closures and checkpoints its learned SMT query.
The known-halter gate's individual queries are packed in
`data/stage2b/far-gate-queries.tar.gz`; its summary and archive hash remain beside it.

`stage2b_packed_cps.py` is the corrected, packed position-phase search. Its
`promotion-v2` result records identify the current algorithm. The earlier
packed run is explicitly marked discarded. Completed control closures agree
with the upstream implementation. Position-phase certificates use
`check_phase_cps.py`; search limits and abstract halting windows are not decisions.
The memory setting is an RSS stop threshold, with the measured peak recorded.


The signed-position hypothetical-family tests use `build/stage2b_family signed
TRIALS MAX_DIGITS EVEN_FRONTIER_RETURNS WALL_SECONDS LOG [ODD_RUN_CHOICES
[RESUME_CHECKPOINT]]`. `ODD_RUN_CHOICES=3` permits runs 2, 3, 4 at negative
base-minus-two positions. The source snapshot for the earlier seven-choice
run is retained separately. These are frame-counterexample searches, not
blank-start decisions. Checkpoints retain the PRNG state and aggregate counts.

The exhaustive carry test is `build/stage2b_family guarded-all MAX_DIGITS
STEP_CAP WALL_SECONDS LOG CHECKPOINT [RESUME_CHECKPOINT]`. It enumerates the
revised guarded frame with a leading 3 or guarded 4 and records complete
lengths separately from a partial checkpoint. The independent count check
runs in `make verify-decisions`; it does not turn finite simulations into a
nonhalting certificate. `python3 tools/stage2b_discover.py bases --output
data/stage2b/024-small-counter-proposals.json` regenerates the small counter
proposals before `tools/stage2b_rules.py` and the separate symbolic checker.

Candidate 444 has its own generator and checked state-entry guard. The guard
and the local `F00` path justify the F0-shortened machine's blank-start halting
equivalence, without a decision. Reproduce its local proof and bounded run:

```sh
python3 tools/stage2b_rules_444.py
python3 tools/check_symbolic.py data/stage2b/444-local-lemmas.json
make verify-decisions
build/stage2b_block 1RB0RD_1RC---_0LA1RA_0RE1RC_1LE0LF_0RC0LF 16 100000000000 data/stage2b/444-deep.checkpoint 300 data/stage2b/444-block16-billion.checkpoint
python tools/stage2b_far_cegis.py --index 444 --machine 1RB0RD_1RC---_0LA1RA_0RE1RC_1LE0LF_0RC0LF --states 12 --seconds 1200 --solver-check-seconds 300 --minimize-support --tag cegis
```

Add `--mirror` for the reflected FAR query. Recorded logs, rather than the
requested horizons, define completed work. The two attempt notes distinguish
proved local rules, measured counter relations and the missing global proofs.

## Stage 2c reproduction

Candidate 24 only. The current outcome and timing are in `REPORT.md` and
`notes/024-attempt.md`. Local lemmas, conditional boundary safety and finite
hypothetical halts do not decide the blank-start machine.

```sh
python3 tools/stage2_status.py --stage2c
python3 tools/stage2c_rules.py
python3 tools/stage2c_boundary.py --max-digits 10
python3 tools/stage2c_simulators.py
python3 tools/stage2c_witnesses.py
make verify-decisions
```

The nonblank simulator adapters preserve both original transition-execution
implementations. They add finite initialization and exact final-tape export.
Fresh verification rebuilds them, compares the hypothetical halts, checks exact
blank rebuilding tapes, and replays the selected primitive blank anchor with
corruption controls. `check_guarded_phase.py` accepts only a conditional
statement that halting requires a previous unary-prefix visit.
`check_guarded_anchor.py` additionally requires a full primitive blank replay
and a global FAR invariant; no global claim exists without a checked registry
entry and decision document.

The optional synthesis campaigns require the same `z3-solver` dependency as
stage 2b. Their saved UTC deadlines are specific to this research interval;
edit those before deliberately starting a new campaign. Search outcomes,
configured limits and concrete hypotheses are distinct from decisions.
`tools/stage2c_progress.py` reads the current checkpoints without running a
search. Every accepted global candidate must be checked independently before
updating `decisions/registry.json`. No worker commits or external posts are
part of this workflow.

`data/stage2c/search-steering.json` records later search-bias overrides. A raw
query filename may retain the coordinator's requested bias; its JSON record
contains the effective bias and the steering-file hash. Saved SMT-LIB files
are the authoritative query constraints. Cross-size reuse imports only learned
edge-blocking clauses; a full resume with a different period bias is discarded.
The same steering record can select the reflected machine for the general
blank-start search. Effective orientation is explicit in query JSON and in any
certificate. Parsed blocking-clause caches are derived from saved SMT-LIB and
are ignored by git; they are never proof certificates.
