from pathlib import Path
import os
os.environ['MPLCONFIGDIR']=str(Path(__file__).resolve().parent/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'answers/figures'; OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':'#334155','text.color':'#152a3a','axes.edgecolor':'#cbd5e1','xtick.color':'#475569','ytick.color':'#475569','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fafaf7','axes.facecolor':'#fafaf7','savefig.facecolor':'#fafaf7'})
BLUE='#177e89'; ORANGE='#bd5a2e'; PURPLE='#7653a6'; GRAY='#687785'
def canvas(title,subtitle,size=(12,8)):
 f=plt.figure(figsize=size); f.text(.065,.95,title,fontsize=23,fontweight='bold',va='top');f.text(.065,.888,subtitle,fontsize=12,va='top',color='#475569'); return f
def footer(f,text): f.text(.065,.035,text,fontsize=9,color='#475569',va='bottom',linespacing=1.5)
def save(f,name): f.savefig(OUT/name,dpi=180);plt.close(f)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv');c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
c=c[(c.State!='PR') & (pd.to_numeric(c['FIPS Code'])%1000!=0)].copy()
ru='2023 Rural-urban Continuum Code';c=c[c[ru].between(1,9)].copy();c[ru]=c[ru].astype(int)
countries=['France','Japan','United States','Sweden','Brazil','South Africa']
p=l[l['Country Name'].isin(countries)].pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)');p['gap']=p.Female-p.Male
colors={'France':PURPLE,'Japan':BLUE,'United States':ORANGE,'Sweden':'#57772e','Brazil':'#a34878','South Africa':'#536475'}
f=canvas('A longer life for women — but a changing gap','Female minus male life expectancy, 1960–2023 • Six selected countries; gaps are measured in years')
axs=f.subplots(2,3);f.subplots_adjust(left=.07,right=.95,bottom=.18,top=.80,wspace=.23,hspace=.45)
for ax,name in zip(axs.flat,countries):
 d=p.loc[name];ax.plot(d.index,d.gap,color=colors[name],lw=2.7);ax.set_title(name,loc='left',fontweight='bold',fontsize=13);ax.set_ylim(0,10);ax.set_xlim(1960,2027);ax.set_xticks([1960,1990,2023]);ax.set_yticks([0,5,10]);ax.grid(axis='y',alpha=.25);ax.scatter([1990,2023],d.loc[[1990,2023],'gap'],s=28,color=colors[name]);ax.text(2024,d.loc[2023,'gap'],f"{d.loc[2023,'gap']:.1f}",va='center',fontsize=10)
