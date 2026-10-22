"""Generate all figures for DE4-2. Run: /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py  (from the project root)"""
import os, textwrap
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data"); OUT = os.path.join(ROOT, "answers", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold"})
INK, GRAY = "#222222", "#8a8a8a"
BLUE, ORANGE, RED, TEAL = "#2b6cb0", "#d95f02", "#b2182b", "#1b9e77"

def finish(fig, name, title, subtitle, caption, bottom=0.12):
    w = fig.get_figwidth()
    t = "\n".join(textwrap.wrap(title, int(w * 5.4)))
    fig.text(0.02, 0.985, t, ha="left", va="top", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.02, 0.985 - 0.043 * (t.count("\n") + 1) * 8 / fig.get_figheight() - 0.01,
             "\n".join(textwrap.wrap(subtitle, int(w * 10))), ha="left", va="top", fontsize=11.5, color="#444")
    fig.text(0.02, 0.012, "\n".join(textwrap.wrap(caption, 150)), ha="left", va="bottom", fontsize=9.5, color="#444")
    fig.savefig(os.path.join(OUT, name), dpi=150, facecolor="white")
    plt.close(fig)

# ---------------- data ----------------
wb = pd.read_csv(f"{D}/lifespan_dataset_1960.csv", index_col=0)
owid = pd.read_csv(f"{D}/life-expectancy-owid/life-expectancy-owid.csv")
owid.columns = ["Entity", "Code", "Year", "LE"]
# real countries = OWID rows with an ISO code (drops regions/income aggregates in both files)
countries = set(owid.Code.dropna()) - {c for c in owid.Code.dropna() if c.startswith("OWID")}
wb = wb[wb["Country Code"].isin(countries)]
p = wb.pivot_table(index=["Country Name", "Country Code"], columns=["Sex", "Year"], values="Life Expectancy (years)")
gap = (p["Female"] - p["Male"]).droplevel("Country Code")           # countries x years
gap_world = (wb.pivot_table(index="Year", columns="Sex", values="Life Expectancy (years)")) # placeholder (unused)

# ---------------- Fig 1A: scatter 1960 vs 2023 gap ----------------
g = gap[[1960, 2023]].dropna()
d = g[2023] - g[1960]
col = np.where(d > 1, ORANGE, np.where(d < -1, BLUE, GRAY))
fig, ax = plt.subplots(figsize=(11, 8.6)); fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.17)
ax.plot([-5, 14], [-5, 14], color=INK, lw=1, ls="--", zorder=1)
ax.scatter(g[1960], g[2023], c=col, s=38, alpha=.85, edgecolor="white", lw=.5, zorder=3)
ax.set_xlim(-5, 13.5); ax.set_ylim(-0.5, 14.5)
ax.set_xlabel("Female minus male life expectancy in 1960 (years)"); ax.set_ylabel("Female minus male life expectancy in 2023 (years)")
ax.grid(color="#e6e6e6", zorder=0)
ax.text(-4.6, 13.6, "Gap WIDER than in 1960", color=ORANGE, fontweight="bold", va="top")
ax.text(13.3, -0.2, "Gap NARROWER than in 1960", color=BLUE, fontweight="bold", ha="right")
ax.text(6.2, 6.9, "no change", rotation=38, color=INK, fontsize=9, ha="center")
lab = {"Ukraine": (6, 13.4, "left"), "Russian Federation": (8.6, 11.6, "left"), "Latvia": (6.1, 10.3, "left"), "Georgia": (9.6, 8.0, "left"),
       "El Salvador": (2.2, 8.9, "right"), "Thailand": (0.9, 8.5, "right"), "Viet Nam": (6.2, 9.0, "left"), "India": (-1.4, 3.0, "right"),
       "China": (2.7, 5.9, "left"), "United States": (6.6, 5.0, "left"), "Japan": (5.0, 6.3, "left"), "Togo": (3.1, 0.4, "left"),
       "Nigeria": (4.2, 0.6, "left"), "Kuwait": (3.9, 1.0, "left"), "United Arab Emirates": (6.6, 2.2, "left"), "Niger": (0.9, 1.9, "left"),
       "Mongolia": (1.5, 9.3, "right")}
