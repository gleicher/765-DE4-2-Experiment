# Work files

`make_figures.py` generates the six PNG figures referenced by `answers/answer.md`. It reads the course-provided CSV files in `data/` and writes to `answers/figures/`.

Run it from this folder’s root with the curated Python environment:

```sh
MPLCONFIGDIR="$PWD/work/.matplotlib" /opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses the installed pandas and Matplotlib packages. It writes all six figures automatically; there are no manual steps. The answer text and figure annotations were drafted from descriptive summaries of the supplied data. No external pages or data were used.
