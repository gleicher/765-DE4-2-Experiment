# Instructions for this folder

If Mike says **“go”**, read and follow `RUNBOOK.md`. Otherwise, work on what you're asked.

Agents may choose Python, R, or other tools. If Python is used, always use
`/opt/anaconda3/envs/p314/bin/python`. Do not create virtual environments or use another
Python interpreter. Propose needed package additions together with a reason for each and
wait for Mike's approval. Approved additions go into `p314` using conda-forge and are
recorded in `~/Python/p314-environment.yml`; installing an editable local package also
requires telling Mike first.

Node is managed by mise: do not change managers, versions, or shims. R is installed via
Homebrew and its project packages live in `.Rlib/`: do not relocate R or manage or modify
`.Rlib/`.
