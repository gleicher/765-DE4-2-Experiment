import pandas as pd, numpy as np, warnings, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
OUT='../answers/figures/'; os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':100,'savefig.dpi':200})
BLUE,ORANGE,GRAY,RED,GREEN='#1f77b4','#e66101','#8c8c8c','#b2182b','#4d9221'

def cap(fig,text,y=0.01):
    fig.text(0.02,y,text,fontsize=9,color='#444',va='bottom',ha='left',wrap=True)

# ---------- life expectancy ----------
l=pd.read_csv('../data/lifespan_dataset_1960.csv'); l.columns=['i','country','code','sex','year','le']
w=l.pivot_table(index=['country','year'],columns='sex',values='le').reset_index()
w['gap']=w.Female-w.Male

# Fig 1A: gap over time by income group
groups={'High income':BLUE,'Upper middle income':'#7b3294','Lower middle income':GREEN,'Low income':ORANGE}
fig,ax=plt.subplots(figsize=(9,6.2))
for g,col in groups.items():
    d=w[w.country==g]; ax.plot(d.year,d.gap,color=col,lw=2.5)
    ax.text(2024,d.gap.iloc[-1]+{'High income':0.2,'Upper middle income':-0.2}.get(g,0),g,color=col,va='center',fontsize=10)
d=w[w.country=='High income']; pk=d.loc[d.gap.idxmax()]
ax.annotate(f'High-income peak:\n{pk.gap:.1f} yrs in {int(pk.year)}',(pk.year,pk.gap),(1962,7.3),arrowprops=dict(arrowstyle='-',color=BLUE),color=BLUE,fontsize=10)
ax.set_xlim(1960,2041); ax.set_xticks(range(1960,2030,10)); ax.set_ylim(0,8)
ax.annotate('1971: Bangladesh war\nspike in lower-middle group',(1971,2.0),(1976,0.3),arrowprops=dict(arrowstyle='-',color=GREEN),color=GREEN,fontsize=9); ax.set_xlabel('Year'); ax.set_ylabel('Female minus male life expectancy at birth (years)')
ax.yaxis.grid(True,color='#ddd'); ax.set_axisbelow(True)
fig.suptitle('Women\'s life-expectancy advantage peaked in rich countries in 1994\nand has shrunk since, while it kept growing in poorer groups',x=0.02,ha='left',fontsize=14,fontweight='bold')
fig.subplots_adjust(top=0.87,bottom=0.17,left=0.09,right=0.98)
cap(fig,'World Bank life expectancy at birth by sex, 1960-2023, for World Bank income groups. The high-income gap rose to 1994 and has\nfallen since; the lower-middle and low-income gaps kept widening for decades (low-income peaked in 2020).')
fig.savefig(OUT+'q1_vis1_gap_by_income_group.png'); plt.close(fig)

# Fig 1B: dumbbell 1960 / peak / 2023 for selected countries
sel=['Russian Federation','Japan','United States','Germany','France','United Kingdom','Brazil','Mexico','China','India','Indonesia','Turkiye','Iran, Islamic Rep.','Pakistan','Nigeria','Egypt, Arab Rep.','South Africa','Korea, Rep.','Bangladesh','Ethiopia']
rows=[]
for c in sel:
    d=w[w.country==c].set_index('year').gap
    rows.append((c,d[1960],d.idxmax(),d.max(),d[2023]))
t=pd.DataFrame(rows,columns=['c','g60','pky','pk','g23']).sort_values('g23')
t['c']=t.c.replace({'Russian Federation':'Russia','Iran, Islamic Rep.':'Iran','Egypt, Arab Rep.':'Egypt','Korea, Rep.':'South Korea','Turkiye':'Turkey'})
fig,ax=plt.subplots(figsize=(8.5,8.2))
y=np.arange(len(t))
ax.hlines(y,t.g60,t.g23,color='#bbb',lw=3,zorder=1)
ax.scatter(t.g60,y,color=GRAY,s=60,zorder=2,label='1960')
ax.scatter(t.g23,y,color=[RED if a<b-0.5 else BLUE for a,b in zip(t.g23,t.pk)],s=70,zorder=3)
ax.scatter(t.pk,y,marker='|',color='k',s=150,zorder=2,label='Peak year')
for yi,(a,b) in enumerate(zip(t.pky,t.pk)): ax.text(b+0.25,yi,int(a),fontsize=8,va='center',color='#333')
ax.set_yticks(y); ax.set_yticklabels(t.c); ax.set_xlabel('Female minus male life expectancy (years)')
ax.xaxis.grid(True,color='#eee'); ax.set_axisbelow(True); ax.set_xlim(-10,16); ax.axvline(0,color='k',lw=.8)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=GRAY,label='1960'),Line2D([],[],marker='o',ls='',color=BLUE,label='2023 (still near its peak)'),Line2D([],[],marker='o',ls='',color=RED,label='2023 (>0.5 yr below its peak)'),Line2D([],[],marker='|',ls='',color='k',markersize=12,label='Peak (label = year)')],loc='upper center',bbox_to_anchor=(0.4,-0.08),ncol=4,frameon=False,fontsize=8.5)
nb=int(((t.pk-t.g23)>0.5).sum())
fig.suptitle(f'{nb} of these 20 large countries now have a female advantage\nmore than half a year below their own peak',x=0.02,ha='left',fontsize=13,fontweight='bold')
fig.subplots_adjust(top=0.9,bottom=0.17,left=0.17,right=0.97)
cap(fig,'Women\'s minus men\'s life expectancy at birth for 20 large countries (World Bank). Sorted by 2023 gap.\nNegative values mean men lived longer (Pakistan, Iran, Bangladesh and India in 1960).')
fig.savefig(OUT+'q1_vis2_gap_dumbbell_countries.png'); plt.close(fig)

