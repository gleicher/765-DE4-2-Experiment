"""Run from the project root:  /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py"""
import sys; sys.path.insert(0,'work')
from common import *
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D
OUT='answers/figures/'
INK='#222222'; GREY='#b8b8b8'; BLUE='#1f6fb4'; ORANGE='#d95f02'; TEAL='#1b9e77'; PURPLE='#7b3294'
def caption(fig,text,y=0.01):
    fig.text(0.015,y,text,ha='left',va='bottom',fontsize=8.5,color='#444444',wrap=True)

w=load_le(); cty=w[w.country]

# ---------- Q1A: lines of the female-male gap ----------
fig,ax=plt.subplots(figsize=(12,7.4))
fig.subplots_adjust(left=0.07,right=0.86,top=0.84,bottom=0.17)
for n,d in cty.groupby('name'):
    ax.plot(d.Year,d.gap,color=GREY,lw=0.6,alpha=0.55,zorder=1)
hi={'Russian Federation':(ORANGE,'Russia'),'Ukraine':('#b2182b','Ukraine'),'United States':(BLUE,'United States'),
    'India':(TEAL,'India'),'Nigeria':(PURPLE,'Nigeria'),'China':('#b8860b','China')}
ends={}
for n,(col,lab) in hi.items():
    d=cty[cty.name==n]; ax.plot(d.Year,d.gap,color=col,lw=2.4,zorder=3)
    ends[lab]=(d.gap.iloc[-1],col)
wd=w[w.name=='World']; ax.plot(wd.Year,wd.gap,color=INK,lw=3.2,ls='--',zorder=4)
ends['World']=(wd.gap.iloc[-1],INK)
# spread end labels
items=sorted(ends.items(),key=lambda kv:kv[1][0]); ys=[]
for i,(lab,(y,col)) in enumerate(items):
    yy=y if not ys else max(y,ys[-1]+0.75); ys.append(yy)
    ax.text(2023.8,yy,lab,color=col,fontsize=10.5,va='center',fontweight='bold')
ax.axhline(0,color=INK,lw=1)
ax.text(1960.3,0.25,'equal life expectancy',fontsize=9,color=INK)
ax.set_xlim(1960,2023); ax.set_ylim(-3,15)
ax.set_ylabel('Female minus male life expectancy at birth (years)')
ax.grid(axis='y',color='#e6e6e6',lw=0.7); ax.set_axisbelow(True)
ax.annotate('Russia: gap widens to 13 years\nafter the Soviet collapse',xy=(1995,13.5),xytext=(1966,12.6),fontsize=9.5,color=ORANGE,arrowprops=dict(arrowstyle='-',color=ORANGE))
ax.annotate('US: gap closes from 7.6 (1970)\nto 4.8 (2010)',xy=(2010,4.8),xytext=(1998,7.4),fontsize=9.5,color=BLUE,arrowprops=dict(arrowstyle='-',color=BLUE),bbox=dict(fc='white',ec='none',alpha=0.85))
ax.annotate("India: women's disadvantage\nin 1960 becomes a 3-year advantage",xy=(1975,-0.3),xytext=(1965,-2.5),fontsize=9.5,color=TEAL)
fig.suptitle('Women outlive men almost everywhere, but the gap has moved in opposite directions',x=0.07,ha='left',fontsize=16,fontweight='bold',y=0.965)
fig.text(0.07,0.885,'Female minus male life expectancy at birth, 1960-2023. Each grey line is one country; selected countries and the world are highlighted.',fontsize=10.5,color='#333')
caption(fig,'Data: World Bank life expectancy at birth by sex (course file lifespan_dataset_1960.csv); 219 countries/territories, regional aggregates excluded from grey lines.\nA positive value means women live longer. The world gap rose from 4.0 to 4.9 years, but countries differ widely: Nigeria has nearly closed its gap while Ukraine (2023) exceeds 13 years.')
fig.savefig(OUT+'q1_a_gap_over_time.png'); plt.close(fig)

