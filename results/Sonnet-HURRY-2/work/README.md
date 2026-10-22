# Tools and regeneration
Everything is produced by one script, `work/make_figures.py`, using Python (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib (already installed; nothing was installed, no venv).

Regenerate all six figures from the project root:

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

Outputs go to `answers/figures/`. No manual steps. Notes: `full_census_dataset.csv` is comma-separated and latin-1 encoded (the data README says tab-separated, which is wrong); county rows are those with a 2023 Rural-Urban Continuum Code (state/US rows have none). World Bank aggregates are removed by keeping only codes that OWID lists as countries (non-"OWID_" ISO codes).