# ---------- census ----------
c=pd.read_csv('../data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin1')
c=c[c.State!='PR'].copy()
ED="Percent of adults with a bachelor's degree or higher, 2019-23"
c['rucc']=c['Rural Urban Continuum Code 2023']
c['metro']=np.where(c.rucc<=3,'Metro counties (RUCC 1-3)','Nonmetro counties (RUCC 4-9)')
yrs=list(range(2000,2024))
UC=[f'Unemployment rate {y}' for y in yrs]
cc=c.dropna(subset=[ED]+UC).copy()
cc['tier']=pd.qcut(cc[ED],3,labels=['Lowest third','Middle third','Highest third'])
cols={'Lowest third':ORANGE,'Middle third':GRAY,'Highest third':BLUE}

# Fig 2A: time series by education tercile
fig,ax=plt.subplots(figsize=(9.5,6.2))
for k,col in cols.items():
    s=cc[cc.tier==k][UC].median(); s.index=yrs
    ax.plot(yrs,s.values,color=col,lw=2.6); ax.text(2023.3,s.values[-1]+(0.0 if k!='Middle third' else 0.0),k,color=col,va='center',fontsize=10)
ax.axvspan(2007.5,2009.5,color='#eee',zorder=0); ax.axvspan(2019.5,2020.5,color='#eee',zorder=0)
ax.text(2008.5,11.6,'Great\nRecession',ha='center',fontsize=9,color='#555'); ax.text(2020,11.6,'COVID',ha='center',fontsize=9,color='#555')
ax.annotate('2020: highest-education\ncounties pass the middle third',(2020,6.3),(2011.5,1.3),arrowprops=dict(arrowstyle='->',color=BLUE),color=BLUE,fontsize=9.5)
ax.set_xlim(2000,2026.3); ax.set_ylim(0,12.5); ax.set_ylabel('Median county unemployment rate (%)'); ax.set_xlabel('Year')
ax.yaxis.grid(True,color='#ddd'); ax.set_axisbelow(True)
fig.suptitle('Counties with fewer college graduates have had higher unemployment\nin every year, but in 2020 the gap nearly closed',x=0.02,ha='left',fontsize=14,fontweight='bold')
fig.subplots_adjust(top=0.87,bottom=0.17,left=0.09,right=0.88)
cap(fig,'Median unemployment rate across US counties (excluding Puerto Rico), grouped into thirds by share of adults with a bachelor\'s degree or\nhigher in 2019-23 (about 1,000 counties each). USDA ERS county data. Education groups are fixed using the 2019-23 values.')
fig.savefig(OUT+'q2_vis1_unemployment_by_education_tier.png'); plt.close(fig)

# Fig 2B: scatter 2019 vs 2020
fig,axs=plt.subplots(1,2,figsize=(11,5.8),sharey=True)
for ax,yr in zip(axs,[2019,2020]):
    x=cc[ED]; yv=cc[f'Unemployment rate {yr}']
    cl=np.where(cc.rucc<=3,BLUE,ORANGE)
    ax.scatter(x,yv,s=np.sqrt(cc['Census Population 2020'])/9,c=cl,alpha=.28,lw=0)
    m,b=np.polyfit(x,yv,1); xs=np.array([x.min(),x.max()])
    ax.plot(xs,m*xs+b,color='k',lw=2); ax.text(0.97,0.95,f'trend: {m*10:+.2f} pts per +10 pts\nbachelor\'s share',transform=ax.transAxes,ha='right',va='top',fontsize=10)
    ax.set_title(str(yr),fontsize=13,loc='left',fontweight='bold'); ax.set_xlabel("Adults with a bachelor's degree or higher, 2019-23 (%)"); ax.set_ylim(0,16)
    ax.yaxis.grid(True,color='#eee'); ax.set_axisbelow(True)
axs[0].set_ylabel('County unemployment rate (%)')
axs[1].legend(handles=[Line2D([],[],marker='o',ls='',color=BLUE,alpha=.6,label='Metro (RUCC 1-3)'),Line2D([],[],marker='o',ls='',color=ORANGE,alpha=.6,label='Nonmetro (RUCC 4-9)')],loc='lower right',frameon=False,fontsize=9)
fig.suptitle('More educated counties had lower unemployment in 2019;\nin 2020 the relationship was about half as steep',x=0.02,ha='left',fontsize=14,fontweight='bold')
fig.subplots_adjust(top=0.84,bottom=0.2,left=0.07,right=0.98,wspace=0.05)
cap(fig,'Each dot is a county (Puerto Rico excluded); area scales with 2020 population. Line is an ordinary least squares fit on all counties, unweighted.')
fig.savefig(OUT+'q2_vis2_scatter_2019_2020.png'); plt.close(fig)
for yr in [2019,2020]:
    print(yr,np.polyfit(cc[ED],cc[f'Unemployment rate {yr}'],1)[0]*10)