f.text(.025,.47,'Female advantage (years)',rotation=90,va='center',fontsize=11)
footer(f,'Four of these six countries have smaller gaps than in 1990; Japan and Brazil have larger gaps.\nSelection illustrates contrasting trajectories, not a representative world sample. Source: supplied World Bank life expectancy CSV.')
save(f,'01_life_gap_trajectories.png')
gaps=p['gap'].unstack('Year')[[1990,2023]].sort_values(2023)
f=canvas('The sex gap narrowed in some places, widened in others','The same six countries • Female minus male life expectancy in 1990 and 2023')
ax=f.add_axes([.19,.23,.65,.55]); y=np.arange(len(gaps));ax.hlines(y,gaps[1990],gaps[2023],color='#cbd5e1',lw=5);ax.scatter(gaps[1990],y,s=100,facecolors='#fafaf7',edgecolors=GRAY,lw=2,label='1990',zorder=3);ax.scatter(gaps[2023],y,s=100,color=BLUE,label='2023',zorder=4)
for i,(name,row) in enumerate(gaps.iterrows()):ax.text(8.65,i,f'{row[2023]-row[1990]:+.1f}',va='center',fontweight='bold',color=ORANGE if row[2023]>row[1990] else BLUE)
ax.text(8.65,5.65,'Change\n(years)',fontsize=10,va='center');ax.set_yticks(y,gaps.index);ax.set_xlim(0,9.3);ax.set_xticks(range(9));ax.set_xlabel('Female advantage in life expectancy (years)');ax.grid(axis='x',alpha=.2);ax.legend(loc='upper left',bbox_to_anchor=(0,1.12),frameon=False,ncol=2);ax.spines['left'].set_visible(False)
footer(f,'Read the filled dot against the hollow dot: movement left is a smaller gap; movement right is a larger gap.\nCountries sorted by 2023 gap. Endpoint comparison hides intervening changes. Source: supplied World Bank CSV; gap = female − male.')
save(f,'02_life_gap_endpoints.png')
a="Percent of adults with a bachelor's degree or higher, 1990";b="Percent of adults with a bachelor's degree or higher, 2019-23";edu=c.dropna(subset=[a,b]).copy();med=edu.groupby(ru)[[a,b]].median();counts=edu.groupby(ru).size()
labels=['1  Metro ≥1 million','2  Metro 250,000–999,999','3  Metro <250,000','4  Nonmetro ≥20,000; adjacent','5  Nonmetro ≥20,000; nonadjacent','6  Nonmetro 5,000–19,999; adjacent','7  Nonmetro 5,000–19,999; nonadjacent','8  Nonmetro <5,000; adjacent','9  Nonmetro <5,000; nonadjacent']
f=canvas('College attainment rose in every county type','Median county share of adults with a bachelor’s degree or higher • Matched counties, 1990 vs. 2019–23')
ax=f.add_axes([.34,.22,.53,.57]);y=np.arange(9);ax.hlines(y,med[a],med[b],lw=4,color='#d2d9de');ax.scatter(med[a],y,s=80,facecolors='#fafaf7',edgecolors=GRAY,lw=1.7,label='1990',zorder=3);ax.scatter(med[b],y,s=80,color=BLUE,label='2019–23',zorder=3)
for i,k in enumerate(med.index):ax.text(med.loc[k,b]+.65,i,f'{med.loc[k,b]:.1f}%',va='center',fontsize=10);ax.text(43,i,f'+{med.loc[k,b]-med.loc[k,a]:.1f}',va='center',fontsize=10)
ax.text(43,-.8,'Gain (pp)',fontsize=10);ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,47);ax.set_xticks([0,10,20,30,40]);ax.set_xlabel('Adults with a bachelor’s degree or higher (%)');ax.grid(axis='x',alpha=.22);ax.legend(loc='upper left',bbox_to_anchor=(0,1.12),frameon=False,ncol=2);ax.spines['left'].set_visible(False)
footer(f,f'Each county has equal weight (n = {len(edu):,}); these are medians of county percentages, not shares of all residents.\nCounty types use 2023 rural–urban codes for both periods; “adjacent” means adjacent to a metro area.\n2019–23 is a pooled estimate. U.S. counties / equivalents, excluding Puerto Rico. Source: supplied USDA / Census county CSV.')
save(f,'03_education_medians.png')
f=canvas('Gains extend beyond the median county','Distribution of county bachelor’s attainment, by 2023 rural–urban code • Same matched counties as the paired-dot view')
ax=f.add_axes([.12,.24,.83,.55]);pos=np.arange(1,10)
for col,offset,color,label in [(a,-.17,GRAY,'1990'),(b,.17,BLUE,'2019–23')]:
 vals=[edu.loc[edu[ru]==k,col].to_numpy() for k in pos];bp=ax.boxplot(vals,positions=pos+offset,widths=.27,patch_artist=True,showfliers=False,whis=(10,90),manage_ticks=False)
 for box in bp['boxes']:box.set(facecolor=color,alpha=.5,edgecolor=color)
 for el in ['whiskers','caps','medians']:
  for line in bp[el]:line.set(color=color,lw=1.6)
 ax.plot([],[],color=color,lw=8,alpha=.6,label=label)
ax.set_xticks(pos,[f'{k}\nn={counts[k]}' for k in pos]);ax.set_xlabel('2023 rural–urban code (sample size is matched counties)');ax.set_ylabel('Adults with a bachelor’s degree or higher (%)');ax.set_ylim(0,65);ax.grid(axis='y',alpha=.23);ax.legend(frameon=False,ncol=2,loc='upper right');ax.axvline(3.5,color='#94a3b8',ls=':',lw=1);ax.text(2,61,'METRO',ha='center',fontsize=10);ax.text(6.5,61,'NONMETRO',ha='center',fontsize=10)
footer(f,'Boxes: middle 50% of counties; line: median; whiskers: 10th–90th percentiles. Outside observations omitted visually, retained in summaries.\nCodes 1–3: metro sizes ≥1m / 250k–999k / <250k. Codes 4–9: nonmetro urban sizes ≥20k / 5k–19,999 / <5k, each adjacent then nonadjacent.\nEqual county weights; 2023 classifications held fixed; 2019–23 pooled estimates. Source: supplied USDA / Census CSV; Puerto Rico excluded.')
save(f,'04_education_distributions.png')
f=canvas('South Africa’s life expectancy reversed, then recovered','Female and male life expectancy, 1960–2023 • Both series recover from their own post-1990 low')
ax=f.add_axes([.09,.24,.77,.55]);d=p.loc['South Africa']
for sex,color in [('Female',PURPLE),('Male',BLUE)]:
 ax.plot(d.index,d[sex],color=color,lw=3);low=d.loc[1990:,sex].idxmin();v=d.loc[low,sex];ax.scatter([low,2023],[v,d.loc[2023,sex]],color=color,s=60,zorder=3);ax.annotate(f'{low} low: {v:.1f}',(low,v),xytext=(low-15,v-5),arrowprops={'arrowstyle':'-','color':color},color=color,fontsize=11);ax.text(2024,d.loc[2023,sex],f'{sex}\n{d.loc[2023,sex]:.1f}',color=color,va='center',fontsize=12,fontweight='bold')
