# Work notes

Tools: Python (/opt/anaconda3/envs/p314/bin/python) with pandas, numpy and matplotlib. No Tableau
(it is not installed here); the figures are matplotlib charts styled to imitate default Tableau
worksheets (Tableau 10 palette, Arial, light gridlines, legends at right, direct labels, reference lines).

Regenerate all six figures (no manual steps):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

Run from the project folder. Input: data/ (full_census_dataset.csv is latin-1; aggregate_census_dataset.csv is
tab-separated). Output: answers/figures/*.png. The script also prints the numbers quoted in answers/answer.md.
Data processing: pivoted World Bank sex into columns to compute female-male gap; grouped counties by 2023
Rural-urban Continuum Code (1-3 metro; 4,6,8 nonmetro adjacent; 5,7,9 nonmetro not adjacent); education quartiles;
labor-force-weighted unemployment rates; 3-year average of state domestic migration rates.