for n, (tx, ty, ha) in lab.items():
    if n in g.index:
        x, y = g.loc[n, 1960], g.loc[n, 2023]
        ax.annotate(n, (x, y), (tx, ty), fontsize=9, ha=ha, va="center", color=INK,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=.7, shrinkA=0, shrinkB=2))
nw, nn, ns = (d > 1).sum(), (d < -1).sum(), (d.abs() <= 1).sum()
finish(fig, "fig1a_gap_scatter.png", "The female longevity edge grew most in the former USSR, and shrank in rich and oil-rich countries",
       f"Each dot is one of {len(g)} countries. Distance above the dashed line = how much the female-male gap changed from 1960 to 2023.",
       f"Gap = female minus male life expectancy at birth (years). Orange: gap grew by more than 1 year ({nw} countries); blue: shrank by more than 1 year ({nn}); gray: within 1 year ({ns}). "
       "Countries only (World Bank regional aggregates removed). Source: World Bank life expectancy by sex, 1960-2023. India's women lived 1.4 years LESS than men in 1960.")

# ---------------- Fig 1B: gap over time ----------------
fig, ax = plt.subplots(figsize=(12, 8)); fig.subplots_adjust(left=0.07, right=0.84, top=0.80, bottom=0.17)
yrs = gap.columns
for n, r in gap.iterrows(): ax.plot(yrs, r.values, color="#c9c9c9", lw=.7, zorder=1)
med = gap.median(); ax.plot(yrs, med.values, color=INK, lw=3, zorder=4)
hl = {"Ukraine": RED, "Russian Federation": "#e7298a", "United States": BLUE, "Japan": TEAL, "India": ORANGE, "Togo": "#7570b3"}
nm = {"Russian Federation": "Russia"}
for n, c in hl.items():
    s = gap.loc[n].dropna(); ax.plot(s.index, s.values, color=c, lw=2.4, zorder=3)
off = {"Ukraine": 0.15, "Russian Federation": -0.25, "Japan": 0.15, "United States": 0.3, "India": 0, "Togo": 0}
for n, c in hl.items():
    s = gap.loc[n].dropna(); ax.text(2024, s.iloc[-1] + off[n], f"{nm.get(n, n)}  {s.iloc[-1]:.1f}", color=c, fontweight="bold", va="center", fontsize=10.5)
ax.text(2024, med.iloc[-1] - 0.35, f"Median country  {med.iloc[-1]:.1f}", color=INK, fontweight="bold", va="center", fontsize=10.5)
ax.axhline(0, color=INK, lw=.8); ax.set_xlim(1960, 2023); ax.set_ylim(-4.5, 15)
ax.set_ylabel("Female minus male life expectancy (years)"); ax.grid(axis="y", color="#e6e6e6", zorder=0)
ax.text(1961, -0.45, "men live longer than women", fontsize=9, va="top", color=GRAY)
finish(fig, "fig1b_gap_lines.png", "Women outlive men almost everywhere, but the size of the gap has moved in very different directions",
       "Gray: every country (n=%d). Black: median country. Colors: selected countries with contrasting trajectories." % len(gap),
       "Female minus male life expectancy at birth, 1960-2023. The typical gap rose from about 4 years (1960) to about 5 years (1990s) and has since been flat; the former Soviet states diverge upward "
       "(Ukraine 13.3 years in 2023, partly reflecting wartime male mortality in recent estimates) while the US gap fell from 7.0 (1990) to 5.3. Source: World Bank; countries only (regional aggregates removed).")

# ---------------- census ----------------
c = pd.read_csv(f"{D}/full_census_dataset.csv", dtype={"FIPS Code": str}, encoding="latin-1")
R = "2023 Rural-urban Continuum Code"
c = c[c[R].notna()].copy()                       # keeps counties only (state/US rows have no code)
c["grp"] = np.where(c[R] <= 3, "Metro (codes 1-3)", np.where(c[R].isin([4, 6, 8]), "Nonmetro, next to a metro (4, 6, 8)", "Nonmetro, remote (5, 7, 9)"))
GC = {"Metro (codes 1-3)": BLUE, "Nonmetro, next to a metro (4, 6, 8)": ORANGE, "Nonmetro, remote (5, 7, 9)": TEAL}
RL = {1: "Metro, 1M+ people", 2: "Metro, 250k-1M", 3: "Metro, <250k", 4: "Urban 20k+, next to metro", 5: "Urban 20k+, remote",
      6: "Urban 5-20k, next to metro", 7: "Urban 5-20k, remote", 8: "Rural, next to metro", 9: "Rural, remote"}
