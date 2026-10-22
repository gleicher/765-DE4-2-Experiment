# Work notes

Tools: Python 3.14 from the `p314` conda environment (`/opt/anaconda3/envs/p314/bin/python`), pandas and matplotlib. No packages installed, no virtual environment, no manual steps.

Regenerate all six figures (from the project root, `runs/Sonnet-CAREFUL-2`):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

Outputs go to `answers/figures/`. The script also writes two intermediate tables to `work/`:
`gender_gap_by_country_year.csv` and `unemployment_rate_by_group.csv`.
Inputs: `data/lifespan_dataset_1960.csv`, `data/life-expectancy-owid/life-expectancy-owid.csv`, `data/full_census_dataset.csv` (read as latin-1).
