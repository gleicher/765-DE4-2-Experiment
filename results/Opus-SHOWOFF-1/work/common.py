"""Shared paths, data loaders and visual style for all DE4-2 figures."""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "answers" / "figures"
INTER = ROOT / "work" / "intermediate"
FIG.mkdir(parents=True, exist_ok=True); INTER.mkdir(parents=True, exist_ok=True)

# ---- palette (validated reference palette from the dataviz skill) ----
SURFACE = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; AXIS = "#c3c2b7"; NEUTRAL = "#f0efec"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
BLUE_RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
             "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]

def setup():
    plt.rcParams.update({
        "font.family": ["Helvetica Neue", "Arial Unicode MS"], "font.size": 10.5,
        "axes.facecolor": SURFACE, "figure.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlecolor": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
        "axes.axisbelow": True, "legend.frameon": False,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
    })

def header(fig, title, subtitle, y=0.975, x=0.035):
    fig.text(x, y, title, fontsize=19, fontweight="bold", color=INK, va="top")
    fig.text(x, y - 0.042, subtitle, fontsize=11.5, color=INK2, va="top", linespacing=1.4)

def footer(fig, text, y=0.012, x=0.035):
    fig.text(x, y, text, fontsize=8.6, color=MUTED, va="bottom", linespacing=1.35)

def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=200)
    plt.close(fig)
    print("wrote", FIG / f"{name}.png")

# ---- loaders ----
WB_AGG = set("AFE AFW ARB CSS CEB EAR EAS EAP TEA EMU ECS ECA TEC EUU FCS HPC HIC IBD IBT IDB IDX IDA "
             "LTE LCN LAC TLA LDC LMY LIC LMC MEA MNA TMN MIC NAC INX OED OSS PSS PST PRE SST SAS TSA "
             "SSF SSA TSS UMC WLD".split())

def load_wb():
    """World Bank life expectancy, one row per country-year with Male/Female/Both + gap."""
    w = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    w.columns = ["name", "code", "sex", "year", "le"]
    p = w.pivot_table(index=["name", "code", "year"], columns="sex", values="le").reset_index()
    p.columns.name = None
    p["gap"] = p["Female"] - p["Male"]
    p["is_agg"] = p.code.isin(WB_AGG)
    return p

def load_owid():
    o = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    o.columns = ["ent", "code", "year", "lex"]
    return o

def load_counties():
    c = pd.read_csv(DATA / "full_census_dataset.csv", dtype={"FIPS Code": str}, encoding="latin-1").copy()
    c["fips"] = c["FIPS Code"].str.zfill(5)
    cty = c[~c.fips.str.endswith("000")].copy()   # drop US and state rows
    cty["rucc"] = cty["2023 Rural-urban Continuum Code"]
    return cty

RUCC_LABEL = {
    1: "Metro, 1 million+", 2: "Metro, 250k-1M", 3: "Metro, <250k",
    4: "Nonmetro, 20k+ urban, adjacent to metro", 5: "Nonmetro, 20k+ urban, not adjacent",
    6: "Nonmetro, 5-20k urban, adjacent", 7: "Nonmetro, 5-20k urban, not adjacent",
    8: "Nonmetro, <5k urban, adjacent", 9: "Nonmetro, <5k urban, not adjacent",
}