# ---------- Q3: COVID life expectancy ----------
b=l[l.sex=='Both'].pivot(index='country',columns='year',values='le')
sel3=['Bolivia','Mexico','Peru','Colombia','South Africa','India','Brazil','Russian Federation','United States','Germany','United Kingdom','France','Japan','China','Korea, Rep.','Australia','Indonesia','Egypt, Arab Rep.']
t=pd.DataFrame({'d21':b.loc[sel3,2021]-b.loc[sel3,2019],'d23':b.loc[sel3,2023]-b.loc[sel3,2019]}).sort_values('d21',ascending=False)
t.index=t.index.str.replace('Russian Federation','Russia').str.replace('Egypt, Arab Rep.','Egypt').str.replace('Korea, Rep.','South Korea')
fig,ax=plt.subplots(figsize=(8.5,7.2))
y=np.arange(len(t))[::-1]
ax.hlines(y,t.d21,t.d23,color='#bbb',lw=3)
ax.scatter(t.d21,y,color=RED,s=65,label='2021',zorder=3); ax.scatter(t.d23,y,color=BLUE,s=65,label='2023',zorder=3)
ax.axvline(0,color='k',lw=1); ax.set_yticks(y); ax.set_yticklabels(t.index)
ax.set_xlabel('Change in life expectancy at birth since 2019 (years)'); ax.xaxis.grid(True,color='#eee'); ax.set_axisbelow(True)
ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0.0,0.85))
fig.suptitle('The pandemic cost Latin America and South Asia 3-6 years of life expectancy;\nby 2023 most had recovered, Germany and the US were still below 2019',x=0.02,ha='left',fontsize=13,fontweight='bold')
fig.subplots_adjust(top=0.89,bottom=0.15,left=0.2,right=0.97)
cap(fig,'Life expectancy at birth, both sexes, relative to its 2019 value, for 18 large countries (World Bank). Red = 2021, blue = 2023; the grey bar is the recovery.')
fig.savefig(OUT+'q3_vis_covid_life_expectancy.png'); plt.close(fig)
print(t.round(2))

# ---------- Q4: 2020 unemployment jump by rurality ----------
c4=c.dropna(subset=['Unemployment rate 2019','Unemployment rate 2020']).copy()
c4['d']=c4['Unemployment rate 2020']-c4['Unemployment rate 2019']
lab={1:'1 Metro, 1M+',2:'2 Metro, 250k-1M',3:'3 Metro, <250k',4:'4 Urban 20k+, adj. to metro',5:'5 Urban 20k+, not adj.',6:'6 Urban 5-20k, adj.',7:'7 Urban 5-20k, not adj.',8:'8 Rural, adj. to metro',9:'9 Rural, not adj.'}
fig,ax=plt.subplots(figsize=(9.5,6.6))
rng=np.random.default_rng(1)
for k in range(1,10):
    d=c4[c4.rucc==k].d
    col=BLUE if k<=3 else ORANGE
    ax.scatter(d,k+rng.uniform(-.28,.28,len(d)),s=7,color=col,alpha=.25,lw=0)
    q1,md,q3=d.quantile([.25,.5,.75]); ax.hlines(k,q1,q3,color='k',lw=4); ax.scatter(md,k,color='white',edgecolor='k',s=55,zorder=5,lw=1.5)
    ax.text(10.3,k,f'{md:.1f}',va='center',fontsize=9.5,fontweight='bold')
ax.text(10.3,0.4,'median',fontsize=9,color='#444')
ax.set_yticks(range(1,10)); ax.set_yticklabels([lab[k] for k in range(1,10)]); ax.invert_yaxis()
ax.set_xlim(-3,10); ax.set_clip_on(False); ax.set_xlabel('Change in county unemployment rate, 2019 to 2020 (percentage points)')
ax.axvline(0,color='#888',lw=.8); ax.xaxis.grid(True,color='#eee'); ax.set_axisbelow(True)
fig.suptitle('The 2020 unemployment jump was biggest in big metros and generally shrinks\nas counties get more rural',x=0.02,ha='left',fontsize=14,fontweight='bold')
fig.subplots_adjust(top=0.87,bottom=0.17,left=0.27,right=0.93)
cap(fig,'Each dot is a US county (Puerto Rico excluded; 7 outliers above +10 not shown), grouped by 2023 USDA Rural-Urban Continuum Code. Black bar =\ninterquartile range; white circle = median. Blue = metro codes, orange = nonmetro.')
fig.savefig(OUT+'q4_vis_unemployment_jump_by_rucc.png'); plt.close(fig)
print(c4.groupby('rucc').d.median(), (c4.d>10).sum(), len(c4))
