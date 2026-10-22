from common import *; from style import *
import matplotlib.pyplot as plt, textwrap
setup()
p=wb(); c=p[~p.is_agg].dropna(subset=['Both','gap']).copy()
FIG='%s/answers/figures/'%ROOT
HL={'United States':BLUE,'Korea, Rep.':GREEN,'Russian Federation':VERM,'India':PINK,'Brazil':ORANGE,'Nigeria':'#555555'}
LAB={'Korea, Rep.':'South Korea','Russian Federation':'Russia'}
# ---------- Fig 1 connected scatter
fig,ax=plt.subplots(figsize=(11,7.4)); fig.subplots_adjust(left=.07,right=.95,top=.84,bottom=.17)
for n,s in c.groupby('Country Name'):
    s=s.sort_values('Year'); ax.plot(s.Both,s.gap,color='#bdbdbd',lw=.6,alpha=.55,zorder=1)
# median curve
c['bin']=(c.Both//2.5)*2.5+1.25
m=c.groupby('bin').gap.agg(['median','count']); m=m[m['count']>=25]
ax.plot(m.index,m['median'],color=INK,lw=3,zorder=3,solid_capstyle='round')
ax.text(31,1.9,'Median of all countries,\nby life-expectancy level',fontsize=9,color=INK,va='top',ha='left',fontweight='bold',bbox=dict(fc='white',ec='none',alpha=.85,pad=1.5),zorder=7)
ax.axvline(70,color='#888',lw=.8,ls=(0,(4,3)),zorder=0)
ax.text(70.4,13.9,'life expectancy 70',fontsize=8.5,color=MUTED,ha='left',va='top')
LP={'United States':(80.5,3.2),'Korea, Rep.':(82.5,8.3),'Russian Federation':(73.3,11.4),'India':(72.5,2.0),'Brazil':(73.2,3.9),'Nigeria':(55.3,0.55)}
for n,col in HL.items():
    s=c[c['Country Name']==n].sort_values('Year')
    ax.plot(s.Both,s.gap,color=col,lw=2.3,zorder=4)
    a,b=s.iloc[0],s.iloc[-1]
    ax.scatter([a.Both],[a.gap],s=34,color='white',edgecolor=col,lw=1.8,zorder=5)
    ax.scatter([b.Both],[b.gap],s=46,color=col,edgecolor='white',lw=1,zorder=5)
    tx,ty=LP[n]
    ax.annotate(LAB.get(n,n),(b.Both,b.gap),(tx,ty),color=col if n!='Nigeria' else INK,fontsize=10.5,fontweight='bold',zorder=6,
        arrowprops=dict(arrowstyle='-',color=col,lw=.8,shrinkA=2,shrinkB=3) if n!='Nigeria' else None, va='center')
ax.set_xlim(28,88); ax.set_ylim(-4.5,14.5)
ax.axhline(0,color='#888',lw=.8)
ax.text(29,-0.4,'men live longer',fontsize=8.5,color=MUTED,va='top'); 
ax.set_xlabel('Life expectancy at birth, both sexes combined (years)  →  as a country gets healthier',fontsize=10.5)
ax.set_ylabel('Women\'s advantage: female minus male life expectancy (years)',fontsize=10.5)
ax.grid(axis='y',color=GRID,lw=.7); ax.set_axisbelow(True)
ax.scatter([],[],s=34,color='white',edgecolor='#444',lw=1.8,label='1960'); ax.scatter([],[],s=46,color='#444',label='2023')
ax.legend(loc='upper left',frameon=False,fontsize=9.5,title='Each path runs 1960 → 2023',title_fontsize=9,bbox_to_anchor=(0.0,1.0),labelcolor=INK)
titles(fig,"Women's survival edge rises with life expectancy, then shrinks",
 "The typical country's female-male gap peaks near 70 years of life expectancy, then narrows. Each grey line is one of 217 countries, 1960 to 2023; coloured lines are examples.",
 "Source: World Bank life expectancy at birth by sex, 1960-2023 (course file lifespan_dataset_1960.csv); regional and income aggregates excluded. The median curve pools country-years in 2.5-year bands of life expectancy (bands with fewer than 25 country-years omitted). Highlighted countries show different paths: peaked then narrowed (United States, South Korea), still very large (Russia), rising from a negative gap (India), shrinking toward zero (Nigeria). Spikes in the grey paths come from war, genocide and epidemic years, which distort one sex's life expectancy.")
fig.savefig(FIG+'q1_primary_connected_scatter.png'); plt.close(fig)

# ---------- Fig 2 small multiples
C=['United States','Germany','Korea, Rep.','Japan','Brazil','China','India','Russian Federation','Nigeria']
cols0={'United States':BLUE,'Germany':BLUE,'Korea, Rep.':BLUE,'Japan':GREEN,'Brazil':GREEN,'China':GREEN,'India':PINK,'Russian Federation':VERM,'Nigeria':'#555555'}
med=c.groupby('Year').gap.median()
fig,axs=plt.subplots(3,3,figsize=(11,8.6),sharex=True,sharey=True); fig.subplots_adjust(left=.07,right=.97,top=.83,bottom=.17,hspace=.28,wspace=.07)
for ax,n in zip(axs.flat,C):
    s=c[c['Country Name']==n].sort_values('Year'); col=BLUE if n!='Russian Federation' else VERM
    ax.plot(med.index,med.values,color='#bbb',lw=1.8,zorder=1)
    ax.fill_between(s.Year,0,s.gap,color=col,alpha=.13,lw=0)
    ax.plot(s.Year,s.gap,color=col,lw=2.2,zorder=3)
    ax.axhline(0,color='#888',lw=.7)
    ax.text(0.03,0.97,f"life expectancy {s.Both.iloc[0]:.0f} → {s.Both.iloc[-1]:.0f} yrs",transform=ax.transAxes,fontsize=8,color=MUTED,va='top')
    pk=s.loc[s.gap.idxmax()]
    ax.scatter([pk.Year],[pk.gap],s=26,color=col,zorder=5); ax.scatter([2023],[s.gap.iloc[-1]],s=26,color=col,zorder=5,edgecolor='white')
    ax.set_title(f'peak {pk.gap:.1f} yrs ({int(pk.Year)})  ·  2023: {s.gap.iloc[-1]:.1f}',loc='right',fontsize=8.3,color=INK,fontweight='normal')
    ax.set_title(LAB.get(n,n),fontsize=11,loc='left',color=INK)
    ax.set_ylim(-3,17); ax.set_xlim(1960,2024); ax.grid(axis='y',color=GRID,lw=.6); ax.set_xticks([1960,1980,2000,2020])
for ax in axs[:,0]: ax.set_ylabel('Female − male (yrs)',fontsize=9)
fig.text(.5,.125,'Year',ha='center',fontsize=10)
titles(fig,"The female edge narrowed in rich countries, but not in Russia or Nigeria",
 "Female minus male life expectancy over time (shaded), against the median country (grey line). The United States, Germany and South Korea peaked and then narrowed; Brazil, China and India are near or at their peaks; Russia and Nigeria sit far from the median in opposite directions.",
 "Source: World Bank life expectancy at birth by sex, 1960-2023. Shaded line = female minus male life expectancy in each country; grey line = median across 217 countries (aggregates excluded); dot on the line = the country's peak year, dot at the right edge = 2023. Countries were chosen to contrast narrowing, flat, rising, very large and shrinking gaps. All panels share axes.")
fig.savefig(FIG+'q1_alternate_small_multiples.png'); plt.close(fig)
for n in C:
    s=c[c['Country Name']==n].sort_values('Year'); print(n, s.loc[s.gap.idxmax(),['Year','gap']].tolist(), s.gap.iloc[-1], s[s.Both>=70].Year.min())
