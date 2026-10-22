"""Q1 primary: female-minus-male life expectancy gap vs. overall life expectancy (connected scatter)."""
from common import *
import matplotlib.patheffects as pe
setup()
p = load_wb()
cty = p[~p.is_agg].dropna(subset=["Both", "gap"]).copy()

# pooled "typical path": median gap in 2-year bins of overall life expectancy
bins = np.arange(30, 88, 2)
cty["bin"] = pd.cut(cty.Both, bins)
med = cty.groupby("bin", observed=True).gap.agg(["median", lambda s: s.quantile(.25), lambda s: s.quantile(.75), "size"])
med.columns = ["med", "q25", "q75", "n"]; med = med[med.n >= 60]
mid = np.array([iv.mid for iv in med.index])
med.assign(mid=mid).to_csv(INTER / "fig1a_median_path.csv")

HL = [("Sweden", BLUE, "Sweden"), ("Korea, Rep.", AQUA, "South Korea"),
      ("India", ORANGE, "India"), ("Russian Federation", RED, "Russia")]

fig = plt.figure(figsize=(12, 8.6))
ax = fig.add_axes([0.065, 0.115, 0.675, 0.745])
header(fig, "The female lead in life expectancy rises, peaks, then shrinks as countries get healthier",
       "Each grey dot is one country in one year (1960–2023). The black curve is the typical gap at each level of overall life expectancy.\n"
       "Coloured trails follow four countries through time (3-year smoothing; peaks quoted from smoothed values). Above the zero line women outlive men.")
ax.scatter(cty.Both, cty.gap, s=3, color="#b9b7ae", alpha=.25, lw=0, rasterized=True, zorder=1)
ax.fill_between(mid, med.q25, med.q75, color="#8a887f", alpha=.18, lw=0, zorder=2)
ax.plot(mid, med.med, color=INK, lw=2.6, zorder=3, solid_capstyle="round")
ax.axhline(0, color=INK2, lw=1, zorder=2)
ax.text(31, -0.35, "Men outlive women", color=INK2, fontsize=9.5, va="top", style="italic")
ax.text(31, 0.35, "Women outlive men", color=INK2, fontsize=9.5, va="bottom", style="italic")

# annotate the typical curve
i = np.argmax(med.med.values)
ax.annotate(f"Typical gap peaks at ~{med.med.values[i]:.1f} years\nwhen life expectancy is ~{mid[i]:.0f}",
            xy=(mid[i], med.med.values[i]), xytext=(41, 10.2), fontsize=10, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK, lw=.8, connectionstyle="arc3,rad=-.25"))
ax.text(36, 1.55, "Typical gap: median of all\ncountries (band = middle 50%)", fontsize=9, color=INK2, ha="left")

stats = {}
for name, col, lab in HL:
    s = p[p.name == name].set_index("year")[["Both", "gap"]].rolling(3, center=True, min_periods=1).mean()
    stats[lab] = s
    ax.plot(s.Both, s.gap, color="white", lw=4.6, zorder=4, solid_capstyle="round")
    ax.plot(s.Both, s.gap, color=col, lw=2.2, zorder=5, solid_capstyle="round")
    dec = s.loc[[y for y in range(1960, 2024, 10) if y in s.index]]
    ax.scatter(dec.Both, dec.gap, s=22, color=col, edgecolor="white", lw=1, zorder=6)
    ax.scatter([s.Both.iloc[0]], [s.gap.iloc[0]], s=60, facecolor="white", edgecolor=col, lw=2, zorder=7)
    ax.scatter([s.Both.iloc[-1]], [s.gap.iloc[-1]], s=70, color=col, edgecolor="white", lw=1.2, zorder=7)

def lab(x, y, t, col, **kw):
    ax.text(x, y, t, color=col, fontsize=10, fontweight="bold", zorder=8,
            path_effects=[pe.withStroke(linewidth=3, foreground=SURFACE)], **kw)
def yr(lb, y, dx=0, dy=0, ha="center", col=INK2):
    s = stats[lb]; ax.annotate(str(y), (s.loc[y, "Both"], s.loc[y, "gap"]), xytext=(dx, dy), textcoords="offset points",
                               fontsize=8.3, color=col, ha=ha, va="center", zorder=8,
                               path_effects=[pe.withStroke(linewidth=2.5, foreground=SURFACE)])

