"""Q3: how long did it take each country to go from life expectancy 50 to 70? (scatter + cohort Kaplan-Meier curves)"""
from common import *
from q3_milestones import milestones
import matplotlib.patheffects as pe
setup()
d = milestones()
COH = [(1800, 1900, "before 1900"), (1900, 1930, "1900–29"), (1930, 1950, "1930–49"),
       (1950, 1965, "1950–64"), (1965, 1980, "1965–79"), (1980, 2024, "1980 or later")]
import seaborn as sns
_m = sns.color_palette("mako", as_cmap=True)
RAMP = [_m(v) for v in (0.88, 0.74, 0.60, 0.46, 0.31, 0.14)]   # ordinal: light = early, dark = recent
d["coh"] = pd.cut(d.c50, [c[0] for c in COH] + [2024], labels=[c[2] for c in COH], right=False)
d.to_csv(INTER / "fig3_milestones_with_cohort.csv", index=False)

fig = plt.figure(figsize=(14, 8.4))
header(fig, "Latecomers reach a life expectancy of 70 faster than the pioneers did, but the speed-up peaked long ago",
       "For every country with a clear record of reaching a life expectancy of 50, when it got there (left, x) and how long it then took to reach 70 (left, y).\n"
       "Right: the same countries grouped by when they reached 50. Countries reaching 50 before 1930 needed 50–60+ years to get to 70;\n"
       "those reaching 50 in 1930–49 needed ~35, the fastest of any group. Groups that reached 50 after 1965 are tracking slower than that, and 45 of those 64 have not yet arrived.",
       x=0.03)
st = [pe.withStroke(linewidth=3, foreground=SURFACE)]

# ---- left: scatter ----
ax = fig.add_axes([0.06, 0.13, 0.53, 0.62])
xs = np.array([1840, 2025])
ax.fill_between(xs, 2023 - xs, 110, color="#efede7", zorder=0, lw=0)
ax.plot(xs, 2023 - xs, color=AXIS, lw=1, zorder=1)
ax.text(1985, 88, "Not yet observable\n(would end after 2023).\nTriangles sit on this edge:\nstill waiting in 2023.", fontsize=8.8, color=MUTED, ha="left", va="top")
for (lo, hi, lab), col in zip(COH, RAMP):
    s = d[d.coh == lab]
    dn, cn = s[s.done], s[s.cens]
    ax.scatter(dn.c50, dn.years, s=42, color=col, edgecolor="white", lw=.7, zorder=3)
    ax.scatter(cn.c50, cn.years, s=46, marker="^", facecolor=SURFACE, edgecolor=col, lw=1.4, zorder=3)
LAB = {"Sweden": (6, 2, "left"), "Australia": (6, 2, "left"), "United States": (6, 2, "left"),
       "United Kingdom": (-6, -9, "right"), "Uruguay": (6, 3, "left"), "Hungary": (6, 2, "left"), "Argentina": (-6, 6, "right"),
       "Spain": (-6, -6, "right"), "South Korea": (-6, -8, "right"), "China": (6, 8, "left"),
       "Guyana": (-6, 5, "right"), "Zimbabwe": (6, 4, "left"), "South Africa": (6, 2, "left"), "Brazil": (-6, 4, "right"),
       "India": (5, 5, "left"), "Bangladesh": (5, -9, "left"), "Oman": (5, -6, "left"), "Maldives": (5, -6, "left"),
       "Pakistan": (6, 3, "left"), "Nigeria": (6, -5, "left"), "Chad": (5, -9, "left"), "Russia": (6, -4, "left"),
       "Kenya": (6, 2, "left"), "Iran": (6, -6, "left")}
for e, (dx, dy, ha) in LAB.items():
    r = d[d.ent == e]
    if len(r) == 0: continue
    r = r.iloc[0]
    ax.annotate(e, (r.c50, r.years), xytext=(dx, dy), textcoords="offset points", fontsize=8.6, color=INK, ha=ha,
                va="center", path_effects=st, zorder=5)
