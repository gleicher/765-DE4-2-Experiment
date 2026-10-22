"""Shared prep for Q2: components of county population change, 2021-2023 (per 1,000 residents per year)."""
from common import *
Y = [2021, 2022, 2023]
COMP = {"nat": "Natural Change", "dom": "Domestic migration", "intl": "International Migration",
        "chg": "Population Change"}

def county_components():
    c = load_counties()
    c = c[c.rucc.notna() & (c.State != "PR")].copy()   # drop 17 old AK/CT units without a 2023 code; PR has no components data
    for k, col in COMP.items():
        c[k] = sum(c[f"{col} {y}"] for y in Y)
    c["base"] = c["Population Estimate 2020"]
    for k in COMP:
        c[k + "_r"] = c[k] / c.base * 1000 / len(Y)
    c["rucc"] = c.rucc.astype(int)
    c["grp"] = np.select([c.rucc == 1, c.rucc <= 3], ["Large metro", "Smaller metro"], "Nonmetro")
    return c

def rucc_components(c):
    g = c.groupby("rucc")[list(COMP) + ["base"]].sum()
    out = g[list(COMP)].div(g.base, axis=0) * 1000 / len(Y)
    out["pop"] = g.base; out["n"] = c.groupby("rucc").size()
    return out
