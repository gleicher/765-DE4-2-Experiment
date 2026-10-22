# Figure generation

The six static PNGs in `../answers/figures/` are generated from the course-provided life-expectancy and census files by `make_figures.py`. The script uses the curated Python environment at `/opt/anaconda3/envs/p314/bin/python`, with the already-installed pandas and Matplotlib packages. It installs nothing and writes its Matplotlib cache under `work/mplconfig/`.

From this run directory, regenerate the figures with:

```sh
MPLCONFIGDIR="$PWD/work/mplconfig" /opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script reads the life-expectancy CSV with its index column, reads the census CSV as Latin-1 because of a non-UTF-8 character in the supplied file, filters county/county-equivalent records using the metropolitan-area indicator, and derives the female-minus-male gap and the education-attainment quartiles. It writes all six PNGs to `answers/figures/` and prints the descriptive values used in the write-up. There are no manual steps required to regenerate them. `figures_contact_sheet.png` is a local review montage, not a submitted figure.

The charts were authored with Python/Matplotlib, not Tableau. Their layouts use familiar Tableau worksheet operations and restrained worksheet styling, but the generation was fully scripted.
