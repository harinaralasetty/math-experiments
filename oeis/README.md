# OEIS term extensions

Run `make verify` here to recompute every distributed b-file with both methods.
`make quick` checks only the previously published overlap and is not extension verification.
Python and a C++ compiler are required. No third-party implementation is included.

The source programs are copied without changes from the pinned `oeis` workspace.
The portable `verify.py` replaces the source campaign runner's cache and machine-log
handling, and compares all computed values against `../docs/data/` and the selected
published DATA fields in `data/`. Source timings and ranges are in
`data/verification.json` and `data/stage3-verification.json`. The original status checks are in
`data/STATUS-stage2.txt` and `data/stage3-STATUS.txt`; the stage 3 report and
unsubmitted drafts are preserved as plain text alongside them. Stage 3 programs
are in `code/stage3/`.

See [the sequence index](../docs/oeis/index.html), [source hashes](../sources.json)
and [provenance](../docs/PROVENANCE.md). These terms have not yet been submitted to OEIS.
