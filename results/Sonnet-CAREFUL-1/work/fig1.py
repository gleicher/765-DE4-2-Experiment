"""Story 1: has the female life-expectancy advantage shrunk or grown since 1960?
Produces q1_a (1960 vs 2023 scatter) and q1_b (trajectories over time)."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from common import *
style()
l = wb()
p = l.pivot_table(index=["country", "Year"], columns="Sex", values="le").reset_index()
p["gap"] = p.Female - p.Male
g60 = p[p.Year == 1960].set_index("country").gap
g23 = p[p.Year == 2023].set_index("country").gap
d = pd.DataFrame({"g60": g60, "g23": g23}).dropna()
d["chg"] = d.g23 - d.g60
print(len(d), (d.chg > 0).mean(), d.g60.median(), d.g23.median(), d.g23.min(), d.g23.max())

# ---------- Figure A: scatter 1960 vs 2023 ----------
fig, ax = plt.subplots(figsize=(9, 7.6))
lo, hi = -5, 14.5
ax.plot([lo, hi], [lo, hi], color="#999999", lw=1, ls="--", zorder=1)
ax.axhline(0, color="#cccccc", lw=0.8, zorder=0); ax.axvline(0, color="#cccccc", lw=0.8, zorder=0)
col = np.where(d.chg > 0.5, ORANGE, np.where(d.chg < -0.5, BLUE, "#B5B5B5"))
ax.scatter(d.g60, d.g23, c=col, s=34, alpha=.85, edgecolor="white", lw=.5, zorder=3)
lab = {"Ukraine": (5, 0), "Russian Federation": (6, -12), "Pakistan": (6, 0), "United States": (8, 0),
       "United Kingdom": (-10, -16), "Cameroon": (6, -3), "Japan": (-8, 8), "India": (6, -4),
       "Thailand": (6, 0), "China": (-30, -14), "Kazakhstan": (6, 2), "Georgia": (-52, 3),
       "Bangladesh": (-30, 8), "Mongolia": (6, 0), "Nigeria": (6, -10), "Isle of Man": (-30, 8)}
for k, (dx, dy) in lab.items():
    r = d.loc[k]
    ax.annotate(k.replace("Russian Federation", "Russia"), (r.g60, r.g23), xytext=(dx, dy),
                textcoords="offset points", fontsize=9, color=DARK, zorder=5)
ax.set_xlim(lo, hi); ax.set_ylim(-1, 14.5)
ax.set_xlabel("Female minus male life expectancy in 1960 (years)")
ax.set_ylabel("Female minus male life expectancy in 2023 (years)")
ax.text(-4.6, 12.7, "Gap WIDER in 2023", color=ORANGE, fontsize=11, fontweight="bold")
ax.text(9.5, 0.2, "Gap NARROWER in 2023", color=BLUE, fontsize=11, fontweight="bold")
ax.text(10.6, 11.6, "no change", color="#777777", fontsize=9, rotation=40)
n_w, n_n = (d.chg > .5).sum(), (d.chg < -.5).sum()
ax.text(-4.6, 11.7, f"{n_w} countries", color=ORANGE, fontsize=10)
ax.text(9.5, 1.1, f"{n_n} countries", color=BLUE, fontsize=10)
fig.suptitle("Women's life-expectancy edge widened in most countries since 1960, but narrowed in 55",
             x=0.02, ha="left", fontsize=13.5, fontweight="bold", y=0.99)
ax.set_title("Each dot is one country (n = %d). Orange/blue: gap changed by more than 0.5 years." % len(d),
             loc="left", fontsize=10, fontweight="normal", color="#444444")
fig.text(0.02, -0.02,
         "The typical (median) gap rose from 4.1 to 5.0 years. It grew most where women were disadvantaged in 1960 (India, Pakistan, Bangladesh) and in\n"
         "post-Soviet states (Ukraine, Russia); it shrank in the UK, US and several other high-income countries. Ukraine's 2022-23 jump coincides with the war.\n"
         "Data: World Bank life expectancy at birth by sex, 1960 and 2023; aggregates and regions excluded.",
         fontsize=9, color="#444444", va="top")
save(fig, "q1_a_gap_scatter.png")

# ---------- Figure B: trajectories ----------
fig, ax = plt.subplots(figsize=(10, 6.2))
q = p.groupby("Year").gap.quantile([.1, .5, .9]).unstack()
ax.fill_between(q.index, q[.1], q[.9], color="#E3E3E3", zorder=1, lw=0)
ax.plot(q.index, q[.5], color="#777777", lw=1.5, ls="--", zorder=2)
ax.text(1960.5, 3.0, "median country", fontsize=9, color="#666666")
ax.text(2003, 8.4, "middle 80% of countries", fontsize=9, color="#888888", rotation=0)
hl = {"Russian Federation": (ORANGE, "Russia"), "Ukraine": (PURPLE, "Ukraine"),
      "United States": (BLUE, "United States"), "United Kingdom": (GREEN, "United Kingdom"),
      "India": (RED, "India"), "Japan": ("#555555", "Japan")}
for k, (c, nm) in hl.items():
    s = p[p.country == k]
    ax.plot(s.Year, s.gap, color=c, lw=2.3, zorder=3)
    y = s.gap.iloc[-1]
    off = {"Japan": 0.45, "India": -0.5, "United Kingdom": -0.1, "United States": 0.25}.get(k, 0)
    ax.text(2023.8, y + off, nm, color=c, fontsize=10, va="center", fontweight="bold")
ax.axhline(0, color="#888888", lw=.8)
ax.set_xlim(1960, 2030); ax.set_ylim(-5, 15)
ax.set_xticks(range(1960, 2030, 10)); ax.set_xticks([1960,1970,1980,1990,2000,2010,2020])
ax.set_ylabel("Female minus male life expectancy (years)")
ax.text(2004, 0.3, "women live longer ↑", fontsize=9, color="#666666")
ax.text(2004, -0.4, "men live longer ↓", fontsize=9, color="#666666", va="top")
ax.annotate("Soviet collapse: male life\nexpectancy falls, gap peaks", xy=(1994, 14.0), xytext=(1963, 13.3),
            fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE))
ax.annotate("India (and Pakistan, Bangladesh):\nmen outlived women in 1960", xy=(1962, -1.3), xytext=(1968, -3.7),
            fontsize=9, color=RED, arrowprops=dict(arrowstyle="-", color=RED))
fig.suptitle("Women's life-expectancy edge: rising in India, falling in the US and UK, swinging in post-Soviet states",
             x=0.02, ha="left", fontsize=14, fontweight="bold", y=1.0)
ax.set_title("Gap in years over time. Gray band: middle 80%% of the %d countries; dashed: median." % p.country.nunique(),
             loc="left", fontsize=10, fontweight="normal", color="#444444")
fig.text(0.02, -0.015,
         "Gaps fell in the US and UK after the 1970s, rose in India as women's survival caught up, and swung with the 1990s mortality crisis in Russia and Ukraine.\n"
         "Data: World Bank life expectancy at birth by sex, 1960-2023.",
         fontsize=9, color="#444444", va="top")
save(fig, "q1_b_gap_lines.png")
