"""Shared loaders and styling for all figures."""
import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "answers" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

INK = "#1f2933"; MUTED = "#616e7c"; FAINT = "#cbd2d9"; GRID = "#e4e7eb"; BG = "white"

mpl.rcParams.update({
    "font.family": "Arial", "font.size": 11, "text.color": INK,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "axes.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": BG, "axes.facecolor": "none",
    "savefig.facecolor": BG, "axes.titlelocation": "left", "legend.frameon": False,
})

# ---------- life expectancy (World Bank) ----------
_AGG = re.compile(r"income|dividend|IDA|IBRD|&|Euro|World|OECD|small states|Small states|"
                  r"Fragile|Heavily|Least developed|North America|South Asia$|Sub-Saharan|"
                  r"Africa Eastern|Africa Western|Central Europe|Pacific island|Other small|"
                  r"Middle East, North")

def life_wide():
    """One row per country-year with Male, Female, Both and gap (F - M); aggregates removed."""
    d = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    d = d[~d["Country Name"].str.contains(_AGG)]
    w = d.pivot_table(index=["Country Name", "Country Code", "Year"], columns="Sex",
                      values="Life Expectancy (years)").reset_index()
    w["gap"] = w["Female"] - w["Male"]
    return w

# ---------- census ----------
def census_counties():
    c = pd.read_csv(DATA / "full_census_dataset.csv", encoding="latin-1")
    c["rucc"] = c["2023 Rural-urban Continuum Code"]
    c["pop"] = c["Population Estimate 2023"]
    return c

def census_states():
    a = pd.read_csv(DATA / "aggregate_census_dataset.csv", sep="\t", encoding="latin-1")
    return a

# ---------- layout helpers ----------
def frame(fig, title, subtitle=None, caption=None, source=None, top=0.935, left=0.04, wrap=150):
    fig.text(left, top, title, fontsize=19, fontweight="bold", ha="left", va="top", color=INK)
    if subtitle:
        fig.text(left, top - 0.085, subtitle, fontsize=11.5, ha="left", va="top", color=MUTED,
                 linespacing=1.35)
    if caption:
        fig.text(left, 0.012 + (0.02 if source else 0), caption, fontsize=9.5, ha="left", va="bottom",
                 color=INK, linespacing=1.4)
    if source:
        fig.text(left, 0.008, source, fontsize=8, ha="left", va="bottom", color=MUTED)

def save(fig, name):
    p = FIG / name
    fig.savefig(p, dpi=170)
    plt.close(fig)
    print("saved", p)


def spread(ys, gap, lo=None, hi=None):
    """Nudge label y-positions apart so adjacent labels are >= gap apart (keeps order)."""
    order = np.argsort(ys); y = np.array(ys, float)[order]
    for i in range(1, len(y)):
        if y[i] - y[i-1] < gap: y[i] = y[i-1] + gap
    # re-centre the pushed cluster
    shift = (np.array(ys, float)[order] - y).mean()
    y = y + shift
    for i in range(1, len(y)):
        if y[i] - y[i-1] < gap: y[i] = y[i-1] + gap
    out = np.empty_like(y); out[order] = y
    return out

# Consistent grouping of countries used by both Story-1 figures
GROUPS = {
    "Post-Soviet states": dict(color="#D55E00",
        codes=["RUS","UKR","BLR","LVA","EST","LTU","KAZ"],
        blurb="Gap surged after 1990, then fell,\nbut Ukraine's has jumped since 2020"),
    "Wealthy countries": dict(color="#0072B2",
        codes=["USA","GBR","FRA","DEU","SWE","JPN","KOR","AUS"],
        blurb="Widened to ~6-8 yrs by the 1970s-90s,\nthen steadily narrowed"),
    "South Asia": dict(color="#009E73",
        codes=["IND","PAK","BGD","NPL"],
        blurb="Men once outlived women (gap < 0);\nwomen now ahead by 3-5 yrs"),
    "Gulf states & West Africa": dict(color="#8E4585",
        codes=["NGA","TGO","KWT","QAT","BHR","ARE"],
        blurb="Gap nearly closed:\nwomen's edge is only 0.4-2 yrs"),
}
SHORT = dict(RUS="Russia", UKR="Ukraine", BLR="Belarus", LVA="Latvia", EST="Estonia", LTU="Lithuania",
             KAZ="Kazakhstan", USA="US", GBR="UK", FRA="France", DEU="Germany", SWE="Sweden",
             JPN="Japan", KOR="S. Korea", AUS="Australia", IND="India", PAK="Pakistan",
             BGD="Bangladesh", NPL="Nepal", NGA="Nigeria", TGO="Togo", KWT="Kuwait", QAT="Qatar",
             BHR="Bahrain", ARE="UAE")

import warnings
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

# ---------- Story 2: education by county type ----------
EDU_PCT = {1970: 'Percent of adults completing four years of college or higher, 1970',
           1980: 'Percent of adults completing four years of college or higher, 1980',
           1990: "Percent of adults with a bachelor's degree or higher, 1990",
           2000: "Percent of adults with a bachelor's degree or higher, 2000",
           2010: "Percent of adults with a bachelor's degree or higher, 2008-12",
           2021: "Percent of adults with a bachelor's degree or higher, 2019-23"}
EDU_N = {1970: 'Four years of college or higher, 1970', 1980: 'Four years of college or higher, 1980',
         1990: "Bachelor's degree or higher, 1990", 2000: "Bachelor's degree or higher, 2000",
         2010: "Bachelor's degree or higher, 2008-12", 2021: "Bachelor's degree or higher, 2019-23"}
GRP_LABEL = {"metro": "Metro counties\n(RUCC 1-3)", "urb20k": "Small cities, 20k+ residents\n(RUCC 4-5)",
             "urb5k": "Small towns, 5-20k residents\n(RUCC 6-7)", "rural": "Most rural, <5k residents\n(RUCC 8-9)"}
GRP_SHORT = {"metro": "Metro", "urb20k": "Small cities (20k+)", "urb5k": "Small towns (5-20k)", "rural": "Most rural (<5k)"}
GRP_COLOR = {"metro": "#1f3a93", "urb20k": "#2a9d8f", "urb5k": "#d9992b", "rural": "#c0392b"}

def edu_counties():
    c = census_counties().copy()
    c["grp"] = pd.cut(c["rucc"], [0, 3, 5, 7, 9], labels=list(GRP_LABEL))
    for y in EDU_PCT:
        c[f"pct{y}"] = c[EDU_PCT[y]]
        c[f"adults{y}"] = c[EDU_N[y]] / c[EDU_PCT[y]] * 100
        c[f"n{y}"] = c[EDU_N[y]]
    return c

def edu_weighted(c):
    out = {}
    for y in EDU_PCT:
        d = c.dropna(subset=["grp", f"adults{y}", f"n{y}"])
        out[y] = d.groupby("grp", observed=True).apply(lambda t: t[f"n{y}"].sum() / t[f"adults{y}"].sum() * 100)
    return pd.DataFrame(out)
