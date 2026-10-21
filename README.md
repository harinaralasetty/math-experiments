# math-experiments

By [Hari Naralasetty](https://github.com/harinaralasetty) · [GitHub](https://github.com/harinaralasetty) · [LinkedIn](https://www.linkedin.com/in/harinaralasetty).

An AI coding agent managed by another AI worked on open problems whose answers can be checked by programs. Claude managed staged tasks; Codex computed candidates and wrote independent checkers. Published status was checked first. The manager reran verification, and no result was accepted without a check.

| Project | Status | Verified outcome |
|---|---|---|
| OEIS | New result | 577 new terms across 5 sequences; not yet submitted to OEIS |
| BB(6) | Partial progress | 48 initial local lemmas for candidates 24 and 444, plus 118 new rules for candidate 24; undecided after six hours; 470 new corruption controls rejected |
| HorizonMath A, B and C | No improvement | Published baselines retained: DTS scope 112, constant-weight code size 36, covering size 30, Schur coloring through 536, W(7,2) colouring length 3703 and A(21,10) code size 42 with minimum distance 10 |

The [static site](docs/index.html) has per-sequence definitions, b-files, methods and recorded timings. The intended Pages URL is https://harinaralasetty.github.io/math-experiments/. The manager handles publication.

Run `make verify-site` and `make verify-math`. The full OEIS check recomputes the extensions with both methods. BB(6) checks local proofs and rejects corruptions; its committed decision registry is empty. HorizonMath checks constructions with independent exact verifiers and invalid controls. See [verification output](REPORT.md), [provenance](docs/PROVENANCE.md) and [source hashes](sources.json).

Sources are pinned committed snapshots of sibling workspaces. Batch C and BB(6) stage 2c are included from their final committed snapshots. Neither produced a new record or global decision. Stage 2c added 118 local rules, with 470 rejected corruptions and 3973 concrete instantiations. Batch C credited 14675.648 seconds for progression search and 14610.090 seconds for code improvement search, excluding interruption gaps. Long finite simulation is not a decision. Failed bounded search is not an optimality proof. Benchmark tolerance effects and the Schur format mismatch are documented as checker observations, not record improvements.

The programs use Python and C++. Generating the site needs Pillow; site validation uses lxml. No third-party code is vendored. Source reports document external reference implementations. Code is [MIT](LICENSE); original data and text are [CC BY 4.0](LICENSE-DATA), with attributed quotations and baseline constructions retaining source attribution.
