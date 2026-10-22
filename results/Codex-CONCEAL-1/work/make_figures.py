"""Run from the run directory with the p314 Python."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mplconfig')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
OUT=ROOT/'answers/figures'; OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelsize':12,'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'xtick.color':'#46505a','ytick.color':'#46505a','text.color':'#202a35','axes.labelcolor':'#202a35','savefig.facecolor':'#fbfaf7','figure.facecolor':'#fbfaf7'})
BLUE='#236b8e'; ORANGE='#c56a32'; GRAY='#81909b'; TEAL='#318674'; PURPLE='#82629f'
def page(title,subtitle,caption,size=(11,7.5)):
 f=plt.figure(figsize=size)
 f.text(.08,.935,title,fontsize=20,weight='bold',va='top')
 f.text(.08,.873,subtitle,fontsize=11.5,va='top',color='#46505a')
 f.text(.08,.045,caption,fontsize=9.3,va='bottom',linespacing=1.5,color='#46505a')
 return f

def save(f,name):
 f.savefig(OUT/name,dpi=180)
 plt.close(f)

def grid(a,axis='x'):
 a.grid(axis=axis,color='#deded8',lw=.7);a.set_axisbelow(True);a.tick_params(length=0)

life=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
codes=['USA','FRA','JPN','CHN','IND','BRA','RUS','ZAF']
name={'USA':'United States','FRA':'France','JPN':'Japan','CHN':'China','IND':'India','BRA':'Brazil','RUS':'Russia','ZAF':'South Africa'}
p=life[life['Country Code'].isin(codes)].pivot(index=['Country Code','Year'],columns='Sex',values='Life Expectancy (years)')
p['gap']=p.Female-p.Male
g=pd.DataFrame({str(y):p.xs(y,level='Year')['gap'] for y in [1990,2023]}).loc[codes]
g['change']=g['2023']-g['1990'];g.to_csv(ROOT/'work/life_gap_summary.csv')
f=page('The female advantage narrowed in France and the US',
       'Female minus male life expectancy, 1990 and 2023 • eight selected countries',
       'Source: supplied World Bank life expectancy data. Gap = female − male life expectancy at birth.\nCountries are illustrative cases, not a representative sample. Values rounded to one decimal; sorting uses unrounded values.')
a=f.add_axes([.19,.22,.62,.58]);s=g.sort_values('change');ys=np.arange(len(s))
a.hlines(ys,s['1990'],s['2023'],color='#c0c5c4',lw=4)
a.scatter(s['1990'],ys,c=GRAY,s=75,label='1990',zorder=3);a.scatter(s['2023'],ys,c=BLUE,s=75,label='2023',zorder=4)
a.set_yticks(ys,[name[c] for c in s.index]);a.invert_yaxis();a.set_xlim(0,12);a.set_xlabel('Female advantage in life expectancy (years)');grid(a)
a.legend(loc='upper left',bbox_to_anchor=(0,1.12),frameon=False,ncol=2)
a.text(12.05,-.65,'Change',fontsize=10,weight='bold')
for i,(c,r) in enumerate(s.iterrows()):
 a.text(12.05,i,f"{r['change']:+.1f} yr",va='center',fontsize=10,color=BLUE if r['change']<0 else ORANGE)
 a.text(r['2023'],i+.27,f"{r['2023']:.1f}",ha='center',va='top',fontsize=9,color=BLUE)
save(f,'01_life_gap_dumbbell.png')

f=page('Which countries narrowed the female advantage?',
       'The same eight countries • compare the gap in 1990 with the gap in 2023',
       'Source: supplied World Bank life expectancy data. Each point is one selected country; regional aggregates are excluded.\nGap = female − male life expectancy at birth. The diagonal marks no change; positions use unrounded data.')
a=f.add_axes([.12,.21,.76,.60]);a.set_aspect('equal',adjustable='box');a.plot([0,12],[0,12],c=GRAY,lw=1.2,ls='--')
a.fill_between([0,12],[0,12],12,color=ORANGE,alpha=.06);a.fill_between([0,12],0,[0,12],color=BLUE,alpha=.06)
a.text(.5,10.5,'Wider gap in 2023',color=ORANGE,fontsize=11);a.text(7,.7,'Narrower gap in 2023',color=BLUE,fontsize=11)
for c,r in g.iterrows():
 color=BLUE if r['change']<-.1 else ORANGE if r['change']>.1 else GRAY
 a.scatter(r['1990'],r['2023'],s=90,c=color,zorder=3)
 positions={'USA':(7.5,4.3),'FRA':(9.0,5.6),'JPN':(7.1,6.3),'CHN':(2.9,5.2),'IND':(1.7,3.4),'BRA':(4.1,7.4),'RUS':(10.8,11.1),'ZAF':(8.0,7.7)}
 a.annotate(name[c],(r['1990'],r['2023']),xytext=positions[c],fontsize=10,arrowprops={'arrowstyle':'-','lw':.7,'color':GRAY})
a.set(xlim=(0,12),ylim=(0,12),xlabel='Female advantage in 1990 (years)',ylabel='Female advantage in 2023 (years)');grid(a,'both')
save(f,'02_life_gap_scatter.png')

c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252')
c=c[(c.State!='PR') & c['2023 Rural-urban Continuum Code'].between(1,9)].copy()
c['group']=np.where(c['2023 Rural-urban Continuum Code']<=3,'Metro','Nonmetro')
n=c.dropna(subset=['Natural Change 2023','Net Migration 2023','Population Estimate 2023']).copy()
n=n[n['Natural Change 2023']<0].copy();n['ratio']=n['Net Migration 2023']/(-n['Natural Change 2023'])
n['status']=np.where(n.ratio>=1,'Offsets natural decrease',np.where(n.ratio>0,'Gain, but insufficient','No migration gain'))
n[['FIPS Code','State','Area name','group','Natural Change 2023','Net Migration 2023','ratio','status']].to_csv(ROOT/'work/migration_counties.csv',index=False)
counts=pd.crosstab(n.group,n.status).reindex(['Metro','Nonmetro'])
counts.to_csv(ROOT/'work/migration_summary.csv')
print('Natural-decrease county counts:\n',counts)
print('Ratio range:',n.ratio.min(),n.ratio.max())
f=page('Migration more often offsets loss in metro counties',
       '2023 • among counties with more deaths than births: 592 metro and 1,563 nonmetro counties',
       'Source: supplied USDA county data. Each county has equal weight; this is not a share of people. Net migration includes\ndomestic and international migration. US counties/equivalents, excluding Puerto Rico; metro = 2023 RUCC 1–3, nonmetro = 4–9.\nHorizontal scale is linear from −1 to +1 and logarithmic beyond; offset excludes residual population adjustments.')
a=f.add_axes([.11,.25,.79,.54]);
for group,color in [('Metro',BLUE),('Nonmetro',ORANGE)]:
 v=n.loc[n.group==group,'ratio'].sort_values().to_numpy(); y=np.arange(1,len(v)+1)/len(v)
 a.step(v,y,where='post',color=color,lw=2.5,label=group)
 prop=(v<1).mean();a.scatter([1],[prop],c=color,s=70,zorder=5)
 a.annotate(f'{prop:.0%} below offset threshold',(1,prop),xytext=(20,-18) if group=='Metro' else (60,-30),textcoords='offset points',color=color,fontsize=10)
a.set_xscale('symlog',linthresh=1,linscale=.8);a.set_xlim(-200,1000);a.set_ylim(0,1.03)
a.axvline(1,color='#46505a',ls='--',lw=1);a.text(1,1.055,'Migration = natural loss',ha='center',fontsize=10)
a.set_xticks([-200,-10,-1,0,1,10,100,1000],['−200','−10','−1','0','1','10','100','1,000'])
a.yaxis.set_major_formatter(PercentFormatter(1));a.set_xlabel('Net migrants / (deaths − births)');a.set_ylabel('Share of counties at or below this ratio');grid(a,'y');a.legend(frameon=False,loc='lower right')
save(f,'03_migration_cumulative.png')

f=page('Migration offsets natural decrease in 67% of metro counties',
       'Compared with 49% of nonmetro counties • US counties with more deaths than births in 2023',
       'Source: supplied USDA county data. Percentages use counties, not people, as the denominator; each county has equal weight.\nNet migration includes domestic and international migration. Metro = 2023 RUCC 1–3; nonmetro = 4–9. Puerto Rico excluded.\n“Offsets” means net migration ≥ deaths − births; residual population adjustments are not included.')
a=f.add_axes([.18,.29,.72,.43]);categories=['No migration gain','Gain, but insufficient','Offsets natural decrease'];colors=['#b8bebf',ORANGE,BLUE]
left=np.zeros(2)
for category,color in zip(categories,colors):
 values=counts[category].to_numpy();pct=values/counts.sum(axis=1).to_numpy()*100
 a.barh([1,0],pct,left=left,height=.44,color=color,label=category)
 for y,w,l,v in zip([1,0],pct,left,values):a.text(l+w/2,y,f'{w:.0f}%\n({v:,})',ha='center',va='center',color='white' if color!=colors[0] else '#202a35',fontsize=12)
 left+=pct
a.set_yticks([1,0],['Metro\nn = 592','Nonmetro\nn = 1,563']);a.set_xlim(0,100);a.xaxis.set_major_formatter(PercentFormatter());a.set_xlabel('Share of counties with natural decrease');grid(a)
a.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,1.3),ncol=3,fontsize=10)
save(f,'04_migration_stacked.png')

q=p.loc[(['CHN','IND'],slice(None)),:].reset_index();q.to_csv(ROOT/'work/china_india_series.csv',index=False)
f=page('China’s lead over India narrowed after 1980, but persists',
       'Life expectancy at birth by sex, 1960–2023 • the distance between lines is the country gap',
       'Source: supplied World Bank life expectancy data. Female and male estimates are shown separately; both panels share a scale.\nEndpoint labels show 2023 estimates. Trends are descriptive; the figure does not identify causes of changes.')
for i,sex in enumerate(['Female','Male']):
 a=f.add_axes([.10+i*.45,.24,.36,.55])
 for code,color in [('CHN',BLUE),('IND',ORANGE)]:
  v=q[q['Country Code']==code];a.plot(v.Year,v[sex],color=color,lw=2.5,label=name[code])
  a.scatter([2023],[v[sex].iloc[-1]],c=color,s=35)
  a.text(2025,v[sex].iloc[-1],f'{v[sex].iloc[-1]:.1f}',color=color,va='center',fontsize=10)
 a.set(xlim=(1960,2031),ylim=(30,90),xticks=[1960,1980,2000,2023],xlabel='Year');a.set_title(sex,loc='left',weight='bold');grid(a,'y')
 if i==0:a.set_ylabel('Life expectancy (years)');a.legend(frameon=False,loc='lower right')
 else:a.set_yticklabels([])
 for year in [1980,2023]:
  vals=q[q.Year==year].set_index('Country Code');gap=vals.loc['CHN',sex]-vals.loc['IND',sex]
  a.text(.03,.92 if year==1980 else .85,f'{year} country gap: {gap:.1f} years',transform=a.transAxes,fontsize=10)
save(f,'05_china_india_lines.png')

cols=[f"Percent of adults with a bachelor's degree or higher, {y}" for y in ['2000','2019-23']]
e=c.dropna(subset=cols).copy();e[['FIPS Code','group']+cols].to_csv(ROOT/'work/education_paired_counties.csv',index=False)
f=page('College attainment rose, but county distributions remain apart',
       'Bachelor’s degree or higher among adults • same counties compared in 2000 and 2019–23',
       'Source: supplied USDA county data. Boxes = middle 50% of counties; center lines = medians; whiskers = 1.5 × IQR; dots = outliers.\nEach county has equal weight, not each adult. Complete cases in both periods: 1,149 metro and 1,940 nonmetro counties.\nMetro/nonmetro uses fixed 2023 RUCC (1–3 / 4–9); Puerto Rico excluded. 2019–23 is a five-year estimate, not a single-year census.')
a=f.add_axes([.11,.24,.79,.55]);positions=[1,2,4,5];data=[];colors=[]
for group,color in [('Metro',BLUE),('Nonmetro',ORANGE)]:
 for col in cols:data.append(e.loc[e.group==group,col].to_numpy());colors.append(color)
b=a.boxplot(data,positions=positions,widths=.58,orientation='horizontal',patch_artist=True,
            flierprops={'marker':'.','markersize':3,'alpha':.28,'markeredgecolor':GRAY},medianprops={'color':'white','linewidth':2},whiskerprops={'color':GRAY},capprops={'color':GRAY})
for patch,color in zip(b['boxes'],colors):patch.set_facecolor(color);patch.set_edgecolor(color)
a.set_yticks(positions,['Metro · 2000','Metro · 2019–23','Nonmetro · 2000','Nonmetro · 2019–23']);a.invert_yaxis();a.set(xlim=(0,85),xlabel='Adults with a bachelor’s degree or higher (%)');grid(a)
for pos,v,col in zip(positions,data,colors):
 a.text(np.median(v)+1.2,pos-.19,f'Median {np.median(v):.1f}%',color=col,fontsize=10,va='bottom')
print('Education medians:',[float(np.median(v)) for v in data])
save(f,'06_education_boxplots.png')
