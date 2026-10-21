# Independent HorizonMath verifiers

Run `make verify` here. The portable runner checks each saved construction using
the original exact verifier, then tests an invalid construction. It also rejects
the Schur prompt's wrapper format. No claimed score is trusted.

The verifier programs and baseline constructions are byte-identical copies from
committed batch A, B and C source trees. Each batch's `REPORT.txt` is archival text;
its artifact paths refer to that source workspace. `record-status.md` preserves
the authorized record-review note. Source reports document witness attribution.

The original source targets compare against the separately checked-out HorizonMath
benchmark as well. That third-party implementation is not vendored here. Batch C
finished with W(7,2) colouring length 3703 and A(21,10) code size 42 with minimum
distance 10, matching the published bounds. Its two exact verifiers and baseline
constructions are included; its third-party sources folder is excluded. None of
the committed batches found a new record.

See [the project page](../docs/horizonmath.html), [source hashes](../sources.json)
and [provenance](../docs/PROVENANCE.md).
