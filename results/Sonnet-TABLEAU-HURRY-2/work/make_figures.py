"""Build the six figures for DE4-2 (Tableau-style worksheets drawn with matplotlib).

Run:  /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py   (from the run folder)
Writes PNGs to answers/figures/ and prints the statistics quoted in answers/answer.md.
"""
import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "answers", "figures")
os.makedirs(OUT, exist_ok=True)

# ---- Tableau-like look -------------------------------------------------
BLUE, ORANGE, RED, TEAL, GREEN, YELLOW, PURPLE, PINK, BROWN, GRAY = (
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC")
TXT = "#4a4a4a"
LIGHT = "#e4e4e4"
plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11, "text.color": TXT, "axes.labelcolor": TXT,
    "xtick.color": "#6b6b6b", "ytick.color": "#6b6b6b",
    "axes.edgecolor": "#b5b5b5", "axes.linewidth": 0.8,
    "xtick.major.size": 3, "ytick.major.size": 0,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "savefig.dpi": 150,
})


def style(ax, grid="y"):
    ax.set_axisbelow(True)
    if grid in ("y", "both"):
        ax.yaxis.grid(True, color=LIGHT, lw=0.8)
    if grid in ("x", "both"):
        ax.xaxis.grid(True, color=LIGHT, lw=0.8)
    ax.spines["left"].set_visible(False)


def title(fig, text, y=0.965):
    fig.text(0.03, y, text, fontsize=16.5, color="#3a3a3a", ha="left", va="top")


def caption(fig, text, width, y=0.035):
    fig.text(0.03, y, textwrap.fill(text, width), fontsize=10, color="#6b6b6b",
             ha="left", va="bottom", linespacing=1.4)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


# ======================================================================
# Life expectancy (World Bank file, countries only)
# ======================================================================
lf = pd.read_csv(os.path.join(DATA, "lifespan_dataset_1960.csv")).rename(
    columns={"Life Expectancy (years)": "LE", "Country Name": "country",
             "Country Code": "code"})
owid = pd.read_csv(os.path.join(DATA, "life-expectancy-owid", "life-expectancy-owid.csv"))
# keep real countries: codes that are not OWID aggregates in the OWID file
lf = lf[lf.code.isin(set(owid.Code.dropna()))]
wide = lf.pivot_table(index=["country", "Year"], columns="Sex", values="LE").reset_index()
wide["gap"] = wide.Female - wide.Male           # calculated field
g = wide.pivot(index="country", columns="Year", values="gap")

# ---------------- Figure 1: scatter 1960 gap vs 2023 gap ----------------
d = g[[1960, 2023]].dropna().rename(columns={1960: "g60", 2023: "g23"})
d["wider"] = d.g23 > d.g60
n, nw = len(d), int(d.wider.sum())
print(f"Fig1: {n} countries with both years; gap wider in 2023: {nw} ({nw/n:.0%})")
print("median gap 1960 %.2f, 2023 %.2f" % (d.g60.median(), d.g23.median()))

fig, ax = plt.subplots(figsize=(10.5, 8.6))
fig.subplots_adjust(left=0.085, right=0.80, top=0.90, bottom=0.21)
style(ax, "both")
lo, hi = -5, 15
ax.plot([lo, hi], [lo, hi], color="#8a8a8a", lw=1.2, ls=(0, (5, 3)), zorder=1)
ax.text(14.8, 10.9, "Dashed line: no change\n(2023 gap = 1960 gap)", fontsize=9, color="#6b6b6b",
        ha="right", va="top")
for flag, col, lab in [(True, BLUE, "Wider in 2023"), (False, ORANGE, "Narrower in 2023")]:
    s = d[d.wider == flag]
    ax.scatter(s.g60, s.g23, s=46, color=col, alpha=0.75, edgecolor="white", lw=0.6,
               label=lab, zorder=3)
labels = {"Ukraine": (7, 3, "left"), "Russian Federation": (7, 4, "left"), "Latvia": (-7, 3, "right"),
          "Pakistan": (7, 4, "left"), "Thailand": (-7, 0, "right"), "Nigeria": (7, -9, "left"),
          "Cameroon": (0, -14, "center"), "Isle of Man": (4, -13, "center"), "United Arab Emirates": (8, -10, "left"),
          "United States": (-6, 7, "right"), "Japan": (-7, 6, "right"), "India": (7, -9, "left"),
          "Viet Nam": (7, 4, "left"), "Mongolia": (-7, 3, "right"), "Palau": (-4, 8, "center")}
