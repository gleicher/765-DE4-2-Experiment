"""Q1 data: pandemic-era life-expectancy loss and 'years of progress erased'.

For each country (World Bank data, both sexes):
  trough      = lowest life expectancy in 2020-2022
  loss        = LE(2019) - trough
  setback_to  = latest year before 2019 whose LE was <= trough
                (i.e. the trough put the country back to that year's level)
  yrs_erased  = 2019 - setback_to
  rec         = LE(2023) - LE(2019)   (>= 0 means fully recovered)
"""
import numpy as np
import pandas as pd
from common import worldbank, INTER


def q1_table(sex="Both"):
    wb = worldbank()
    p = wb[wb.Sex == sex].pivot(index="country", columns="Year", values="le")
    rows = []
    for c, r in p.iterrows():
        if r[[2019, 2020, 2021, 2022, 2023]].isna().any():
            continue
        win = r[[2020, 2021, 2022]]
        tr, ty = win.min(), int(win.idxmin())
        pre = r.loc[:2018].dropna()
        below = pre[pre <= tr]
        sb = int(below.index.max()) if len(below) else np.nan
        rows.append(dict(country=c, le2019=r[2019], trough=tr, trough_year=ty,
                         loss=r[2019] - tr, setback_to=sb, yrs_erased=2019 - sb,
                         le2023=r[2023], rec=r[2023] - r[2019]))
    return pd.DataFrame(rows), p


if __name__ == "__main__":
    t, _ = q1_table()
    t.sort_values("loss", ascending=False).to_csv(INTER / "q1_pandemic_setback.csv", index=False)
    print(t.sort_values("yrs_erased", ascending=False).head(25).round(2).to_string())
    print(len(t), (t.loss >= 1).sum(), (t.rec >= 0).sum(), t.yrs_erased.median())
