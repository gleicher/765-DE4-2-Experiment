# work/ README

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib. No other software; no manual steps (all annotations are placed in code). Font: Arial from /System/Library/Fonts/Supplemental.

Regenerate all figures (writes PNGs to `../answers/figures/`):

    cd work
    for f in fig1a fig1b fig2a fig2b fig3 fig4; do /opt/anaconda3/envs/p314/bin/python $f.py; done

Files
- `common.py` : shared style, data loaders (World Bank, OWID, census), RUCC grouping and colors.
- `fig1a.py` / `fig1b.py` : Story 1 (female-minus-male life expectancy gap): trajectories and arrows.
- `fig2a.py` / `fig2b.py` : Story 2 (rural vs urban unemployment): lines + gap bars, and county-level strips.
- `fig3.py` : Story 3 (college attainment divergence, 1990 to 2019-23).
- `fig4.py` : Story 4 (setbacks in life expectancy since 1950, OWID).
- `fig2_unemployment_by_group.csv`, `fig4_episodes_5yr.csv` : intermediate outputs written by the scripts.

Notes: the census CSV is read with `encoding='latin-1'` and comma separator (despite the README saying tab). Pandas fragmentation warnings are harmless.
