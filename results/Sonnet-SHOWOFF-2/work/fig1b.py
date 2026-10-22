from common import *
w = load_wb()
g = w.pivot(index='Country Name', columns='Year', values='gap')
big = ['United States','China','India','Japan','Brazil','Indonesia','Nigeria','Pakistan','Bangladesh','Germany','United Kingdom','France','Mexico','Russian Federation','Ukraine','Egypt, Arab Rep.','Iran, Islamic Rep.','Korea, Rep.','South Africa','Turkiye','Viet Nam','Thailand','Ethiopia','Philippines']
sel = list(dict.fromkeys(big + ['Belarus','Latvia','Lithuania','Kazakhstan','Georgia','Mongolia','Estonia']))
d = g.loc[sel, [1960, 2023]].dropna()
d['chg'] = d[2023] - d[1960]
d = d.sort_values(2023)
print(d.round(1))
n = len(d)
fig, ax = plt.subplots(figsize=(11, 10.6))
fig.subplots_adjust(left=0.20, right=0.93, top=0.86, bottom=0.115)
UP, DOWN = '#b5481b', '#1d6fa5'
for i, (c, r) in enumerate(d.iterrows()):
    col = UP if r.chg > 0.5 else (DOWN if r.chg < -0.5 else MUTED)
    ax.annotate('', xy=(r[2023], i), xytext=(r[1960], i),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=2.2, mutation_scale=13, shrinkA=4.5, shrinkB=0))
    ax.scatter([r[1960]], [i], s=46, facecolor='white', edgecolor=col, lw=1.8, zorder=4)
    ax.text(max(r[1960], r[2023]) + 0.35, i, f'{r.chg:+.1f}', va='center', fontsize=9.5, color=col, fontweight='bold')
ax.set_yticks(range(n)); ax.set_yticklabels([c.replace(', Arab Rep.', '').replace(', Islamic Rep.', '').replace('Russian Federation', 'Russia').replace(', Rep.', '') for c in d.index], fontsize=10.5)
ax.axvline(0, color=INK2, lw=1.2)
ax.set_xlim(-5, 15); ax.set_ylim(-0.8, n - 0.2)
ax.set_xlabel('Female minus male life expectancy at birth (years)')
clean_grid(ax, 'x')
ax.text(-0.15, n - 0.35, 'men live longer', ha='right', va='bottom', fontsize=10, color=MUTED, style='italic')
ax.text(0.15, n - 0.35, 'women live longer', ha='left', va='bottom', fontsize=10, color=MUTED, style='italic')
ax.scatter([], [], s=46, facecolor='white', edgecolor=INK2, lw=1.8, label='1960')
ax.plot([], [], color=UP, lw=2.2, label='Gap widened by 2023'); ax.plot([], [], color=DOWN, lw=2.2, label='Gap narrowed by 2023')
ax.plot([], [], color=MUTED, lw=2.2, label='Little change (within 0.5 yr)')
ax.legend(loc='lower right', frameon=False, fontsize=10, title='Open circle = 1960, arrow head = 2023', title_fontsize=10, alignment='left')
header(fig, 'Where the female advantage grew, and where it shrank',
       'Between 1960 and 2023 the gender gap in life expectancy moved in both directions: it widened by 4 to 9 years in South Asia,\n'
       'Iran, Thailand and Ukraine, but narrowed in the UK, Egypt, Nigeria and the US as men caught up.')
caption(fig, '31 countries: populous countries in the data plus the Baltic, Slavic and Caucasus post-Soviet states and Mongolia (a judgment selection, not a random sample). Gap = female minus male life expectancy at birth (World Bank); '
        'the number at each arrow is the change in years from 1960 to 2023. Sorted by the 2023 gap. India, Pakistan and Bangladesh began with negative gaps (women lived shorter lives).', width=160)
save(fig, 'fig1b_gender_gap_arrows.png')
