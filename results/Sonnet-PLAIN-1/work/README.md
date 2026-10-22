# work/ README

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy, matplotlib (already installed; nothing was installed). No manual steps; all six figures are drawn by code (titles, captions, labels included). Nothing was edited by hand.

Regenerate (from the Sonnet-PLAIN-1 folder):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

Output: answers/figures/q1a_*, q1b_*, q2a_*, q2b_*, q3_*, q4_*.png. The script also prints the episode table and group medians used in the text.

Data notes: full_census_dataset.csv is actually comma-separated (the README says tab) and needs latin-1 encoding; aggregate_census_dataset.csv is tab-separated. World Bank aggregates (regions, income groups) are removed for Fig 3 by keeping only country codes that appear in the Our World in Data file as real countries.
