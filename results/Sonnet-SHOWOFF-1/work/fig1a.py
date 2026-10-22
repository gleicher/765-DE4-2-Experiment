from common import *

w = life_wide()
g = w.pivot(index="Year", columns="Country Code", values="gap")
noisy = g.diff().abs().max() > 2.5
bg = g.loc[:, ~noisy | g.columns.isin(sum([x["codes"] for x in GROUPS.values()], []))]
fig, axs = plt.subplots(2, 2, figsize=(12.5, 9.2), sharex=True, sharey=True)
fig.subplots_adjust(left=0.065, right=0.925, top=0.79, bottom=0.145, hspace=0.22, wspace=0.10)

for ax, (name, gr) in zip(axs.flat, GROUPS.items()):
    for k in bg.columns:
        ax.plot(bg.index, bg[k], color=FAINT, lw=0.7, alpha=0.5, zorder=1)
    ax.plot(g.index, g.median(axis=1), color=MUTED, lw=1.6, ls=(0, (4, 2)), zorder=2)
    ax.axhline(0, color=INK, lw=1.0, zorder=2)
    ends = []
    for k in gr["codes"]:
        s = g[k].dropna()
        ax.plot(s.index, s.values, color=gr["color"], lw=2.0, zorder=3)
        ends.append((k, s.iloc[-1]))
    ys = spread([e[1] for e in ends], 0.95)
    for (k, y0), y in zip(ends, ys):
        ax.text(2024.3, y, SHORT[k], color=gr["color"], fontsize=9.5, va="center", fontweight="bold", clip_on=False)
    ax.set_title(name, fontsize=13.5, fontweight="bold", color=gr["color"], pad=22)
    ax.text(0, 1.015, gr["blurb"].replace("\n", " "), transform=ax.transAxes, fontsize=9.3, color=MUTED, va="bottom")
    ax.set_xlim(1960, 2023); ax.set_ylim(-4.5, 15)
    ax.set_yticks([-4, 0, 4, 8, 12]); ax.set_xticks([1960, 1980, 2000, 2020])
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
    ax.tick_params(length=0, labelsize=10)
    ax.spines["left"].set_visible(False)
    ax.text(1961, 0.35, "men = women", fontsize=8.3, color=INK, style="italic")
    if name == "Post-Soviet states":
        ax.annotate("Russia peaks:\n14.2 yrs in 1994", xy=(1994, 14.2), xytext=(1962, 14.0), fontsize=8.6, color=gr["color"],
                    arrowprops=dict(arrowstyle="-", color=gr["color"], lw=0.8), va="center")
    if name == "South Asia":
        ax.annotate("Pakistan: men outlived\nwomen by 4 yrs in 1960", xy=(1960, -4.0), xytext=(1976, -3.5), fontsize=8.6,
                    color=gr["color"], va="center", arrowprops=dict(arrowstyle="-", color=gr["color"], lw=0.8))

for ax in axs[:, 0]: ax.set_ylabel("Years women outlive men", fontsize=10.5)
# legend for the backdrop
fig.text(0.065, 0.118, "", fontsize=9)
frame(fig, "Women outlive men almost everywhere, but the size of that edge\nhas followed four very different paths",
      "Female minus male life expectancy at birth, 1960-2023. In each panel the colored lines are the highlighted countries; "
      "grey lines are about 200 other countries;\nthe dashed line is the median country.",
      caption=("Reading the chart: a line above the black zero line means women live longer. The 'average' story hides at least four regimes. "
               "Post-Soviet men suffered a mortality collapse in the 1990s (gap > 11 yrs);\nin wealthy countries men's survival caught up after the 1980s; "
               "in South Asia women moved from disadvantage to advantage; in the Gulf and West Africa the gap is almost gone.\n"
               "Countries chosen to illustrate each pattern; panel groupings are my own descriptive labels, not a World Bank classification."),
      source="Data: World Bank life expectancy at birth (SP.DYN.LE00.IN), course file lifespan_dataset_1960.csv; regional/income aggregates excluded.",
      top=0.985)
save(fig, "q1_fig1_gap_small_multiples.png")