# ---------- Q1B: scatter 1960 gap vs 2023 gap ----------
g=cty[cty.Year.isin([1960,2023])].pivot(index='name',columns='Year',values='gap').dropna()
g['d']=g[2023]-g[1960]
fig,ax=plt.subplots(figsize=(10,8.4))
fig.subplots_adjust(left=0.09,right=0.97,top=0.87,bottom=0.17)
lo,hi_=-9,15
ax.fill_between([lo,hi_],[lo,hi_],hi_,color=ORANGE,alpha=0.06); ax.fill_between([lo,hi_],lo,[lo,hi_],color=BLUE,alpha=0.06)
ax.plot([lo,hi_],[lo,hi_],color=INK,lw=1)
col=np.where(g.d>1,ORANGE,np.where(g.d<-1,BLUE,'#8c8c8c'))
ax.scatter(g[1960],g[2023],c=col,s=34,alpha=0.85,edgecolor='white',lw=0.5,zorder=3)
ax.set_xlim(-3,12); ax.set_ylim(-1,14)
labs={'Ukraine':(6,13.3,'Ukraine'),'Russian Federation':(8.3,10.7,'Russia'),'Poland':(5.5,8,'Poland'),'India':(-1.4,3.1,'India'),'China':(2.7,5.7,'China'),
 'United States':(6.5,5.3,'United States'),'Nigeria':(4.2,0.6,'Nigeria'),'Togo':(3.1,0.4,'Togo'),'Japan':(4.9,6.0,'Japan'),'Germany':(5.2,4.8,'Germany'),
 'Brazil':(4.5,6.2,'Brazil'),'Pakistan':(-0.5,8.3,'Pakistan'),'Kuwait':(3.9,1.0,'Kuwait'),'Lithuania':(None,None,'Lithuania'),'Cameroon':(None,None,'Cameroon'),'Korea, Rep.':(None,None,'South Korea'),'Bangladesh':(None,None,'Bangladesh')}
off={'Ukraine':(-6,6),'Russian Federation':(5,4),'Poland':(5,-12),'India':(6,-3),'China':(5,-12),'United States':(6,-14),'Nigeria':(6,-12),'Togo':(-30,-12),
 'Japan':(6,3),'Germany':(-36,-13),'Brazil':(-42,3),'Pakistan':(6,-3),'Kuwait':(6,3),'Lithuania':(6,-2),'Cameroon':(6,0),'Korea, Rep.':(6,0),'Bangladesh':(6,-4)}
for n,(_,_,lab) in labs.items():
    if n in g.index:
        ax.annotate(lab,(g.loc[n,1960],g.loc[n,2023]),xytext=off[n],textcoords='offset points',fontsize=9,color=INK)
ax.text(-2.8,13.4,'Gap WIDER in 2023\nthan in 1960',color=ORANGE,fontsize=11,fontweight='bold',va='top')
ax.text(11.8,-0.7,'Gap NARROWER\nin 2023 than in 1960',color=BLUE,fontsize=11,fontweight='bold',ha='right',va='bottom')
ax.text(1.6,1.0,'no change',rotation=45,fontsize=9,color=INK,ha='center')
ax.set_xlabel('Female advantage in 1960 (years)'); ax.set_ylabel('Female advantage in 2023 (years)')
ax.grid(color='#ececec',lw=0.7); ax.set_axisbelow(True)
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=ORANGE,label='widened by more than 1 year'),Line2D([],[],marker='o',ls='',color='#8c8c8c',label='within 1 year'),Line2D([],[],marker='o',ls='',color=BLUE,label='narrowed by more than 1 year')],loc='upper left',bbox_to_anchor=(0.0,0.82),frameon=False,fontsize=9.5,title='Change 1960 to 2023',title_fontsize=9.5)
fig.suptitle('Where did the female life-expectancy advantage grow, and where did it shrink?',x=0.09,ha='left',fontsize=13,fontweight='bold',y=0.965)
fig.text(0.09,0.915,'Each dot is a country: female minus male life expectancy in 1960 (x) against 2023 (y). Above the diagonal = gap grew.',fontsize=10,color='#333')
caption(fig,'Data: World Bank life expectancy at birth by sex; %d countries/territories with data in both years (aggregates excluded). Gap = female minus male, in years.\nMost countries lie near or above the diagonal (gap widened or held), but the biggest gaps in 2023 are in Eastern Europe, and several African countries have nearly closed theirs.'%len(g))
fig.savefig(OUT+'q1_b_gap_1960_vs_2023.png'); plt.close(fig)

