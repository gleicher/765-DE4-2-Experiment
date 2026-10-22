# Reproducing the instructor example

All six images were made with Python 3.14 in the curated p314 environment, using pandas, NumPy, and Matplotlib. Pillow was used to create `visual_check.png`, an inspection montage, not an assignment figure. Tableau was not used. Codex generated the complete example and inspected the exported images. No packages were installed. The script reads only supplied local CSVs, creates the six PNGs in `answers/figures/`, and retains supporting summaries here.

From this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

There are no manual processing or image-editing steps. The script configures a local Matplotlib font cache in `work/mplconfig/`. The census file is decoded as CP1252 and FIPS values are padded to five digits. Assertions check country/sex/year and FIPS uniqueness, required values, valid rural–urban codes, and final analysis counts. Supporting CSVs contain country levels and baseline changes, code-level county means/counts/gains, country sex-specific gains, and migration status counts/percentages.

The figures intentionally use standard worksheet operations:

- Q1 primary: Country panes; Year columns; life expectancy rows; line marks and a country-specific 2019 reference line. Fixed shared axes. Order by largest 2019 shortfall in 2020–23.
- Q1 alternate: Country rows; Year columns; baseline difference on diverging color and text. A highlight table with symmetric limits.
- Q2 primary: Code rows; period measures on a common axis; two circle marks and a connecting line. Mean of county percentages, same complete county set. Code order and displayed difference labels.
- Q2 alternate: Code columns; paired period measure bars; period color; mean county percentage on rows and text.
- Q3: Male endpoint gain columns; female endpoint gain rows; Country detail/label; comparison calculated field on color. The equality guide can be represented by a separate two-point line layer; the source plot here is drawn directly with Matplotlib.
- Q4: Metro/nonmetro rows; count of county IDs on columns as percent of group total; three-way offset status on color; stacked bars and labels. Negative natural-change filter precedes percent-of-total calculation.

These are conceptual authoring equivalents, not a claim that a Tableau workbook exists. PNGs have no interactive dependency. All analytic selections and limitations appear in the figures and the numbered responses.
