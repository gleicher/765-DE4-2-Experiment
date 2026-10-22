"""Shared loaders and style for the DE4-2 figures."""
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "answers", "figures")
os.makedirs(FIG, exist_ok=True)

# Palette (colorblind-safe: Okabe-Ito subset)
BLUE, ORANGE, GREEN, PURPLE, GREY, RED, DARK = (
    "#0072B2", "#D55E00", "#009E73", "#8C5FA8", "#8A8A8A", "#C0392B", "#222222")


def style():
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#555555", "axes.titleweight": "bold",
        "figure.dpi": 100, "savefig.dpi": 200, "savefig.facecolor": "white",
    })


def save(fig, name):
    path = os.path.join(FIG, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", path)


def census():
    """County-level rows only (drops US and state summary rows)."""
    c = pd.read_csv(os.path.join(DATA, "full_census_dataset.csv"), encoding="latin-1")
    c = c[c["FIPS Code"] % 1000 != 0].copy()
    return c


def wb():
    """World Bank life expectancy, countries only (aggregates removed using
    the OWID country codes, which only list real countries/territories)."""
    l = pd.read_csv(os.path.join(DATA, "lifespan_dataset_1960.csv"), index_col=0)
    o = pd.read_csv(os.path.join(DATA, "life-expectancy-owid", "life-expectancy-owid.csv"))
    codes = set(o.Code.dropna()) - {c for c in o.Code.dropna() if c.startswith("OWID")}
    l = l[l["Country Code"].isin(codes)].copy()
    l = l.rename(columns={"Life Expectancy (years)": "le", "Country Name": "country"})
    return l
