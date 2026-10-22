"""Figure 2b: heatmap of annual population-change components by urban-rural class and year."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from common import setup_style, FIG, INK, INK2, MUTED
from q2_data import annual_rates, COMP, YEARS

setup_style()
a = annual_rates()
SHORT_ROWS = ["Metro, 1 million+", "Metro, 250k–1M", "Metro, under 250k",
              "Town 20k+, next to metro", "Town 20k+, remote",
              "Town 5k–20k, next to metro", "Town 5k–20k, remote",
              "Rural (<5k), next to metro", "Rural (<5k), remote"]
comps = list(COMP)
HEAD = ["Natural change\n(births − deaths)", "Domestic migration\n(moves within the US)",
        "International\nmigration", "Net change\n(sum of the three)"]

M = np.zeros((9, 12))
for j, comp in enumerate(comps):
    for k, y in enumerate(YEARS):
        s = a[(a.component == comp) & (a.year == y)].set_index("rucc").rate
        M[:, j * 3 + k] = s.sort_index().values
for k in range(3):
    M[:, 9 + k] = M[:, k] + M[:, 3 + k] + M[:, 6 + k]

# diverging: orange = losing people, blue = gaining, light gray midpoint
cmap = LinearSegmentedColormap.from_list("div", ["#b4441a", "#eb6834", "#f6c2a6", "#f2f1ee",
                                                 "#9ec5f4", "#2a78d6", "#104281"])
norm = TwoSlopeNorm(vmin=-9, vcenter=0, vmax=9)

fig, ax = plt.subplots(figsize=(11, 7.2))
X = np.array([0, 1, 2, 3.4, 4.4, 5.4, 6.8, 7.8, 8.8, 10.4, 11.4, 12.4])
for j in range(12):
    for i in range(9):
        v = M[i, j]
        ax.add_patch(plt.Rectangle((X[j] - 0.48, i - 0.46), 0.96, 0.92,
                                   color=cmap(norm(np.clip(v, -9, 9))), lw=0))
        txt = f"{v:+.1f}".replace("-", "−") if abs(v) >= 0.05 else "0.0"
        dark = abs(v) > 5.5
        ax.text(X[j], i, txt, ha="center", va="center", fontsize=8.6,
                color="white" if dark else INK, fontweight="bold" if j >= 9 else "normal")
ax.set_xlim(-0.6, 13.0)
ax.set_ylim(8.6, -2.0)
ax.set_yticks(range(9), SHORT_ROWS, fontsize=9.6)
ax.set_xticks([])
for j in range(12):
    ax.text(X[j], -0.68, str(YEARS[j % 3]), ha="center", va="center", fontsize=8.5, color=INK2)
ax.grid(False)
for sp in ax.spines.values():
    sp.set_visible(False)
for j, h in enumerate(HEAD):
    ax.text(X[j * 3 + 1], -1.45, h, ha="center", va="center", fontsize=9.5, fontweight="bold", color=INK)
ax.axhline(2.5, color=INK2, lw=0.8, xmin=-0.3, clip_on=False)
ax.text(-4.0, 1.0, "METRO", rotation=90, ha="center", va="center", fontsize=8.5, color=INK2,
        fontweight="bold", transform=ax.transData, clip_on=False)
ax.text(-4.0, 5.5, "NONMETRO", rotation=90, ha="center", va="center", fontsize=8.5, color=INK2,
        fontweight="bold", clip_on=False)

# colorbar
cax = fig.add_axes([0.30, 0.085, 0.42, 0.022])
grad = np.linspace(-9, 9, 256)[None, :]
cax.imshow(grad, aspect="auto", cmap=cmap, norm=norm, extent=[-9, 9, 0, 1])
cax.set_yticks([]); cax.set_xticks([-9, -6, -3, 0, 3, 6, 9], ["≤−9", "−6", "−3", "0", "+3", "+6", "≥+9"], fontsize=8.5)
for sp in cax.spines.values():
    sp.set_visible(False)
cax.grid(False)
cax.set_title("Change per 1,000 residents per year     ← losing people  ·  gaining people →",
              fontsize=8.8, color=INK2, pad=4)

fig.suptitle("Three years, same pattern: big metros lose movers, rural counties lose to deaths",
             x=0.01, ha="left", y=0.985, fontsize=15, fontweight="bold")
fig.text(0.01, 0.94,
         "Annual components of population change by county type, per 1,000 residents. The 1M+ metros lose people to domestic\n"
         "migration every year and rely on births and fast-rising immigration; every nonmetro group has more deaths than births\n"
         "every year, and the groups next to a metro gain the most from people moving in.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "Census years run July–June (2021 = July 2020 – June 2021). Rows: USDA 2023 Rural-Urban Continuum Codes 1–9 ('town' = size of the county's\n"
         "urban population; 'next to metro' = adjacent to a metro area). Rates are population-weighted. 50 states + DC. Data: USDA ERS (CS765 census dataset).",
         fontsize=8.3, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.215, right=0.985, top=0.83, bottom=0.17)
fig.savefig(FIG / "q2b_population_change_components_heatmap.png")
print(np.round(M, 1))
