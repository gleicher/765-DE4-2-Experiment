from common import *; from style import *
import matplotlib.pyplot as plt, numpy as np
setup(); FIG='%s/answers/figures/'%ROOT
d=census()
b90="Percent of adults with a bachelor's degree or higher, 1990"; b23="Percent of adults with a bachelor's degree or higher, 2019-23"
d['rucc']=d['2023 Rural-urban Continuum Code']; d['pop']=d['Census Population 2020']
e=d.dropna(subset=[b90,b23,'rucc','pop']); e=e[e[b90]>0].copy()
e['grp']=pd.cut(e.rucc,[0,3,7,9],labels=['Metro counties (codes 1-3)','Smaller-town counties, nonmetro (4-7)','Most rural counties (8-9)'])
GC={'Metro counties (codes 1-3)':BLUE,'Smaller-town counties, nonmetro (4-7)':ORANGE,'Most rural counties (8-9)':VERM}
print(len(e), e.groupby('grp',observed=True)[[b90,b23]].median())
# ---- Fig 3 scatter
fig,ax=plt.subplots(figsize=(10.5,8)); fig.subplots_adjust(left=.08,right=.96,top=.84,bottom=.17)
order=['Smaller-town counties, nonmetro (4-7)','Most rural counties (8-9)','Metro counties (codes 1-3)']
rng=np.random.default_rng(1)
for g in order:
    s=e[e.grp==g]
    ax.scatter(s[b90],s[b23],s=6+np.sqrt(s['pop'])/18,color=GC[g],alpha=.28,lw=0,zorder=2)
ax.plot([0,70],[0,70],color='#888',lw=.9,ls=(0,(4,3)),zorder=1)
ax.text(55,50,'no change',rotation=36,fontsize=8.5,color=MUTED,ha='center')
for g in ['Metro counties (codes 1-3)','Smaller-town counties, nonmetro (4-7)','Most rural counties (8-9)']:
    s=e[e.grp==g]; mx,my=s[b90].median(),s[b23].median()
    ax.scatter([mx],[my],s=180,color=GC[g],edgecolor='white',lw=2,zorder=6,marker='D')
    ax.annotate(f"{g.split(' (')[0]}\nmedian {mx:.0f}% → {my:.0f}%",(mx,my),(mx+ {'Metro':6,'Smaller-town':10,'Most':14}[g.split()[0]], my+ {'Metro':5,'Smaller-town':-8,'Most':-14}[g.split()[0]]),
      fontsize=9.5,fontweight='bold',color=GC[g],arrowprops=dict(arrowstyle='-',color=GC[g],lw=1),zorder=7,va='center')
lab=[('San Miguel County, CO','San Miguel Co., CO\n(Telluride)'),('Loudoun County, VA',None)]
for n,t in [('San Miguel County','San Miguel Co., CO (ski resort)'),('Lamoille County','Lamoille Co., VT')]:
    r=e[(e['Area name']==n)].iloc[0] if (e['Area name']==n).any() else None
    if r is not None and n=='San Miguel County': ax.annotate(t,(r[b90],r[b23]),(r[b90]+4,r[b23]+3),fontsize=8.5,color=INK,arrowprops=dict(arrowstyle='-',color='#555',lw=.7))
big=e.sort_values('pop').tail(1).iloc[0]; 
for nm in ['Los Angeles County','Cook County']: pass
ax.set_xlim(0,62); ax.set_ylim(0,70)
ax.set_xlabel("Adults with a bachelor's degree or higher, 1990 (% of county adults)",fontsize=10.5)
ax.set_ylabel("Same measure, 2019-23 (%)",fontsize=10.5)
ax.grid(color=GRID,lw=.6); ax.set_axisbelow(True)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker='o',ls='',color='#777',alpha=.5,ms=m,label=l) for m,l in [(3,'small county'),(7,'large county (area = population)')]],loc='upper left',frameon=False,fontsize=8.5,title='Dot size',title_fontsize=8.5)
titles(fig,"Nearly every county gained, but metro counties pulled further ahead",
 "Each dot is a county, positioned by its 1990 college share (x) and 2019-23 college share (y). Diamonds are group medians. Counties that were already educated gained the most: the median metro county went up about 13 points, the median most-rural county about 9.",
 "Source: USDA Economic Research Service county data via course file full_census_dataset.csv. 3,000+ counties with both years available (Connecticut counties and planning regions are not comparable across years and drop out). Groups use the 2023 USDA Rural-urban Continuum Code: 1-3 metro, 4-7 nonmetro with urban population, 8-9 completely rural. Dot area scales with 2020 population. Strongly rising rural outliers are mostly Colorado/Mountain West resort counties.",sw=120)
