"""Story 4: where did domestic migrants go in 2021-23? County size vs net domestic migration."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from common import *
style()
c = census()
c["rucc"] = c["2023 Rural-urban Continuum Code"]
c = c.dropna(subset=["rucc"])
pop = "Census Population 2020"
c["mig"] = sum(c[f"Domestic migration {y}"] for y in (2021, 2022, 2023))
c = c.dropna(subset=["mig", pop])
c["rate"] = c.mig / c[pop] * 1000
grp = {1: "Metro area 1M+", 2: "Smaller metro area", 3: "Smaller metro area", 4: "Nonmetro, urban (20k+)", 5: "Nonmetro, urban (20k+)"}
c["grp"] = c.rucc.map(lambda r: grp.get(r, "Nonmetro, small town / rural (<20k)"))
order = ["Metro area 1M+", "Smaller metro area", "Nonmetro, urban (20k+)", "Nonmetro, small town / rural (<20k)"]
colors = dict(zip(order, [BLUE, GREEN, ORANGE, PURPLE]))
tot = c.groupby("grp").apply(lambda d: d.mig.sum() / d[pop].sum() * 1000).loc[order]
net = c.groupby("grp").mig.sum().loc[order]
print(tot, net)
print(c.nlargest(6, "mig")[["Area name", "State", "mig", "rate"]]); print(c.nsmallest(8, "mig")[["Area name", "State", "mig", "rate"]])
print(c.groupby("grp").rate.median())

fig = plt.figure(figsize=(12, 6.6))
gs = fig.add_gridspec(1, 2, width_ratios=[2.5, 1], wspace=0.28)
ax = fig.add_subplot(gs[0]); bx = fig.add_subplot(gs[1])
ax.axhline(0, color="#777777", lw=1)
for g in order:
    s = c[c.grp == g]
    ax.scatter(s[pop], s.rate.clip(-150, 250), s=10, color=colors[g], alpha=.35, lw=0, label=g)
# binned medians
bins = np.logspace(np.log10(c[pop].min()), np.log10(c[pop].max()), 13)
c["bin"] = pd.cut(c[pop], bins)
m = c.groupby("bin", observed=True).agg(x=(pop, "median"), y=("rate", "median"), n=("rate", "size"))
m = m[m.n >= 8]
ax.plot(m.x, m.y, color="#111111", lw=2.2, marker="o", ms=4, label="Median of all counties (by size band)", zorder=5)
ax.set_xscale("log"); ax.set_ylim(-60, 200)
ax.set_xlabel("County population, 2020 (log scale)")
ax.set_ylabel("Net domestic migration, 2021-23\n(people per 1,000 residents)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
lab = {"Los Angeles County": (-30, 9), "Cook County": (-40, -4), "Maricopa County": (5, 3), "Harris County": (6, -3)}
for nm, (dx, dy) in lab.items():
    r = c[(c["Area name"] == nm)]
    if len(r) == 0: continue
    r = r.sort_values(pop).iloc[-1]
    ax.annotate(nm.replace(" County", ""), (r[pop], r.rate), xytext=(dx, dy), textcoords="offset points", fontsize=8.5)
    ax.scatter(r[pop], r.rate, s=22, facecolor="none", edgecolor="#222222", lw=1, zorder=6)
ax.legend(loc="upper left", fontsize=8.5, frameon=False, markerscale=1.8)
ax.set_title("Each dot is a county (n = %d)" % len(c), loc="left", fontsize=10, color="#444444", fontweight="normal")
# bar panel: by county size band (all residents combined)
edges = [0, 25e3, 100e3, 500e3, 1e6, 1e9]
names = ["Under 25k", "25k-100k", "100k-500k", "500k-1M", "1M+"]
c["size"] = pd.cut(c[pop], edges, labels=names)
sz = c.groupby("size", observed=True).apply(lambda d: d.mig.sum() / d[pop].sum() * 1000)
cnt = c.groupby("size", observed=True).size()
print(sz, cnt)
yy = np.arange(len(names))[::-1]
bx.barh(yy, sz.values, color=[ORANGE if v < 0 else BLUE for v in sz.values], height=.6)
bx.axvline(0, color="#555555", lw=1)
for yv, v in zip(yy, sz.values):
    bx.text(v + 1 if v >= 0 else 1, yv, f"{v:+.0f}", va="center", ha="left", fontsize=10, fontweight="bold", color=ORANGE if v < 0 else BLUE)
bx.set_yticks(yy); bx.set_yticklabels([f"{n}\n({k:,} counties)" for n, k in zip(names, cnt)], fontsize=9)
bx.set_xlim(-30, 30); bx.set_xlabel("Net migration per 1,000 residents")
bx.set_title("All residents combined, by county size", loc="left", fontsize=10, color="#444444", fontweight="normal")
fig.suptitle("Since 2020, the biggest counties lost residents to domestic moves while mid-sized and small ones gained",
             x=0.02, ha="left", fontsize=13.5, fontweight="bold", y=1.0)
fig.text(0.02, -0.02,
         "Net domestic migration = people arriving from elsewhere in the US minus people leaving, July 2020 - June 2023, per 1,000 residents in the 2020 Census. Counties of 1M+ people\n"
         "(Los Angeles, Cook, Brooklyn, Queens, the Bronx) lost most; the fastest growers are mid-sized suburban and exurban counties in the Sun Belt. Metropolitan suburbs, not just\n"
         "rural places, absorbed the movers. International migration is excluded; dots outside the axis range are not shown. Colors show the USDA metro/nonmetro type of the county. Data: Census/USDA ERS county estimates via course file.",
         fontsize=9, color="#444444", va="top")
save(fig, "q4_migration.png")
