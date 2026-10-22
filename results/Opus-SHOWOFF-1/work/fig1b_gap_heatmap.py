"""Q1 alternate: heatmap of the female-male gap, countries ordered by the year their gap peaked,
plus a dumbbell showing peak vs. 2023."""
from common import *
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
setup()
p = load_wb()
SEL = {'China': 'China', 'India': 'India', 'United States': 'United States', 'Indonesia': 'Indonesia',
       'Pakistan': 'Pakistan', 'Nigeria': 'Nigeria', 'Brazil': 'Brazil', 'Bangladesh': 'Bangladesh',
       'Russian Federation': 'Russia', 'Mexico': 'Mexico', 'Japan': 'Japan', 'Ethiopia': 'Ethiopia',
       'Philippines': 'Philippines', 'Egypt, Arab Rep.': 'Egypt', 'Viet Nam': 'Viet Nam',
       'Congo, Dem. Rep.': 'DR Congo', 'Turkiye': 'Türkiye', 'Germany': 'Germany', 'Thailand': 'Thailand',
       'United Kingdom': 'United Kingdom', 'France': 'France', 'Italy': 'Italy', 'South Africa': 'South Africa',
       'Tanzania': 'Tanzania', 'Kenya': 'Kenya', 'Korea, Rep.': 'South Korea', 'Colombia': 'Colombia',
       'Spain': 'Spain', 'Argentina': 'Argentina', 'Ukraine': 'Ukraine', 'Poland': 'Poland', 'Canada': 'Canada',
       'Morocco': 'Morocco', 'Peru': 'Peru', 'Australia': 'Australia', 'Sweden': 'Sweden', 'Nepal': 'Nepal',
       'Sri Lanka': 'Sri Lanka', 'Chile': 'Chile', 'Netherlands': 'Netherlands', 'Ghana': 'Ghana',
       'Malaysia': 'Malaysia', 'Kazakhstan': 'Kazakhstan'}
LE_BINS = np.arange(30, 88, 2)
sub = p[p.name.isin(SEL) & (p.year <= 2019)].dropna(subset=["Both", "gap"]).copy()   # pre-COVID
sub["b"] = pd.cut(sub.Both, LE_BINS, labels=LE_BINS[:-1] + 1)
M = sub.groupby(["name", "b"], observed=True).gap.mean().unstack()
M = M.reindex(columns=LE_BINS[:-1] + 1)
last = p[p.name.isin(SEL) & (p.year == 2023)].set_index("name")
peakbin = M.idxmax(axis=1)
first_year = sub.groupby("name").year.min()
info = pd.DataFrame({"peak_bin": peakbin, "peak": M.max(axis=1), "g2023": last.gap, "le2023": last.Both,
                     "le1960": sub[sub.year == 1960].set_index("name").Both})
info["label"] = info.index.map(SEL)
info = info.sort_values("le2023", ascending=False)
info.to_csv(INTER / "fig1b_rows.csv"); M.to_csv(INTER / "fig1b_matrix.csv")
M = M.loc[info.index]

from matplotlib.colors import ListedColormap, BoundaryNorm
BOUNDS = [-6, -2, 0, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15]
COLS = ["#1c5cab", "#86b6ef", "#dedbd2", "#fbd9c0", "#f7bb93", "#f19a67", "#e8773f",
        "#d4572a", "#b13d1e", "#8a2a15", "#5e1a0d", "#3a0f07"]
cmap = ListedColormap(COLS); cmap.set_bad(SURFACE)
norm = BoundaryNorm(BOUNDS, cmap.N)

n = len(M)
fig = plt.figure(figsize=(12, 13.2))
header(fig, "Women's lead widens as countries get healthier, then narrows past ~75 years",
       "Each row is a country, 1960–2019. Instead of calendar years, columns are levels of overall life expectancy (2-year bins), so a row\n"
       "reads left to right as the country got healthier. Colour shows how many more years women lived than men at that stage.\n"
       "The darkest cells sit around 65–78; most of the healthiest countries (top) have lighter cells at their right-hand end.",
       y=0.982)
ax = fig.add_axes([0.17, 0.125, 0.56, 0.66])
im = ax.imshow(np.ma.masked_invalid(M.values), aspect="auto", cmap=cmap, norm=norm, interpolation="nearest",
               extent=[30, 86, n - .5, -.5])
ax.grid(False)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_yticks(range(n)); ax.set_yticklabels(info.label, fontsize=9.6, color=INK)
ax.tick_params(axis="y", length=0, pad=4)
ax.set_xticks(range(30, 87, 10)); ax.tick_params(axis="x", length=0, labelsize=9.5)
ax.set_xlim(30, 86)
for i, (nm, r) in enumerate(info.iterrows()):
    ax.plot(r.peak_bin, i, marker="o", ms=5, mfc="none", mec="white", mew=1.4)
    ax.plot(r.peak_bin, i, marker="o", ms=5, mfc="none", mec=INK, mew=0.8)
