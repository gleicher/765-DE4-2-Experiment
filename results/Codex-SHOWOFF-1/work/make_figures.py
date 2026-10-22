from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/.mplconfig')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm
OUT=ROOT/'answers/figures'; OUT.mkdir(parents=True,exist_ok=True)
BG='#faf8f2'; INK='#182d3a'; MUTED='#586975'; TEAL='#007f80'; ORANGE='#c75b27'; BLUE='#426bb5'; GREY='#c9cdd0'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,'axes.edgecolor':'#b6bdc0','figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG,'axes.spines.top':False,'axes.spines.right':False})
def page(k,title,sub,caption):
 f=plt.figure(figsize=(15,9.5));f.text(.055,.953,f'DESIGN EXERCISE 4–2    /    {k}',fontsize=10,color=TEAL,weight='bold',va='top');f.text(.055,.90,title,fontfamily='DejaVu Serif',fontsize=27,weight='bold',va='top');f.text(.055,.825,sub,fontsize=13,color=MUTED,va='top');f.text(.055,.065,caption,fontsize=10.5,color=MUTED,va='top',linespacing=1.5);return f
def save(f,name):
 f.canvas.draw()
 from matplotlib.text import Text
 renderer=f.canvas.get_renderer()
 overflow=[]
 for item in f.findobj(Text):
  if not item.get_visible() or not item.get_text(): continue
  bb=item.get_window_extent(renderer)
  if bb.x0<0 or bb.y0<0 or bb.x1>f.bbox.width or bb.y1>f.bbox.height: overflow.append(item.get_text())
 if overflow: raise ValueError(f'{name}: clipped text {overflow}')
 f.savefig(OUT/(name+'.png'),dpi=190);f.savefig(OUT/(name+'.svg'));plt.close(f)
def style(ax,axis='y'):
 ax.grid(axis=axis,color='#dce0df',lw=.7);ax.set_axisbelow(True);ax.tick_params(length=0,pad=7)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv');value='Life Expectancy (years)'
codes=['IND','CHN','JPN','USA','ZAF','RUS'];names=['India','China','Japan','United States','South Africa','Russia']
l=l.drop(columns=['Unnamed: 0']); selected=l[l['Country Code'].isin(codes)&l.Year.between(1990,2023)]
selected.to_csv(ROOT/'work/life_selected.csv',index=False)
f=page('01A / LIFE EXPECTANCY','Longer lives, different gaps','Six selected countries, 1990–2023 · Female and male period life expectancy at birth (years)',
 'The shaded distance is the female–male gap. All six countries gained total life expectancy, but India and China widened their gaps.\nSource: supplied World Bank data, lifespan_dataset_1960.csv. Countries are illustrative cases, not a representative sample; values are estimates.')
axes=f.subplots(2,3,gridspec_kw={'left':.07,'right':.96,'top':.74,'bottom':.17,'wspace':.25,'hspace':.40})
for ax,code,name in zip(axes.flat,codes,names):
 d=selected[selected['Country Code'].eq(code)].pivot(index='Year',columns='Sex',values=value); ax.fill_between(d.index,d.Male,d.Female,color=TEAL,alpha=.10)
 ax.plot(d.index,d.Female,color=TEAL,lw=2.5);ax.plot(d.index,d.Male,color=ORANGE,lw=2.5)
 ax.set(xlim=(1990,2026),ylim=(45,91),xticks=[1990,2000,2010,2023],yticks=[50,60,70,80,90]);style(ax);ax.set_title(name,loc='left',fontsize=14,weight='bold',pad=9)
 for sex,col in [('Female',TEAL),('Male',ORANGE)]:
  ax.scatter(2023,d.loc[2023,sex],s=18,color=col);ax.text(2024,d.loc[2023,sex],f'{d.loc[2023,sex]:.1f}',color=col,fontsize=10,va='center')
 a=d.loc[1990,'Female']-d.loc[1990,'Male'];b=d.loc[2023,'Female']-d.loc[2023,'Male'];ax.text(.03,.06,f'Gap: {a:.1f} → {b:.1f} years',transform=ax.transAxes,fontsize=10,color=MUTED)
f.legend([Line2D([0],[0],color=TEAL,lw=3),Line2D([0],[0],color=ORANGE,lw=3)],['Female','Male'],frameon=False,loc='upper right',bbox_to_anchor=(.96,.79),ncol=2)
save(f,'01a_life_trajectories')
metrics=[]
for code,name in zip(codes,names):
 d=selected[selected['Country Code'].eq(code)].pivot(index='Year',columns='Sex',values=value);metrics.append({'name':name,'gap1990':d.loc[1990,'Female']-d.loc[1990,'Male'],'gap2023':d.loc[2023,'Female']-d.loc[2023,'Male'],'gain':d.loc[2023,'Both']-d.loc[1990,'Both']})