ax.set_xlim(1845, 2015); ax.set_ylim(0, 100)
ax.set_xlabel("Year life expectancy first reached 50", fontsize=10)
ax.set_ylabel("Years from 50 to 70", fontsize=10)
ax.set_title("Each country: when it reached 50, and how long 50 → 70 took", fontsize=11.5, pad=10)
# key
ax.scatter([1852], [26], s=42, color=INK2, edgecolor="white"); ax.text(1856, 26, "reached 70", va="center", fontsize=8.8, color=INK2)
ax.scatter([1852], [20], s=46, marker="^", facecolor=SURFACE, edgecolor=INK2, lw=1.4)
ax.text(1856, 20, "not yet at 70 in 2023\n(y = years so far)", va="center", fontsize=8.8, color=INK2)
ax.text(1850, 32, "Colour = when the country reached 50\n(same groups as the right panel)", fontsize=8.8, color=INK2, va="bottom")
ax.annotate("Japan: 17 years\n(1947–1964)", xy=(d[d.ent == "Japan"].c50.iloc[0], 16.7), xytext=(1915, 6), fontsize=8.8, color=INK2,
            arrowprops=dict(arrowstyle="-", lw=.7, color=INK2), va="center")
ax.annotate("Norway: 93 years\n(1854–1947)", xy=(d[d.ent == "Norway"].c50.iloc[0], 93.4), xytext=(1868, 80), fontsize=8.8, color=INK2,
            arrowprops=dict(arrowstyle="-", lw=.7, color=INK2), va="center")

# ---- right: Kaplan-Meier style curves ----
bx = fig.add_axes([0.665, 0.13, 0.31, 0.62])
def km(t, done):
    order = np.argsort(t); t = np.asarray(t)[order]; done = np.asarray(done)[order]
    n = len(t); S = 1.0; xs, ys = [0], [0]
    at_risk = n
    for ti, di in zip(t, done):
        if di:
            S *= (1 - 1 / at_risk); xs += [ti, ti]; ys += [ys[-1], 1 - S]
        at_risk -= 1
    return np.array(xs), np.array(ys), t.max()
for (lo, hi, lab), col in zip(COH, RAMP):
    s = d[d.coh == lab]
    x, y, tmax = km(s.years.values, s.done.values)
    x = np.append(x, tmax); y = np.append(y, y[-1])
    bx.plot(x, 100 * y, color="white", lw=4.2, zorder=2, drawstyle="default")
    bx.plot(x, 100 * y, color=col, lw=2.2, zorder=3)
    bx.plot([], [], color=col, lw=2.4, label=f"reached 50 {lab}  (n={len(s)})")
bx.set_xlim(0, 100)
bx.legend(loc="lower right", fontsize=8.8, handlelength=1.6, title="Group", title_fontsize=9, alignment="left"); bx.set_ylim(0, 104)
bx.set_xticks(range(0, 101, 20)); bx.set_yticks(range(0, 101, 25))
bx.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
bx.set_xlabel("Years since reaching 50", fontsize=10)
bx.set_ylabel("Share of group that has reached 70", fontsize=10)
bx.set_title("Grouped by when they reached 50 (countries)", fontsize=11.5, pad=10)
bx.axvline(40, color=AXIS, lw=1, ls=(0, (2, 2)), zorder=1)
bx.text(41, 97, "40 years", fontsize=8.4, color=MUTED)
for sp in ["right"]: bx.spines[sp].set_visible(False)

footer(fig, "Data: Our World in Data, period life expectancy at birth, long-run series (Riley 2005; Zijdeman et al. 2015; HMD 2024; UN WPP 2024), CS765 course data. Countries only (regional aggregates excluded).\n"
       "Milestone years are linearly interpolated between observations and counted only when the bracketing observations are ≤10 years apart; countries already above 50 at their first observation are omitted (160 countries shown).\n"
       "Right panel is a Kaplan–Meier estimate: countries not yet at 70 count as 'still waiting' up to 2023 rather than being dropped, so slow recent groups are not hidden. Lines end at each group's longest observed wait.",
       x=0.03)
save(fig, "q3_fifty_to_seventy")
