"""Build the six figures, styled after default Tableau worksheets (Tableau 10 palette, Arial)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os, textwrap
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, OUT = f"{ROOT}/data", f"{ROOT}/answers/figures"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": ["Arial", "Helvetica"], "font.size": 10, "axes.edgecolor": "#b0b0b0",
    "axes.labelcolor": "#444", "xtick.color": "#555", "ytick.color": "#555", "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.7,
    "axes.axisbelow": True, "figure.facecolor": "white"})
BLUE, ORANGE, RED, TEAL, GREEN, YELLOW, PURPLE, PINK, BROWN, GRAY = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
    "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac")

def frame(title, sub, caption, w, h):
    fig = plt.figure(figsize=(w, h), dpi=150)
    fig.text(0.02, 0.975, title, fontsize=13, fontweight="bold", color="#333", va="top", ha="left")
    fig.text(0.02, 0.975 - 0.055 * 7 / h * 1.0, sub, fontsize=10, color="#555", va="top", ha="left")
    fig.text(0.02, 0.012, caption, fontsize=8.5, color="#555", va="bottom", ha="left", linespacing=1.3)
    return fig

def wrap(s, n): return "\n".join(textwrap.wrap(s, n))

# ---------------- data ----------------
life = pd.read_csv(f"{D}/lifespan_dataset_1960.csv")
p = life.pivot_table(index=["Country Name", "Year"], columns="Sex", values="Life Expectancy (years)").reset_index()
p["Gap"] = p["Female"] - p["Male"]
cen = pd.read_csv(f"{D}/full_census_dataset.csv", encoding="latin-1")
agg = pd.read_csv(f"{D}/aggregate_census_dataset.csv", sep="\t", encoding="latin-1")
cen = cen[cen["State"].notna()].copy()
RU = "2023 Rural-urban Continuum Code"
def grp(c):
    if c <= 3: return "Metro (codes 1-3)"
    if c in (4, 6, 8): return "Nonmetro, adjacent to metro"
    return "Nonmetro, not adjacent"
cen["Group"] = cen[RU].map(lambda v: grp(v) if pd.notna(v) else np.nan)
GCOL = {"Metro (codes 1-3)": BLUE, "Nonmetro, adjacent to metro": ORANGE, "Nonmetro, not adjacent": RED}

# ---------------- Fig 1A: line chart of gap ----------------
sel = ["Russian Federation", "Ukraine", "Japan", "United States", "China", "India", "Bangladesh", "Nigeria"]
cols = [RED, ORANGE, BLUE, TEAL, GREEN, PURPLE, BROWN, GRAY]
fig = frame("Women outlive men almost everywhere, but the gap has moved in very different directions",
            "Female minus male life expectancy at birth (years), 1960-2023, selected countries",
            wrap("Source: World Bank life expectancy data (lifespan_dataset_1960). Gap = female life expectancy minus male life "
                 "expectancy. Selected countries are the extremes and a few large nations; below zero means men lived longer. "
                 "Russia's gap jumped after 1990 (Bangladesh's 1971 spike reflects the war year in the source data); it is shrinking in Nigeria and has turned positive in India and Bangladesh.", 150), 11, 6.6)
ax = fig.add_axes([0.07, 0.17, 0.80, 0.68])
ends = {}
for n, c in zip(sel, cols):
    q = p[p["Country Name"] == n].sort_values("Year")
    ax.plot(q.Year, q.Gap, color=c, lw=2.0)
    ends[n] = q.Gap.iloc[-1]
ys = {}; last = -99
for n in sorted(ends, key=ends.get):   # nudge end labels apart (manual-style label placement)
    ys[n] = max(ends[n], last + 0.65); last = ys[n]
for n, c in zip(sel, cols):
    ax.text(2023.8, ys[n], n.replace("Russian Federation", "Russia"), color=c, fontsize=9, va="center", fontweight="bold")
ax.axhline(0, color="#333", lw=1, ls="--")
ax.set_xlim(1960, 2023); ax.set_ylabel("Female - male life expectancy (years)"); ax.set_xlabel("Year")
ax.grid(axis="x", visible=False)
fig.savefig(f"{OUT}/q1a_gap_lines.png"); plt.close(fig)

# ---------------- Fig 1B: dumbbell 1960 vs 2023 ----------------
w = p[p.Year.isin([1960, 2023])].pivot(index="Country Name", columns="Year", values="Gap").dropna()
codes = pd.read_csv(f"{D}/lifespan_dataset_1960.csv")[["Country Name", "Country Code"]].drop_duplicates().set_index("Country Name")["Country Code"]
agg_codes = {"AFE","AFW","ARB","CEB","CSS","EAP","EAR","EAS","ECA","ECS","EMU","EUU","FCS","HIC","HPC","IBD","IBT","IDA","IDB","IDX","INX","LAC","LCN","LDC","LIC","LMC","LMY","LTE","MEA","MIC","MNA","NAC","OED","OSS","PRE","PSS","PST","SAS","SSA","SSF","SST","TEA","TEC","TLA","TMN","TSA","TSS","UMC","WLD"}
w = w[~w.index.map(lambda n: codes.get(n) in agg_codes)]
w["chg"] = w[2023] - w[1960]
pop_ok = w.copy()
pick = pd.concat([pop_ok.sort_values(2023).head(5), pop_ok.sort_values(2023).tail(7),
                  pop_ok.loc[[n for n in ["United States", "China", "India", "Japan", "Germany", "Brazil", "Nigeria"] if n in pop_ok.index]]]).drop_duplicates()
pick = pick.sort_values(2023)
fig = frame("Where is the female advantage in life expectancy largest, and how did it change?",
            "Female minus male life expectancy (years), 1960 vs 2023",
            wrap("Source: World Bank life expectancy data. Countries shown: the five smallest and seven largest 2023 gaps (aggregates "
                 "excluded) plus seven large countries for reference. Gap = female minus male. Sorted by 2023 gap. Orange dots to the "
                 "right of blue dots mean the gap widened since 1960.", 150), 10, 8)
ax = fig.add_axes([0.2, 0.13, 0.75, 0.75])
y = np.arange(len(pick))
ax.hlines(y, pick[1960], pick[2023], color="#999", lw=1.5, zorder=2)
ax.scatter(pick[1960], y, color=BLUE, s=55, zorder=3, label="1960")
ax.scatter(pick[2023], y, color=ORANGE, s=55, zorder=3, label="2023")
ax.set_yticks(y); ax.set_yticklabels(pick.index.str.replace("Russian Federation", "Russia"), fontsize=9)
ax.axvline(0, color="#333", lw=1, ls="--"); ax.grid(axis="y", visible=False)
ax.set_xlabel("Female - male life expectancy (years)")
ax.legend(title="Year", frameon=False, loc="lower right")
fig.savefig(f"{OUT}/q1b_gap_dumbbell.png"); plt.close(fig)
print(pick[[1960, 2023]].round(1))

# ---------------- Fig 2A: scatter education vs unemployment ----------------
E = "Percent of adults with a bachelor's degree or higher, 2019-23"
d = cen.dropna(subset=[E, "Unemployment rate 2023", "Group"])
fig = frame("Counties with more college graduates tend to have lower unemployment, in metro and nonmetro areas alike",
            f"US counties: unemployment rate (2023) vs. share of adults with a bachelor's degree or higher (2019-23); n = {len(d):,}",
            wrap("Source: USDA ERS county data. Each circle is a county, sized by 2020 population and colored by 2023 Rural-urban "
                 "Continuum Code group. Lines are linear trend lines for each group. Counties with unemployment above 12% are not shown "
                 "(a handful of outliers).", 150), 11, 7)
ax = fig.add_axes([0.07, 0.16, 0.72, 0.70])
dd = d[d["Unemployment rate 2023"] <= 12]
for g, c in GCOL.items():
    s = dd[dd.Group == g]
    ax.scatter(s[E], s["Unemployment rate 2023"], s=8 + s["Census Population 2020"] / 6000, color=c, alpha=0.45, edgecolor="none")
    m, b = np.polyfit(s[E], s["Unemployment rate 2023"], 1)
    xs = np.array([s[E].min(), s[E].max()]); ax.plot(xs, m * xs + b, color=c, lw=2.5)
    print(g, "slope", round(m, 3), "r", round(s[E].corr(s["Unemployment rate 2023"]), 2), len(s))
ax.set_xlabel("Adults with bachelor's degree or higher (%)"); ax.set_ylabel("Unemployment rate, 2023 (%)")
hs = [Line2D([], [], marker="o", color=c, ls="-", lw=2.5, ms=7, alpha=.8, label=g) for g, c in GCOL.items()]
fig.legend(handles=hs, title="Rural-urban group", loc="upper left", bbox_to_anchor=(0.81, 0.82), frameon=False, fontsize=9)
fig.savefig(f"{OUT}/q2a_scatter.png"); plt.close(fig)

# ---------------- Fig 2B: bars by education quartile x group ----------------
d = d.copy()
d["Edu"] = pd.qcut(d[E], 4, labels=["Lowest 25%", "Second 25%", "Third 25%", "Highest 25%"])
t = d.groupby(["Edu", "Group"], observed=True).apply(
    lambda s: s["Unemployment rate 2023"].median(), include_groups=False).unstack()
nn = d.groupby(["Edu", "Group"], observed=True).size().unstack()
print(t.round(2).to_string()); print(nn.to_string())
fig = frame("Unemployment is lower in better-educated counties, with a similar pattern in every rural-urban group",
            "Median 2023 unemployment rate (%) by education quartile of counties and rural-urban group",
            wrap("Source: USDA ERS county data. Counties are split into quartiles by the share of adults with a bachelor's degree or "
                 "higher (2019-23); bars show the median county unemployment rate (2023) within each quartile and group. "
                 "Bar labels are medians.", 150), 11, 6.5)
ax = fig.add_axes([0.07, 0.16, 0.72, 0.68])
bw = 0.26
for i, g in enumerate(GCOL):
    xs = np.arange(4) + (i - 1) * bw
    bars = ax.bar(xs, t[g].values, bw * 0.95, color=GCOL[g], label=g)
    for x, v in zip(xs, t[g].values): ax.text(x, v + 0.05, f"{v:.1f}", ha="center", fontsize=8.5, color="#333")
ax.set_xticks(range(4)); ax.set_xticklabels(t.index)
ax.set_xlabel("County education level (share of adults with a bachelor's degree or higher)")
ax.set_ylabel("Median unemployment rate, 2023 (%)"); ax.grid(axis="x", visible=False)
fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in GCOL.values()], labels=list(GCOL), title="Rural-urban group",
           loc="upper left", bbox_to_anchor=(0.81, 0.82), frameon=False, fontsize=9)
fig.savefig(f"{OUT}/q2b_bars.png"); plt.close(fig)

# ---------------- Fig 3: unemployment by group over time ----------------
yrs = range(2000, 2024)
rows = []
for g in GCOL:
    s = cen[cen.Group == g]
    for y_ in yrs:
        rows.append((g, y_, s[f"Unemployed {y_}"].sum() / s[f"Civilian labor force {y_}"].sum() * 100))
u = pd.DataFrame(rows, columns=["Group", "Year", "Rate"])
print(u[u.Year.isin([2007, 2009, 2010, 2019, 2020, 2023])].pivot(index="Year", columns="Group", values="Rate").round(1))
fig = frame("The 2020 spike hit metro counties hardest; the 2009 recession hit adjacent nonmetro counties hardest",
            "Unemployment rate (%) by rural-urban group, 2000-2023",
            wrap("Source: USDA ERS county data. Rate = total unemployed divided by total civilian labor force for all counties in the "
                 "group (so large counties count more). Groups use 2023 Rural-urban Continuum Codes; nonmetro counties are split by "
                 "whether they are adjacent to a metro area. Dotted lines mark 2009 and 2020.", 150), 11, 6.3)
ax = fig.add_axes([0.07, 0.2, 0.72, 0.64])
for g, c in GCOL.items():
    q = u[u.Group == g]; ax.plot(q.Year, q.Rate, color=c, lw=2.2, marker="o", ms=3.5, label=g)
for yv in (2009, 2020): ax.axvline(yv, color="#888", ls=":", lw=1.2)
ax.text(2009.2, 3.5, "2009", fontsize=8.5, color="#555"); ax.text(2020.2, 3.5, "2020", fontsize=8.5, color="#555")
ax.set_xlim(2000, 2023.5); ax.set_ylabel("Unemployment rate (%)"); ax.set_xlabel("Year"); ax.grid(axis="x", visible=False)
ax.set_xticks(range(2000, 2024, 4)); ax.set_xticks(range(2000, 2024), minor=True)
fig.legend(handles=[Line2D([], [], color=c, lw=2.2, marker="o", ms=4) for c in GCOL.values()], labels=list(GCOL),
           title="Rural-urban group", loc="upper left", bbox_to_anchor=(0.81, 0.82), frameon=False, fontsize=9)
fig.savefig(f"{OUT}/q3_unemployment_time.png"); plt.close(fig)

# ---------------- Fig 4: state migration ----------------
a = agg[~agg["State"].isin(["US"])].copy()
mc = ["Domestic Migration Rate 2021", "Domestic Migration Rate 2022", "Domestic Migration Rate 2023"]
a["avg"] = a[mc].mean(axis=1)
a = a.dropna(subset=["avg"]).sort_values("avg")
print(a[["Area name", "avg"]].round(1).to_string())
fig = frame("Net domestic migration, 2021-2023: Idaho gained the most, New York lost the most",
            "Net domestic migration per 1,000 residents, average of 2021, 2022 and 2023, by state",
            wrap("Source: USDA ERS state-level data (from Census Bureau population estimates). Domestic migration = people moving in "
                 "from elsewhere in the US minus people moving out, per 1,000 residents, averaged over three years. Blue = net gain, "
                 "red = net loss. Includes DC.", 150), 9, 11)
ax = fig.add_axes([0.2, 0.09, 0.74, 0.8])
cl = [BLUE if v >= 0 else RED for v in a["avg"]]
ax.barh(a["Area name"], a["avg"], color=cl, height=0.75)
for i, v in enumerate(a["avg"]):
    ax.text(v + (0.15 if v >= 0 else -0.15), i, f"{v:.1f}", va="center", ha="left" if v >= 0 else "right", fontsize=7.5, color="#333")
ax.tick_params(axis="y", labelsize=8); ax.axvline(0, color="#333", lw=1); ax.grid(axis="y", visible=False)
ax.set_xlabel("Net domestic migration per 1,000 residents (3-year average)"); ax.set_ylim(-0.7, len(a) - 0.3)
fig.savefig(f"{OUT}/q4_migration_states.png"); plt.close(fig)
