"""Shared paths, data loaders, and matplotlib style for DE4-2 figures."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "answers" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Palette (validated with the dataviz skill validator; see README)
BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
SURFACE = "#ffffff"
# sequential blue ramp (light -> dark) for ordinal rurality
SEQ = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "legend.frameon": False,
})


def title_block(fig, title, subtitle, x=0.06, y=0.975, gap=0.045):
    fig.text(x, y, title, fontsize=16, fontweight="bold", color=INK, va="top")
    fig.text(x, y - gap, subtitle, fontsize=10.5, color=INK2, va="top", linespacing=1.4)


def caption(fig, text, x=0.06, y=0.015):
    fig.text(x, y, text, fontsize=8.3, color=INK2, va="bottom", linespacing=1.45, wrap=True)


def save(fig, name):
    out = FIG / name
    fig.savefig(out, dpi=200)
    print("wrote", out)


# ---------------- World Bank life expectancy ----------------
WB_AGGREGATE_CODES = set("""AFE AFW ARB CEB CSS EAP EAR EAS ECA ECS EMU EUU FCS HIC HPC IBD IBT IDA IDB IDX
INX LAC LCN LDC LIC LMC LMY LTE MEA MIC MNA NAC OED OSS PRE PSS PST SAS SSA SSF SST TEA TEC
TLA TMN TSA TSS UMC WLD""".split())


def load_wb():
    w = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    p = (w.pivot_table(index=["Country Name", "Country Code", "Year"], columns="Sex",
                       values="Life Expectancy (years)").reset_index())
    p.columns.name = None
    p["gap"] = p["Female"] - p["Male"]
    p["is_country"] = ~p["Country Code"].isin(WB_AGGREGATE_CODES)
    return p


# ---------------- USDA county census ----------------
RUCC_GROUPS = [
    (1, 1, "Large metro (1M+ people)"),
    (2, 3, "Smaller metro"),
    (4, 5, "Nonmetro, town 20k+"),
    (6, 7, "Nonmetro, town 5k–20k"),
    (8, 9, "Rural (no town of 5k)"),
]


def load_counties():
    c = pd.read_csv(DATA / "full_census_dataset.csv", dtype={"FIPS Code": str}, encoding="latin-1")
    c = c[(c["FIPS Code"].astype(int) % 1000 != 0) & (c["State"] != "PR")].copy()
    # 2023 codes; fall back to 2013 codes for areas without one (e.g. Connecticut's
    # former counties, which carry the labor-force data but have no 2023 code)
    r = c["2023 Rural-urban Continuum Code"].fillna(c["2013 Rural-urban Continuum Code"])
    labels = pd.Series(pd.NA, index=c.index, dtype="object")
    for lo, hi, lab in RUCC_GROUPS:
        labels[(r >= lo) & (r <= hi)] = lab
    c["rgroup"] = pd.Categorical(labels, [g[2] for g in RUCC_GROUPS], ordered=True)
    return c.copy()