for k, (dx, dy, ha) in labels.items():
    r = d.loc[k]
    ax.annotate(k, (r.g60, r.g23), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color=TXT, ha=ha)
ax.set_xlim(lo, hi); ax.set_ylim(-0.5, 15)
ax.set_xlabel("Female minus male life expectancy in 1960 (years)", fontsize=11)
ax.set_ylabel("Female minus male life expectancy in 2023 (years)", fontsize=11)
ax.axvline(0, color="#d0d0d0", lw=0.8, zorder=0)
leg = ax.legend(title="Gap in 2023 vs. 1960", loc="upper left", bbox_to_anchor=(1.02, 1.0),
                frameon=False, labelspacing=0.9, title_fontsize=11, fontsize=10.5, handletextpad=0.3)
leg._legend_box.align = "left"
title(fig, "Women's life-expectancy advantage grew in about two-thirds of countries, 1960 to 2023")
caption(fig, f"Each dot is one country ({n} countries with data in both years). A dot above the dashed "
        f"line means women's advantage over men (female minus male life expectancy at birth) is "
        f"larger in 2023 than in 1960; {nw} countries ({nw/n:.0%}) are above the line. The biggest "
        f"increases are in Eastern Europe and Central Asia (Ukraine, Russia, Latvia) and Pakistan; "
        f"the gap shrank in places such as Cameroon, Nigeria and the Gulf states. Source: World Bank.",
        150)
save(fig, "q1_a_gap_scatter.png")

# ---------------- Figure 2: gap over time, selected countries ------------
sel = [("Russian Federation", RED), ("Ukraine", ORANGE), ("Japan", PURPLE),
       ("United States", BLUE), ("India", GREEN), ("Nigeria", BROWN)]
med = g.median()
years = g.columns.values
fig, ax = plt.subplots(figsize=(11.5, 7.6))
fig.subplots_adjust(left=0.07, right=0.84, top=0.91, bottom=0.2)
style(ax, "y")
ax.axhline(0, color="#9a9a9a", lw=1)
ax.plot(years, med.values, color="#8c8c8c", lw=4.5, alpha=0.55, solid_capstyle="round", zorder=2)
ax.annotate(f"Median of all\ncountries ({med[2023]:.1f})", (2023, med[2023]), xytext=(2023.8, 4.45),
            textcoords="data", fontsize=9.5, color="#6b6b6b", va="center")
ends = {}
for name, col in sel:
    ax.plot(years, g.loc[name].values, color=col, lw=2, zorder=3)
    ends[name] = g.loc[name, 2023]
# nudge end labels apart
ylab = dict(ends); ylab["Nigeria"] = ends["Nigeria"] - 0.35; ylab["India"] = ends["India"] + 0.0
ylab["United States"] = 5.5; ylab["Japan"] = 6.5
ylab["Russian Federation"] = ends["Russian Federation"] - 0.5
for name, col in sel:
    ax.annotate(f"{name} ({ends[name]:.1f})", (2023, ends[name]), xytext=(2023.8, ylab[name]),
                textcoords="data", fontsize=9.5, color=col, va="center", fontweight="bold")
