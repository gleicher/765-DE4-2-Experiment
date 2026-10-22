from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mplconfig')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
OUT=ROOT/'answers/figures'; OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#c4cbd0','axes.labelcolor':'#344351','text.color':'#243441','xtick.color':'#536573','ytick.color':'#536573','figure.facecolor':'#fafaf7','axes.facecolor':'#fafaf7','savefig.facecolor':'#fafaf7'})
BLUE='#176d8c'; ORANGE='#c55a31'; GREY='#8a959c'
def frame(title,sub,caption,size=(12,8)):
 f=plt.figure(figsize=size)
 f.text(.075,.95,title,fontsize=22,weight='bold',va='top')
 f.text(.075,.889,sub,fontsize=11.5,va='top')
 f.text(.075,.045,caption,fontsize=9,color='#536573',va='bottom',linespacing=1.5)
 return f
def save(f,name):
 f.savefig(OUT/name,dpi=180);plt.close(f)
def grid(a):
 a.grid(axis='y',color='#dce1e2',linewidth=.7);a.set_axisbelow(True)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
p=l.pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)')
gap=(p.Female-p.Male).unstack('Year')
names=['Russian Federation','France','South Africa','Japan','United States','India']
short={'Russian Federation':'Russia'}
sel=gap.loc[names,1990:2023];sel.to_csv(ROOT/'work/life_sex_gap.csv')
f=frame('The female advantage follows different paths','Female minus male life expectancy at birth, 1990–2023 • Six illustrative countries',
 'Source: supplied World Bank life expectancy file. Gap = female estimate − male estimate (years).\nCountries were chosen to contrast trajectories; they are not a representative sample. No causal explanation is inferred.')
axs=f.subplots(2,3); f.subplots_adjust(left=.075,right=.96,bottom=.19,top=.80,hspace=.48,wspace=.22)
for a,n in zip(axs.flat,names):
 s=sel.loc[n];a.plot(s.index,s,color=BLUE,lw=2.5);a.scatter([1990,2023],[s[1990],s[2023]],c=BLUE,s=28,zorder=3)
 a.set(title=short.get(n,n),ylim=(0,14),xlim=(1989,2025),xticks=[1990,2000,2010,2023],yticks=[0,4,8,12]);grid(a)
 a.text(2023,s[2023]+.65,f'{s[2023]:.1f}',ha='right',color=BLUE,fontsize=10)
for a in axs[:,0]:a.set_ylabel('Gap (years)')
save(f,'01-life-gap-trajectories.png')
f=frame('A smaller sex gap is not a universal trend','Female minus male life expectancy at birth • The same six countries, 1990 and 2023',
 'Source: supplied World Bank life expectancy file. Gap = female estimate − male estimate. Sorted by 2023 gap.\nEndpoint comparison omits the intervening path; selected countries illustrate contrasts, not a global ranking.')
a=f.add_axes([.22,.23,.69,.55]);order=sel[2023].sort_values().index
for i,n in enumerate(order):
 x,y=sel.loc[n,[1990,2023]];a.plot([x,y],[i,i],c='#b7c1c5',lw=4);a.scatter(x,i,c=GREY,s=65,zorder=3);a.scatter(y,i,c=BLUE,s=65,zorder=4)
 a.text(12.3,i,f'{y-x:+.1f} years',va='center',fontsize=10)
