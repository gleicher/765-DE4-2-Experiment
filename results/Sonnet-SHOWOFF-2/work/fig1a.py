from common import *
w = load_wb()
g = w.pivot(index='Country Name', columns='Year', values='gap')
print(len(g), 'countries')
fig, ax = plt.subplots(figsize=(11, 8.2))
fig.subplots_adjust(left=0.07, right=0.80, top=0.835, bottom=0.17)
ax.axhspan(-5, 0, color='#fbe9e4', zorder=0)
for c, r in g.iterrows():
    ax.plot(r.index, r.values, color='#c9ced6', lw=0.7, alpha=0.8, zorder=1)
med = g.median()
ax.plot(med.index, med.values, color=INK, lw=2.4, zorder=3)
hl = {'Russian Federation': ('Russia', '#b5481b', (1, 0.9)), 'Ukraine': ('Ukraine', '#d9822b', (1, 0.2)),
      'India': ('India', '#1d7a74', (1, 0)), 'Pakistan': ('Pakistan', '#6a4c93', (1, 0)),
      'Bangladesh': ('Bangladesh', '#8a7a12', (1, 0)), 'United States': ('United States', '#1d4e89', (1, 0)),
      'Japan': ('Japan', '#c23a7a', (1, 0))}
for k, (lab, col, _) in hl.items():
    r = g.loc[k]; ax.plot(r.index, r.values, color=col, lw=2.4, zorder=4)
    ax.scatter([2023], [r[2023]], color=col, s=28, zorder=5)
# manual label offsets to avoid collisions at 2023 (value, y-label position)
pos = {'Ukraine': 13.3, 'Russian Federation': 11.0, 'Japan': 6.8, 'United States': 5.9, 'Pakistan': 4.2, 'Bangladesh': 3.4, 'India': 2.6}
for k, y in pos.items():
    lab, col, _ = hl[k]
    ax.annotate(f'{lab}  {g.loc[k,2023]:+.1f}', (2023, g.loc[k, 2023]), xytext=(2026, y), color=col,
                fontsize=11, fontweight='bold', va='center', annotation_clip=False,
                arrowprops=dict(arrowstyle='-', color=col, lw=0.8, shrinkA=0, shrinkB=2))
ax.annotate('Median country', (2023, med[2023]), xytext=(2026, 5.05), color=INK, fontsize=11, fontweight='bold',
            va='center', annotation_clip=False, arrowprops=dict(arrowstyle='-', color=INK, lw=0.8, shrinkB=2))
ax.text(2003, -0.45, 'Men outlive women', fontsize=11, color='#9b3d1f', va='top', fontweight='bold')
ax.text(2003, 0.25, 'Women outlive men', fontsize=11, color=INK2, va='bottom')
ax.axhline(0, color=INK2, lw=1.2, zorder=2)
ax.annotate('Soviet collapse:\nRussian gap peaks\nat 14.2 years (1994)', (1994, 14.2), xytext=(1975.5, 14.3),
            fontsize=10, color='#b5481b', va='center', ha='center', bbox=dict(fc='white', ec='none', pad=2),
            arrowprops=dict(arrowstyle='-', color='#b5481b', lw=0.8, shrinkB=3))
ax.annotate('India: women lived\nshorter lives until\nthe early 1980s', (1976, -0.9), xytext=(1984, -3.0), fontsize=10,
            color='#1d7a74', ha='left', va='center', arrowprops=dict(arrowstyle='-', color='#1d7a74', lw=0.8))
ax.set_xlim(1960, 2023); ax.set_ylim(-4.5, 15)
ax.set_xlabel('Year'); ax.set_ylabel('Female minus male life expectancy at birth (years)')
clean_grid(ax)
header(fig, 'The female survival advantage is not a constant of nature',
       'Since 1960 the typical country has gained about a year of gap, but the extremes moved far more: women in India caught up\n'
       'from a deficit, while post-Soviet countries opened gaps of 10 to 14 years that have never closed.')
caption(fig, 'Each gray line is one of 215 countries and territories (World Bank life expectancy at birth, 1960-2023, female minus male). The black line is the median country. '
        'Colored lines are selected countries; the number after each name is its 2023 gap in years. The pink band marks years in which men outlived women. '
        'World Bank aggregates (regions, income groups) were removed. Brief spikes (e.g., Bangladesh and Pakistan in 1971) are single-year estimates around wars and are uncertain.', width=165)
save(fig, 'fig1a_gender_gap_trajectories.png')
