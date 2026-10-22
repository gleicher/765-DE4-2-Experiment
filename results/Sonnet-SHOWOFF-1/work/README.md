# How the figures were made

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib (all already installed; nothing was installed). No manual steps; every figure is drawn entirely by code and no image editor was used.

Regenerate everything (from this folder):

    cd work
    for f in fig1a fig1b fig2a fig2b fig3 fig4; do /opt/anaconda3/envs/p314/bin/python $f.py; done

Outputs go to `../answers/figures/`. `common.py` holds the data loaders (the census CSV is latin-1 encoded; the state file is tab-separated), the aggregate-removal filter, shared colours and layout helpers.

- fig1a.py / fig1b.py: Question 1 (life-expectancy sex gap): small multiples and dumbbell
- fig2a.py / fig2b.py: Question 2 (education by county type): pooled lines and county distributions
- fig3.py: Question 3 (COVID loss and recovery of life expectancy)
- fig4.py: Question 4 (state unemployment tile grid)