fig.savefig(FIG+'q2_primary_scatter.png'); plt.close(fig)

# ---- Fig 4 dumbbell by RUCC with IQR
lab={1:'1  Metro, 1 million+',2:'2  Metro, 250k-1 million',3:'3  Metro, under 250k',4:'4  Urban 20k+, next to metro',5:'5  Urban 20k+, not next to metro',6:'6  Urban 5-20k, next to metro',7:'7  Urban 5-20k, not next to metro',8:'8  Rural (<5k), next to metro',9:'9  Rural (<5k), not next to metro'}
fig,ax=plt.subplots(figsize=(10.5,7.6)); fig.subplots_adjust(left=.28,right=.96,top=.84,bottom=.17)
for i,k in enumerate(range(1,10)):
    s=e[e.rucc==k]; y=9-i
    q9=s[b90].quantile([.25,.5,.75]).values; q2=s[b23].quantile([.25,.5,.75]).values
    ax.plot([q9[0],q9[2]],[y+.16,y+.16],color='#999',lw=7,solid_capstyle='butt',alpha=.55,zorder=1)
    ax.plot([q2[0],q2[2]],[y-.16,y-.16],color=BLUE,lw=7,solid_capstyle='butt',alpha=.55,zorder=1)
    ax.scatter([q9[1]],[y+.16],s=60,color='#555',zorder=3,edgecolor='white'); ax.scatter([q2[1]],[y-.16],s=60,color=BLUE,zorder=3,edgecolor='white')
    ax.annotate('',(q2[1]-.5,y-.16),(q9[1]+.5,y+.16),arrowprops=dict(arrowstyle='-|>',color='#333',lw=1,shrinkA=0,shrinkB=0),zorder=2)
    ax.text(q2[2]+1,y-.16,f'+{q2[1]-q9[1]:.0f}',va='center',fontsize=9.5,fontweight='bold',color=BLUE)
    ax.text(-.012,y,lab[k],transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=9.5,color=INK)
ax.set_yticks([]); ax.set_ylim(.4,9.6); ax.set_xlim(0,56)
ax.spines['left'].set_visible(False)
ax.grid(axis='x',color=GRID,lw=.6); ax.set_axisbelow(True)
ax.set_xlabel("Adults with a bachelor's degree or higher (% of county adults)",fontsize=10.5)
ax.scatter([],[],s=60,color='#555',label='1990 median (bar = middle half of counties)'); ax.scatter([],[],s=60,color=BLUE,label='2019-23 median (bar = middle half)')
ax.legend(loc='lower right',frameon=False,fontsize=9)
ax.text(0,-.12,'',transform=ax.transAxes)
titles(fig,"The college gap between big-metro and remote rural counties nearly tripled",
 "Median county college share rose in every type of county, but the median gap between the largest-metro counties (code 1) and the most remote rural counties (code 9) grew from about 4 points to about 11. Numbers show each type's change in the median.",
 "Source: USDA Economic Research Service county data via course file full_census_dataset.csv. Rows are 2023 Rural-urban Continuum Code categories (my paraphrase of the USDA definitions; 'next to' = adjacent to a metro area). Each bar spans the 25th to 75th percentile of counties; dots are medians. Counties are unweighted by population; about 3,000 counties with data in both periods.",sw=120)
fig.savefig(FIG+'q2_alternate_range_dumbbell.png'); plt.close(fig)
print(e.groupby('rucc')[[b90,b23]].median())

# ---- Fig 5 unemployment by education quartile
f=d[d[b90].notna()&(d[b90]>0)].copy()
f['q']=pd.qcut(f[b90],4,labels=['Q1','Q2','Q3','Q4'])
yrs=list(range(2000,2024)); R={}
for q,s in f.groupby('q',observed=True):
    R[q]=[s[f'Unemployed {y}'].sum()/s[f'Civilian labor force {y}'].sum()*100 for y in yrs]
