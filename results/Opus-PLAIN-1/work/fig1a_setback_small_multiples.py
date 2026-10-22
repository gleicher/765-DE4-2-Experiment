"""Figure 1a: small multiples showing how far back the pandemic pushed life expectancy."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from common import setup_style, FIG, INK, INK2, MUTED, ORANGE, BLUE, GRID
from q1_data import q1_table

setup_style()
t, p = q1_table()
t = t[t.country != "Central African Republic"]  # implausible series (31.5 -> 50.6 -> 18.8)
sel = (t[t.loss >= 2].sort_values(["yrs_erased", "loss"], ascending=False).head(16))
NAMES = {"St. Lucia": "St. Lucia", "Bosnia and Herzegovina": "Bosnia & Herz.",
         "Brunei Darussalam": "Brunei"}

fig, axes = plt.subplots(4, 4, figsize=(11, 10.2), sharex=True)
SPAN = 13  # every panel shows the same 13-year y-range so slopes are comparable
first = True
for ax, (_, r) in zip(axes.flat, sel.iterrows()):
    s = p.loc[r.country, 1975:2023]
    top = max(s.max(), r.le2023) + 1.8
    ax.set_ylim(top - SPAN, top)
    ax.set_xlim(1974, 2029)
    ax.plot(s.index, s.values, color=INK, lw=1.5, zorder=3)
    # pre-pandemic peak and trough
    ax.scatter([2019], [r.le2019], s=22, color=INK, zorder=4)
    ax.scatter([r.trough_year], [r.trough], s=28, color=ORANGE, zorder=5,
               edgecolor="white", linewidth=1)
    ax.scatter([2023], [r.le2023], s=22, color=BLUE, zorder=5, edgecolor="white", linewidth=0.8)
    # arrow from trough back in time to the year with the same life expectancy
    arr = FancyArrowPatch((r.trough_year - 0.6, r.trough), (r.setback_to, r.trough),
                          arrowstyle="-|>", mutation_scale=9, color=ORANGE, lw=1.3, zorder=4)
    ax.add_patch(arr)
    ax.text(r.setback_to + 0.5, r.trough - 0.35, f"back to {r.setback_to} level", ha="left",
            va="top", fontsize=8.3, color="#b8461a")
    name = NAMES.get(r.country, r.country)
    ax.text(0.0, 1.17, name, transform=ax.transAxes, fontsize=10.5, fontweight="bold",
            va="bottom", ha="left")
    ax.text(0.0, 1.03, f"lost {r.loss:.1f} yrs of life exp. = {r.yrs_erased} yrs of progress",
            transform=ax.transAxes, fontsize=7.8, color=INK2, va="bottom", ha="left")
    if first:
        ax.annotate("2019", (2019, r.le2019), xytext=(2003, r.le2019 + 1.5), fontsize=8,
                    color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
        ax.text(2024.2, r.le2023, "2023", fontsize=8, color=BLUE, va="center")
        ax.annotate("pandemic\nlow", (r.trough_year, r.trough), xytext=(2012, r.trough - 3.6),
                    fontsize=8, color="#b8461a", linespacing=0.95,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
        first = False
    ax.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax.tick_params(labelsize=8)
    ax.set_xticks([1980, 2000, 2020])
    ax.grid(axis="x", visible=False)

for ax in axes[:, 0]:
    ax.set_ylabel("Life expectancy (yrs)", fontsize=8.5)

fig.suptitle("COVID-19 pushed life expectancy back decades — and most countries won it back within two years",
             x=0.01, ha="left", y=0.995, fontsize=15.5, fontweight="bold")
fig.text(0.01, 0.955,
         "Life expectancy at birth, 1975–2023. Each orange arrow runs from the country's pandemic low (2020–22) back to the last year\n"
         "it was that low.  Black dot = 2019,  orange dot = pandemic low,  blue dot = 2023 — by 2023 most had climbed back to 2019 levels.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "Shown: the 16 countries (of 214 with data) that lost at least 2 years of life expectancy and were pushed back the furthest in time.\n"
         "Every panel spans the same 13 years of life expectancy, so slopes are comparable. Countries whose progress had stalled (Jamaica, Cuba)\n"
         "lose more 'years of progress' for the same drop.\nCentral African Republic omitted (implausible series). Data: World Bank, life expectancy at birth, both sexes (CS765 dataset).",
         fontsize=8.3, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.065, right=0.99, top=0.875, bottom=0.095, hspace=0.55, wspace=0.18)
fig.savefig(FIG / "q1a_pandemic_setback_small_multiples.png")
print(sel[["country", "loss", "yrs_erased", "setback_to", "rec"]].round(2).to_string())