a.set(yticks=range(6),yticklabels=[short.get(n,n) for n in order],xlim=(0,14),xlabel='Female − male life expectancy (years)');a.grid(axis='x',color='#dce1e2');a.set_axisbelow(True)
a.text(12.3,5.7,'Change',fontsize=10,weight='bold')
a.legend(handles=[Line2D([],[],marker='o',ls='',color=GREY,label='1990'),Line2D([],[],marker='o',ls='',color=BLUE,label='2023')],loc='upper left',bbox_to_anchor=(0,-.15),ncol=2,frameon=False)
save(f,'02-life-gap-endpoints.png')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
ru=pd.to_numeric(c['2023 Rural-urban Continuum Code'],errors='coerce')
c=c[c.State.ne('PR') & ru.between(1,9)].copy();c['group']=np.where(ru.loc[c.index].le(3),'Metro','Nonmetro')
old="Percent of adults with a bachelor's degree or higher, 1990";new="Percent of adults with a bachelor's degree or higher, 2019-23"
for col in [old,new,'Natural Change Rate 2023','Net Migration Rate 2023']:c[col]=pd.to_numeric(c[col],errors='coerce')
e=c.dropna(subset=[old,new]).copy();e[['FIPS Code','State','Area name','group',old,new]].to_csv(ROOT/'work/education_counties.csv',index=False)
stats=e.groupby('group')[[old,new]].agg(['count','median']);stats.to_csv(ROOT/'work/education_summary.csv')
cap='Source: supplied USDA/census county file. Adults’ bachelor’s degree or higher share; counties weighted equally.\nComplete pairs only; 50 states + DC, no Puerto Rico. Metro = 2023 RUCC 1–3, nonmetro = 4–9 (fixed across both periods).'
f=frame('College attainment rose; the county gap widened','Median bachelor’s share: metro 14.2% → 27.2%; nonmetro 10.9% → 19.5%',cap)
a=f.add_axes([.09,.24,.83,.54]);positions=[1,2,4,5];data=[e.loc[e.group.eq(g),col] for col in [old,new] for g in ['Metro','Nonmetro']]
b=a.boxplot(data,positions=positions,widths=.65,patch_artist=True,showfliers=False,whis=(10,90),medianprops={'color':'white','lw':2},boxprops={'lw':0},whiskerprops={'color':GREY},capprops={'color':GREY})
for box,color in zip(b['boxes'],[BLUE,ORANGE]*2):box.set_facecolor(color)
for x,s in zip(positions,data):a.text(x,s.median()+2.2,f'{s.median():.1f}%',ha='center',weight='bold')
a.set(xticks=positions,xticklabels=['Metro','Nonmetro','Metro','Nonmetro'],ylim=(0,65),ylabel='Adults with bachelor’s degree or higher (%)');grid(a)
a.text(1.5,-11,'1990',ha='center',weight='bold');a.text(4.5,-11,'2019–23',ha='center',weight='bold')
a.text(.02,.98,'Box: middle 50% of counties\nLine: median • whiskers: 10th–90th percentiles',transform=a.transAxes,va='top',fontsize=10)
save(f,'03-education-boxplots.png')
f=frame('More college graduates, but overlapping county profiles','County distributions shift right in both groups; the median gap grows from 3.3 to 7.7 percentage points',cap)
axs=f.subplots(1,2);f.subplots_adjust(left=.09,right=.95,bottom=.25,top=.78,wspace=.22)
for a,col,title in zip(axs,[old,new],['1990','2019–23']):
 for g,color in [('Metro',BLUE),('Nonmetro',ORANGE)]:
  vals=np.sort(e.loc[e.group.eq(g),col]);a.step(vals,np.arange(1,len(vals)+1)/len(vals)*100,where='post',c=color,lw=2.5,label=f'{g} (n={len(vals):,})')
  med=np.median(vals);a.scatter(med,50,c=color,s=35,zorder=4);a.annotate(f'{med:.1f}%',(med,50),xytext=(5,10 if g=='Metro' else -20),textcoords='offset points',color=color,fontsize=10)
 a.axhline(50,c=GREY,ls=':',lw=1);a.set(title=title,xlim=(0,80),ylim=(0,100),xlabel='Bachelor’s degree or higher (%)');grid(a);a.legend(loc='lower right',frameon=False,fontsize=9)