pc = lambda s: f"Percent of adults {s}"
ed_cols = [("1970", "Percent of adults completing four years of college or higher, 1970"), ("1980", "Percent of adults completing four years of college or higher, 1980"),
           ("1990", "Percent of adults with a bachelor's degree or higher, 1990"), ("2000", "Percent of adults with a bachelor's degree or higher, 2000"),
           ("2008-12", "Percent of adults with a bachelor's degree or higher, 2008-12"), ("2019-23", "Percent of adults with a bachelor's degree or higher, 2019-23")]
med_ed = c.groupby(R)[[v for _, v in ed_cols]].median(); med_ed.columns = [k for k, _ in ed_cols]

# ---------------- Fig 2A: education lines by RUCC ----------------
fig, ax = plt.subplots(figsize=(12, 8.2)); fig.subplots_adjust(left=0.07, right=0.70, top=0.80, bottom=0.17)
cmap = plt.cm.viridis(np.linspace(0.05, 0.85, 9))
xs = np.arange(len(ed_cols))
ends = {}
for i, code in enumerate(range(1, 10)):
    y = med_ed.loc[code].values; ax.plot(xs, y, color=cmap[i], lw=2.6, marker="o", ms=5)
    ends[code] = y[-1]
# de-overlap end labels
order = sorted(ends, key=ends.get); pos = {}; last = -99
for k in order:
    pos[k] = max(ends[k], last + 1.7); last = pos[k]
for k in range(1, 10):
    ax.annotate(f"{k}  {RL[k]}  ({med_ed.loc[k].iloc[-1]:.0f}%)", (xs[-1], ends[k]), (xs[-1] + 0.12, pos[k]), color=cmap[k - 1], fontsize=10, va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=cmap[k - 1], lw=.6), annotation_clip=False)
ax.set_xticks(xs); ax.set_xticklabels([k for k, _ in ed_cols]); ax.set_xlim(-.1, len(xs) - 1 + .05)
ax.set_ylim(0, 34); ax.set_ylabel("Median county: % of adults with 4+ years of college"); ax.grid(axis="y", color="#e6e6e6")
ax.set_xlabel("Census period")
ax.text(-.05, 33, "Rural-Urban Continuum Code (2023) and county type", fontsize=9.5, color="#444", va="top", ha="left", transform=ax.transData, alpha=0)
finish(fig, "fig2a_education_lines.png", "Every kind of county got more educated, but the college gap between big metros and rural counties has widened",
       "Median share of adults with a four-year degree, by county type, 1970 to 2019-23. Color runs from big metro (purple) to remote rural (yellow).",
       f"Each line is the median of the counties in one USDA Rural-Urban Continuum Code (2023 codes; n={len(c)} counties). 1970-80 values are 'four years of college or higher'; 1990 onward 'bachelor's degree or higher'. "
       f"Since 1990 the median big-metro county gained {med_ed.loc[1].iloc[-1]-med_ed.loc[1,'1990']:.0f} points, versus {med_ed.loc[9].iloc[-1]-med_ed.loc[9,'1990']:.0f} in remote rural counties. Source: USDA ERS county data.")

# ---------------- Fig 2B: county scatter 1990 vs 2019-23 ----------------
a, b = ed_cols[2][1], ed_cols[5][1]
s = c.dropna(subset=[a, b]); s = s[(s[a] > 0) & (s[b] > 0)]
fig, axs = plt.subplots(1, 1, figsize=(11, 8.6)); ax = axs; fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.17)
ax.plot([0, 80], [0, 80], color=INK, lw=1, ls="--"); ax.text(52, 49.5, "no change", rotation=40, fontsize=9, ha="center", color=INK)
for gname in ["Nonmetro, remote (5, 7, 9)", "Nonmetro, next to a metro (4, 6, 8)", "Metro (codes 1-3)"]:
    q = s[s.grp == gname]; ax.scatter(q[a], q[b], s=14, color=GC[gname], alpha=.4, edgecolor="none", label=gname)