# reference annotations
ax.annotate("Russia 1994: %.1f" % g.loc["Russian Federation", 1994], (1994, g.loc["Russian Federation", 1994]),
            xytext=(1976, 14.9), fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
ax.text(1960.5, 0.25, "Men live longer than women", fontsize=8.5, color="#8a8a8a", va="bottom")
ax.set_xlim(1960, 2023); ax.set_ylim(-3, 16)
ax.set_xticks(range(1960, 2021, 10)); ax.set_xticks([2023], minor=True)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Female minus male life expectancy (years)", fontsize=11)
title(fig, "Women's life-expectancy advantage has widened overall, but countries diverge")
caption(fig, "Gap = female life expectancy at birth minus male life expectancy at birth. The thick gray line is the "
        f"median across all countries, which rose from {med[1960]:.1f} years in 1960 to about 5.3 around 1990 and {med[2023]:.1f} in 2023. "
        "Six countries are highlighted: the gap in Russia and Ukraine grew to 10 to 13 years, in the United States it rose "
        "then fell back, in India it moved from negative (men lived longer) to positive, and in Nigeria it nearly "
        "disappeared. Source: World Bank.", 165)
save(fig, "q1_b_gap_lines.png")
print("Fig2 medians:", round(med[1960], 2), round(med[1980], 2), round(med[2000], 2), round(med[2023], 2))
for name, _ in sel:
    print("  ", name, round(g.loc[name, 1960], 1), round(g.loc[name, 1990], 1), round(g.loc[name, 2023], 1),
          "max", round(g.loc[name].max(), 1), int(g.loc[name].idxmax()))

# ======================================================================
# Census
# ======================================================================
cen = pd.read_csv(os.path.join(DATA, "full_census_dataset.csv"), dtype={"FIPS Code": str},
                  encoding="latin-1")   # NOTE: despite the README this file is comma separated
cen["R"] = cen["2023 Rural-urban Continuum Code"]
yrs = list(range(2015, 2024))
need = [f"Unemployed {y}" for y in yrs] + [f"Civilian labor force {y}" for y in yrs] + ["R"]
cu = cen.dropna(subset=need).copy()
print(f"\nUnemployment counties used: {len(cu)} of {len(cen)}")
cu["grp"] = pd.cut(cu.R, [0, 3, 7, 9], labels=["Metro (codes 1-3)", "Smaller nonmetro (codes 4-7)",
                                               "Most rural nonmetro (codes 8-9)"])


def rate(df, by):
    out = {}
    for k, gp in df.groupby(by, observed=True):
        out[k] = [gp[f"Unemployed {y}"].sum() / gp[f"Civilian labor force {y}"].sum() * 100 for y in yrs]
    return pd.DataFrame(out, index=yrs).T


rg = rate(cu, "grp"); rc = rate(cu, "R")
print(rg.round(2)); print(rc.round(2))
print("rise 2019->2020 by group:", (rg[2020] - rg[2019]).round(2).to_dict())
print("rise by code:", (rc[2020] - rc[2019]).round(2).to_dict())
print("2023 vs 2019 by code:", (rc[2023] - rc[2019]).round(2).to_dict())
print(cu.groupby("grp", observed=True)["Civilian labor force 2019"].sum())

# ---------------- Figure 3: lines by group ------------------------------
cols = {"Metro (codes 1-3)": BLUE, "Smaller nonmetro (codes 4-7)": ORANGE,
        "Most rural nonmetro (codes 8-9)": GREEN}
fig, ax = plt.subplots(figsize=(10.5, 7.2))
fig.subplots_adjust(left=0.08, right=0.70, top=0.90, bottom=0.24)
style(ax, "y")
for k, col in cols.items():
    ax.plot(yrs, rg.loc[k].values, color=col, lw=2.4, marker="o", ms=5, label=k)
    ax.annotate(f"{rg.loc[k, 2020]:.1f}%", (2020, rg.loc[k, 2020]),
                xytext=(12, 0), textcoords="offset points", fontsize=9.5, color=col, va="center",
                bbox=dict(fc="white", ec="none", pad=1))
ax.axvline(2020, color="#9a9a9a", lw=1, ls=(0, (4, 3)))
ax.text(2019.9, 0.3, "2020", fontsize=9, color="#7a7a7a", ha="right")
ax.set_ylim(0, 9.5); ax.set_xlim(2014.7, 2023.3)
ax.set_xticks(yrs)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.0f}%"))
ax.set_xlabel("Year", fontsize=11); ax.set_ylabel("Unemployment rate", fontsize=11)
leg = ax.legend(title="Rural-urban Continuum\nCode group (2023)", loc="upper left",
                bbox_to_anchor=(1.02, 1.0), frameon=False, labelspacing=0.9, fontsize=10.5,
                title_fontsize=11)
leg._legend_box.align = "left"
title(fig, "The 2020 unemployment spike was sharpest in metro counties")
caption(fig, "Unemployment rate = total unemployed / total civilian labor force, summed over counties in each group "
        f"(Rural-urban Continuum Code 2023; {len(cu):,} counties with complete 2015-2023 data). All groups jumped in 2020 and "
        f"returned to about 3.6% by 2022, but metro counties went from {rg.iloc[0][2019]:.1f}% to {rg.iloc[0][2020]:.1f}% "
        f"(+{rg.iloc[0][2020]-rg.iloc[0][2019]:.1f} points), versus +{rg.iloc[2][2020]-rg.iloc[2][2019]:.1f} points in the most rural counties.",
        130)
