# How the figures were made

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib (all already
installed; nothing was installed). Tableau was NOT used and is not installed. The figures are drawn with
matplotlib to imitate the look of Tableau worksheets (Tableau 10 palette, light gridlines, left-aligned titles,
legends at right, caption below), and each design was chosen so it could be built from standard Tableau operations
(dimensions/measures on rows and columns, aggregation, color, labels, sort, Top-N filter, reference line,
trend line, simple calculated fields).

Regenerate (from the run folder, no manual steps):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

This reads `data/` and writes the six PNGs to `answers/figures/` and prints the statistics quoted in
`answers/answer.md`.

Data notes: `data/full_census_dataset.csv` is actually comma-separated (the README says tab) and Latin-1 encoded;
`aggregate_census_dataset.csv` is the tab-separated one. Country-level life expectancy uses the World Bank file with
aggregate regions removed by keeping only codes that appear as real countries in the OWID file.
Calculated fields: gap = Female - Male; unemployment rate = sum(Unemployed)/sum(Civilian labor force).
Connecticut and Puerto Rico are excluded from the state migration chart; one county with 0% bachelor's is dropped
from the education scatter.
