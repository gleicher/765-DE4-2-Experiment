# work/

Tool: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas and matplotlib already in p314. No packages installed, no virtual environment.

Regenerate all six figures (no manual steps; run from this folder):

    /opt/anaconda3/envs/p314/bin/python -I make_figs.py

Outputs: `../answers/figures/q1_a_*.png, q1_b_*.png, q2_a_*.png, q2_b_*.png, q3_*.png, q4_*.png`, plus small CSV summaries here (`education_by_rucc.csv`, `education_by_group.csv`, `unemployment_by_group.csv`).

- `make_figs.py` reads `../data/` only (World Bank lifespan file, OWID file, full census file read as latin-1; the census file is comma-separated despite the README). Regional aggregates are removed from World Bank data by keeping only country codes that appear in the OWID file with a non-"OWID_" code.
- `explore.py` is the first quick look at the female-male gap.
- Layout (titles, captions, label positions) was tuned by hand in the script after viewing the PNGs.
