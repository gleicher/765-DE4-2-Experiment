"""Shared loading + style helpers. Run scripts with /opt/anaconda3/envs/p314/bin/python."""
import pathlib, textwrap
import numpy as np, pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'answers' / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

for f in ['Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf', 'Arial Bold Italic.ttf']:
    p = pathlib.Path('/System/Library/Fonts/Supplemental') / f
    if p.exists():
        fm.fontManager.addfont(str(p))
INK, INK2, MUTED, GRID, BG = '#1f2933', '#4b5563', '#8a929c', '#e5e7eb', '#ffffff'
mpl.rcParams.update({
    'font.family': 'Arial', 'font.size': 11, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2,
    'xtick.color': INK2, 'ytick.color': INK2, 'text.color': INK, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': False, 'figure.facecolor': BG, 'axes.facecolor': BG,
    'savefig.facecolor': BG, 'axes.titleweight': 'bold'})

def header(fig, title, subtitle, y=0.975):
    fig.text(0.03, y, title, fontsize=21, fontweight='bold', va='top', ha='left', color=INK)
    fig.text(0.03, y - 0.052, subtitle, fontsize=12.5, va='top', ha='left', color=INK2, linespacing=1.35)

def caption(fig, text, width=150, y=0.012, size=9.5):
    fig.text(0.03, y, textwrap.fill(text, width), fontsize=size, va='bottom', ha='left', color=INK2,
             linespacing=1.4)

def save(fig, name):
    fig.savefig(FIG / name, dpi=200)
    plt.close(fig)
    print('wrote', name)

def clean_grid(ax, axis='y'):
    ax.grid(axis=axis, color=GRID, lw=0.8); ax.set_axisbelow(True)

# ---------- life expectancy ----------
def load_wb():
    l = pd.read_csv(DATA / 'lifespan_dataset_1960.csv', index_col=0)
    w = l.pivot_table(index=['Country Name', 'Country Code', 'Year'], columns='Sex',
                      values='Life Expectancy (years)').reset_index()
    w['gap'] = w.Female - w.Male
    o = pd.read_csv(DATA / 'life-expectancy-owid' / 'life-expectancy-owid.csv')
    o.columns = ['Entity', 'Code', 'Year', 'LE']
    # real countries = codes that OWID treats as countries (excludes World Bank aggregates like 'ARB')
    ok = set(o.Code.dropna()) - {c for c in o.Code.dropna() if str(c).startswith('OWID')}
    w = w[w['Country Code'].isin(ok)]
    return w

def load_owid():
    o = pd.read_csv(DATA / 'life-expectancy-owid' / 'life-expectancy-owid.csv')
    o.columns = ['Entity', 'Code', 'Year', 'LE']
    return o

# ---------- census ----------
def load_census():
    d = pd.read_csv(DATA / 'full_census_dataset.csv', dtype={'FIPS Code': str}, encoding='latin-1')
    d = d.copy()
    d['rucc'] = d['Rural Urban Continuum Code 2023']
    return d

GROUPS = [('Large metro (RUCC 1)', [1]), ('Other metro (2-3)', [2, 3]),
          ('Small urban nonmetro (4-7)', [4, 5, 6, 7]), ('Rural nonmetro (8-9)', [8, 9])]
def grp_of(r):
    if pd.isna(r): return np.nan
    for n, v in GROUPS:
        if r in v: return n
GCOL = {'Large metro (RUCC 1)': '#1d4e89', 'Other metro (2-3)': '#5b9bd5',
        'Small urban nonmetro (4-7)': '#e0a458', 'Rural nonmetro (8-9)': '#b5481b'}