m=pd.DataFrame(metrics);m.to_csv(ROOT/'work/life_endpoint_metrics.csv',index=False)
f=page('01B / LIFE EXPECTANCY','Improvement does not imply convergence','Six selected countries · Endpoint comparison, 1990 to 2023',
 'Left: female life expectancy minus male life expectancy. Right: change in total (both-sex) life expectancy.\nSource: supplied World Bank data. Rows are ordered by 1990 gap. Endpoints suppress intervening reversals; these are descriptive comparisons.')
m=m.sort_values('gap1990');ax=f.add_axes([.16,.20,.47,.51]);bx=f.add_axes([.72,.20,.21,.51]);y=np.arange(6)
for i,r in enumerate(m.itertuples()):
 ax.plot([r.gap1990,r.gap2023],[i,i],lw=3,color=GREY);ax.scatter(r.gap1990,i,s=80,facecolor=BG,edgecolor=INK,zorder=3);ax.scatter(r.gap2023,i,s=80,color=TEAL,zorder=3);ax.text(max(r.gap1990,r.gap2023)+.28,i,f'{r.gap2023-r.gap1990:+.1f}',fontsize=11,va='center',color=TEAL)
 bx.barh(i,r.gain,color=BLUE,height=.38);bx.text(r.gain+.25,i,f'+{r.gain:.1f}',va='center',fontsize=11)
ax.set(yticks=y,yticklabels=m.name,xlim=(0,12.8),ylim=(-.6,5.6),xlabel='Female advantage (years)');bx.set(yticks=y,yticklabels=[],xlim=(0,16),ylim=(-.6,5.6),xlabel='Total gain (years)');ax.invert_yaxis();bx.invert_yaxis();style(ax,'x');style(bx,'x');ax.set_title('Gap between sexes',loc='left',weight='bold',pad=22);bx.set_title('Longer lives',loc='left',weight='bold',pad=22)
f.legend([Line2D([0],[0],marker='o',ls='',markerfacecolor=BG,markeredgecolor=INK,markersize=8),Line2D([0],[0],marker='o',ls='',color=TEAL,markersize=8)],['1990','2023; signed label = gap change'],frameon=False,ncol=2,bbox_to_anchor=(.67,.79));save(f,'01b_life_endpoints')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',low_memory=False)
c=c[(c['FIPS Code']%1000!=0)&c.State.ne('PR')].copy();k='2023 Rural-urban Continuum Code';cols=['Natural Change 2023','Domestic migration 2023','International Migration 2023'];needed=cols+['Population Estimate 2022','Population Estimate 2023',k]
v=c.dropna(subset=needed);g=v.groupby(k)[needed[:-1]].sum();den=(g['Population Estimate 2022']+g['Population Estimate 2023'])/2;rates=g[cols].div(den,axis=0)*1000;rates['Total']=rates.sum(axis=1);rates['n']=v.groupby(k).size();rates.to_csv(ROOT/'work/growth_rates.csv');labels=[('Metro' if i<=3 else 'Nonmetro')+f' · code {i}' for i in range(1,10)]
print(rates.round(3).to_string())
f=page('02A / COUNTY DEMOGRAPHY','Migration changes the growth equation','2023 · Components per 1,000 residents, by 2023 rural–urban continuum class',
 f'Natural change = births − deaths; migration is net inflow. Diamond = sum of the three components (excludes the estimation residual).\nSource: supplied USDA county data. {len(v):,} complete county records; U.S. states + DC, excluding Puerto Rico. Rates = summed counts / mean 2022–2023 population × 1,000.')
ax=f.add_axes([.21,.19,.72,.52]);colors=[ORANGE,TEAL,BLUE];offsets=[-.19,0,.19]
for j,col in enumerate(cols):
 vals=rates[col].to_numpy();yy=np.arange(9)+offsets[j];ax.hlines(yy,0,vals,color=colors[j],lw=2);ax.scatter(vals,yy,s=50,color=colors[j],zorder=3)
