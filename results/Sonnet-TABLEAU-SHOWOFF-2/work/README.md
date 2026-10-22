# How the figures were made

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas and matplotlib, styled to look like Tableau worksheets. No Tableau was used and nothing was installed; no manual steps.

Regenerate (from the run folder):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figs.py

This reads `data/` and writes the six PNGs to `answers/figures/` and intermediate tables to `work/intermediate/`.
