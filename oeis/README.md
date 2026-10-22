# OEIS term extensions

Run `make verify` here to recompute every distributed b-file with both methods.
`make quick` checks only the previously published overlap and is not extension verification.
Python and a C++ compiler are required. No third-party implementation is included.

The source programs are copied without changes from the pinned `oeis` workspace.
The portable `verify.py` replaces the source campaign runner's cache and machine-log
handling, and compares all computed values against `../docs/data/` and the selected
published DATA fields in `data/`. Source timings and ranges are in
`data/verification.json`, `data/stage3-verification.json` and
`data/stage4-verification.json`. The original status checks are in
`data/STATUS-stage2.txt`, `data/stage3-STATUS.txt` and `data/stage4-STATUS.txt`.
The later-stage reports and unsubmitted drafts are preserved as plain text
alongside them. Machine-home paths in the stage 4 source report are redacted;
the original source hash remains in the provenance manifest. Programs are in
`code/`, `code/stage3/` and `code/stage4/`; stage 4's standalone draft programs
are in `code/stage4/drafts/`. The full check compares the original index of
every row, including sequences whose first index is one.

See [the sequence index](../docs/oeis/index.html), [source hashes](../sources.json)
and [provenance](../docs/PROVENANCE.md). These terms have not yet been submitted to OEIS.
