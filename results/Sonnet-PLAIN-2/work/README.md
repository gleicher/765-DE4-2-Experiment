# Work notes

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas and matplotlib, both already installed in p314. Nothing was installed. No manual steps (no Tableau, Illustrator, etc.); every figure is fully scripted.

Regenerate all six figures (run from the project folder `runs/Sonnet-PLAIN-2`):

    /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py

Output goes to `answers/figures/`. Files:
- `common.py` - data loading (the county CSV is comma-separated and latin-1 encoded despite what data/README.md says; aggregates are filtered out of the life-expectancy file by name pattern).
- `make_figures.py` - all figures.
- `explore*.py` - scratch scripts used to check numbers quoted in captions and answers.
