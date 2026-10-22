"""Builds all six figures. Run: /opt/anaconda3/envs/p314/bin/python make_figs.py  (from work/)"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
D='../data/'; OUT='../answers/figures/'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,
                     'axes.titleweight':'bold','figure.dpi':100})
def finish(fig,name,title,sub,cap):
    import textwrap
    t='\n'.join(textwrap.wrap(title,62)); sb='\n'.join(textwrap.wrap(sub,105))
    nt=t.count('\n')+1
    fig.text(0.04,0.985,t,ha='left',va='top',fontsize=17,fontweight='bold')
    fig.text(0.04,0.985-0.04*nt-0.012,sb,ha='left',va='top',fontsize=11.5,color='#444')
    cap='\n'.join(textwrap.wrap(cap.replace('\n',' '),150))
    fig.text(0.04,0.012,cap,ha='left',va='bottom',fontsize=9.5,color='#444')
    fig.savefig(OUT+name,dpi=150); plt.close(fig)

# ---------------- life expectancy (World Bank, countries only) ----------------
l=pd.read_csv(D+'lifespan_dataset_1960.csv',index_col=0)
o=pd.read_csv(D+'life-expectancy-owid/life-expectancy-owid.csv')
codes=set(o.dropna(subset=['Code']).query("~Code.str.startswith('OWID')").Code)
l=l[l['Country Code'].isin(codes)]
p=l.pivot_table(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)').reset_index()
p['gap']=p.Female-p.Male
g=p.pivot(index='Country Name',columns='Year',values='gap')
g.index=g.index.str.replace('Russian Federation','Russia').str.replace('Iran, Islamic Rep.','Iran')
BLUE,ORG,GRY,RED='#1f77b4','#d95f02','#9a9a9a','#b2182b'

# Fig 1a: scatter 1960 vs 2023 gap
s=g[[1960,2023]].dropna()
fig,ax=plt.subplots(figsize=(11,8.6)); fig.subplots_adjust(top=0.80,bottom=0.15,left=0.08,right=0.97)
lim=(-5,15)
ax.fill_between(lim,lim,[15,15],color='#fde0dd',alpha=.35,lw=0); ax.fill_between(lim,lim,[-5,-5],color='#deebf7',alpha=.5,lw=0)
ax.plot(lim,lim,color='k',lw=1); ax.axhline(0,color='#777',lw=.8,ls=':'); ax.axvline(0,color='#777',lw=.8,ls=':')
ax.scatter(s[1960],s[2023],s=28,color=GRY,alpha=.8,edgecolor='white',lw=.4)
lab={'Ukraine':(8,-4),'Pakistan':(8,-6),'Russia':(8,-10),'Cameroon':(5,-8),'India':(8,-13),'United States':(8,-4),'Iran':(8,3),
     'Bangladesh':(-72,2),'Thailand':(8,-8),'Nigeria':(8,-10),'Japan':(8,-8),'Latvia':(-30,6),'Georgia':(-45,-14),'Qatar':(8,-4)}
hi=['Ukraine','Pakistan','Russia','India','Iran','Bangladesh','Thailand','Cameroon','Nigeria']
for n,(dx,dy) in lab.items():
    if n in s.index:
        c=ORG if n in hi else '#333'
        ax.scatter(s.loc[n,1960],s.loc[n,2023],s=55,color=ORG if n in hi else '#333',zorder=3,edgecolor='white')
        ax.annotate(n,(s.loc[n,1960],s.loc[n,2023]),xytext=(dx,dy),textcoords='offset points',fontsize=10,color=c)
ax.set_xlim(lim);ax.set_ylim(-1,15);ax.set_xlim(-5,14)
ax.set_xlabel('Female minus male life expectancy in 1960 (years)'); ax.set_ylabel('Female minus male life expectancy in 2023 (years)')
ax.text(-4.6,13.2,'Above the line: women\'s advantage\ngrew since 1960',color=RED,fontsize=10.5,va='top')
ax.text(13.8,-0.6,'Below the line: women\'s advantage shrank',color=BLUE,fontsize=10.5,ha='right')
ax.text(-4.8,5.6,'Men outlived women in 1960',fontsize=9.5,color='#555',rotation=90,va='center')
finish(fig,'q1_a_gap_scatter.png','Women now outlive men almost everywhere, but the gap moved in different directions',
 'Each dot is a country: the female-male life expectancy gap in 1960 (x) vs 2023 (y); points on the diagonal did not change.',
 'Source: World Bank life expectancy at birth (course file lifespan_dataset_1960.csv), 213 countries with data in both years; regional aggregates removed.\nThe gap is female minus male life expectancy in years. Orange labels mark the largest shifts. Descriptive only, no causal claim.')

# Fig 1b: lines
sel=['Russia','Ukraine','Pakistan','India','United States','Japan']
col={'Russia':RED,'Ukraine':'#e6550d','Pakistan':'#6a3d9a','India':'#a6a0d0','United States':BLUE,'Japan':'#2ca02c'}
yrs=g.columns
fig,ax=plt.subplots(figsize=(11,8.2)); fig.subplots_adjust(top=0.80,bottom=0.14,left=0.08,right=0.84)
q1,med,q3=g.quantile(.25),g.median(),g.quantile(.75)
ax.fill_between(yrs,q1,q3,color='#d9d9d9',alpha=.7,lw=0); ax.plot(yrs,med,color='#555',lw=2,ls='--')
ax.text(1985,-3.5,'Middle half of all countries (band)\nand the median (dashed)',fontsize=9.5,color='#555',va='bottom')
ax.axhline(0,color='#777',lw=.8,ls=':')
LY={'Russia':10.9,'Ukraine':13.5,'Pakistan':4.4,'India':3.0,'United States':5.4,'Japan':6.4}
for n in sel:
    ax.plot(yrs,g.loc[n],color=col[n],lw=2.4)
    ax.text(2024,LY[n],n,color=col[n],va='center',fontsize=11,fontweight='bold')
ax.annotate('Soviet-era gap peaks\n(Russia 14.2 yrs, 1994)',xy=(1994,14.2),xytext=(1966,14.5),fontsize=9.5,arrowprops=dict(arrowstyle='-',color='#555'),va='center')
ax.annotate('In 1960 Pakistan and India:\nmen outlived women',xy=(1961,-3.9),xytext=(1966,-4.6),fontsize=9.5,va='center')
ax.set_ylim(-5.5,16);ax.set_xlim(1960,2023)
ax.set_ylabel('Female minus male life expectancy (years)'); ax.set_xlabel('Year')
finish(fig,'q1_b_gap_lines.png','Where women gained, where they lost: six countries tell the gap\'s different stories',
 'Female minus male life expectancy at birth, 1960-2023, against the spread of all countries.',
 'Source: World Bank life expectancy at birth, male and female series (course file lifespan_dataset_1960.csv). Grey band = interquartile range across countries with data each year,\ndashed = median. Countries chosen to show the widest rise (Ukraine, Pakistan, Russia), the decline (US since 1980) and a stable case (Japan).')

# ---------------- census ----------------
c=pd.read_csv(D+'full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1')
c=c[~c['FIPS Code'].str.endswith('000') & (c['FIPS Code']!='0')].copy()
rucc=c['2023 Rural-urban Continuum Code']; c=c[rucc.notna()].copy(); rucc=c['2023 Rural-urban Continuum Code'].astype(int)
c['rucc']=rucc
c['grp']=np.select([rucc<=3,rucc.isin([4,6,8])],['Metro','Nonmetro, next to a metro'],'Nonmetro, not adjacent')
periods=['1990','2000','2008-12','2019-23']
lvl={'less':'Less than high school graduate, ','hs':'High school graduate (or equivalency), ','sc':'Some college or associate degree, ','ba':"Bachelor's degree or higher, "}
for pr in periods:
    c['tot'+pr]=sum(c[v+pr] for v in lvl.values())
    for k,v in lvl.items(): c[k+pr]=c[v+pr]
def pooled(by,k): return pd.DataFrame({pr:c.groupby(by)[k+pr].sum()/c.groupby(by)['tot'+pr].sum()*100 for pr in periods})
byr=pooled('rucc','ba'); bg=pooled('grp','ba')
GC={'Metro':BLUE,'Nonmetro, next to a metro':'#e08214','Nonmetro, not adjacent':'#8c2d04'}
xl=['1990','2000','2008-12','2019-23']

# Fig 2a: 9 RUCC lines, direct labels
fig,ax=plt.subplots(figsize=(11,8.4)); fig.subplots_adjust(top=0.80,bottom=0.16,left=0.08,right=0.78)
cm=matplotlib.colormaps['viridis']
names={1:'1 Metro, 1M+',2:'2 Metro, 250k-1M',3:'3 Metro, <250k',4:'4 Urban 20k+, adj.',5:'5 Urban 20k+, not adj.',6:'6 Urban 5-20k, adj.',7:'7 Urban 5-20k, not adj.',8:'8 Rural, adj.',9:'9 Rural, not adj.'}
ypos={}
for r in range(1,10):
    col_=cm(0.05+0.8*(r-1)/8)
    ax.plot(range(4),byr.loc[r],marker='o',color=col_,lw=2.4 if r in(1,9) else 1.6)
    ypos[r]=byr.loc[r,'2019-23']
# de-overlap labels
ys=sorted(ypos.items(),key=lambda t:t[1]); adj={}; last=-99
for r,v in ys:
    y=max(v,last+1.35); adj[r]=y; last=y
for r in range(1,10):
    ax.text(3.08,adj[r],names[r],va='center',fontsize=10,color=cm(0.05+0.8*(r-1)/8))
ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_xlim(-.1,3.05); ax.set_ylim(0,48)
ax.set_xlabel('Census / ACS period'); ax.set_ylabel('Adults (25+) with a bachelor\'s degree or higher (%)')
ax.annotate('',xy=(3,byr.loc[1,'2019-23']),xytext=(3,byr.loc[9,'2019-23']),arrowprops=dict(arrowstyle='<->',color='k'))
ax.text(2.95,44,f"2019-23: largest metros lead the most rural by {byr.loc[1,'2019-23']-byr.loc[9,'2019-23']:.0f} pts",ha='right',va='center',fontsize=10.5,fontweight='bold')
ax.text(0.0,44,f"1990: the same gap was {byr.loc[1,'1990']-byr.loc[9,'1990']:.0f} pts",fontsize=10.5,fontweight='bold')
ax.grid(axis='y',color='#eee')
finish(fig,'q2_a_education_lines.png','College education rose everywhere, but big metros pulled away from rural counties',
 'Share of adults with a bachelor\'s degree or higher, by 2023 USDA rural-urban continuum code (1 = largest metros, 9 = most rural).',
 'Source: USDA ERS county data (course file full_census_dataset.csv). Shares are pooled over counties (sum of degree holders / sum of adults in four attainment levels), so large counties count more.\n3,100+ counties; counties without a 2023 code excluded. Education categories use 2023 county codes for all periods (counties\' type may have differed in 1990).')

# Fig 2b: county scatter 1990 vs 2019-23
fig,ax=plt.subplots(figsize=(11,8.4)); fig.subplots_adjust(top=0.80,bottom=0.15,left=0.08,right=0.97)
c['p90']=c['ba1990']/c['tot1990']*100; c['p23']=c['ba2019-23']/c['tot2019-23']*100
for gname in ['Nonmetro, not adjacent','Nonmetro, next to a metro','Metro']:
    sub=c[c.grp==gname]
    ax.scatter(sub.p90,sub.p23,s=11,alpha=.35,color=GC[gname],lw=0)
ax.plot([0,70],[0,70],color='k',lw=1); ax.text(52,48,'no change',rotation=34,fontsize=9.5)
for gname in GC:
    m=bg.loc[gname]
    ax.scatter(m['1990'],m['2019-23'],s=230,marker='D',color=GC[gname],edgecolor='k',lw=1.5,zorder=4)
    ax.annotate(f"{gname}\n{m['1990']:.0f}% to {m['2019-23']:.0f}%",(m['1990'],m['2019-23']),xytext={'Metro':(14,-30),'Nonmetro, next to a metro':(27,11),'Nonmetro, not adjacent':(27,4)}[gname],textcoords='offset points' if gname=='Metro' else 'data',fontsize=10.5,fontweight='bold',color=GC[gname],arrowprops=dict(arrowstyle='-',color=GC[gname],lw=1.2))
ax.set_xlim(0,60);ax.set_ylim(0,75)
ax.set_xlabel('Adults with bachelor\'s or higher, 1990 (%)'); ax.set_ylabel('Adults with bachelor\'s or higher, 2019-23 (%)')
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=GC[k],alpha=.7,label=k) for k in GC]+[Line2D([],[],marker='D',ls='',color='w',markeredgecolor='k',label='Group average (pooled)')],loc='upper left',frameon=False)
finish(fig,'q2_b_education_scatter.png','Nearly every county gained, and the places that started ahead gained the most',
 'Each dot is a county: share of adults with a bachelor\'s degree or higher in 1990 (x) and 2019-23 (y).',
 'Source: USDA ERS county data (course file full_census_dataset.csv). Metro = RUCC 1-3; nonmetro adjacent = 4, 6, 8; nonmetro not adjacent = 5, 7, 9 (2023 codes). Diamonds are pooled averages\nweighted by adult population. Dots above the diagonal gained; counties are not weighted by size, so many small rural counties appear.')

# Fig 3: pandemic unemployment
ys_=range(2000,2024)
ur={}
for gname in GC:
    sub=c[c.grp==gname]
    ur[gname]=[sub[f'Unemployed {y}'].sum()/sub[f'Civilian labor force {y}'].sum()*100 for y in ys_]
ur=pd.DataFrame(ur,index=ys_)
fig,ax=plt.subplots(figsize=(11,8)); fig.subplots_adjust(top=0.80,bottom=0.15,left=0.08,right=0.74)
ax.axvspan(2007.9,2009.9,color='#eee'); ax.axvspan(2019.9,2020.9,color='#eee')
ax.text(2008.9,11.7,'Great\nRecession',ha='center',fontsize=9.5,color='#555'); ax.text(2020.4,11.7,'2020',ha='center',fontsize=9.5,color='#555')
for gname in GC:
    ax.plot(ys_,ur[gname],color=GC[gname],lw=2.5,marker='o',ms=3.5)
off={'Metro':0.5,'Nonmetro, next to a metro':0.0,'Nonmetro, not adjacent':-0.5}
for gname in GC: ax.text(2023.3,ur[gname][2023]+off[gname],gname,color=GC[gname],va='center',fontsize=10.5,fontweight='bold')
m20=ur.loc[2020]-ur.loc[2019]
ax.annotate(f"2019 to 2020 jump:\nMetro +{m20['Metro']:.1f} pts\nNonmetro adj. +{m20['Nonmetro, next to a metro']:.1f}\nNonmetro not adj. +{m20['Nonmetro, not adjacent']:.1f}",xy=(2020,ur.loc[2020,'Metro']),xytext=(2013.3,9.9),fontsize=10,arrowprops=dict(arrowstyle='->',color='#555'))
ax.set_ylim(0,12.5);ax.set_xlim(2000,2023);ax.set_ylabel('Unemployment rate (% of civilian labor force)');ax.set_xlabel('Year');ax.grid(axis='y',color='#eee')
finish(fig,'q3_unemployment_pandemic.png','The 2020 job shock hit metro areas hardest, then all county types converged',
 'Unemployment rate by county type, 2000-2023. The 2020 spike was smaller than the Great Recession\'s in every group, and rates converged by 2023.',
 'Source: USDA ERS county data (course file full_census_dataset.csv): unemployed / civilian labor force, pooled across counties in each group (2023 rural-urban codes).\nMetro = RUCC 1-3; nonmetro adjacent = 4, 6, 8; nonmetro not adjacent = 5, 7, 9. Descriptive; the data do not show why the groups differ.')
ur.to_csv('unemployment_by_group.csv'); byr.to_csv('education_by_rucc.csv'); bg.to_csv('education_by_group.csv')

# ---------------- Fig 4: OWID biggest one-year drops ----------------
o=o.dropna(subset=['Code']); o=o[~o.Code.str.startswith('OWID')].rename(columns={'Period life expectancy at birth':'le'})
o=o.sort_values(['Entity','Year']); o['d']=o.groupby('Entity').le.diff(); o['gy']=o.groupby('Entity').Year.diff()
o=o[(o.gy==1)&(o.Year>=1950)]
big=o[o.d<=-5].copy()
fig,(ax0,ax)=plt.subplots(2,1,figsize=(12,9.2),sharex=True,gridspec_kw={'height_ratios':[1,2.3]})
fig.subplots_adjust(top=0.80,bottom=0.17,left=0.08,right=0.97,hspace=0.08)
share=o.groupby('Year').d.apply(lambda x:(x<0).mean()*100)
ax0.bar(share.index,share.values,color=['#b2182b' if v>40 else '#bbbbbb' for v in share.values],width=.8)
ax0.set_ylabel('Countries with a\nfall that year (%)'); ax0.set_ylim(0,75)
ax0.annotate(f'2020 and 2021: {share[2020]:.0f}% and {share[2021]:.0f}% of countries fell (COVID-19 pandemic)',xy=(2020,share[2020]),xytext=(2018.5,57),fontsize=10,ha='right',va='center')
ax0.text(1951,66,f'In a typical year only about {share[share.index<2019].median():.0f}% fall',fontsize=10,va='center')
ax.scatter(o.Year,o.d,s=5,color='#d5d5d5',lw=0)
ax.scatter(big.Year,big.d,s=big.d.abs()*6,color=RED,alpha=.8,edgecolor='white',lw=.5)
ax.axhline(0,color='k',lw=.8)
lab=big[(big.d<=-13)&(big.Entity!='Cyprus')].sort_values('d')
for _,r in lab.iterrows():
    right=r.Year in(2010,2019,2022,2009,1995,1974)
    dy={'Haiti2010':13,'Central African Republic2019':9,'Central African Republic2022':-9,'Equatorial Guinea1969':7,'Cyprus1974':-9,'Bangladesh1971':5,'Burundi1972':-5,'Somalia1991':-6,'South Sudan1995':11,'South Sudan1998':6,'Lebanon1976':0}.get(r.Entity+str(int(r.Year)),0)
    ax.annotate(f"{r.Entity} {int(r.Year)}",(r.Year,r.d),xytext=(-7 if right else 7,dy),textcoords='offset points',fontsize=9,ha='right' if right else 'left',va='center')
ax.set_xlim(1950,2025);ax.set_ylim(-37,10)
ax.set_xlabel('Year');ax.set_ylabel('One-year change in life expectancy at birth (years)')
ax.text(1951,-34,'Red dots: drops of 5+ years in a single year (size = size of drop). Labeled: drops of 13+ years (Cyprus 1974 omitted for space). Grey: all other country-years.',color=RED,fontsize=9.5)
finish(fig,'q4_owid_drops.png','Life expectancy falls are rare, and the largest ones are sharp, short-lived crises',
 'Year-over-year change in life expectancy for every country, 1950-2023, and the share of countries falling each year.',
 'Source: Our World in Data period life expectancy at birth (course file life-expectancy-owid.csv); rows with an ISO code (countries and some territories), consecutive years only. Period life expectancy reflects that year\'s death rates, so one-off crises show up sharply; some very large drops (e.g. Central African Republic 2009) may reflect estimation uncertainty in the source.')

print(byr.round(1)); print(bg.round(1)); print(ur.round(2).loc[[2000,2007,2009,2010,2019,2020,2021,2023]])
print(big.sort_values('d').head(15)[['Entity','Year','d']]); print((o.d<0).mean(), len(big), share[2020], share[share.index<2019].median())
print(g.loc[sel,[1960,1980,2023]].round(1)); print(med[[1960,2023]], s.shape, ((s[2023]-s[1960])>0).sum(), (s[1960]<0).sum(), (s[2023]<0).sum())