save(fig, "q2_a_unemployment_lines.png")

# ---------------- Figure 4: bars of 2019->2020 change by code ------------
rise = (rc[2020] - rc[2019])
codes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
cl = {1: "Metro, 1 million+", 2: "Metro, 250k-1M", 3: "Metro, under 250k",
      4: "Nonmetro", 5: "Nonmetro", 6: "Nonmetro", 7: "Nonmetro", 8: "Nonmetro", 9: "Nonmetro"}
fig, ax = plt.subplots(figsize=(10.5, 7.2))
fig.subplots_adjust(left=0.23, right=0.70, top=0.90, bottom=0.24)
style(ax, "x")
grpcol = {c: (BLUE if c <= 3 else ORANGE if c <= 7 else GREEN) for c in codes}
ypos = np.arange(len(codes))[::-1]
ax.barh(ypos, [rise[c] for c in codes], color=[grpcol[c] for c in codes], height=0.68, zorder=3)
for y, c in zip(ypos, codes):
    ax.text(rise[c] + 0.06, y, f"+{rise[c]:.1f}", va="center", fontsize=10, color=TXT)
ax.set_yticks(ypos); ax.set_yticklabels([f"{c}  {cl[c]}" for c in codes], fontsize=10)
ax.set_xlim(0, 6)
ax.set_xlabel("Change in unemployment rate, 2019 to 2020 (percentage points)", fontsize=11)
ax.set_ylabel("Rural-urban Continuum Code (2023)", fontsize=11)
ax.spines["bottom"].set_visible(True)
from matplotlib.patches import Patch
leg = ax.legend(handles=[Patch(color=BLUE, label="Metro (1-3)"), Patch(color=ORANGE, label="Smaller nonmetro (4-7)"),
                         Patch(color=GREEN, label="Most rural nonmetro (8-9)")],
                title="Code group", loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
                labelspacing=0.9, fontsize=10.5, title_fontsize=11)
leg._legend_box.align = "left"
title(fig, "The more urban the county, the bigger the 2020 jump in unemployment")
caption(fig, "Each bar is the 2020 unemployment rate minus the 2019 rate for all counties with that Rural-urban Continuum "
        f"Code (rate = total unemployed / total civilian labor force). The increase falls, with small exceptions among codes 3-5, from +{rise[1]:.1f} points "
        f"in the largest metro counties to +{rise[9]:.1f} in code 9. Codes 1-3 are metro counties (by metro-area population); "
        "higher codes among 4-9 are less urban.", 135)
save(fig, "q2_b_unemployment_bars.png")

# ---------------- Figure 5: migration by state ---------------------------
mig = [f"Domestic migration {y}" for y in range(2020, 2024)]
sm = cen[~cen.State.isin(["PR", "CT"])].dropna(subset=mig + ["Census Population 2020"]).copy()
st = sm.groupby("State").agg(mig=("Domestic migration 2020", "sum"), m21=("Domestic migration 2021", "sum"),
                             m22=("Domestic migration 2022", "sum"), m23=("Domestic migration 2023", "sum"),
                             pop=("Census Population 2020", "sum"))
st["net"] = st[["mig", "m21", "m22", "m23"]].sum(axis=1)
st["per1000"] = st.net / st["pop"] * 1000
print("\nStates:", len(st)); print(st.sort_values("per1000")[["net", "pop", "per1000"]].round(1).to_string())
top = st.sort_values("per1000", ascending=False)
sel5 = pd.concat([top.head(10), top.tail(10)])
fig, ax = plt.subplots(figsize=(10.5, 8.3))
fig.subplots_adjust(left=0.1, right=0.76, top=0.91, bottom=0.2)
style(ax, "x")
ypos = np.arange(len(sel5))[::-1]
colr = [BLUE if v > 0 else ORANGE for v in sel5.per1000]
ax.barh(ypos, sel5.per1000, color=colr, height=0.7, zorder=3)
for y, (s, r) in zip(ypos, sel5.iterrows()):
    ax.text(r.per1000 + (0.8 if r.per1000 > 0 else -0.8), y, f"{r.per1000:+.0f}", va="center",
            ha="left" if r.per1000 > 0 else "right", fontsize=9.5, color=TXT)
