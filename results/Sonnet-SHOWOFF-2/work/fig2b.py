from common import *
d = load_census()
names = {1: 'Metro, 1M+ people', 2: 'Metro, 250k-1M', 3: 'Metro, <250k', 4: 'Urban 20k+, metro-adjacent', 5: 'Urban 20k+, not adjacent',
         6: 'Urban 5-20k, adjacent', 7: 'Urban 5-20k, not adjacent', 8: 'Rural, metro-adjacent', 9: 'Rural, not adjacent'}
panels = [('Great Recession: 2007 to 2010', 2007, 2010, '#6b7280'), ('Pandemic: 2019 to 2020', 2019, 2020, '#b5481b')]
rng = np.random.default_rng(7)
fig, axes = plt.subplots(1, 2, figsize=(12, 8.6), sharey=True)
fig.subplots_adjust(left=0.255, right=0.97, top=0.80, bottom=0.19, wspace=0.07)
stats = {}
for ax, (ttl, y0, y1, col) in zip(axes, panels):
    dd = d[d.rucc.notna()].copy()
    dd['chg'] = dd[f'Unemployment rate {y1}'] - dd[f'Unemployment rate {y0}']
    dd = dd.dropna(subset=['chg'])
    for k in range(1, 10):
        s = dd[dd.rucc == k]
        yy = (k) + rng.uniform(-0.3, 0.3, len(s))
        ax.scatter(s.chg, yy, s=6, color=col, alpha=0.28, lw=0, zorder=2)
        # labor-force weighted change of group rate
        m = s[[f'Unemployed {y0}', f'Civilian labor force {y0}', f'Unemployed {y1}', f'Civilian labor force {y1}']].dropna()
        w = 100 * m.iloc[:, 2].sum() / m.iloc[:, 3].sum() - 100 * m.iloc[:, 0].sum() / m.iloc[:, 1].sum()
        med = s.chg.median(); stats[(y0, k)] = (med, w, len(s))
        ax.plot([med, med], [k - 0.38, k + 0.38], color=INK, lw=2.6, zorder=4)
        ax.scatter([w], [k], marker='D', s=46, color='white', edgecolor=INK, lw=1.6, zorder=5)
    ax.set_title(ttl, fontsize=13, loc='left', color=INK)
    ax.set_xlim(-3, 15 if y0 == 2007 else 15); ax.axvline(0, color=INK2, lw=1)
    ax.set_xlabel('Change in county unemployment rate (percentage points)'); clean_grid(ax, 'x')
for ax in axes: ax.set_ylim(9.7, 0.3)
axes[0].set_yticks(range(1, 10)); axes[0].set_yticklabels([f'{names[k]}  (RUCC {k})' for k in range(1, 10)], fontsize=10)
axes[0].spines['left'].set_visible(False); axes[0].tick_params(axis='y', length=0)
for k in (3, 7): 
    for ax in axes: ax.axhline(k + 0.5, color=GRID, lw=1.2)
def ann(ax, y0, k, txt, xy_text):
    ax.annotate(txt.format(stats[(y0, k)][0]), xy=(stats[(y0, k)][0], k), xytext=xy_text, fontsize=10, color=INK, arrowprops=dict(arrowstyle='-', color=INK2))
ann(axes[1], 2019, 1, 'Big metros: median\n+{:.1f} pts', (8.5, 1.7))
ann(axes[1], 2019, 9, 'Remote rural: median\n+{:.1f} pts', (8.5, 7.9))
ann(axes[0], 2007, 1, 'Big metros: median\n+{:.1f} pts', (8.8, 1.7))
ann(axes[0], 2007, 9, 'Remote rural: median\n+{:.1f} pts', (8.8, 7.9))
for (y0, k), v in stats.items():
    if k in (1, 9): print(y0, k, [round(float(x), 2) for x in v])
axes[0].scatter([], [], s=6, color='#6b7280', alpha=.5, label='One county'); axes[0].plot([], [], color=INK, lw=2.6, label='Median county')
axes[0].scatter([], [], marker='D', s=46, color='white', edgecolor=INK, lw=1.6, label='Whole group (labor-force weighted)')
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', bbox_to_anchor=(0.55, 0.075), ncol=3, frameon=False, fontsize=10)
header(fig, 'Both downturns hit cities harder, but the pandemic hit them much harder',
       'Each dot is a county. The pandemic rise in unemployment generally climbed with urbanness: the median big-metro county rose more than twice\n'
       'as much as a remote rural one (3.4 vs 1.5 points). The Great Recession gradient was milder (4.7 vs 3.1 points), so rural counties,\n'
       'which start from higher unemployment, ended the recession level with the cities, but not the pandemic.')
caption(fig, 'US counties (about 3,100 with data), grouped by 2023 Rural-Urban Continuum Code (USDA ERS). Change = annual-average unemployment rate in the end year minus the start year. '
        'Dots jittered vertically. Both panels share a scale. Diamonds weight counties by labor force, so they reflect where people live; vertical bars show the unweighted median county. Descriptive only.', width=170)
save(fig, 'fig2b_unemployment_county_change.png')
