"""Q1 primary: female-minus-male life expectancy gap by World Bank region, 1960-2023."""
import matplotlib.pyplot as plt

from common import *

style()
w = load_worldbank()

REGIONS = {  # name in data -> (label, color, emphasis)
    "North America": ("North America", ORANGE, True),
    "Europe & Central Asia": ("Europe & Central Asia", YELLOW, True),
    "South Asia": ("South Asia", BLUE, True),
    "Middle East, North Africa, Afghanistan & Pakistan": ("Middle East & N. Africa*", AQUA, True),
    "East Asia & Pacific": ("East Asia & Pacific", GRAY, False),
    "Latin America & Caribbean": ("Latin America & Caribbean", GRAY, False),
    "Sub-Saharan Africa": ("Sub-Saharan Africa", GRAY, False),
    "World": ("World", INK, True),
}

g = w[w["Country Name"].isin(REGIONS)].pivot(index="Year", columns="Country Name", values="gap")
g.to_csv(Path(__file__).parent / "out_fig1_gap_by_region.csv", float_format="%.2f")

fig = plt.figure(figsize=(11, 7.4))
ax = fig.add_axes([0.07, 0.2, 0.70, 0.67])

ax.axhspan(-2.5, 0, color="#f3f2ee", zorder=0)
ax.axhline(0, color=GRAY, lw=0.8, zorder=1)
ax.text(2008, -2.2, "Below zero: men outlive women", fontsize=8.5, color=INK2, va="bottom")
ax.axvspan(2019.5, 2021.5, color="#f3f2ee", zorder=0)
ax.text(2020.5, 9.35, "COVID-19", fontsize=8, color=INK2, ha="center")

# context lines first, then emphasized lines on top
order = [k for k, v in REGIONS.items() if not v[2]] + [k for k, v in REGIONS.items() if v[2]]
label_y = {}
for name in order:
    lab, col, emph = REGIONS[name]
    s = g[name]
    lw = 2.4 if name == "World" else (2.0 if emph else 1.2)
    ax.plot(s.index, s.values, color=col, lw=lw, zorder=3 if emph else 2,
            solid_capstyle="round")
    ax.plot(s.index[-1], s.values[-1], "o", ms=4.5 if emph else 3.5, color=col, zorder=4)
    label_y[name] = s.values[-1]

# direct labels at right end, nudged apart to avoid collisions
nudges = {"North America": 0.0, "Europe & Central Asia": 0.3, "East Asia & Pacific": 0.15,
          "Latin America & Caribbean": -0.15, "World": -0.05, "Sub-Saharan Africa": 0.05,
          "Middle East, North Africa, Afghanistan & Pakistan": 0.0, "South Asia": -0.25}
# resolve stacking manually: sort by end value then enforce min spacing
items = sorted(label_y.items(), key=lambda kv: kv[1])
placed = []
for name, y in items:
    y = y + nudges.get(name, 0)
    if placed and y - placed[-1][1] < 0.36:
        y = placed[-1][1] + 0.36
    placed.append((name, y))
for name, y in placed:
    lab, col, emph = REGIONS[name]
    txt = f"{lab}  {label_y[name]:.1f}"
    ax.text(2024.3, y, txt, fontsize=9.5 if emph else 8.8, va="center",
            color=INK if emph else INK2, fontweight="bold" if name == "World" else "normal")
    ax.plot([2023.2, 2024.1], [label_y[name], y], color=col, lw=0.7)

# annotations telling the story (describe plateaus rather than one-year spikes)
na = g["North America"]
ax.annotate(f"North America: ~{na.loc[1970:1979].mean():.1f} yrs through the 1970s,\n"
            f"{na.loc[2023]:.1f} yrs by 2023",
            xy=(1976, na.loc[1976]), xytext=(1963, 9.0), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
eu = g["Europe & Central Asia"]
ax.annotate(f"Europe & Central Asia: ~{eu.loc[1990:1999].mean():.1f} yrs in the 1990s\n"
            "(post-Soviet spike in male deaths)",
            xy=(1994, eu.loc[1994]), xytext=(1996, 9.0), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
sa = g["South Asia"]
neg_years = sa[sa <= 0].index
cross = int(neg_years.max()) + 1  # first year after which the gap stays positive
ax.annotate(f"South Asia: men outlived women until {cross - 1};\n"
            f"women now live {sa.loc[2023]:.1f} yrs longer",
            xy=(cross, sa.loc[cross]), xytext=(1987, -1.6), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
ax.annotate("1971 spike:\nBangladesh war", xy=(1971, sa.loc[1971]), xytext=(1972.2, -0.75),
            fontsize=8, color=INK2, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
me = g["Middle East, North Africa, Afghanistan & Pakistan"]
ax.annotate(f"Middle East & N. Africa:\n{me.loc[1960]:.1f} yrs in 1960", xy=(1960.3, me.loc[1960]),
            xytext=(1962, 2.0), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
ssa = g["Sub-Saharan Africa"]
lo = ssa.loc[1995:2010].idxmin()
ax.annotate("Sub-Saharan Africa dips\nduring the HIV/AIDS era",
            xy=(lo, ssa[lo]), xytext=(2003, 1.2), fontsize=8.5, color=INK2,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
regs7 = [k for k in REGIONS if k != "World"]
sp60 = g.loc[1960, regs7].max() - g.loc[1960, regs7].min()
sp23 = g.loc[2023, regs7].max() - g.loc[2023, regs7].min()

ax.set_xlim(1960, 2023.2)
ax.set_ylim(-2.5, 9.8)
ax.set_yticks(range(-2, 10, 2))
ax.set_ylabel("Female minus male life expectancy at birth (years)")
ax.grid(axis="y")
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

title_block(fig, "The gap between women's and men's life expectancy is converging",
            "Where women's advantage was largest (North America, Europe) it is shrinking; where it was "
            "smallest (South Asia, Middle East) it has grown.\n"
            f"The spread between regions fell from {sp60:.1f} years in 1960 to {sp23:.1f} years in 2023.")
caption(fig,
        "Each line is the difference between female and male life expectancy at birth for a World Bank "
        "region (population-weighted aggregate as published by the World Bank); the black line is the world. "
        "Colored lines are the four regions that moved most; the others are gray for context. Values at right "
        "are 2023. *Region is \"Middle East, North Africa, Afghanistan & Pakistan\" in the data.\n"
        "Data: World Bank life expectancy at birth by sex, 1960-2023 (CS765 lifespan_dataset_1960.csv).",
        chars=165)
fig.savefig(FIG / "q1a_gap_lines.png")
print("saved")