axs[0].set_ylabel('Counties at or below this share (%)')
save(f,'04-education-cumulative.png')
shock=['Mexico','South Africa','India','Russian Federation','United States','Japan']
f=frame('Recovery by 2023 did not erase every shortfall','Life expectancy at birth relative to each country’s 2019 level • Both sexes',
 'Source: supplied World Bank life expectancy file. Annual estimates minus the same country’s 2019 estimate.\nSix illustrative countries selected for contrasting declines and recovery. Timing alone does not establish causes.')
axs=f.subplots(2,3);f.subplots_adjust(left=.085,right=.96,bottom=.20,top=.79,hspace=.48,wspace=.23)
rows=[]
for a,n in zip(axs.flat,shock):
 s=p.loc[n,'Both'].loc[2019:2023];delta=s-s.loc[2019];rows.extend([(n,y,v) for y,v in delta.items()])
 a.axhline(0,c=GREY,lw=1);a.fill_between(delta.index,delta,0,color=BLUE,alpha=.10);a.plot(delta.index,delta,c=BLUE,lw=2.5,marker='o',ms=4)
 a.set(title=short.get(n,n),xlim=(2018.8,2023.4),ylim=(-5.5,2),xticks=[2019,2021,2023],yticks=[-4,-2,0,2]);grid(a)
 a.annotate(f'{delta.iloc[-1]:+.2f}',(2023,delta.iloc[-1]),xytext=(-3,10),textcoords='offset points',ha='right',color=BLUE,weight='bold')
for a in axs[:,0]:a.set_ylabel('Change from 2019 (years)')
pd.DataFrame(rows,columns=['country','year','change']).to_csv(ROOT/'work/life_recovery.csv',index=False)
save(f,'05-life-recovery.png')
m=c.dropna(subset=['Natural Change Rate 2023','Net Migration Rate 2023']).copy();x=m['Natural Change Rate 2023'];y=m['Net Migration Rate 2023'];q=(x.lt(0)&y.gt(0));print('Counties',len(m),'natural decrease migration gain',q.sum(),'positive combined',(q&(x+y>0)).sum());print(stats)
m[['FIPS Code','State','Area name','group','Natural Change Rate 2023','Net Migration Rate 2023']].to_csv(ROOT/'work/migration_counties.csv',index=False)
f=frame('Migration gains can offset a natural population decrease',f'{q.sum():,} of {len(m):,} counties have more deaths than births and positive net migration in 2023',
 'Source: supplied USDA/census county file. Rates per 1,000 residents; 50 states + DC, no Puerto Rico; complete rates only.\nMetro = 2023 RUCC 1–3. The diagonal marks zero combined natural-change + migration rate; residual change is excluded.')
a=f.add_axes([.085,.23,.61,.55]);
for g,color in [('Metro',BLUE),('Nonmetro',ORANGE)]:
 z=m[m.group.eq(g)];a.scatter(z['Natural Change Rate 2023'],z['Net Migration Rate 2023'],s=12,alpha=.40,c=color,edgecolors='none',label=g)
a.axvline(0,c=GREY,lw=1);a.axhline(0,c=GREY,lw=1);bounds=[min(x.min(),-10)-1,max(x.max(),10)+1];a.plot(bounds,[-v for v in bounds],c='#354856',ls='--',lw=1.2);a.set(xlim=bounds,xlabel='Natural change per 1,000 (births − deaths)',ylabel='Net migration per 1,000 (inflows − outflows)');grid(a)
a.legend(loc='upper right',frameon=False)
f.text(.73,.75,'Natural decrease +\nmigration gain',fontsize=13,weight='bold');f.text(.73,.65,f'{q.sum():,} counties',fontsize=22,color=BLUE,weight='bold');f.text(.73,.56,f'{(q&(x+y>0)).sum():,} above the diagonal:\nmigration more than offsets\nthe natural decrease.',fontsize=11,linespacing=1.5)
f.text(.73,.39,'Each dot is one county.\nAll complete rates are shown;\nextreme counties expand\nthe scale.',fontsize=10,linespacing=1.5)
save(f,'06-migration-natural-change.png')
