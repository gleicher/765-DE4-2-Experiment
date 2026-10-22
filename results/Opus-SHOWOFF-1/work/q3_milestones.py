"""Q3 prep: year each country first reached life expectancy 50 and 70 (OWID long-run data)."""
from common import *
MAXGAP = 10   # only trust a crossing if the bracketing observations are <= 10 years apart

def crossing(g, th):
    """Linear-interpolated first year g.lex reaches th. NaN if never; 'left' if already above at first obs; 'gap' if bracket too wide."""
    above = np.where(g.lex.values >= th)[0]
    if len(above) == 0: return np.nan, "never"
    i = above[0]
    if i == 0: return np.nan, "left"
    y0, y1 = g.year.values[i-1], g.year.values[i]; v0, v1 = g.lex.values[i-1], g.lex.values[i]
    if y1 - y0 > MAXGAP: return np.nan, "gap"
    return y0 + (th - v0) / (v1 - v0) * (y1 - y0), "ok"

def milestones():
    o = load_owid()
    o = o[o.code.notna() & ~o.code.astype(str).str.startswith("OWID")].sort_values(["ent", "year"])
    rows = []
    for e, g in o.groupby("ent"):
        c50, s50 = crossing(g, 50); c70, s70 = crossing(g, 70)
        rows.append(dict(ent=e, c50=c50, s50=s50, c70=c70, s70=s70, le2023=g[g.year == 2023].lex.max(),
                         first=g.year.min()))
    d = pd.DataFrame(rows)
    d = d[d.s50 == "ok"].copy()
    d["done"] = d.s70 == "ok"
    d["cens"] = d.s70 == "never"
    d["years"] = np.where(d.done, d.c70 - d.c50, 2023 - d.c50)
    d = d[d.done | d.cens]
    return d

if __name__ == "__main__":
    d = milestones(); d.to_csv(INTER / "q3_milestones.csv", index=False)
    print(len(d), d.done.sum(), d.cens.sum())
    d["era"] = pd.cut(d.c50, [1800, 1900, 1930, 1950, 1960, 1970, 2000])
    print(d.groupby("era", observed=True).agg(n=("ent", "size"), done=("done", "sum"), med=("years", "median")))
    print(d.sort_values("c50")[["ent", "c50", "c70", "years", "done"]].round(1).to_string())
