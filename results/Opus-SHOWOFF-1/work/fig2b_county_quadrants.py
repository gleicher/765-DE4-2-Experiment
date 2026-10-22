"""Q2 alternate: every county, natural change vs. domestic migration, small multiples by metro status."""
from census_components import *
import matplotlib.patheffects as pe
setup()
c = county_components()
c.to_csv(INTER / "q2_county_components.csv", columns=["fips", "State", "Area name", "rucc", "grp", "base", "nat_r", "dom_r", "intl_r", "chg_r"], index=False)
G = [("Large metro", "Metro areas of 1 million+ (code 1)", BLUE),
     ("Smaller metro", "Smaller metro areas (codes 2–3)", AQUA),
     ("Nonmetro", "Nonmetro / rural counties (codes 4–9)", ORANGE)]
XL, YL = (-16, 12), (-32, 42)

fig = plt.figure(figsize=(14, 7.6))
header(fig, "Five in six rural counties have more deaths than births; most of them are gaining Americans from elsewhere",
       "Each dot is a US county: yearly natural change (births − deaths) against net domestic migration, per 1,000 residents, averaged over 2021–2023.\n"
       "Dot area shows population; grey dots repeat the other panels' counties. Percentages are shares of counties in each quadrant of that panel.\n"
       "In big metros the typical county gains movers: the metro-wide outflow comes from a few giant core counties such as Los Angeles and Cook.",
       x=0.03)
W = 0.29
for j, (g, title, col) in enumerate(G):
    ax = fig.add_axes([0.055 + j * (W + 0.035), 0.13, W, 0.60])
    d = c[c.grp == g]; o = c[c.grp != g]
    ax.axvspan(XL[0], 0, ymin=(0 - YL[0]) / (YL[1] - YL[0]), ymax=1, color="#f3ece4", zorder=0, lw=0)
    ax.scatter(o.nat_r.clip(*XL), o.dom_r.clip(*YL), s=4, color="#d6d4cc", lw=0, zorder=1, rasterized=True)
    sz = np.sqrt(d.base) / 18
    ax.scatter(d.nat_r.clip(*XL), d.dom_r.clip(*YL), s=sz, color=col, alpha=.55, edgecolor="white", lw=.35, zorder=2)
    ax.axhline(0, color=INK, lw=.9, zorder=3); ax.axvline(0, color=INK, lw=.9, zorder=3)
    mx, my = d.nat_r.median(), d.dom_r.median()
    ax.plot([mx], [my], marker="+", ms=16, mew=2.6, color="white", zorder=5)
    ax.plot([mx], [my], marker="+", ms=14, mew=1.6, color=INK, zorder=6)
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_title(f"{title}", fontsize=11.5, loc="left", pad=22, color=INK)
    ax.text(0, 1.0, "", transform=ax.transAxes)
    n = len(d)
    q = {"tl": ((d.nat_r < 0) & (d.dom_r > 0)).sum(), "tr": ((d.nat_r >= 0) & (d.dom_r > 0)).sum(),
         "bl": ((d.nat_r < 0) & (d.dom_r <= 0)).sum(), "br": ((d.nat_r >= 0) & (d.dom_r <= 0)).sum()}
    st = [pe.withStroke(linewidth=3, foreground=SURFACE)]
    ax.text(XL[0] + .6, YL[1] - 1.5, f"{100*q['tl']/n:.0f}%", fontsize=20 if g == "Nonmetro" else 15, fontweight="bold", color=INK, va="top", path_effects=st, zorder=7)
    ax.text(XL[0] + .6, YL[1] - (8.2 if g == "Nonmetro" else 7.2), "deaths > births,\nbut Americans move in", fontsize=8.6, color=INK2, va="top", path_effects=st, zorder=7)
    ax.text(XL[1] - .5, YL[1] - 1.5, f"{100*q['tr']/n:.0f}%", fontsize=15, fontweight="bold", color=INK, va="top", ha="right", path_effects=st, zorder=7)
    ax.text(XL[1] - .5, YL[1] - 7.2, "growing\nboth ways", fontsize=8.6, color=INK2, va="top", ha="right", path_effects=st, zorder=7)
    ax.text(XL[0] + .6, YL[0] + 1.5, f"{100*q['bl']/n:.0f}%  shrinking both ways", fontsize=9.2, color=INK, va="bottom", path_effects=st, zorder=7)
    ax.text(XL[1] - .5, YL[0] + 1.5, f"{100*q['br']/n:.0f}%  births > deaths,\nbut Americans leave", fontsize=9.2, color=INK, va="bottom", ha="right", path_effects=st, zorder=7)
    ax.text(0, 1.012, f"{n:,} counties · {d.base.sum()/1e6:.0f}M people · median county ✚ at ({mx:+.1f}, {my:+.1f})",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=8.8, color=INK2)
    ax.set_xticks([-15, -10, -5, 0, 5, 10]); ax.set_yticks([-30, -20, -10, 0, 10, 20, 30, 40])
    ax.tick_params(labelsize=8.8, length=0)
    if j == 0:
        ax.set_ylabel("Net domestic migration per 1,000 per year\n◀ more Americans leave   |   more arrive ▶", fontsize=9.5)
    if j == 1:
        ax.set_xlabel("Natural change per 1,000 per year   ◀ more deaths   |   more births ▶", fontsize=9.5, labelpad=6)
    # highlight a few large named counties for orientation
    if g == "Large metro":
        for f, nm, dx, dy in [("06037", "Los Angeles", -62, 4), ("17031", "Cook (Chicago)", -78, -12), ("36047", "Kings (Brooklyn)", -100, 10)]:
            r = d[d.fips == f]
            if len(r): ax.annotate(nm, (r.nat_r.iloc[0], r.dom_r.iloc[0]), xytext=(dx, dy), textcoords="offset points", fontsize=8.2, color=INK, path_effects=st, zorder=8,
                                   arrowprops=dict(arrowstyle="-", lw=.6, color=INK2))
# size key
kx = fig.add_axes([0.83, 0.80, 0.14, 0.05]); kx.set_axis_off(); kx.set_xlim(0, 10); kx.set_ylim(0, 2)
for x, pop, t in [(1, 1e4, "10k"), (3.6, 1e5, "100k"), (6.6, 1e6, "1M")]:
    kx.scatter([x], [1], s=np.sqrt(pop) / 18, facecolor="none", edgecolor=INK2, lw=.8)
    kx.text(x + .6 + (0.6 if pop == 1e6 else 0), 1, t, va="center", fontsize=8.5, color=INK2)
kx.text(0, 2.1, "Population", fontsize=8.5, color=INK2)

footer(fig, "Data: USDA ERS county-level data sets (Population Estimates 2021–2023; 2023 Rural-Urban Continuum Codes), CS765 course data. Rates = component summed over 2021–2023 ÷ July 2020 population ÷ 3.\n"
       "3,106 counties in the 50 states + DC (Puerto Rico and 17 retired AK/CT units excluded). A few extreme small counties are pinned to the panel edge. "
       "Shaded quadrant = deaths exceed births but net domestic migration is positive.", x=0.03)
save(fig, "q2b_county_quadrants")