# ---------- Census ----------
c=load_census()
rucc='Rural Urban Continuum Code 2023'
c=c.dropna(subset=[rucc]).copy()
names={1:'Metro, 1 million+',2:'Metro, 250k-1M',3:'Metro, under 250k',4:'Urban 20k+, adjacent to metro',5:'Urban 20k+, not adjacent',
       6:'Urban 5-20k, adjacent',7:'Urban 5-20k, not adjacent',8:'Rural (<5k urban), adjacent',9:'Rural (<5k urban), not adjacent'}
B=lambda y:"Percent of adults with a bachelor's degree or higher, %s"%y
# ---------- Q2A dumbbell ----------
med=c.groupby(rucc)[[B('1990'),B('2000'),B('2008-12'),B('2019-23')]].median()
fig,ax=plt.subplots(figsize=(11,7.2))
fig.subplots_adjust(left=0.30,right=0.95,top=0.80,bottom=0.17)
for i,code in enumerate(range(1,10)):
    y=9-i; a,b=med.loc[code,B('1990')],med.loc[code,B('2019-23')]
    metro=code<=3; col=BLUE if metro else ORANGE
    ax.plot([a,b],[y,y],color=col,lw=3,alpha=0.6,zorder=2)
    ax.scatter(a,y,s=70,facecolor='white',edgecolor=col,lw=2,zorder=3); ax.scatter(b,y,s=80,color=col,zorder=3)
    ax.text(a-0.6,y,'%.0f%%'%a,ha='right',va='center',fontsize=9.5,color=INK); ax.text(b+0.6,y,'%.0f%%'%b,ha='left',va='center',fontsize=9.5,color=INK,fontweight='bold')
    ax.text(37.5,y,'+%.1f'%(b-a),ha='center',va='center',fontsize=10,color=col,fontweight='bold')
ax.text(37.5,9.9,'Gain\n(pts)',ha='center',fontsize=9.5,color=INK,va='bottom')
ax.set_yticks(range(9,0,-1)); ax.set_yticklabels([('%d  '%k)+names[k] for k in range(1,10)],fontsize=10)
ax.set_xlim(4,39.5); ax.set_ylim(0.4,10.8)
ax.set_xlabel('Median county: percent of adults with a bachelor\'s degree or higher')
ax.grid(axis='x',color='#ececec'); ax.set_axisbelow(True)
ax.axhline(6.5,color=GREY,lw=0.8,ls=':'); ax.text(4.3,6.42,'metro above / nonmetro below',fontsize=8.5,color='#777',va='top')

ax.legend(handles=[Line2D([],[],marker='o',mfc='white',mec=INK,ls='',mew=2,label='1990'),Line2D([],[],marker='o',color=INK,ls='',label='2019-23')],loc='upper left',frameon=False)
fig.suptitle('College education grew everywhere, but metro counties pulled ahead',x=0.03,ha='left',fontsize=16,fontweight='bold',y=0.975)
fig.text(0.03,0.87,"Median share of adults with a bachelor's degree or higher, by county type, 1990 (open) vs 2019-23 (filled).\nBlue = metropolitan counties; orange = nonmetropolitan. Each row is one USDA Rural-Urban Continuum code (2023).",fontsize=10.5,color='#333',va='bottom')
caption(fig,"Data: USDA ERS county-level census file (course full_census_dataset.csv); %d counties with a 2023 Rural-Urban Continuum Code. Medians are per county, not population-weighted.\nThe largest metro counties gained %.1f points (15%% to 32%%); the most remote rural counties gained %.1f (11%% to 20%%), so the gap between them grew from %.0f to %.0f points."%(len(c),med.loc[1,B('2019-23')]-med.loc[1,B('1990')],med.loc[9,B('2019-23')]-med.loc[9,B('1990')],med.loc[1,B('1990')]-med.loc[9,B('1990')],med.loc[1,B('2019-23')]-med.loc[9,B('2019-23')]))
fig.savefig(OUT+'q2_a_education_by_county_type_dumbbell.png'); plt.close(fig)

