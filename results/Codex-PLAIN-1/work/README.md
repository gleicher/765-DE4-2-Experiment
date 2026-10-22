# Reproducing the figures

Tools: Python 3.14 from the curated `p314` environment, pandas, NumPy, Matplotlib, and Pillow (contact sheet only). No installations were required.

From this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py > work/summary.txt
```

The script reads the supplied local CSVs and writes six 180-dpi PNGs to `answers/figures/`, plus intermediate CSVs in `work/`. It creates its Matplotlib cache under `work/.mplconfig/`. Country subsets, axes, label positions, colors, and captions are specified directly in the script. No manual image editing or interactive steps are required. The original `life_gains.csv` is retained from an earlier exploratory candidate; it is not used in the final figures.

`contact_sheet.png` shows the final six figures. `contact_sheet_initial.png` retains an earlier layout check whose fifth panel is an exploratory candidate. The final fifth figure was separately inspected at full size. `answer.md` was drafted separately, using the local assignment, evaluation guidelines, data documentation, and supplied critique image. No websites were opened or outside data joined.
