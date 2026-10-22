"""Figure 2a: diverging stacked bars of population-change components by urban-rural class."""
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from common import setup_style, FIG, INK, INK2, MUTED, BLUE, ORANGE, AQUA
from q2_data import cumulative_rates, COMP

setup_style()
c = cumulative_rates()
names = list(COMP)
COL = {names[0]: AQUA, names[1]: BLUE, names[2]: ORANGE}

fig, ax = plt.subplots(figsize=(11, 7.4))
ypos = {1: 0, 2: 1, 3: 2, 4: 3.6, 5: 4.6, 6: 5.6, 7: 6.6, 8: 7.6, 9: 8.6}
H = 0.62
for k, r in c.iterrows():
    y = ypos[k]
    pos, neg = 0.0, 0.0
    for n in names:
        v = r[n]
        if v >= 0:
            ax.barh(y, v, left=pos, height=H, color=COL[n], edgecolor="white", linewidth=1.5)
            pos += v
        else:
            ax.barh(y, v, left=neg, height=H, color=COL[n], edgecolor="white", linewidth=1.5)
            neg += v
    net = sum(r[n] for n in names)
    ax.plot([net], [y], marker="D", color=INK, ms=7, mec="white", mew=1.2, zorder=5)
    ax.text(41, y, (f"{net:+.0f}".replace("-", "−") if round(net) != 0 else "0"), ha="right", va="center", fontsize=10.5,
            fontweight="bold", color=INK)
    ax.text(-34.5, y - 0.08, r.label, ha="left", va="center", fontsize=9.6, color=INK)
    ax.text(-34.5, y + 0.27, f"{r.counties} counties · {r.pop2023/1e6:.1f}M people",
            ha="left", va="center", fontsize=7.8, color=MUTED)

ax.axvline(0, color=INK2, lw=0.9)
ax.set_ylim(9.2, -1.3)
ax.set_xlim(-35, 42)
ax.set_yticks([])
ax.set_xticks(range(-15, 31, 5))
ax.grid(axis="y", visible=False)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Population change, July 2020 – June 2023, per 1,000 residents (2020 population)")
ax.text(41, -0.85, "net\nchange", ha="right", va="bottom", fontsize=8.5, color=INK2)
ax.text(-34.5, -0.62, "METRO COUNTIES", fontsize=8.5, fontweight="bold", color=INK2)
ax.text(-34.5, 3.0, "NONMETRO COUNTIES (by size of largest town; adjacent to a metro or not)",
        fontsize=8.5, fontweight="bold", color=INK2)
ax.text(-1, -0.9, "← losing people", ha="right", fontsize=8.5, color=MUTED)
ax.text(1, -0.9, "gaining people →", ha="left", fontsize=8.5, color=MUTED)

# call-outs
ax.text(18.6, 0.0, "Loses 10 per 1,000 to other parts of the US,\ngains 17 from births and immigrants",
        fontsize=8.6, color=INK2, va="center")
ax.text(5.2, 4.6, "Remote counties (not adjacent to a metro) attract far\nfewer movers than similar counties next to a metro",
        fontsize=8.6, color=INK2, va="center")
ax.text(13.3, 8.6, "Deaths exceed births by 14 per 1,000; newcomers\nfrom elsewhere in the US offset most of the loss",
        fontsize=8.6, color=INK2, va="center")

handles = [Patch(color=COL[n], label=n) for n in names] + [
    Line2D([], [], marker="D", ls="", color=INK, mec="white", ms=7, label="Net change (sum of the three)")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=4,
          frameon=False, fontsize=9, handlelength=1.2, columnspacing=1.4)

fig.suptitle("America's largest metros grow from births and immigrants; its rural counties depend on movers",
             x=0.01, ha="left", y=0.985, fontsize=15, fontweight="bold")
fig.text(0.01, 0.938,
         "Where each type of county's population change came from, July 2020 – June 2023. Big metros (1M+) lost 10 residents per 1,000 to\n"
         "domestic migration; small-town and rural counties lost 8–15 per 1,000 to deaths outnumbering births, and gained mostly from people moving in.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "Counties grouped by the USDA 2023 Rural-Urban Continuum Code. Rates are population-weighted (group total ÷ group population in July 2020).\n"
         "Census estimate 'residuals' not shown. 50 states + DC; Puerto Rico excluded. Data: USDA ERS county-level data sets (CS765 census dataset).",
         fontsize=8.3, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.02, right=0.98, top=0.85, bottom=0.17)
fig.savefig(FIG / "q2a_population_change_components_bars.png")