# ---------- Q2B county scatter ----------
d=c.dropna(subset=[B('1990'),B('2019-23'),'Census Population 2020']).copy()
d['metro']=d[rucc]<=3
fig,ax=plt.subplots(figsize=(10,8.4))
fig.subplots_adjust(left=0.09,right=0.97,top=0.86,bottom=0.16)
for m,colr,lab in [(False,ORANGE,'Nonmetro counties'),(True,BLUE,'Metro counties')]:
    s=d[d.metro==m]; ax.scatter(s[B('1990')],s[B('2019-23')],s=8+s['Census Population 2020']/2e4,color=colr,alpha=0.35,edgecolor='none',label=lab,zorder=2)
x=np.array([0,80]); ax.plot(x,x,color=INK,lw=1)
for k in (15,30):
    ax.plot(x,x+k,color=INK,lw=0.8,ls=':'); 
ax.text(57,57+15+1,'+15 pts',fontsize=9,rotation=40,ha='center'); ax.text(41,41+30+1.2,'+30 pts',fontsize=9,rotation=40,ha='center')
ax.text(66,63.5,'no change',fontsize=9,rotation=40,ha='center')
for m,colr in [(True,BLUE),(False,ORANGE)]:
    s=d[d.metro==m]; mx,my=s[B('1990')].median(),s[B('2019-23')].median()
    ax.scatter(mx,my,s=170,color=colr,edgecolor=INK,lw=1.8,zorder=5,marker='D')
    ax.annotate(('Metro' if m else 'Nonmetro')+' median\n%.0f%% -> %.0f%%'%(mx,my),(mx,my),xytext=(12,-34) if m else (18,-26),textcoords='offset points',fontsize=9.5,fontweight='bold',color=colr)
big=d.nlargest(1,'Census Population 2020')
for nm in ['Los Angeles County','Loving County','Falls Church city']: pass
ax.set_xlim(0,70); ax.set_ylim(0,80)
ax.set_xlabel("Adults with a bachelor's degree or higher, 1990 (%)"); ax.set_ylabel("Adults with a bachelor's degree or higher, 2019-23 (%)")
ax.grid(color='#ececec',lw=0.7); ax.set_axisbelow(True)
leg=ax.legend(loc='upper left',frameon=False,markerscale=1.2,fontsize=10,title='Dot area = 2020 population',title_fontsize=9.5)
for h in leg.legend_handles: h.set_sizes([60])
fig.suptitle("Almost every county gained graduates; those that started ahead gained the most",x=0.09,ha='left',fontsize=14,fontweight='bold',y=0.965)
fig.text(0.09,0.915,"Each dot is a county: bachelor's-degree share in 1990 (x) vs 2019-23 (y). Above the solid line = share rose.",fontsize=10,color='#333')
caption(fig,"Data: USDA ERS county-level census file; %d counties with both years. Metro = Rural-Urban Continuum Code 1-3 (2023). Diamonds mark county medians (unweighted).\nThe median county that started above 30%% in 1990 gained 17 points; the median county that started below 10%% gained 8, so the spread between counties widened. (27 counties lost share.)"%len(d))
fig.savefig(OUT+'q2_b_education_1990_vs_2019_scatter.png'); plt.close(fig)

# ---------- Q3 unemployment compound ----------
grp={1:'Large metro (1M+)',2:'Other metro',3:'Other metro',4:'Nonmetro, adjacent to metro',6:'Nonmetro, adjacent to metro',8:'Nonmetro, adjacent to metro',
     5:'Nonmetro, remote',7:'Nonmetro, remote',9:'Nonmetro, remote'}
