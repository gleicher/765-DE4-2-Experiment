"""Q2 data: components of county population change by Rural-Urban Continuum Code (2023).

Census 'year' Y runs July 1 (Y-1) to June 30 (Y). We use 2021-2023 (the three full
years; the '2020' columns cover only April-June 2020).
Rates are population-weighted: sum of component counts in the RUCC group divided by the
group's population at the start of the year (Population Estimate Y-1), per 1,000 residents.
"""
import pandas as pd
from common import census, INTER, RUCC_LABELS

COMP = {"Natural change (births − deaths)": "Natural Change {y}",
        "Domestic migration (moves within the US)": "Domestic migration {y}",
        "International migration": "International Migration {y}"}
YEARS = [2021, 2022, 2023]


def annual_rates():
    d = census().dropna(subset=["rucc"])
    g = d.groupby("rucc")
    rows = []
    for y in YEARS:
        base = g[f"Population Estimate {y-1}"].sum()
        for name, col in COMP.items():
            r = g[col.format(y=y)].sum() / base * 1000
            for k, v in r.items():
                rows.append(dict(rucc=int(k), year=y, component=name, rate=v))
    return pd.DataFrame(rows)


def cumulative_rates():
    d = census().dropna(subset=["rucc"])
    g = d.groupby("rucc")
    base = g["Population Estimate 2020"].sum()
    out = pd.DataFrame({"pop2023": g["Population Estimate 2023"].sum(), "counties": g.size()})
    for name, col in COMP.items():
        out[name] = sum(g[col.format(y=y)].sum() for y in YEARS) / base * 1000
    out.index = out.index.astype(int)
    out["label"] = [RUCC_LABELS[i] for i in out.index]
    return out


if __name__ == "__main__":
    a = annual_rates(); a.to_csv(INTER / "q2_annual_rates.csv", index=False)
    c = cumulative_rates(); c.to_csv(INTER / "q2_cumulative_rates.csv")
    print(c.round(1).to_string())
