# Math Experiments

By [Hari Naralasetty](https://github.com/harinaralasetty) · [GitHub](https://github.com/harinaralasetty) · [LinkedIn](https://www.linkedin.com/in/harinaralasetty).

Working with AI agents, Hari Naralasetty computed 1,350 new terms for 10 OEIS sequences. Each term was produced by two independent programs that agree exactly. This experimental mathematics project also checked partial BB(6) results and found no new records in three record-search batches. The published status of each problem was checked first, and no result is reported without a re-run check.

| Project | Status | Verified outcome |
|---|---|---|
| OEIS | New result | 1,350 new terms across 10 sequences; not yet submitted to OEIS |
| BB(6) | Partial progress | 48 initial local lemmas for candidates 24 and 444, plus 118 new rules for candidate 24; undecided after six hours; 470 new corruption controls rejected |
| HorizonMath A, B and C | No improvement | Published baselines retained: DTS scope 112, constant-weight code size 36, covering size 30, Schur coloring through 536, W(7,2) colouring length 3703 and A(21,10) code size 42 with minimum distance 10 |

The [static site](docs/index.html) has per-sequence definitions, b-files, methods and recorded timings. Live site: https://harinaralasetty.github.io/math-experiments/

Run `make verify-site` and `make verify-math`. The full OEIS check recomputes the extensions with both methods. BB(6) checks local proofs and rejects corruptions; its committed decision registry is empty. HorizonMath checks constructions with independent exact verifiers and invalid controls. See [verification output](REPORT.md), [provenance](docs/PROVENANCE.md) and [source hashes](sources.json).

Sources are pinned committed snapshots of sibling workspaces. Batch C and BB(6) stage 2c are included from their final committed snapshots. Neither produced a new record or global decision. Stage 2c added 118 local rules, with 470 rejected corruptions and 3973 concrete instantiations. Batch C credited 240 min for progression search and 240 min for code improvement search, excluding interruption gaps. Long finite simulation is not a decision. Failed bounded search is not an optimality proof. Benchmark tolerance effects and the Schur format mismatch are documented as checker observations, not record improvements.

The programs use Python and C++. Generating the site needs Pillow; site validation uses lxml. No third-party code is vendored. Source reports document external reference implementations. Code is [MIT](LICENSE); original data and text are [CC BY 4.0](LICENSE-DATA), with attributed quotations and baseline constructions retaining source attribution.
