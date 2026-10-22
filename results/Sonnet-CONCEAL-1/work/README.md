# Work notes

Tool: Python (/opt/anaconda3/envs/p314/bin/python) with pandas, numpy, matplotlib (all already installed; nothing new installed). No manual steps.

Regenerate all six figures (written to ../answers/figures/):

    cd work
    /opt/anaconda3/envs/p314/bin/python -I make_figures.py

Data is read from ../data/ (census CSV is latin-1 encoded; the state-level file is tab separated). World Bank aggregates (income groups, regions) are filtered out by name for the country-level plot and used on purpose for the income-group plot. Census state/US rows (FIPS ending 000) are dropped for county analyses.
