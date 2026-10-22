# Regenerating this example

From the run directory, execute:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses the existing pandas, NumPy, and Matplotlib packages. It reads only the supplied files under `data/` and writes six PNGs to `answers/figures/`, plus calculation tables to `work/`. Matplotlib's cache is directed into `work/mpl-cache/`. No package installation, network lookup, or manual chart-editing step is required. Tableau was not used; the ordinary faceted lines, highlight table, grouped bars, stacked bars, and baseline calculations were chosen to resemble a restrained Tableau worksheet workflow.

`figure_review.png` is a contact sheet made with Pillow for inspecting the six outputs. It is a review artifact, not an assignment figure. The complete numbered responses and critique are in `answers/answer.md`. OpenAI Codex selected the designs, wrote the scripts, inspected outputs, and wrote the answers. See response 20 for the full disclosure.

Intermediate tables: `life_sex_comparison.csv`, `life_gap_table.csv`, `education_shares.csv`, `life_2019_changes.csv`, `natural_loss_counties.csv`, and `natural_loss_summary.csv`. Education record counts are included per period. Natural-loss records include the derived outcome and their original source fields.