ly = {"Metro (codes 1-3)": 24, "Nonmetro, next to a metro (4, 6, 8)": 14, "Nonmetro, remote (5, 7, 9)": 5}
meds = {}
for gname in GC:
    q = s[s.grp == gname]; mx, my = q[a].median(), q[b].median(); meds[gname] = (mx, my)
    ax.scatter([mx], [my], s=170, color=GC[gname], edgecolor=INK, lw=1.8, zorder=5)
    ax.annotate(f"{gname.split(' (')[0]} median:\n{mx:.0f}% -> {my:.0f}%  (+{my-mx:.0f} pts)", (mx, my), (36, ly[gname]),
                fontsize=10, fontweight="bold", color=GC[gname], va="center", arrowprops=dict(arrowstyle="-", color=GC[gname], lw=1.2))
ax.set_xlim(0, 57); ax.set_ylim(0, 80); ax.grid(color="#eee")
ax.set_xlabel("% of adults with a bachelor's degree or higher, 1990"); ax.set_ylabel("% of adults with a bachelor's degree or higher, 2019-23")
ax.legend(loc="upper left", frameon=False, title="County type (USDA 2023 code)", title_fontproperties={"weight": "bold"}, markerscale=2)
finish(fig, "fig2b_education_scatter.png", "Counties above the dashed line gained in college education; metro counties climbed highest",
       f"Each dot is one of {len(s):,} U.S. counties: where it started (1990, across) and where it ended up (2019-23, up). Large circles are group medians.",
       "Education share = adults 25+ with a bachelor's degree or higher, as reported in the USDA ERS county dataset (1990 Census and 2019-23 American Community Survey). Counties with missing or zero values removed. "
       "Nearly every county is above the diagonal; the metro cloud tilts higher and spreads further, so the median metro-versus-remote gap grew from %.0f to %.0f points." % (meds['Metro (codes 1-3)'][0]-meds['Nonmetro, remote (5, 7, 9)'][0], meds['Metro (codes 1-3)'][1]-meds['Nonmetro, remote (5, 7, 9)'][1]) + " Correlation only, no causal claim.")

# ---------------- Fig 3: COVID life expectancy ----------------
o = owid[owid.Code.isin(countries)].pivot(index="Entity", columns="Year", values="LE")
dd = pd.DataFrame({"d21": o[2021] - o[2019], "d23": o[2023] - o[2019]}).dropna()
top = dd.sort_values("d21").head(22)
if "United States" not in top.index: top = pd.concat([top, dd.loc[["United States"]]])
top = top.sort_values("d21", ascending=False)
fig, ax = plt.subplots(figsize=(11, 9.4)); fig.subplots_adjust(left=0.24, right=0.96, top=0.80, bottom=0.14)
yy = np.arange(len(top))
ax.axvline(0, color=INK, lw=1.2)
ax.hlines(yy, top.d21, top.d23, color="#bbb", lw=3, zorder=1)
ax.scatter(top.d21, yy, color=RED, s=75, zorder=3, label="2021 (pandemic low point)")
ax.scatter(top.d23, yy, color=BLUE, s=75, zorder=3, label="2023")
ax.set_yticks(yy); ax.set_yticklabels(top.index)
for t in ax.get_yticklabels():
    if t.get_text() == "United States": t.set_fontweight("bold")
for yv, (n, r) in zip(yy, top.iterrows()):
    ax.text(r.d21 - .25, yv, f"{r.d21:+.1f}", ha="right", va="center", fontsize=8.5, color=RED)
ax.set_xlim(-7.6, 4.5); ax.set_xlabel("Change in life expectancy at birth compared with 2019 (years)")
ax.grid(axis="x", color="#e6e6e6", zorder=0); ax.set_axisbelow(True)
ax.text(0.15, len(top) - .3, "2019 level", fontsize=9, color=INK, va="bottom")
ax.legend(loc="center right", frameon=False)
ax.set_ylim(-.7, len(top) - .1)
finish(fig, "fig3_covid_life_expectancy.png", "COVID-19 cut life expectancy by up to 6 years in some countries; by 2023 nearly all had recovered",
       "The 22 countries with the biggest 2019-2021 drops, plus the United States. Red: 2021 versus 2019. Blue: 2023 versus 2019. Sorted by size of drop.",
       "Period life expectancy at birth, both sexes, from Our World in Data (UN World Population Prospects 2024). Countries only; regional aggregates excluded. Only Lebanon and Mayotte of these were still "
       "below their 2019 level in 2023 (blue dot left of the line); the US dropped less than these 22 but is shown for reference. Estimates for some countries are modeled, not directly measured. Descriptive only.", bottom=.14)

