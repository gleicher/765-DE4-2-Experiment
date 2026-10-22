# How the figures were made

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib, all already installed in p314. No packages were installed, no virtual environment was created, and no manual steps (no hand editing of images) were used.

Regenerate all six figures (run from this folder; the scripts use absolute paths set in `common.py`):

    cd work
    /opt/anaconda3/envs/p314/bin/python fig_q1.py     # Q1 primary + alternate
    /opt/anaconda3/envs/p314/bin/python fig_rest.py   # Q2 primary + alternate, Q3, Q4

Files: `common.py` (data loading, aggregate filtering, county cleaning), `style.py` (fonts, colors, title/caption helper), `explore*.py` (exploratory checks used to choose stories). Figures are written to `answers/figures/`.

Data processing: World Bank file pivoted to Female/Male/Both columns, gap = Female - Male, regional/income aggregates dropped by name pattern (217 countries remain). Census file read as comma-separated latin-1; rows with FIPS codes ending in 000 (state/national totals) dropped; Connecticut drops out of the 1990-vs-2019-23 comparison because its geography changed.
