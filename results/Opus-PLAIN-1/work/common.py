"""Shared data loading and plotting style for the DE 4-2 figures.

All figure scripts import from here. Paths are resolved relative to this file so
scripts can be run from any working directory.
"""
from pathlib import Path

import matplotlib as mpl
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "answers" / "figures"
INTER = Path(__file__).resolve().parent / "intermediate"
FIG.mkdir(parents=True, exist_ok=True)
INTER.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
INK = "#1a1a1a"
INK2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e4e3df"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
RED = "#c8383a"
BLUE_RAMP = ["#86b6ef", "#3987e5", "#256abf", "#0d366b"]  # ordinal, light->dark


def setup_style():
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": INK2,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 200,
    })


# ---------------------------------------------------------------- life expectancy
def owid():
    df = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    df = df.rename(columns={"Period life expectancy at birth": "le"})
    return df


def country_codes():
    """ISO3 codes of real countries/territories, taken from the OWID file
    (OWID marks its regional aggregates with codes starting 'OWID_' or no code).
    Used only to drop World Bank aggregates such as 'Euro area' or 'IDA only'."""
    df = owid()
    codes = df["Code"].dropna()
    return set(codes[~codes.str.startswith("OWID")])


def worldbank(countries_only=True):
    df = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    df = df.rename(columns={"Country Name": "country", "Country Code": "code",
                            "Life Expectancy (years)": "le"})
    if countries_only:
        df = df[df["code"].isin(country_codes())]
    return df


# ---------------------------------------------------------------- census
RUCC_LABELS = {
    1: "Metro, 1 million+",
    2: "Metro, 250k–1 million",
    3: "Metro, under 250k",
    4: "Nonmetro, urban 20k+, adjacent to metro",
    5: "Nonmetro, urban 20k+, not adjacent",
    6: "Nonmetro, urban 5k–20k, adjacent",
    7: "Nonmetro, urban 5k–20k, not adjacent",
    8: "Nonmetro, urban <5k, adjacent",
    9: "Nonmetro, urban <5k, not adjacent",
}


def census():
    """County rows only (state and national summary rows dropped), 50 states + DC.
    The file is comma-separated and Latin-1 encoded (despite the readme)."""
    df = pd.read_csv(DATA / "full_census_dataset.csv", dtype={"FIPS Code": str},
                     encoding="latin-1")
    fips = df["FIPS Code"].astype(int)
    df = df[(fips % 1000 != 0) & (df["State"] != "PR")].copy()
    df["rucc"] = df["2023 Rural-urban Continuum Code"]
    return df
