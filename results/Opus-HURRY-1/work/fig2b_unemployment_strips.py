"""Story 2, alternate: county-level distributions of the 2020 jump and the 2019->2022 net change, by rural-urban group."""
from common import *

c = load_counties()
c = c[c.rgroup.notna()].copy()
c["jump"] = c["Unemployment rate 2020"] - c["Unemployment rate 2019"]
c["net"] = c["Unemployment rate 2022"] - c["Unemployment rate 2019"]
c = c.dropna(subset=["jump", "net"])
groups = list(c.rgroup.cat.categories)
cols = dict(zip(groups, SEQ[::-1]))
rng = np.random.default_rng(7)

fig = plt.figure(figsize=(11, 7.6))
axes = [fig.add_axes([0.2, 0.2, 0.47, 0.6]), fig.add_axes([0.72, 0.2, 0.47 * 8 / 17, 0.6])]
panels = [("jump", "1. The 2020 spike\nChange in unemployment rate, 2019 → 2020", (-4, 13)),
          ("net", "2. Two years later\nChange in unemployment rate, 2019 → 2022", (-4, 4))]

summary = []
for ax, (var, ttl, xl) in zip(axes, panels):
    ax.axvline(0, color=INK2, lw=1, zorder=1)
    for i, grp in enumerate(groups):
        d = c[c.rgroup == grp]
        y = len(groups) - 1 - i
        jit = rng.uniform(-0.3, 0.3, len(d))
        sz = 3 + 60 * np.sqrt(d["Civilian labor force 2019"] / 1e6)
        ax.scatter(d[var].clip(*xl), y + jit, s=sz, color=cols[grp], alpha=0.45, lw=0, zorder=2)
        q1, med, q3 = d[var].quantile([0.25, 0.5, 0.75])
        ax.plot([q1, q3], [y + 0.42] * 2, color=INK, lw=2.5, solid_capstyle="butt", zorder=4)
        ax.plot([med], [y + 0.42], marker="|", ms=12, mew=2.5, color=INK, zorder=5)
        ax.text(q3 + 0.2, y + 0.42, f"median {med:+.1f}", ha="left", va="center", fontsize=8.5, color=INK, fontweight="bold")
        summary.append((var, grp, med, (d[var] >= 3).mean()))
    ax.set_xlim(*xl)
    ax.set_ylim(-0.6, len(groups) - 0.1)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels([] if ax is axes[1] else groups[::-1], fontsize=9.5, color=INK)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("percentage points\n(positive = unemployment rose)")
    ax.set_title(ttl, loc="left", fontsize=10.5, color=INK, linespacing=1.4)
    ax.tick_params(axis="y", length=0)

pd.DataFrame(summary, columns=["panel", "group", "median_pp", "share_ge_3pp"]).to_csv(
    Path(__file__).parent / "q2b_strip_summary.csv", index=False)

# key
fig.text(0.06, 0.875, "Each dot is a county, sized by its 2019 labor force. Black bar: middle 50% of counties in the group; tick: median.",
         fontsize=9, color=INK2, va="top")

title_block(fig, "In 2020, unemployment spiked most in big-metro counties and least in rural ones",
            "Change in county unemployment rate, grouped by USDA 2023 Rural-Urban Continuum Code (3,102 counties)", gap=0.045)
caption(fig, "Left: in the typical large-metro county unemployment rose 3.4 points from 2019 to 2020; in the typical rural county (no town of 5,000 people)\n"
             "it rose 1.8 points, and some rural counties saw no rise at all. The biggest dots, the largest labor markets, sit far to the right\n"
             "(Los Angeles +7.8, Cook +6.7). Right: by 2022 every group's typical county was at or slightly below its 2019 rate: the urban penalty did not last.\n"
             "Both panels share the same horizontal scale; dots beyond the axis range are pinned to the edge. Data: USDA ERS county-level data sets (BLS LAUS), via CS765 765Data repository.")
save(fig, "q2b_unemployment_county_strips.png")