c['grp']=c[rucc].map(grp)
need=['Unemployed %d'%y for y in range(2000,2024)]+['Civilian labor force %d'%y for y in range(2000,2024)]
c3=c.dropna(subset=need).copy(); N3=len(c3)
order=['Large metro (1M+)','Other metro','Nonmetro, adjacent to metro','Nonmetro, remote']
colors=dict(zip(order,[BLUE,'#6baed6',ORANGE,'#8c510a']))
yrs=list(range(2000,2024))
rate={}
for gname,s in c3.groupby('grp'):
    rate[gname]=[s['Unemployed %d'%y].sum()/s['Civilian labor force %d'%y].sum()*100 for y in yrs]
rate=pd.DataFrame(rate,index=yrs)[order]
fig=plt.figure(figsize=(13,7.4))
gs=fig.add_gridspec(1,2,width_ratios=[1.75,1],left=0.06,right=0.97,top=0.82,bottom=0.2,wspace=0.28)
ax=fig.add_subplot(gs[0]); 
for a,b,t in [(2007.9,2009.9,'Great\nRecession'),(2019.7,2020.4,'Pandemic')]:
    ax.axvspan(a,b,color='#eeeeee',zorder=0); ax.text((a+b)/2,15.2 if t=='Pandemic' else 14.2,t,ha='center',fontsize=9,va='top',color='#555')
for gname in order:
    ax.plot(yrs,rate[gname],color=colors[gname],lw=2.4,label=gname)
    yl={'Large metro (1M+)':5.0,'Other metro':4.4,'Nonmetro, adjacent to metro':3.8,'Nonmetro, remote':3.2}[gname]
    ax.annotate(gname,(2023,rate[gname].iloc[-1]),xytext=(2023.8,yl),color=colors[gname],fontsize=9,va='center',arrowprops=dict(arrowstyle='-',color=colors[gname],lw=0.8))
ax.set_xlim(2000,2028.2); ax.set_ylim(2,15.5); ax.set_xticks(range(2000,2024,4))
ax.set_ylabel('Unemployment rate (%)'); ax.grid(axis='y',color='#ececec'); ax.set_axisbelow(True)
ax.set_title('Unemployment rate by county type, 2000-2023',loc='left',fontsize=11)
ax2=fig.add_subplot(gs[1])
ch=pd.DataFrame({'Great Recession\n2007 to 2010':rate.loc[2010]-rate.loc[2007],'Pandemic\n2019 to 2020':rate.loc[2020]-rate.loc[2019]})
yy=np.arange(len(order))[::-1]
for i,gname in enumerate(order):
    ax2.plot([ch.iloc[i,0],ch.iloc[i,1]],[yy[i]]*2,color=GREY,lw=1.5,zorder=1)
    ax2.scatter(ch.iloc[i,0],yy[i],s=90,color='white',edgecolor=colors[gname],lw=2.2,zorder=3)
    ax2.scatter(ch.iloc[i,1],yy[i],s=95,color=colors[gname],zorder=3)
    ax2.text(ch.iloc[i,0],yy[i]+0.22,'%+.1f'%ch.iloc[i,0],ha='center',fontsize=9)
    ax2.text(ch.iloc[i,1],yy[i]-0.42,'%+.1f'%ch.iloc[i,1],ha='center',fontsize=9,fontweight='bold')
