"""Q4: the Great Recession and the COVID shock hit different parts of the urban-rural spectrum."""
from common import *
import matplotlib.patheffects as pe
setup()
c = load_counties()
c = c[c.rucc.notna() & (c.State != "PR")].copy(); c["rucc"] = c.rucc.astype(int)
c["grp"] = np.select([c.rucc == 1, c.rucc <= 3], ["Large metro", "Smaller metro"], "Nonmetro")
YRS = list(range(2000, 2024))
def rate(df, y): return 100 * df[f"Unemployed {y}"].sum() / df[f"Civilian labor force {y}"].sum()
G = [("Large metro", "Metros of 1M+", BLUE), ("Smaller metro", "Smaller metros", AQUA), ("Nonmetro", "Nonmetro (rural)", ORANGE)]
ts = pd.DataFrame({g: [rate(c[c.grp == g], y) for y in YRS] for g, _, _ in G}, index=YRS)
ts["US"] = [rate(c, y) for y in YRS]
ts.to_csv(INTER / "q4_unemployment_by_group.csv")
by = pd.DataFrame({k: {"gr": rate(c[c.rucc == k], 2010) - rate(c[c.rucc == k], 2007),
                       "cv": rate(c[c.rucc == k], 2020) - rate(c[c.rucc == k], 2019),
                       "lf": c[c.rucc == k]["Civilian labor force 2019"].sum()} for k in range(1, 10)}).T
by.to_csv(INTER / "q4_rise_by_rucc.csv")
# county-level: share of counties hit harder in 2020 than 2007-10
c["gr"] = c["Unemployment rate 2010"] - c["Unemployment rate 2007"]
c["cv"] = c["Unemployment rate 2020"] - c["Unemployment rate 2019"]
share = c.groupby("rucc").apply(lambda d: (d.cv > d.gr).mean(), include_groups=False)
by["share_cv_worse"] = share

fig = plt.figure(figsize=(14, 8.6))
header(fig, "For two decades rural unemployment ran above the big metros', until COVID flipped the pattern",
       "Unemployment rate for US counties grouped by the USDA 2023 Rural-Urban Continuum Code, 2000–2023. In the Great Recession every kind of county saw a similar\n"
       "rise (4–5 points) on top of rural America's usual extra unemployment. In 2020 the jump was largest in the biggest metros and smallest in the most remote counties.",
       x=0.03)
st = [pe.withStroke(linewidth=3, foreground=SURFACE)]
# --- top-left: levels ---
ax = fig.add_axes([0.06, 0.40, 0.50, 0.42])
for lo, hi, t in [(2007.5, 2010.5, "Great Recession\n& slow recovery"), (2019.5, 2021.5, "COVID-19")]:
    ax.axvspan(lo, hi, color="#efede7", lw=0, zorder=0)
    ax.text((lo + hi) / 2, 10.9, t, ha="center", va="top", fontsize=8.8, color=INK2)
for g, lab, col in G:
    ax.plot(ts.index, ts[g], color=col, lw=2.2, zorder=3)
    ax.scatter([2010, 2020], ts.loc[[2010, 2020], g], s=26, color=col, edgecolor="white", zorder=4)