ax.set_yticks(ypos); ax.set_yticklabels(sel5.index, fontsize=10)
ax.axvline(0, color="#7a7a7a", lw=1)
ax.axvline(0, color="#7a7a7a", lw=1)
ax.set_xlim(-60, 85)
ax.set_xlabel("Net domestic migration 2020-2023 per 1,000 residents (2020 census population)", fontsize=11)
ax.set_ylabel("State", fontsize=11)
ax.spines["bottom"].set_visible(True)
leg = ax.legend(handles=[Patch(color=BLUE, label="More people moved in"), Patch(color=ORANGE, label="More people moved out")],
                title="Net domestic migration", loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
                labelspacing=0.9, fontsize=10.5, title_fontsize=11)
leg._legend_box.align = "left"
title(fig, "Idaho gained the most residents from other states per capita; New York lost the most")
caption(fig, "Net domestic migration (people moving in from elsewhere in the US minus people moving out), summed over 2020-2023 "
        "and divided by each state's 2020 census population. Shown: the 10 states with the largest gains and the 10 with the "
        "largest losses (of 49 states and DC; Puerto Rico and Connecticut excluded because their county-equivalents changed). Computed from county estimates.", 140)
save(fig, "q3_state_migration.png")

# ---------------- Figure 6: education vs income scatter ------------------
ed = "Percent of adults with a bachelor's degree or higher, 2019-23"
sc = cen.dropna(subset=[ed, "Median Household Income 2023", "R", "Census Population 2020"]).copy()
sc = sc[sc[ed] > 0]   # one county reports 0% (treated as missing)
sc["metro"] = np.where(sc.R <= 3, "Metro", "Nonmetro")
print("\nScatter counties:", len(sc), sc.metro.value_counts().to_dict())
print("corr all %.2f" % sc[ed].corr(sc["Median Household Income 2023"]))
fig, ax = plt.subplots(figsize=(10.5, 7.8))
fig.subplots_adjust(left=0.09, right=0.76, top=0.89, bottom=0.26)
style(ax, "both")
slopes = {}
for k, col in [("Nonmetro", ORANGE), ("Metro", BLUE)]:
    s = sc[sc.metro == k]
    ax.scatter(s[ed], s["Median Household Income 2023"], s=8 + s["Census Population 2020"] / 15000,
               color=col, alpha=0.4, edgecolor="none", zorder=3)
    m, b = np.polyfit(s[ed], s["Median Household Income 2023"], 1)
    xs = np.array([s[ed].min(), s[ed].max()])
    ax.plot(xs, m * xs + b, color=col, lw=2.2, zorder=4)
    slopes[k] = m
    r = s[ed].corr(s["Median Household Income 2023"])
    print(f"{k}: n={len(s)} slope ${m:,.0f} per pct pt, r={r:.2f}, R2={r*r:.2f}")
ax.set_xlabel("Adults with a bachelor's degree or higher, 2019-23 (%)", fontsize=11)
ax.set_ylabel("Median household income, 2023", fontsize=11)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v/1000:.0f}K"))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.0f}%"))
ax.set_xlim(0, 85); ax.set_ylim(20000, 160000)
from matplotlib.lines import Line2D
leg = ax.legend(handles=[Line2D([], [], marker="o", ls="", color=c, ms=8, alpha=0.85, label=k)
                         for k, c in [("Nonmetro", ORANGE), ("Metro", BLUE)]],
                title="County type\n(Continuum Code 2023)", loc="upper left", bbox_to_anchor=(1.02, 1.0),
                frameon=False, labelspacing=0.9, fontsize=10.5, title_fontsize=11)
leg._legend_box.align = "left"
ax.text(1.02, 0.66, "Dot size = 2020\npopulation\nLines = linear\ntrend per type", transform=ax.transAxes,
        fontsize=9.5, color="#6b6b6b", va="top")
title(fig, "Counties with more college graduates have higher incomes, in metro and nonmetro areas alike")
caption(fig, f"Each dot is one county ({len(sc):,} counties with both measures); metro = Rural-urban Continuum Codes 1-3, "
        "nonmetro = 4-9. Trend lines are least-squares fits for each type: each extra point of college graduates goes with about "
        f"${slopes['Metro']:,.0f} higher median income in metro counties and ${slopes['Nonmetro']:,.0f} in nonmetro counties, so the "
        "relationship is steeper in metro areas. This is correlation only; one county reporting 0% was dropped.", 135)
save(fig, "q4_education_income.png")