R=pd.DataFrame(R,index=yrs); print(R.round(2).loc[[2007,2010,2019,2020,2021,2023]])
cols={'Q1':'#c6dbef','Q2':'#6baed6','Q3':'#2171b5','Q4':'#08306b'}
fig=plt.figure(figsize=(10.5,8.4)); gs=fig.add_gridspec(2,1,height_ratios=[3,1.3],hspace=.28); fig.subplots_adjust(left=.08,right=.83,top=.84,bottom=.14)
ax=fig.add_subplot(gs[0]); ax2=fig.add_subplot(gs[1],sharex=ax)
for lo,hi in [(2007.5,2009.5),(2019.5,2020.5)]:
    ax.axvspan(lo,hi,color='#f0e6d2',lw=0,zorder=0); ax2.axvspan(lo,hi,color='#f0e6d2',lw=0,zorder=0)
names={'Q1':'Least-educated','Q2':'Second','Q3':'Third','Q4':'Most-educated'}
for q in R:
    ax.plot(yrs,R[q],color=cols[q] if q!='Q1' else '#9ecae1',lw=2.6,zorder=3)
ytxt={'Q1':3.65,'Q2':4.25,'Q3':4.85,'Q4':3.05}
for q in R: ax.text(2023.4,ytxt[q],names[q],fontsize=9,color=cols[q] if q!='Q1' else '#4a90c2',va='center',fontweight='bold')
ax.text(2008.5,12.7,'Great\nRecession',ha='center',fontsize=8.5,color=MUTED,va='top'); ax.text(2020,12.7,'COVID-19\n(2020)',ha='center',fontsize=8.5,color=MUTED,va='top')
ax.set_ylim(1.5,13); ax.set_ylabel('Unemployment rate (%)\nunemployed / labor force',fontsize=10); ax.grid(axis='y',color=GRID,lw=.6)
ax.annotate('2020: the ranking\nscrambles; third-quartile\ncounties are hit hardest',(2020,R['Q3'][2020]),(2010.2,2.3),fontsize=9,color=INK,arrowprops=dict(arrowstyle='->',color=INK,lw=.9))
gap=R['Q1']-R['Q4']
ax2.bar(yrs,gap,color=[BLUE if g>=0 else VERM for g in gap],width=.75,zorder=3)
ax2.axhline(0,color='#555',lw=.8); ax2.grid(axis='y',color=GRID,lw=.6)
ax2.set_ylabel('Lowest minus highest\n(percentage points)',fontsize=9.5); ax2.set_ylim(-1.9,3.9)
ax2.text(2020,-1.0,f'{gap[2020]:.1f}',ha='center',fontsize=9,color=VERM,fontweight='bold'); ax2.text(2009,gap[2009]+.15,f'+{gap[2009]:.1f}',ha='center',fontsize=9,color=BLUE,fontweight='bold')
ax2.text(2000.2,3.8,'Positive: less-educated\ncounties had higher unemployment',fontsize=8.5,color=BLUE,va='top'); ax2.text(2012.3,-1.0,'Negative: more-educated counties\nhad higher unemployment',fontsize=8.5,color=VERM,va='top')
ax2.set_xlim(1999.3,2023.7); ax2.set_xticks(range(2000,2024,4)); ax2.set_xlabel('Year')
plt.setp(ax.get_xticklabels(),visible=False)
titles(fig,"In 2020 the usual college advantage in unemployment vanished",
 "Counties are grouped into quartiles by 1990 college share (about 800 counties each). In every year 2000-2019 the least-educated counties had the highest unemployment, and the gap peaked in the Great Recession. In 2020 it reversed.",
 "Source: USDA Economic Research Service county data via course file full_census_dataset.csv. Rate = total unemployed / total civilian labor force in each quartile (annual averages, so the April 2020 peak is smoothed). Education quartile uses 1990 bachelor's share so groups are fixed before the period shown. Correlation only: high-college counties are also larger and more metropolitan (average rural-urban code 3.5 vs 6.0), which likely matters for 2020.",sw=120)
fig.savefig(FIG+'q3_unemployment_by_education.png'); plt.close(fig)

