# OEIS term extensions

Run `make verify` here to recompute every distributed b-file with both methods.
`make quick` checks only the previously published overlap and is not extension verification.
Python and a C++ compiler are required. No third-party implementation is included.

The source programs are copied without changes from the pinned `oeis` workspace.
The portable `verify.py` replaces the source campaign runner's cache and machine-log
handling, and compares all computed values against `../docs/data/` and the selected
published DATA fields in `data/`. Source timings and ranges are in
`data/verification.json`; `data/STATUS-stage2.txt` is the original status-gate report.

See [the sequence index](../docs/oeis/index.html), [source hashes](../sources.json)
and [provenance](../docs/PROVENANCE.md). These terms have not yet been submitted to OEIS.
