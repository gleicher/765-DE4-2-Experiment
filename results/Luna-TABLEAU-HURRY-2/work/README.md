# Figure source and regeneration

The six PNG figures in `answers/figures/` are generated with Python 3.14 from the `p314` environment, using pandas to read and shape the local course CSV files and Matplotlib to draw static charts. ChatGPT assisted with question selection, data exploration, code, design decisions, rationales, and the critique. Tableau was not used.

Run this from the `runs/Luna-TABLEAU-HURRY-2` folder:

```sh
MPLCONFIGDIR=work/.mpl-cache /opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script reads `data/lifespan_dataset_1960.csv` and `data/full_census_dataset.csv`, then overwrites the six PNGs under `answers/figures/`. It reads the Census file with `cp1252` encoding and zero-pads FIPS codes for consistent IDs. The figures use calculated female-minus-male life-expectancy gaps, metro/nonmetro groupings from 2023 continuum codes, complete-case filters for each comparison, attainment quartiles for the Census boxplots, and the twelve largest 2019–2021 life-expectancy declines for the final view.

There are no manual figure edits or other manual regeneration steps.