ax2.set_yticks(yy); ax2.set_yticklabels(order,fontsize=9.5); ax2.set_ylim(-0.8,4.4); ax2.set_xlim(0,6)
ax2.set_xlabel('Rise in unemployment rate (percentage points)'); ax2.grid(axis='x',color='#ececec'); ax2.set_axisbelow(True)
ax2.set_title('How hard each shock hit',loc='left',fontsize=11)
ax2.legend(handles=[Line2D([],[],marker='o',mfc='white',mec=INK,ls='',mew=2,label='Great Recession (2007 to 2010)'),Line2D([],[],marker='o',color=INK,ls='',label='Pandemic (2019 to 2020)')],loc='upper left',frameon=False,fontsize=9)
fig.suptitle('The Great Recession hit every kind of county; the 2020 pandemic shock was steepest in big metros',x=0.06,ha='left',fontsize=14.5,fontweight='bold',y=0.965)
fig.text(0.06,0.885,'County unemployment rate (all unemployed / all labor force in each group), grouped by 2023 Rural-Urban Continuum Code.',fontsize=10.5,color='#333')
caption(fig,'Data: USDA ERS county-level census file (course full_census_dataset.csv), '+str(N3)+' counties with unemployment data in every year 2000-2023, summed within group. Rates are labor-force weighted.\nRecession dates (2007-09, 2020 pandemic) are common knowledge, not from the data. Descriptive only; the data show correlation, not cause.')
fig.savefig(OUT+'q3_unemployment_shocks_by_county_type.png'); plt.close(fig)

# ---------- Q4 heatmap ----------
p=cty.pivot(index='name',columns='Year',values='Both')
tiny={'Andorra','French Polynesia','Gibraltar','St. Lucia','Isle of Man','Channel Islands','Cayman Islands','Bermuda'}
ch=p[[2020,2021,2022,2023]].sub(p[2019],axis=0).drop(index=[t for t in tiny if t in p.index])
ch['m']=ch[[2020,2021]].min(axis=1)
top=ch.sort_values('m').head(25).drop(columns='m')
wl=w[w.name=='World'].set_index('Year').Both; top.loc['World (average)']=[wl[y]-wl[2019] for y in (2020,2021,2022,2023)]
top=top.rename(index={'Venezuela, RB':'Venezuela'})
fig=plt.figure(figsize=(9,10.4))
ax=fig.add_axes([0.2,0.15,0.62,0.68])
norm=TwoSlopeNorm(vmin=-6.5,vcenter=0,vmax=2.5)
im=ax.imshow(top.values,cmap='RdBu',norm=norm,aspect='auto')
for i in range(top.shape[0]):
    for j in range(4):
        v=top.values[i,j]; ax.text(j,i,'%+.1f'%v,ha='center',va='center',fontsize=9,color='white' if abs(v)>3.8 else INK)
ax.set_xticks(range(4)); ax.set_xticklabels(['2020','2021','2022','2023']); ax.xaxis.tick_top()
ax.set_yticks(range(len(top))); ax.set_yticklabels(top.index,fontsize=9.5)
for lab in ax.get_yticklabels():
    if lab.get_text().startswith('World'): lab.set_fontweight('bold')
ax.set_xticks(np.arange(-.5,4,1),minor=True); ax.set_yticks(np.arange(-.5,len(top),1),minor=True); ax.grid(which='minor',color='white',lw=1.5); ax.tick_params(which='both',length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.axhline(len(top)-1.5,color=INK,lw=1.5)
cax=fig.add_axes([0.2,0.115,0.62,0.016]); cb=fig.colorbar(im,cax=cax,orientation='horizontal'); cb.set_label('Change in life expectancy vs 2019 (years)',fontsize=9.5); cb.outline.set_visible(False)
fig.suptitle('Life expectancy fell sharply in 2020-21 in the hardest-hit countries,\nand had mostly recovered by 2023',x=0.03,ha='left',fontsize=15,fontweight='bold',y=0.975)
fig.text(0.03,0.885,'Change in life expectancy at birth (both sexes) relative to 2019, for the 25 countries with the largest drop in 2020 or 2021.',fontsize=10,color='#333')
caption(fig,'Data: World Bank life expectancy at birth, both sexes. Countries ranked by their largest 2020 or 2021 loss; very small territories (e.g., Andorra, Gibraltar) omitted.\nLatin America supplies the most entries (10 of 25). By 2023 most countries are back at or above their 2019 level; North Macedonia and Lebanon remain below.',y=0.012)
fig.savefig(OUT+'q4_covid_life_expectancy_heatmap.png'); plt.close(fig)
print(top.round(1)); print(med.round(1)); print(rate.loc[[2007,2010,2019,2020,2021,2023]].round(2)); print(ch.shape,len(g),len(d),len(c))
