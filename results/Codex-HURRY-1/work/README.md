# Regenerate the figures

Run from this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses existing pandas, NumPy, and Matplotlib in `p314`. It creates six static 2160×1440 PNG figures in `answers/figures/`, `work/summary.json`, and `work/migration_plot_data.csv`. `work/mplconfig/` holds Matplotlib's local font cache. No package installation or manual chart editing is needed.

Data inputs are the supplied World Bank life expectancy CSV and county Census CSV. The latter is comma-delimited and Windows-1252 encoded. The script records the population filters, matched education sample, and derived gap/component calculations directly. It retains full-range migration data in an inset while zooming the main panel.

`work/contact_sheet.png` was created with Pillow by placing reduced versions of the six figure images in a two-column, three-row grid, for visual review only. `work/render_log.txt` records the script's numerical summaries. These intermediates remain available.

Manual steps before submission: review all six full-size figures and the numerical summaries; revise the AI-drafted critique and rationales to reflect your own choices and judgments; replace answer 1 if you participated in CLO; retain an accurate AI disclosure; upload the six images to their corresponding Canvas questions. `answers/answer.md` maps all 20 Canvas items to responses or files. No online sources were used.
