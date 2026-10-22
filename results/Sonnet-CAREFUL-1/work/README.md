# How the figures were made

Tool: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib, all already installed in p314. No packages were installed and no virtual environment was created. No manual steps (no hand editing of images).

Regenerate all figures (writes PNGs to `answers/figures/`):

    cd work
    for f in fig1 fig2 fig3 fig4; do /opt/anaconda3/envs/p314/bin/python $f.py; done

Files:
- `common.py`  shared loaders, palette and save helper. Census file is read with latin-1 encoding and tab/comma as given; state and US summary rows (FIPS ending 000) are dropped, leaving counties. World Bank rows are restricted to countries by keeping only codes that appear in the OWID file as real country codes (this removes regional/income aggregates such as "World" or "High income").
- `fig1.py`  Story 1 (female-male life expectancy gap): q1_a scatter, q1_b trajectories.
- `fig2.py`  Story 2 (college attainment by county type): q2_a lines, q2_b dumbbell.
- `fig3.py`  Story 3 (COVID-era life expectancy losses): q3.
- `fig4.py`  Story 4 (net domestic migration vs county size): q4.

Derived quantities: gap = Female minus Male life expectancy; migration rate = (Domestic migration 2021+2022+2023) / Census Population 2020 x 1000; county types use the 2023 Rural-urban Continuum Code.