for g, lab, col in G:
    ax.plot([], [], color=col, lw=2.4, label={"Large metro": "Metros of 1M+ (code 1)", "Smaller metro": "Smaller metros (codes 2–3)", "Nonmetro": "Nonmetro / rural (codes 4–9)"}[g])
ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.78), fontsize=9, handlelength=1.6)
ax.annotate(f"2020: big metros {ts.loc[2020,'Large metro']:.1f}%\nvs. rural {ts.loc[2020,'Nonmetro']:.1f}%",
            (2020, ts.loc[2020, "Large metro"]), xytext=(2013.3, 10.75), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", lw=.7, color=INK2), path_effects=st)
ax.annotate(f"2010: rural {ts.loc[2010,'Nonmetro']:.1f}%\nvs. big metros {ts.loc[2010,'Large metro']:.1f}%",
            (2010, ts.loc[2010, "Nonmetro"]), xytext=(2001.0, 9.4), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", lw=.7, color=INK2), path_effects=st)
ax.set_xlim(1999.5, 2023.5); ax.set_ylim(2.5, 11)
ax.set_xticks(range(2000, 2024, 4)); ax.tick_params(labelbottom=False, length=0)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.set_title("Unemployment rate", fontsize=11.5, pad=8)
# --- bottom-left: gap ---
bx = fig.add_axes([0.06, 0.13, 0.50, 0.22], sharex=ax)
gap = ts["Nonmetro"] - ts["Large metro"]
bx.bar(gap.index, gap, width=.72, color=[ORANGE if v > 0 else BLUE for v in gap], zorder=3)
bx.axhline(0, color=INK, lw=.9, zorder=4)
for lo, hi in [(2007.5, 2010.5), (2019.5, 2021.5)]:
    bx.axvspan(lo, hi, color="#efede7", lw=0, zorder=0)
bx.set_ylim(-2.5, 1.5); bx.set_yticks([-2, -1, 0, 1])
bx.yaxis.set_major_formatter(lambda v, _: f"{v:+.0f}" if v else "0")
bx.set_xticks(range(2000, 2024, 4)); bx.tick_params(length=0)
bx.set_title("Rural minus big-metro unemployment (percentage points)", fontsize=10.5, pad=6)
bx.text(2000.0, 1.25, "rural worse", fontsize=8.6, color=ORANGE, va="top", fontweight="bold")
bx.text(2000.0, -2.2, "big metros worse", fontsize=8.6, color=BLUE, va="bottom", fontweight="bold")
bx.text(2020, gap[2020] - .12, f"{gap[2020]:+.1f}", ha="center", va="top", fontsize=8.6, color=INK)
bx.text(2009, gap[2009] + .1, f"{gap[2009]:+.1f}", ha="center", va="bottom", fontsize=8.6, color=INK)

# --- right: dumbbell of the rise by RUCC ---
cx = fig.add_axes([0.70, 0.13, 0.27, 0.69])
rows = list(range(1, 10)); yp = {k: i + (0.6 if k >= 4 else 0) for i, k in enumerate(rows)}
for k in rows:
    y = yp[k]; r = by.loc[k]
    cx.plot([r.gr, r.cv], [y, y], color=AXIS, lw=2.2, zorder=1, solid_capstyle="round")
    cx.scatter(r.gr, y, s=60, marker="s", color=INK2, edgecolor="white", zorder=3)
    cx.scatter(r.cv, y, s=70, color=RED, edgecolor="white", zorder=3)
cx.set_yticks([yp[k] for k in rows])
cx.set_yticklabels([f"{k}  {RUCC_LABEL[k].replace('Nonmetro, ', '').replace(', adjacent to metro', ', adj.').replace(', adjacent', ', adj.').replace(', not adjacent', ', not adj.')}" for k in rows], fontsize=8.9)
cx.set_ylim(max(yp.values()) + .6, -1.6)
cx.set_xlim(0, 5.8); cx.xaxis.set_major_formatter(lambda v, _: f"+{v:.0f}")
cx.tick_params(length=0); cx.grid(axis="y", visible=False)
cx.set_xlabel("Rise in unemployment rate (percentage points)", fontsize=9.5)
cx.set_title("How much unemployment rose, by county type", fontsize=11.5, pad=8, loc="left")
cx.scatter([0.15], [-1.0], s=60, marker="s", color=INK2, edgecolor="white"); cx.text(0.35, -1.0, "2007 → 2010", va="center", fontsize=9, color=INK2)
cx.scatter([2.55], [-1.0], s=70, color=RED, edgecolor="white"); cx.text(2.75, -1.0, "2019 → 2020", va="center", fontsize=9, color=INK2)
cx.text(0.1, yp[1] - .55, "METRO", ha="left", fontsize=8.6, color=MUTED, fontweight="bold")
cx.text(0.1, yp[4] - .55, "NONMETRO", ha="left", fontsize=8.6, color=MUTED, fontweight="bold")
cx.axhline((yp[3] + yp[4]) / 2, color=GRID, lw=1)
cx.text(0.1, yp[6] + .4, "COVID's jump falls almost\nstep by step from the\nbiggest metros (+5.1) to\nthe most remote (+2.2).\n\nThe Great Recession's\nrise barely varied\n(+4.0 to +5.2).", fontsize=8.8, color=INK2, va="center", linespacing=1.35)

footer(fig, "Data: USDA ERS county-level data (Unemployment: civilian labour force and unemployed, annual averages 2000–2023; 2023 Rural-Urban Continuum Codes), CS765 course data. "
       "Rates = total unemployed ÷ total labour force\nfor each group, so large counties count more. 3,106 counties in the 50 states + DC (Puerto Rico and 17 retired AK/CT units excluded). "
       "Current (2023) codes are applied to all years. 'Rural' = nonmetro, codes 4–9.", x=0.03)
save(fig, "q4_two_recessions")
print(ts.round(2).loc[[2007, 2009, 2010, 2019, 2020, 2021, 2023]]); print(by.round(2))