ax.set_xlim(1960,2031);ax.set_ylim(40,75);ax.set_xticks([1960,1970,1980,1990,2000,2010,2023]);ax.set_ylabel('Life expectancy at birth (years)');ax.set_xlabel('Year');ax.grid(axis='y',alpha=.25)
footer(f,'Both sexes surpassed their 1990 life expectancy by 2023, despite a substantial intervening decline.\nLow points are selected separately for each sex over 1990–2023. Lines show reported annual estimates, with no smoothing.\nThis chart describes change; the data alone do not identify its causes. Source: supplied World Bank life expectancy CSV.')
save(f,'05_south_africa_recovery.png')
nat='Natural Change Rate 2023';mig='Net Migration Rate 2023';pop=c.dropna(subset=[nat,mig]);pop.to_csv(ROOT/'work/migration_plot_data.csv',index=False)
f=canvas('Migration can offset more deaths than births','County natural change and net migration, 2023 • Rates per 1,000 residents; each dot is one county')
ax=f.add_axes([.09,.22,.62,.58]);x=pop[nat];z=pop[mig];lim=max(abs(x).max(),abs(z).max());extent=int(np.ceil(lim/10)*10)
for mask,color,label in [(pop[ru]>3,BLUE,'Nonmetro (codes 4–9)'),(pop[ru]<=3,ORANGE,'Metro (codes 1–3)')]:ax.scatter(x[mask],z[mask],s=14,alpha=.38,color=color,label=label,edgecolors='none')
ax.axhline(0,color='#64748b',lw=1);ax.axvline(0,color='#64748b',lw=1);xx=np.linspace(-extent,extent);ax.plot(xx,-xx,color='#536475',ls='--',lw=1.3);ax.set_xlim(-20,20);ax.set_ylim(-25,40);ax.set_xlabel('Natural change: births minus deaths (per 1,000)');ax.set_ylabel('Net migration (per 1,000)');ax.grid(alpha=.15);ax.legend(loc='lower left',frameon=False,fontsize=9);ax.text(.98,.96,'Above dashed line:\ncomponents sum to growth',transform=ax.transAxes,ha='right',va='top',fontsize=9)
loss=pop[pop[nat]<0];off=loss[loss[nat]+loss[mig]>0]
f.text(.755,.75,f'{len(loss):,}',fontsize=30,fontweight='bold');f.text(.755,.68,'counties had more\ndeaths than births',fontsize=12);f.text(.755,.56,f'{len(off):,} / {len(loss):,}',fontsize=24,fontweight='bold',color=BLUE);f.text(.755,.48,f'of those counties ({len(off)/len(loss):.0%})\nhad migration large enough\nto offset natural decrease',fontsize=11);outside=((x < -20)|(x > 20)|(z < -25)|(z > 40)).sum()
axin=f.add_axes([.76,.225,.18,.18]);axin.scatter(x,z,s=3,color=GRAY,alpha=.5);axin.axhline(0,color='#94a3b8',lw=.5);axin.axvline(0,color='#94a3b8',lw=.5);axin.set_xlim(-extent,extent);axin.set_ylim(-extent,extent);axin.set_xticks([-extent,0,extent]);axin.set_yticks([-extent,0,extent]);axin.tick_params(labelsize=7);from matplotlib.patches import Rectangle
axin.add_patch(Rectangle((-20,-25),40,65,fill=False,edgecolor=ORANGE,lw=1));axin.set_title(f'Full range • {outside} outside main view',fontsize=8)
footer(f,'Natural change + net migration is a component-based growth balance; reported population change can also include residual adjustments.\nDashed line: zero sum. Main view zooms in; inset shows every valid county (orange box = main view). Counts use all valid counties.\nSource: supplied USDA / Census county CSV. Association is descriptive; dots do not represent individual migration decisions.')
save(f,'06_migration_balance.png')
summary={'matched_education_count':len(edu),'education_medians':med.round(3).to_dict(),'education_counts':counts.to_dict(),'sex_gap_endpoints':gaps.round(3).to_dict(),'south_africa_lows':{s:{'year':int(d.loc[1990:,s].idxmin()),'value':float(d.loc[1990:,s].min())} for s in ['Female','Male']},'migration_valid':len(pop),'natural_loss_count':len(loss),'offset_count':len(off),'plot_extent':extent}
import json
(ROOT/'work/summary.json').write_text(json.dumps(summary,indent=2))
assert len(list(OUT.glob('*.png')))==6
print(json.dumps(summary,indent=2))