ax.scatter(rates.Total,np.arange(9)+.34,marker='D',facecolor=BG,edgecolor=INK,s=42,zorder=4)
ax.axvline(0,color=INK,lw=1);ax.axhline(2.5,color=GREY,lw=1);ax.set(yticks=np.arange(9),yticklabels=[f'{a}   (n={int(n)})' for a,n in zip(labels,rates.n)],xlim=(-5.4,8.4),xticks=[-4,-2,0,2,4,6,8],ylim=(-.6,8.7),xlabel='Net change per 1,000 residents   ← outflow / decline       inflow / growth →');ax.invert_yaxis();style(ax,'x')
f.legend([Line2D([0],[0],marker='o',color=col,lw=2) for col in colors]+[Line2D([0],[0],marker='D',ls='',markerfacecolor=BG,markeredgecolor=INK)],['Natural change','Domestic migration','International migration','Three-component total'],frameon=False,ncol=4,bbox_to_anchor=(.94,.79));save(f,'02a_growth_components')
f=page('02B / COUNTY DEMOGRAPHY','Inflow can offset a natural decline','2023 · Each arrow adds international migration to the domestic-only balance',
 'Hollow circle: domestic migration. Filled endpoint: domestic + international migration. Above the diagonal, the component sum is positive.\nSource: supplied USDA data; 3,106 complete county records; denominator = mean 2022–2023 population. Codes 1–3 are metro; 4–9 nonmetro. Residual excluded.')
ax=f.add_axes([.10,.19,.62,.55]);ax.set(xlim=(-5.2,4.1),ylim=(-3.7,8.8),xticks=[-4,-2,0,2,4],yticks=[-2,0,2,4,6,8],xlabel='Natural change per 1,000 residents',ylabel='Net migration per 1,000 residents');style(ax);ax.axvline(0,color=GREY,lw=1);ax.axhline(0,color=GREY,lw=1)
xx=np.linspace(-5.2,4.1,100);ax.fill_between(xx,-xx,8.8,color=TEAL,alpha=.045);ax.plot(xx,-xx,color=INK,lw=1,ls='--');ax.text(-4.8,5.2,'Zero component-sum growth',rotation=-40,color=MUTED,fontsize=10)
for i,r in rates.iterrows():
 x=r[cols[0]];a=r[cols[1]];b=a+r[cols[2]];color=BLUE if i<=3 else TEAL;ax.scatter(x,a,facecolor=BG,edgecolor=color,s=58,zorder=3);ax.annotate('',xy=(x,b),xytext=(x,a),arrowprops={'arrowstyle':'-|>','color':color,'lw':2});ax.scatter(x,b,color=color,s=58,zorder=4);ax.annotate(str(int(i)),(x,b),xytext=(8,2),textcoords='offset points',fontsize=12,weight='bold',color=color)
f.text(.77,.73,'READ THE BALANCE',fontsize=11,weight='bold',color=TEAL,va='top');f.text(.77,.63,'Code 1 · largest metros\nDomestic: −2.8\nInternational: +4.6\nCombined migration: +1.8',fontsize=13,linespacing=1.7,va='top');f.text(.77,.41,'Code 9 · nonmetro\nNatural change: −4.1\nCombined migration: +3.0\nComponent total: −1.1',fontsize=13,linespacing=1.7,va='top');f.text(.77,.21,'Blue = metro (1–3)\nTeal = nonmetro (4–9)\nRates per 1,000 residents',fontsize=11,color=MUTED,linespacing=1.6,va='top');save(f,'02b_growth_balance')
# Use a balanced county panel so changes cannot be driven by missing county rows.
edcats=['Less than high school graduate','High school graduate (or equivalency)','Some college or associate degree',"Bachelor's degree or higher"]
edcols=[f'{a}, {t}' for a in edcats for t in ['1990','2019-23']];e=c.dropna(subset=edcols+[k]).copy();e['group']=pd.cut(e[k],[0,3,7,9],labels=['Metro · codes 1–3','Nonmetro · codes 4–7','Nonmetro · codes 8–9'])
shares=[]
for group,d in e.groupby('group',observed=True):
 for t in ['1990','2019-23']:
  vals=d[[f'{a}, {t}' for a in edcats]].sum().to_numpy();shares.append([str(group),t,len(d),*(100*vals/vals.sum())])
s=pd.DataFrame(shares,columns=['group','period','count','Below high school','High school only','Some college / associate','Bachelor+']);s.to_csv(ROOT/'work/education_shares.csv',index=False);print(s.to_string(index=False))
f=page('03 / EDUCATION','More degrees, a wider metro advantage','Educational attainment composition · Same county panel in 1990 and 2019–23',
 f'Each bar sums to 100% of the adults represented by the four attainment counts; these are shares of people, not averages of county percentages.\nSource: supplied USDA data; {len(e):,} counties with complete attainment counts in both periods and a 2023 class. Fixed 2023 classification; ACS 2019–23 is a five-year estimate.')
