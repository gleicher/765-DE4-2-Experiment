# DE 4-2 working files

Tools: Python 3.14 from the `p314` conda env (`/opt/anaconda3/envs/p314/bin/python`) with
pandas, numpy, and matplotlib. Nothing new was installed. R was not used.

Regenerate all six figures (from the run folder):

    /opt/anaconda3/envs/p314/bin/python work/make_figures.py

That writes:

- `answers/figures/q1a_gender_gap_lines.png`, `q1b_gender_gap_small_multiples.png`
  (World Bank life expectancy by sex)
- `answers/figures/q2a_components_by_rucc.png`, `q2b_county_scatter.png` (county census file)
- `answers/figures/q3_fifty_to_seventy.png` (OWID long-run life expectancy)
- `answers/figures/q4_unemployment_two_recessions.png` (state-level census file)

plus intermediate tables in `work/intermediate/` (the summary numbers quoted in the
answers come from these).

There are no manual steps; the PNGs are used exactly as the script saves them. Data
notes: `full_census_dataset.csv` is actually comma-separated and must be read as
latin-1. `aggregate_census_dataset.csv` is tab-separated.
