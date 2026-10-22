"""Q4 data: when did each country first reach life expectancy 50, and how long did it take to reach 70?

OWID period life expectancy at birth. Crossing years are linearly interpolated between the
last observation below the threshold and the first at/above it; a crossing is only accepted
if those two observations are at most 10 years apart (historical series are sparse) and the
country has an observation below the threshold (so we know it was not already above).
Countries that reached 50 but not 70 by 2023 are kept as 'not yet' (right-censored).
"""
import numpy as np
import pandas as pd
from common import owid, INTER

MAXGAP = 10


def crossing(s, thr):
    s = s.sort_index()
    above = s[s >= thr]
    if above.empty:
        return np.nan, "never"
    y1 = above.index[0]
    prev = s[s.index < y1]
    if prev.empty:
        return np.nan, "already"
    y0, v0, v1 = prev.index[-1], prev.iloc[-1], s[y1]
    if y1 - y0 > MAXGAP:
        return np.nan, "gap"
    return y0 + (thr - v0) / (v1 - v0) * (y1 - y0), "ok"


def q4_table():
    df = owid()
    df = df[df.Code.notna() & ~df.Code.fillna("").str.startswith("OWID")]
    rows = []
    for c, g in df.groupby("Entity"):
        s = g.set_index("Year")["le"]
        y50, st50 = crossing(s, 50)
        y70, st70 = crossing(s, 70)
        rows.append(dict(country=c, y50=y50, st50=st50, y70=y70, st70=st70,
                         first_year=s.index.min(), le2023=s.get(2023, np.nan)))
    t = pd.DataFrame(rows)
    t = t[t.st50 == "ok"].copy()
    t["status"] = np.where(t.st70 == "ok", "reached", np.where(t.st70 == "never", "not yet", "drop"))
    t = t[t.status != "drop"]
    t["years"] = np.where(t.status == "reached", t.y70 - t.y50, 2023 - t.y50)
    return t


if __name__ == "__main__":
    t = q4_table()
    t.to_csv(INTER / "q4_50_to_70.csv", index=False)
    print(t.status.value_counts())
    t["era"] = pd.cut(t.y50, [1800, 1920, 1950, 1970, 2030], labels=["<1920", "1920-49", "1950-69", "1970+"])
    print(t[t.status == "reached"].groupby("era", observed=True).years.describe())
    print(t[t.status == "not yet"].sort_values("y50")[["country", "y50", "years", "le2023"]].round(1).to_string())
