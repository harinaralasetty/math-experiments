# BB6 local proof checks

Run `make verify` here. The portable runner checks the distributed symbolic local
lemmas, rejects mutations, replays concrete instances, and checks authentic small-machine
certificate fixtures with deliberately invalid controls. It also requires an empty
decision registry. Local lemmas cannot be promoted to non-halting certificates.

The first-party checker programs and proof objects are byte-identical copies from
the pinned BB6 source. `SOURCE-README.txt`, `REPORT.txt` and
`tools/CERTIFICATES.txt` preserve the original source instructions and trust boundaries.
They are archival text; their relative artifact references refer to the source
workspace, not to a complete vendored copy here. The original third-party simulator
and search implementations are not included. Their upstream references and pinned
setup are documented in `SOURCE-README.txt`.

The full source `make verify` and `make verify-decisions` include historical campaign
artifacts and external tools. The portable target checks only the explicitly distributed
claims and controls. Stage 2c is included from its final committed snapshot. It adds
118 local rules, 470 rejected corruptions and 3973 concrete replays to the earlier
48 local lemmas. Candidate 24 remains undecided after the six-hour interval.
No new decision is claimed. The portable runner replays both stages' local proofs;
it does not rerun the source's global, conditional or anchor search campaigns.

See [the project page](../docs/bb6.html), [source hashes](../sources.json)
and [provenance](../docs/PROVENANCE.md).