S, K, I, R = (stats[k] for k in ["Sweden", "South Korea", "India", "Russia"])
last = {lb: p[(p.name == nm) & (p.year == 2023)].gap.iloc[0] for nm, _, lb in HL}
lab(S.Both.iloc[-1] + .6, S.gap.iloc[-1] - .9, "Sweden", BLUE)
yr("Sweden", 1960, dx=12, dy=-6, ha="left"); yr("Sweden", 1980, dx=-12, dy=6, ha="right"); yr("Sweden", 2023, dx=9, dy=6, ha="left")
lab(K.Both.iloc[-1] + .6, K.gap.iloc[-1] + .25, "South Korea", AQUA)
yr("South Korea", 1960, dx=0, dy=-13); yr("South Korea", 1980, dx=-6, dy=10, ha="right"); yr("South Korea", 2023, dx=8, dy=-9, ha="left")
lab(I.Both.iloc[0] - .2, I.gap.iloc[0] - 1.2, "India", ORANGE, ha="left")
yr("India", 1960, dx=0, dy=11); yr("India", 1990, dx=8, dy=-9, ha="left"); yr("India", 2023, dx=9, dy=-6, ha="left")
lab(R.Both.loc[1994] - .5, R.gap.loc[1994] + .55, "Russia", RED, ha="right")
yr("Russia", 1960, dx=-9, dy=-4, ha="right"); yr("Russia", 1994, dx=8, dy=6, ha="left"); yr("Russia", 2023, dx=9, dy=2, ha="left")

ax.set_xlim(30, 87); ax.set_ylim(-5, 15)
ax.set_xlabel("Overall life expectancy at birth, both sexes (years)", fontsize=10.5)
ax.set_ylabel("Female minus male life expectancy (years)", fontsize=10.5)
ax.set_yticks(range(-4, 16, 2))

# key for trail markers
kx = ax.inset_axes([0.015, 0.83, 0.25, 0.15]); kx.set_axis_off(); kx.set_xlim(0, 10); kx.set_ylim(0, 3)
kx.plot([1, 8.5], [1.5, 1.5], color=INK2, lw=2)
kx.scatter([1], [1.5], s=55, facecolor="white", edgecolor=INK2, lw=2, zorder=3)
kx.scatter([4.75], [1.5], s=22, color=INK2, edgecolor="white", zorder=3)
kx.scatter([8.5], [1.5], s=65, color=INK2, edgecolor="white", zorder=3)
for x, t in [(1, "1960"), (4.75, "each decade"), (8.5, "2023")]:
    kx.text(x, 2.25, t, ha="center", fontsize=8.5, color=INK2)

# right-hand narrative panel
tx = 0.77
fig.text(tx, 0.845, "Four ways through the arc", fontsize=12, fontweight="bold", color=INK, va="top")
notes = [
    (BLUE, "Sweden", f"Rode the typical arc. The gap widened\nto {S.gap.max():.1f} yrs around {int(S.gap.idxmax())}, then nearly\n"
                     f"halved to {last["Sweden"]:.1f} as men's lives lengthened\nfaster than women's."),
    (AQUA, "South Korea", f"Same arc, higher and compressed in\ntime: gap peaked at {K.gap.max():.1f} yrs in {int(K.gap.idxmax())},\nback to {last["South Korea"]:.1f} by 2023."),
    (ORANGE, "India", f"Started below zero: in 1960 men\noutlived women by {-p[(p.name=='India')&(p.year==1960)].gap.iloc[0]:.1f} yrs.\nWomen pulled ahead only in the early\n1980s; India is still on the rising side."),
    (RED, "Russia", f"Far off the arc. A {R.gap.max():.0f}-year gap at its\n"
                    f"{int(R.gap.idxmax())} peak; still {last["Russia"]:.1f} in 2023, well\n"
                    "above the ~6-year typical gap for its\nlife expectancy."),
]
y = 0.80
for col, t, body in notes:
    fig.patches.append(plt.Rectangle((tx, y - 0.012), 0.006, 0.022, transform=fig.transFigure, color=col))
    fig.text(tx + 0.013, y, t, fontsize=10.5, fontweight="bold", color=INK, va="center")
    fig.text(tx + 0.013, y - 0.02, body, fontsize=9.4, color=INK2, va="top", linespacing=1.35)
    y -= 0.062 + 0.0225 * body.count("\n")
fig.text(tx, 0.255, "Reading the arc", fontsize=10.5, fontweight="bold", color=INK, va="top")
fig.text(tx, 0.233, "Countries mostly move left to right\nover time. The arc is a pattern across\ncountries, not a law: timing differs,\nand wars or crises (dots far above\nthe curve) push the gap up for a while.", fontsize=9.2, color=INK2, va="top", linespacing=1.35)

footer(fig, "Data: World Bank life expectancy at birth by sex (SP.DYN.LE00), 1960–2023, via CS765 course data. 217 countries and territories; "
       "World Bank regional/income aggregates excluded.\nTypical curve: median gap of all country-years in 2-year bins of overall life expectancy (bins with ≥60 country-years). "
       "Descriptive only; shows association, not cause.")
save(fig, "q1a_gap_arc")
