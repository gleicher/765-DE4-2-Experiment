# Regenerating this instructor example

Run from the `runs/Sol-SHOWOFF-2` directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses the existing pandas, NumPy, and Matplotlib installations in p314. No environment, packages, or toolchains need to be changed. It reads only the supplied two CSV files, then writes six 2340 × 1620 PNG images and matching SVG images to `answers/figures/`. It also preserves analysis tables and `summary.json` in this directory. Matplotlib's cache is directed into `work/mpl-cache/`.

No manual drawing or data corrections are required. Manual review consists of opening the six exported images to check labels, titles, captions, and the declared viewing window on the migration scatterplots. The prose in `answers/answer.md` was written separately and should be reviewed again if data or filters change.

`life_selected.csv` and `life_changes.csv` document the six-country life-expectancy selection and baseline differences. `migration_classification.csv` contains every included county's rates and outcome class. `unemployment_summary.csv` records the episode/group/year pooled rates, baseline differences, and sample sizes. `education_changes.csv` contains each included county's paired change measures. `summary.json` contains category counts and marginal medians. Inputs remain untouched.

AI disclosure: OpenAI Codex created the code, analysis, designs, and written response for private instructor review. This directory is an instructional example, not a student submission.