ax=f.add_axes([.23,.21,.70,.49]);ecol=['#d6cfc2','#a4adb0','#75b5b2',TEAL];ys=[0,.6,1.65,2.25,3.3,3.9]
for idx,r in enumerate(s.itertuples(index=False,name=None)):
 left=0
 for j,a in enumerate(r[3:]):
  ax.barh(ys[idx],a,left=left,height=.43,color=ecol[j],edgecolor=BG,lw=1.5)
  if a>8:ax.text(left+a/2,ys[idx],f'{a:.1f}%',ha='center',va='center',fontsize=11,color='white' if j==3 else INK)
  left+=a
 ax.text(-2,ys[idx],r[1],ha='right',va='center',fontsize=11)
for j,group in enumerate(s.group.unique()):ax.text(-2,ys[j*2]-.40,group,ha='right',fontsize=12,weight='bold')
ax.set(xlim=(0,100),ylim=(-.7,4.4),yticks=[],xlabel='Share of adults (%)',xticks=[0,25,50,75,100]);ax.invert_yaxis();style(ax,'x');ax.spines['left'].set_visible(False)
f.legend([Line2D([0],[0],color=a,lw=10) for a in ecol],s.columns[3:],frameon=False,ncol=4,bbox_to_anchor=(.93,.79));f.text(.23,.12,'Bachelor’s share gap, metro vs. codes 8–9: 11.9 → 18.0 percentage points',fontsize=13,color=TEAL,weight='bold');save(f,'03_education_composition')
shockcodes=['RWA','RUS','BWA','SWZ','ZAF'];shocknames=['Rwanda','Russia','Botswana','Eswatini','South Africa'];years=np.arange(1990,2024);arr=[];recrows=[]
for code,name in zip(shockcodes,shocknames):
 d=l[l['Country Code'].eq(code)&l.Sex.eq('Both')].set_index('Year')[value].loc[1990:2023];base=d.loc[1990];trough=d.idxmin();rr=d.loc[trough:];rec=rr[rr>=base].index.min();arr.append((d-base).to_numpy());recrows.append({'name':name,'baseline':base,'trough':trough,'trough_deficit':d.min()-base,'recovery':int(rec),'years_after_trough':int(rec-trough)})
rr=pd.DataFrame(recrows);rr.to_csv(ROOT/'work/recovery_metrics.csv',index=False);print(rr.to_string(index=False))
f=page('04 / RECOVERY','A deeper fall is not always a longer wait','Life expectancy relative to each country’s 1990 level · Selected decline-and-recovery cases, 1990–2023',
 'Color shows total (both-sex) life expectancy minus its 1990 level. Ring = trough; square = first later year at or above the 1990 level.\nSource: supplied World Bank data. Recovery is a threshold crossing, not a return to an expected trend; later declines remain visible. Selection is illustrative, not global.')
ax=f.add_axes([.15,.27,.61,.41]);im=ax.imshow(arr,cmap='RdBu',norm=TwoSlopeNorm(vmin=-36,vcenter=0,vmax=36),aspect='auto',interpolation='nearest',extent=(1989.5,2023.5,4.5,-.5));ax.set(yticks=np.arange(5),yticklabels=shocknames,xticks=[1990,1995,2000,2005,2010,2015,2020,2023]);ax.tick_params(length=0);ax.spines[['top','right','left','bottom']].set_visible(False)
for i,r in rr.iterrows():
 ax.scatter(r.trough,i,s=120,facecolor='none',edgecolor=INK,lw=1.6);ax.scatter(r.recovery,i,s=68,marker='s',facecolor=BG,edgecolor=INK,lw=1.3)
 f.text(.80,.68-i*.082,f'{r.years_after_trough} years',fontsize=17,weight='bold',va='center');f.text(.80,.653-i*.082,f'{r.trough} → {r.recovery}   |   low: {r.trough_deficit:.1f} y',fontsize=10.5,color=MUTED,va='center')
f.text(.80,.745,'TROUGH → RECOVERY',fontsize=10.5,weight='bold',color=TEAL);cb=f.add_axes([.15,.17,.61,.025]);bar=f.colorbar(im,cax=cb,orientation='horizontal',ticks=[-36,-24,-12,0,12,24,36]);bar.set_label('Years below / above the 1990 baseline',fontsize=11);bar.outline.set_visible(False);save(f,'04_recovery_calendar')