# ---------------- Fig 4: unemployment by county type ----------------
yrs = list(range(2000, 2024)); W = {}
for gname, q in c.groupby("grp"):
    out = []
    for y in yrs:
        ok = q[f"Unemployment rate {y}"].notna()
        out.append((q.loc[ok, f"Unemployment rate {y}"] * q.loc[ok, f"Civilian labor force {y}"]).sum() / q.loc[ok, f"Civilian labor force {y}"].sum())
    W[gname] = pd.Series(out, index=yrs)
W = pd.DataFrame(W)
fig = plt.figure(figsize=(14, 8)); gs = fig.add_gridspec(1, 2, width_ratios=[2.5, 1], wspace=.22); fig.subplots_adjust(left=.06, right=.97, top=.78, bottom=.17)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1])
ax.axvspan(2007.9, 2010.1, color="#f0f0f0"); ax.axvspan(2019.5, 2021.5, color="#f0f0f0")
ax.text(2009, 12.3, "Great\nRecession", ha="center", fontsize=9.5, color="#555"); ax.text(2020.5, 12.3, "COVID-19", ha="center", fontsize=9.5, color="#555")
for gname in GC: ax.plot(yrs, W[gname], color=GC[gname], lw=2.8, label=gname)
ax.annotate(f"2009-10 peak:\nadjacent nonmetro {W.iloc[10, :].max():.1f}%", (2010, W.loc[2010, "Nonmetro, next to a metro (4, 6, 8)"]), (2012.3, 11.6), fontsize=9.5, color=ORANGE,
            arrowprops=dict(arrowstyle="-", color=ORANGE))
ax.annotate(f"2020: metro {W.loc[2020,'Metro (codes 1-3)']:.1f}%\nvs remote {W.loc[2020,'Nonmetro, remote (5, 7, 9)']:.1f}%", (2020, W.loc[2020, "Metro (codes 1-3)"]), (2015.3, 8.9), fontsize=9.5, color=BLUE,
            arrowprops=dict(arrowstyle="-", color=BLUE))
ax.set_ylim(0, 13); ax.set_xlim(2000, 2023); ax.set_ylabel("Unemployment rate (%), labor-force weighted"); ax.grid(axis="y", color="#e6e6e6")
ax.legend(loc="upper left", frameon=False, fontsize=9.5, bbox_to_anchor=(0, .88)); ax.set_title("Unemployment rate, 2000-2023", loc="left", fontsize=12)
# right panel: rise from pre-shock low to peak
shocks = {"Great Recession\n(2007 to 2010)": (2007, 2010), "COVID-19\n(2019 to 2020)": (2019, 2020)}
xw = np.arange(2); wdt = .26
for i, gname in enumerate(GC):
    vals = [W.loc[e, gname] - W.loc[s0, gname] for (s0, e) in shocks.values()]
    bars = ax2.bar(xw + (i - 1) * wdt, vals, wdt * .92, color=GC[gname])
    for xb, v in zip(xw + (i - 1) * wdt, vals): ax2.text(xb, v + .1, f"+{v:.1f}", ha="center", fontsize=9)
ax2.set_xticks(xw); ax2.set_xticklabels(list(shocks)); ax2.set_ylabel("Percentage-point rise in unemployment"); ax2.set_ylim(0, 6.2)
ax2.set_title("How hard each shock hit", loc="left", fontsize=12); ax2.grid(axis="y", color="#e6e6e6"); ax2.set_axisbelow(True)
finish(fig, "fig4_unemployment_shocks.png", "Metro counties took the biggest pandemic job shock; in 2009-10 unemployment peaked highest in counties next to metros",
       "Unemployment in three kinds of U.S. county. Left: the rate over time. Right: how far it rose in each shock.",
       f"Rates are county unemployment rates averaged with civilian labor force as weights, for {len(c):,} counties grouped by 2023 USDA Rural-Urban Continuum Code (metro 1-3; nonmetro adjacent to a metro 4, 6, 8; "
       "remote nonmetro 5, 7, 9). Rise = rate in the peak year minus the rate in the last pre-shock year. Source: USDA ERS / BLS LAUS county data. Descriptive, not causal.")
print("done")
