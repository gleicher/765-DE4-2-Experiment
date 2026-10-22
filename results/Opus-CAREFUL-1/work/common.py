"""Shared data loading and plot styling for the DE4-2 figures."""
from pathlib import Path

import matplotlib as mpl
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "answers" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Colors (categorical slots 1-4 used in fixed order; gray for context)
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
RED = "#e34948"
GRAY = "#9a9994"
LIGHTGRAY = "#d6d5d0"
INK = "#1d1d1b"
INK2 = "#52514e"
SURFACE = "white"

# World Bank aggregate (non-country) codes, used to drop regions/income groups
WB_AGGREGATES = set(
    "AFE AFW ARB CEB CSS EAP EAR EAS ECA ECS EMU EUU FCS HIC HPC IBD IBT IDA IDB "
    "IDX INX LAC LCN LDC LIC LMC LMY LTE MEA MIC MNA NAC OED OSS PRE PSS PST SAS "
    "SSA SSF SST TEA TEC TLA TMN TSA TSS UMC WLD".split()
)

ECON_TYPES = {
    0: "Nonspecialized",
    1: "Farming",
    2: "Mining",
    3: "Manufacturing",
    4: "Federal/state government",
    5: "Recreation",
}

RUCC_LABELS = {
    1: "Metro area of 1 million+",
    2: "Metro area of 250k-1 million",
    3: "Metro area under 250k",
    4: "Nonmetro, urban pop. 20k+, next to a metro",
    5: "Nonmetro, urban pop. 20k+, not next to a metro",
    6: "Nonmetro, urban pop. 5k-20k, next to a metro",
    7: "Nonmetro, urban pop. 5k-20k, not next to a metro",
    8: "Nonmetro, urban pop. under 5k, next to a metro",
    9: "Nonmetro, urban pop. under 5k, not next to a metro",
}


def style():
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": 10,
        "axes.edgecolor": GRAY,
        "axes.linewidth": 0.6,
        "axes.labelcolor": INK2,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "grid.color": "#ebeae6",
        "grid.linewidth": 0.6,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "savefig.dpi": 200,
    })


def load_census():
    """County rows only (drops Puerto Rico and rows without FIPS)."""
    c = pd.read_csv(DATA / "full_census_dataset.csv", encoding="latin-1",
                    dtype={"FIPS Code": str}, thousands=",").copy()
    c["FIPS Code"] = c["FIPS Code"].str.zfill(5)
    c = c[(c["State"] != "PR") & ~c["FIPS Code"].str.endswith("000")]
    return c


def load_worldbank():
    le = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    w = le.pivot_table(index=["Country Name", "Country Code", "Year"],
                       columns="Sex", values="Life Expectancy (years)").reset_index()
    w["gap"] = w["Female"] - w["Male"]
    return w


def load_owid():
    o = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    o = o.rename(columns={"Period life expectancy at birth": "le"})
    return o


def title_block(fig, title, subtitle, y=0.975):
    fig.text(0.03, y, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.03, y - 0.045, subtitle, fontsize=10.5, color=INK2, va="top")


def caption(fig, text, y=0.015, chars=150, size=8.6):
    import textwrap
    paras = [textwrap.fill(p, chars) for p in text.split("\n")]
    fig.text(0.03, y, "\n".join(paras), fontsize=size, color=INK2, va="bottom",
             linespacing=1.35)
