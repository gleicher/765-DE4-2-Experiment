from common import *

w = life_wide()
g = w.pivot(index="Year", columns="Country Code", values="gap")
rows = []
for name, gr in GROUPS.items():
    for k in sorted(gr["codes"], key=lambda k: -g.loc[2023, k]):
        rows.append((name, k, g.loc[1960, k], g.loc[2023, k], gr["color"]))
fig, ax = plt.subplots(figsize=(11, 10))
fig.subplots_adjust(left=0.19, right=0.95, top=0.80, bottom=0.17)
y = 0; yt = []; yl = []; headers = []; prev = None
for name, k, a, b, col in rows:
    if prev is not None and name != prev: y += 1.3
    if name != prev: headers.append((y, name, col))
    prev = name
    ax.plot([a, b], [y, y], color=col, lw=2.6, alpha=0.55, solid_capstyle="round", zorder=2)
    ax.scatter([a], [y], s=48, facecolor="white", edgecolor=col, lw=1.8, zorder=3)
    ax.scatter([b], [y], s=62, color=col, zorder=4)
    ax.text(max(a, b) + 0.4, y, f"{b-a:+.1f}", fontsize=9, color=col, va="center", ha="left")
    yt.append(y); yl.append(SHORT[k]); y += 1
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=10.5)
ax.set_ylim(y, -1.8)
for yy, name, col in headers:
    ax.text(-0.01, yy - 0.95, name.upper(), transform=ax.get_yaxis_transform(), fontsize=9.5, fontweight="bold", color=col, ha="right", va="center", clip_on=False)
ax.axvline(0, color=INK, lw=1.1, zorder=1)
ax.set_xlim(-5, 15.5); ax.set_xticks(range(-4, 16, 2))
ax.grid(axis="x", color=GRID, lw=0.7, zorder=0); ax.set_axisbelow(True)
ax.tick_params(length=0); ax.spines["left"].set_visible(False)
ax.set_xlabel("Years women outlive men (female minus male life expectancy at birth)", fontsize=11)
ax.scatter([9.4], [-1.1], s=48, facecolor="white", edgecolor=MUTED, lw=1.8); ax.text(9.8, -1.1, "1960", va="center", fontsize=9.5, color=MUTED)
ax.scatter([11.4], [-1.1], s=62, color=MUTED); ax.text(11.8, -1.1, "2023", va="center", fontsize=9.5, color=MUTED)
ax.text(13.1, -1.1, "number = change", va="center", fontsize=9.5, color=MUTED)
frame(fig, "Half a century on, the sex gap in lifespan has moved\nin opposite directions in different parts of the world",
      "Gap in life expectancy at birth (women minus men), 1960 vs 2023, for 25 countries in four groups.\nWithin each group countries are sorted by their 2023 gap.",
      caption=("Open circle = 1960, filled circle = 2023, number = change in years. Post-Soviet gaps are larger than in 1960 (Ukraine 2023: 13.3 years, a war year);\n"
               "in wealthy countries the gap rose in Japan and S. Korea but fell in most others; South Asian women went from living shorter lives than men to 3-5 years longer;\n"
               "Gulf and West African gaps shrank to 0.4-2.2 years. Groupings are descriptive labels chosen by the author."),
      source="Data: World Bank life expectancy at birth (SP.DYN.LE00.IN), course file lifespan_dataset_1960.csv.", top=0.985)
save(fig, "q1_fig2_gap_dumbbell.png")
