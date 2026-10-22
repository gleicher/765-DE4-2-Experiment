from common import *
d = load_census(); d['grp'] = d.rucc.map(grp_of)
b0 = "Percent of adults with a bachelor's degree or higher, 1990"; b1 = "Percent of adults with a bachelor's degree or higher, 2019-23"
d = d.dropna(subset=[b0, b1, 'grp']).copy()
d['gain'] = d[b1] - d[b0]
print(len(d), (d.gain<0).sum(), d.gain.min()); print(d.groupby('rucc')[[b0, b1, 'gain']].median().round(1))
fig = plt.figure(figsize=(13, 8.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1], wspace=0.30, left=0.065, right=0.97, top=0.80, bottom=0.16)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1])
lim = 82
ax.fill_between([0, lim], [0, lim], [lim, lim], color='#f3f4f6', zorder=0)
for gname, _ in GROUPS[::-1]:
    s = d[d.grp == gname].sort_values('Census Population 2020', ascending=False)
    ax.scatter(s[b0], s[b1], s=np.clip(s['Census Population 2020'] / 6000, 5, 260), color=GCOL[gname], alpha=0.42, lw=0.3, edgecolor='white', zorder=3, label=gname)
ax.plot([0, lim], [0, lim], color=INK2, lw=1, ls='--', zorder=4)
ax.plot([0, lim], [10, lim + 10], color=MUTED, lw=0.8, ls=':', zorder=4); ax.plot([0, lim], [20, lim + 20], color=MUTED, lw=0.8, ls=':', zorder=4)
for off, lab, col in [(0, 'no change', INK2), (10, '+10 pts', MUTED), (20, '+20 pts', MUTED)]:
    ax.text(53.5, 53.5 + off - 0.6, lab, rotation=32, color=col, fontsize=9, ha='right', va='top', rotation_mode='anchor')
top = d.sort_values(b1).tail(1).iloc[0]
ax.annotate(f"{top['Area name']}, {top['State']}", (top[b0], top[b1]), xytext=(top[b0] - 14, top[b1] - 4), fontsize=9, color=INK2, ha='right', arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_xlim(0, 56); ax.set_ylim(0, lim)
ax.set_xlabel("Adults with a bachelor's degree or higher, 1990 (% of county adults)")
ax.set_ylabel("Same measure, 2019-23 (%)"); clean_grid(ax, 'both')
ax.set_title('Every county (circle area = population)', loc='left', fontsize=12.5, color=INK)
from matplotlib.lines import Line2D
ax.legend([Line2D([], [], marker='o', ls='', color=GCOL[g], markersize=8, alpha=0.8) for g, _ in GROUPS], [g for g, _ in GROUPS], loc='lower right', frameon=False, fontsize=9.5, labelcolor=INK2, handletextpad=0.3, bbox_to_anchor=(1.0, 0.04))
# right: per-RUCC medians
names = {1: 'Metro, 1M+', 2: 'Metro, 250k-1M', 3: 'Metro, <250k', 4: 'Urban 20k+, adj.', 5: 'Urban 20k+, not adj.', 6: 'Urban 5-20k, adj.', 7: 'Urban 5-20k, not adj.', 8: 'Rural, adj.', 9: 'Rural, not adj.'}
med = d.groupby('rucc')[[b0, b1]].median()
for k in range(1, 10):
    r = med.loc[k]; col = GCOL[grp_of(k)]
    ax2.annotate('', xy=(r[b1], k), xytext=(r[b0], k), arrowprops=dict(arrowstyle='-|>', color=col, lw=2.6, mutation_scale=14, shrinkA=4.5, shrinkB=0))
    ax2.scatter([r[b0]], [k], s=50, facecolor='white', edgecolor=col, lw=2, zorder=4)
    ax2.text(r[b1] + 1.2, k, f'+{r[b1]-r[b0]:.0f}', va='center', color=col, fontsize=10.5, fontweight='bold')
ax2.set_yticks(range(1, 10)); ax2.set_yticklabels([names[k] for k in range(1, 10)]); ax2.set_ylim(9.6, 0.4); ax2.set_xlim(0, 36)
ax2.set_xlabel("Median county, % with bachelor's degree or higher"); clean_grid(ax2, 'x')
ax2.set_title('Typical county in each setting (open circle = 1990)', loc='left', fontsize=12.5, color=INK)
for k in (3, 7): ax2.axhline(k + 0.5, color=GRID, lw=1.2)
ax2.tick_params(axis='y', length=0); ax2.spines['left'].set_visible(False)
header(fig, 'College attainment rose almost everywhere, but the metro lead roughly tripled',
       "In 1990 the typical big-metro county had 4.1 points more college graduates than the typical remote rural county (14.9% vs 10.8%). By 2019-23 the lead\n"
       'was 11 points (31% vs 20%). Only 27 of 3,165 counties lost ground, so this is divergence, not rural decline.')
caption(fig, "Share of adults with a bachelor's degree or higher, county-level, 1990 census vs 2019-23 American Community Survey (USDA ERS). "
        'Counties with missing values or without a 2023 Rural-Urban Continuum Code are omitted. Colors group the nine RUCC settings into four (see legend). '
        'Left: dashed line = no change; points above it gained. Right: median county per setting. Descriptive only.', width=175)
save(fig, 'fig3_college_divergence.png')
