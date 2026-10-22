# Work notes

Tools: Python 3.14 (/opt/anaconda3/envs/p314/bin/python) with pandas and matplotlib. No extra packages were installed, no manual steps.

Regenerate all six figures (writes to ../answers/figures/):

    cd work
    /opt/anaconda3/envs/p314/bin/python -I make_figures.py

Inputs are read from ../data/ (World Bank lifespan_dataset_1960.csv, full_census_dataset.csv; the census CSV needs latin1 encoding). Puerto Rico is dropped from the census charts. The answers are in ../answers/answer.md.