# ---- Fig 6 COVID life expectancy arrow plot
w=wb(); c=w[~w.is_agg]; pp=c.pivot(index='Country Name',columns='Year',values='Both')
x=pd.DataFrame({'a21':pp[2021]-pp[2019],'a23':pp[2023]-pp[2019]})
hit=['Bolivia','Paraguay','Mexico','Peru','Ecuador','Colombia','South Africa','India']
other=['Libya','North Macedonia','Thailand','Germany','Canada','United States','Singapore','Japan','West Bank and Gaza']
NM={'Korea, Rep.':'South Korea'}
sel=hit+other; X=x.loc[sel].sort_values('a21')
hit_rows=X[X.index.isin(hit)].sort_values('a21'); oth_rows=X[X.index.isin(other)].sort_values('a21')
X=pd.concat([hit_rows,oth_rows])
fig,ax=plt.subplots(figsize=(10.5,8.2)); fig.subplots_adjust(left=.2,right=.95,top=.84,bottom=.15)
n=len(X)
for i,(name,r) in enumerate(X.iterrows()):
    y=n-i-(0 if i<len(hit_rows) else .8)
    up=r.a23>=0; col=BLUE if up else VERM
    ax.annotate('',(r.a23,y),(r.a21,y),arrowprops=dict(arrowstyle='-|>',color=col,lw=2,shrinkA=0,shrinkB=0,mutation_scale=12))
    ax.scatter([r.a21],[y],s=48,color='white',edgecolor=col,lw=1.8,zorder=4)
    ax.text(-.01,y,name,transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=10,color=INK)
    ax.text(3.7,y,f'{r.a23:+.1f}',fontsize=9,color=col,va='center',ha='right',fontweight='bold')
ax.axvline(0,color=INK,lw=1.2); ax.text(0,n+1.1,'2019 level',ha='center',fontsize=9,color=INK); ax.text(3.7,n+1.1,'2023 vs 2019',ha='right',fontsize=9,color=INK,fontweight='bold')
sep=n-len(hit_rows)+.0+.4
ax.axhline(n-len(hit_rows)+.6,color='#bbb',lw=.8,ls=(0,(4,3)))
ax.text(-9.3,n+.9,'Hardest-hit by 2021 (selected)',fontsize=9.5,color=MUTED,fontweight='bold',va='bottom') if False else None
ax.text(.995,n+.5,'Deep 2021 losses, then full recovery',transform=ax.get_yaxis_transform(),ha='right',fontsize=9.5,color=BLUE,fontweight='bold',va='center') if False else None
ax.set_xlim(-11,3.8); ax.set_ylim(-.4,n+1.6); ax.set_yticks([])
ax.spines['left'].set_visible(False); ax.grid(axis='x',color=GRID,lw=.6); ax.set_axisbelow(True)
ax.set_xlabel('Change in life expectancy relative to 2019 (years)',fontsize=10.5)
ax.scatter([],[],s=48,color='white',edgecolor='#444',lw=1.8,label='2021'); ax.plot([],[],color=BLUE,lw=2,label='arrow to 2023: back above 2019'); ax.plot([],[],color=VERM,lw=2,label='arrow to 2023: still below 2019')
ax.legend(loc='lower left',frameon=False,fontsize=9,bbox_to_anchor=(0,.02))
ax.text(-10.8,len(X)-len(hit_rows)+ -0.0+1.45-1.0+0.0,'',fontsize=1)
ax.text(.01,.975,'Among the biggest 2019-21 losses',transform=ax.transAxes,ha='left',va='top',fontsize=9.5,color=MUTED,fontweight='bold')
ax.text(.01,.455,'Contrast cases',transform=ax.transAxes,ha='left',va='top',fontsize=9.5,color=MUTED,fontweight='bold')
titles(fig,"Countries hit hardest by COVID have bounced back; others have not",
 "Life expectancy at birth relative to its 2019 value: open dot = 2021, arrowhead = 2023. Latin American countries, South Africa and India lost 3 to 6 years by 2021 and are back at or above 2019; Germany, Canada and the US dipped less but are still below.",
 "Source: World Bank life expectancy at birth, both sexes, 1960-2023 (course file lifespan_dataset_1960.csv); countries only. Top group: seven of the ten countries with the largest 2019-21 declines (Guyana, Lebanon, Cuba omitted for space) plus India, a populous case; lower group: selected contrast cases with a smaller dip and a weaker recovery, plus Japan and Singapore as stable high-income examples. West Bank and Gaza's 2023 fall reflects the war, not COVID. Selection is deliberate, not a ranking of all 217 countries.",sw=118)
fig.savefig(FIG+'q4_covid_recovery_arrows.png'); plt.close(fig)
print(X.round(1))
