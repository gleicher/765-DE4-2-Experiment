"""Q1 alternate: regional trajectories in (overall life expectancy, female-male gap) space."""
import matplotlib.pyplot as plt
import numpy as np

from common import *

style()
w = load_worldbank()

REGIONS = {
    "North America": ("North America", ORANGE),
    "Europe & Central Asia": ("Europe & Central Asia", YELLOW),
    "South Asia": ("South Asia", BLUE),
    "Middle East, North Africa, Afghanistan & Pakistan": ("Middle East & N. Africa*", AQUA),
    "East Asia & Pacific": ("East Asia & Pacific", GRAY),
    "Latin America & Caribbean": ("Latin America & Caribbean", GRAY),
    "Sub-Saharan Africa": ("Sub-Saharan Africa", GRAY),
}

fig = plt.figure(figsize=(11, 7.6))
ax = fig.add_axes([0.07, 0.2, 0.66, 0.65])

# background: every individual country in 2023 (faint), for context
ctry = w[~w["Country Code"].isin(WB_AGGREGATES) & (w["Year"] == 2023)].dropna(subset=["Both", "gap"])
ax.scatter(ctry["Both"], ctry["gap"], s=11, color=LIGHTGRAY, edgecolor="none", zorder=1)

def smooth(s, k=5):
    """Centered 5-year rolling mean to suppress one-year spikes (wars, data jumps)."""
    return s.rolling(k, center=True, min_periods=1).mean()

end_pts = {}
for name, (lab, col) in REGIONS.items():
    r = w[w["Country Name"] == name].set_index("Year").sort_index()
    x, y = smooth(r["Both"]), smooth(r["gap"])
    emph = col != GRAY
    ax.plot(x, y, color=col, lw=2.2 if emph else 1.3, zorder=3 if emph else 2,
            solid_capstyle="round")
    # decade ticks along each path
    dec = [yr for yr in (1970, 1980, 1990, 2000, 2010) if yr in x.index]
    ax.scatter(x[dec], y[dec], s=9, color=col, zorder=4, edgecolor="white", linewidth=0.4)
    ax.scatter([x.iloc[0]], [y.iloc[0]], s=34, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
    ax.scatter([x.iloc[-1]], [y.iloc[-1]], s=40, color=col, zorder=5)
    end_pts[name] = (x.iloc[-1], y.iloc[-1], x.iloc[0], y.iloc[0])

# label each trajectory at its 2023 end
offsets = {
    "North America": (0.6, -0.15), "Europe & Central Asia": (0.6, 0.45),
    "South Asia": (0.6, -0.2), "Middle East, North Africa, Afghanistan & Pakistan": (0.6, -0.45),
    "East Asia & Pacific": (0.6, 0.0), "Latin America & Caribbean": (-0.4, 0.45),
    "Sub-Saharan Africa": (0.6, 0.15),
}
LEADER = {"Latin America & Caribbean": (64.5, 7.3), "East Asia & Pacific": (81.5, 5.95)}
for name, (lab, col) in REGIONS.items():
    x1, y1, x0, y0 = end_pts[name]
    dx, dy = offsets[name]
    if name in LEADER:
        tx, ty = LEADER[name]
        ax.annotate(lab, xy=(x1, y1), xytext=(tx, ty), fontsize=8.8, color=INK2, va="center",
                    ha="right" if tx < x1 else "left",
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6, shrinkB=4))
        continue
    ax.text(x1 + dx, y1 + dy, lab, fontsize=9.5 if col != GRAY else 8.8,
            color=INK if col != GRAY else INK2, va="center",
            ha="right" if dx < 0 else "left")

ax.axhline(0, color=GRAY, lw=0.8, zorder=1)
ax.text(31.5, -0.35, "Men outlive women below this line", fontsize=8.5, color=INK2, va="top")

# key for markers
kx, ky = 31.5, 13.4
ax.scatter([kx], [ky], s=34, facecolor="white", edgecolor=INK2, lw=1.5)
ax.text(kx + 0.7, ky, "1960", fontsize=8.5, va="center", color=INK2)
ax.scatter([kx + 5.2], [ky], s=9, color=INK2)
ax.text(kx + 5.9, ky, "1970, 1980 ... 2010", fontsize=8.5, va="center", color=INK2)
ax.scatter([kx + 16.6], [ky], s=40, color=INK2)
ax.text(kx + 17.3, ky, "2023", fontsize=8.5, va="center", color=INK2)
ax.scatter([kx + 22], [ky], s=11, color=LIGHTGRAY)
ax.text(kx + 22.7, ky, "individual countries, 2023", fontsize=8.5, va="center", color=INK2)

# story annotations
ax.annotate("Rich regions arrived first and are\nnow moving down: the gap shrinks\nas men's lives lengthen faster",
            xy=(76.2, 7.25), xytext=(80, 10.2), fontsize=9, color=INK, ha="left",
            arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.8, mutation_scale=8,
                            connectionstyle="arc3,rad=-0.2"))
ax.annotate("Poorer regions climb up and to the\nright: the gap opens as life\nexpectancy rises",
            xy=(59.3, 1.45), xytext=(42, 5.6), fontsize=9, color=INK, ha="left",
            arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.8, mutation_scale=8,
                            connectionstyle="arc3,rad=0.2"))
ru = ctry[ctry["Country Name"].isin(["Russian Federation", "Ukraine", "Belarus", "West Bank and Gaza", "Latvia"])]
for _, r in ru.iterrows():
    nm = {"Russian Federation": "Russia", "West Bank and Gaza": "West Bank & Gaza"}.get(r["Country Name"], r["Country Name"])
    ax.text(r["Both"] - 0.5, r["gap"], nm, fontsize=7.5, color=INK2, ha="right", va="center")

ax.set_xlim(30, 92)
ax.set_ylim(-2.2, 14)
ax.set_xlabel("Life expectancy at birth, both sexes (years)")
ax.set_ylabel("Female minus male life expectancy (years)")
ax.grid(True)
ax.set_axisbelow(True)

title_block(fig, "As life expectancy rises, women's advantage first grows, then shrinks",
            "Paths of World Bank regions, 1960-2023. Every region has moved right (longer lives), "
            "but the gap rises at first and falls only in the longest-lived regions.")
caption(fig,
        "Each path traces one World Bank region from 1960 (open circle) to 2023 (filled circle; 2021-23 average); small dots mark "
        "each decade. Paths are smoothed with a centered 5-year moving average so single-year spikes (wars, "
        "famines) don't dominate. Vertical position is the female-minus-male gap; horizontal position is life "
        "expectancy for both sexes combined. Gray dots are individual countries in 2023 (unsmoothed); the highest "
        "outliers are former Soviet states and places at war in 2023 (Ukraine, West Bank & Gaza). *\"Middle East, North Africa, Afghanistan & Pakistan\" in the data.\n"
        "Data: World Bank life expectancy at birth by sex, 1960-2023 (CS765 lifespan_dataset_1960.csv).",
        chars=165)
fig.savefig(FIG / "q1b_gap_trajectories.png")
print("saved")