# group separators by 2023 life expectancy
tiers = [(80, 99, "80+ in 2023"), (75, 80, "75–80"), (70, 75, "70–75"), (0, 70, "Below 70")]
for lo, hi, t in tiers:
    idx = np.where((info.le2023 >= lo) & (info.le2023 < hi))[0]
    a, b = idx.min(), idx.max()
    if a > 0: ax.axhline(a - .5, color=SURFACE, lw=3.5)
    ax.annotate(t, xy=(-0.255, (a + b) / 2), xycoords=("axes fraction", "data"), fontsize=9.6, color=INK2,
                fontweight="bold", ha="center", va="center", rotation=90, annotation_clip=False)
    ax.annotate("", xy=(-0.232, a - .35), xytext=(-0.232, b + .35), xycoords=("axes fraction", "data"),
                arrowprops=dict(arrowstyle="-", color=AXIS, lw=1.5), annotation_clip=False)

# marginal: typical gap (median over ALL countries) per bin, same as Q1 primary
allc = p[(~p.is_agg) & (p.year <= 2019)].dropna(subset=["Both", "gap"]).copy()
allc["b"] = pd.cut(allc.Both, LE_BINS, labels=LE_BINS[:-1] + 1)
g = allc.groupby("b", observed=True).gap.agg(["median", "size"]); g = g[g["size"] >= 60]
mx = fig.add_axes([0.17, 0.81, 0.56, 0.07], sharex=ax)
mx.bar(g.index.astype(float), g["median"], width=1.75, color=[cmap(norm(v)) for v in g["median"]], edgecolor="none")
mx.set_ylim(0, 7.5); mx.set_yticks([0, 3, 6]); mx.tick_params(labelsize=8.5, length=0)
mx.tick_params(axis="x", labelbottom=True, labelsize=9.5)
mx.spines["left"].set_visible(False); mx.grid(axis="x", visible=False)
mx.text(30.5, 7.3, "All 217 countries: median gap at each life expectancy", fontsize=9.5, color=INK, fontweight="bold", va="top")
pk = g["median"].idxmax()
mx.annotate(f"peak ≈ {g['median'].max():.1f} yrs", (float(pk), g["median"].max()), xytext=(8, 2), textcoords="offset points", fontsize=8.8, color=INK2)
ax.set_xlabel("")
fig.text(0.13, 0.917, "", fontsize=1)
ax.text(58, n + 1.6, "Overall life expectancy at birth (years) when the country was at that stage", ha="center", fontsize=9.5, color=INK2)

# dumbbell: peak vs 2023
bx = fig.add_axes([0.765, 0.125, 0.20, 0.66], sharey=ax)
for i, (nm, r) in enumerate(info.iterrows()):
    bx.plot([r.g2023, r.peak], [i, i], color=AXIS, lw=2, solid_capstyle="round", zorder=1)
    bx.scatter(r.peak, i, s=34, facecolor=SURFACE, edgecolor=INK, lw=1.2, zorder=3)
    bx.scatter(r.g2023, i, s=34, color=ORANGE, edgecolor="white", lw=.8, zorder=3)
bx.set_xlim(-0.5, 14.5); bx.set_xticks([0, 4, 8, 12])
bx.xaxis.tick_top(); bx.tick_params(axis="y", left=False, labelleft=False); bx.tick_params(axis="x", length=0, labelsize=9)
bx.spines["left"].set_visible(False); bx.spines["bottom"].set_visible(False)
bx.grid(axis="y", visible=False)
bx.set_title("Widest gap (1960–2019)\nvs. 2023, years", fontsize=10.5, pad=40, loc="left")
bx.scatter([], [], s=34, facecolor=SURFACE, edgecolor=INK, label="widest (bin mean)")
bx.scatter([], [], s=34, color=ORANGE, label="2023")
bx.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.035), ncol=2, columnspacing=.8, fontsize=8.8, handletextpad=.3, borderaxespad=0.2)

# colour bar
cx = fig.add_axes([0.17, 0.06, 0.40, 0.012])
cb = fig.colorbar(im, cax=cx, orientation="horizontal", ticks=BOUNDS[1:-1], spacing="uniform")
cb.outline.set_visible(False); cx.tick_params(labelsize=8.8, length=0)
cx.set_title("Female minus male life expectancy (years)   ◀ men live longer | women live longer ▶",
             fontsize=9, color=INK2, loc="left", pad=4)
fig.text(0.60, 0.066, "○  marks the stage where each country's gap was widest", fontsize=9, color=INK2, va="center")

footer(fig, "Data: World Bank life expectancy at birth by sex, 1960–2023 (CS765 course data). 43 large countries chosen by the author to span all world regions; rows sorted by 2023 life expectancy.\n"
       "Cell = mean gap over the years a country spent in that 2-year life-expectancy bin, 1960–2019 (COVID years excluded). Blank = the country was never at that level. Right panel: widest cell vs. actual 2023 gap.",
       y=0.006)
save(fig, "q1b_gap_heatmap")
