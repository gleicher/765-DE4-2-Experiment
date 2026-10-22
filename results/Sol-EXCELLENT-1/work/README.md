# Regenerating the six figures

Tools: the existing `p314` Python 3.14 environment, pandas, NumPy, and Matplotlib. No package additions or external data are required.

From the run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

This reads `data/lifespan_dataset_1960.csv` and `data/full_census_dataset.csv`, writes six PNGs into `answers/figures/`, and saves the county outcome counts and education quantiles here. The county CSV uses commas and CP1252 encoding. FIPS strings are padded before filtering. The script documents the complete-case selection and plot transformations, and places Matplotlib’s cache under `work/mpl-cache/`.

`explore.py` reproduces the preliminary summaries used to check the story choices. `county_outcomes.csv` and `education_summary.csv` preserve the calculated values used in the finished figures. These are intermediate work, not additional assignment deliverables.

There are no manual image-editing steps. Codex inspected the generated figures using an image viewer and revised the Python layout settings. The answers and critique were written in Markdown after reading the supplied references and examining `reference/images/to-critique.png`. No web pages were opened; all sources were supplied locally.
