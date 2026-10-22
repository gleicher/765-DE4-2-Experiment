from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work'/'mplcache')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#243544','text.color':'#243544','axes.edgecolor':'#bcc6cd','figure.facecolor':'#fcfcfa','axes.facecolor':'#fcfcfa','savefig.facecolor':'#fcfcfa'})
OUT=ROOT/'answers'/'figures'; OUT.mkdir(parents=True,exist_ok=True)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
c['FIPS Code']=c['FIPS Code'].str.zfill(5)
c=c[c['2023 Rural-urban Continuum Code'].between(1,9)&c['State'].ne('PR')].copy()
blue='#007e96';orange='#d76b38';purple='#765ba0'
def page(title,sub,caption,size=(12,8)):
 f,ax=plt.subplots(figsize=size); f.subplots_adjust(left=.14,right=.90,top=.79,bottom=.21)
 f.text(.065,.94,title,fontsize=22,weight='bold',va='top');f.text(.065,.875,sub,fontsize=12,va='top')
 f.text(.065,.045,caption,fontsize=10,va='bottom',linespacing=1.5)
 return f,ax
def save(f,name):
 f.savefig(OUT/name,dpi=180);plt.close(f)
sel=['USA','JPN','CHL'];p=l[l['Country Code'].isin(sel)].pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)');gap=(p.Female-p.Male).unstack();colors={'Japan':purple,'Chile':orange,'United States':blue}
f,a=page('The female advantage narrowed in Chile and the U.S.', 'Japan’s gap stayed near six years • Female minus male life expectancy at birth, 1990–2023', 'Source: supplied World Bank life expectancy data. Three selected countries; no population weighting.\nThe gap describes period life expectancy, not a causal effect of sex or a forecast for a birth cohort.')
for country in gap.index:
 s=gap.loc[country,1990:2023];a.plot(s.index,s.values,lw=3,color=colors[country]);a.text(2023.6,s.iloc[-1],f'{country}\n{s.iloc[-1]:.1f} years',fontsize=11,color=colors[country],va='center')
a.set(xlim=(1989,2029),ylim=(0,8),xlabel='Year',ylabel='Female − male life expectancy (years)',xticks=[1990,2000,2010,2020]);a.grid(axis='y',alpha=.2);save(f,'01_life_gap_trends.png')
f,a=page('Two gaps narrowed; Japan’s barely moved', 'The same three countries, comparing endpoints • Female minus male life expectancy', 'Source: supplied World Bank data. Points represent 1990 and 2023; connectors show endpoint differences.\nThe endpoint view omits intervening fluctuations. Life expectancy at birth; units are years.')
for i,country in enumerate(['United States','Chile','Japan']):
 x0,x1=gap.loc[country,[1990,2023]];a.plot([x0,x1],[i,i],color='#aeb7bc',lw=4);a.scatter(x0,i,color='#71808a',s=110,label='1990' if i==0 else None);a.scatter(x1,i,color=blue,s=110,label='2023' if i==0 else None);a.text(max(x0,x1)+.2,i,f'{x1-x0:+.2f} years',va='center');a.text(x0,i-.16,f'{x0:.2f}',ha='center',fontsize=10);a.text(x1,i+.16,f'{x1:.2f}',ha='center',fontsize=10)
a.set(yticks=range(3),yticklabels=['United States','Chile','Japan'],xlim=(0,8.6),ylim=(-.6,2.6),xlabel='Female − male life expectancy (years)');a.legend(loc='upper left');a.grid(axis='x',alpha=.2);save(f,'02_life_gap_endpoints.png')
b0="Percent of adults with a bachelor's degree or higher, 2000";b1="Percent of adults with a bachelor's degree or higher, 2019-23"
for col in [b0,b1,'Natural Change Rate 2023','Net Migration Rate 2023']:
 c[col]=pd.to_numeric(c[col],errors='coerce')
e=c.dropna(subset=[b0,b1]).copy();e['gain']=e[b1]-e[b0];e['group']=pd.cut(e['2023 Rural-urban Continuum Code'],[0,3,7,9],labels=['Metro (1–3)','Nonmetro (4–7)','Nonmetro (8–9)'])
groups=['Metro (1–3)','Nonmetro (4–7)','Nonmetro (8–9)'];med=e.groupby('group',observed=True)[[b0,b1,'gain']].median();counts=e.groupby('group',observed=True).size()
cap='Source: supplied USDA/course county dataset. Counties equally weighted; U.S. states and DC, excluding Puerto Rico.\n2023 rural–urban codes held fixed; 2019–23 is a five-year estimate. Shares refer to adults age 25+.'
f,a=page('Degree attainment rose across county types', 'Larger typical shares in metro counties • Median county bachelor’s-or-higher share',cap)
for i,g in enumerate(groups):
 x0,x1=med.loc[g,[b0,b1]];a.plot([x0,x1],[i,i],color='#b5bec4',lw=5);a.scatter(x0,i,c=orange,s=120,label='2000' if i==0 else None);a.scatter(x1,i,c=blue,s=120,label='2019–23' if i==0 else None);a.text(x0-.6,i,f'{x0:.1f}%',ha='right',va='center');a.text(x1+.6,i,f'{x1:.1f}%',va='center')
a.set(yticks=range(3),yticklabels=[f'{g}\nn={counts[g]:,} counties' for g in groups],xlim=(0,40),ylim=(2.7,-.7),xlabel='Median county share with a bachelor’s degree or higher (%)');a.legend(loc='upper right');a.grid(axis='x',alpha=.2);save(f,'03_education_levels.png')
f,a=page('Metro counties usually gained more degree share', 'Within-county change, 2000 → 2019–23 • The same county sample as the endpoint view',cap+'\nBoxes show middle 50%; line is median; whiskers extend to 1.5×IQR. Dots show remaining counties.')
vals=[e.loc[e.group==g,'gain'].values for g in groups];bp=a.boxplot(vals,orientation="horizontal",patch_artist=True,positions=[0,1,2],widths=.5,medianprops={'color':'#243544','linewidth':2},flierprops={'marker':'.','markersize':4,'alpha':.3})
for box,col in zip(bp['boxes'],[blue,orange,purple]):box.set_facecolor(col);box.set_alpha(.55)
for i,g in enumerate(groups):a.text(med.loc[g,'gain'],i-.36,f'Median +{med.loc[g,"gain"]:.1f} pp',ha='center',fontsize=11)
a.axvline(0,color='#69767d',ls='--');a.set(yticks=range(3),yticklabels=[f'{g}\nn={counts[g]:,}' for g in groups],ylim=(2.7,-.8),xlabel='Change in bachelor’s-or-higher share (percentage points)');a.grid(axis='x',alpha=.2);save(f,'04_education_change_distribution.png')
co=['Japan','Sweden','United States','Chile','Mexico','South Africa'];q=l[(l.Sex=='Both')&l['Country Name'].isin(co)].pivot(index='Country Name',columns='Year',values='Life Expectancy (years)').loc[co];d=q.loc[:,2020:2023].subtract(q[2019],axis=0)
f,a=page('By 2023, recovery relative to 2019 was uneven', 'Life expectancy at birth, both sexes • Six selected countries, change from each country’s 2019 level', 'Source: supplied World Bank data. Values are differences from the same country’s 2019 estimate, in years.\nSelected examples, not a global sample. This descriptive comparison does not identify causes of the changes.')
im=a.imshow(d.values,cmap='RdBu',vmin=-5,vmax=5,aspect='auto');a.set(xticks=range(4),xticklabels=d.columns,yticks=range(6),yticklabels=co,xlabel='Year');
for i in range(6):
 for j in range(4):a.text(j,i,f'{d.iloc[i,j]:+.1f}',ha='center',va='center',color='white' if abs(d.iloc[i,j])>2.7 else '#243544',fontsize=14)
f.colorbar(im,ax=a,pad=.03,label='Change from 2019 (years)');save(f,'05_life_recovery_heatmap.png')
m=c.dropna(subset=['Natural Change Rate 2023','Net Migration Rate 2023']).copy();decl=m['Natural Change Rate 2023']<0;offset=decl&(m['Natural Change Rate 2023']+m['Net Migration Rate 2023']>0);num=int(offset.sum());den=int(decl.sum())
f,a=page('Migration often outweighed natural population loss', f'{num:,} of {den:,} counties with more deaths than births had a positive combined rate in 2023', 'Source: supplied USDA/course data; rates per 1,000 residents. Counties equally weighted; Puerto Rico excluded.\nDiagonal: migration exactly offsets natural change. Combined rate excludes residual adjustments; not total growth.\nFull sample retained; extreme observations can compress the central cloud. Association is descriptive.')
for yes,col,label in [(False,'#a6afb6','Other counties'),(True,blue,'Natural loss offset by migration')]:
 s=m.loc[offset==yes];a.scatter(s['Natural Change Rate 2023'],s['Net Migration Rate 2023'],s=18,c=col,alpha=.45,edgecolors='none',label=f'{label} (n={len(s):,})')
xmin=min(-22,m['Natural Change Rate 2023'].min()-2);xmax=max(15,m['Natural Change Rate 2023'].max()+2);a.set_xlim(xmin,xmax);a.set_ylim(m['Net Migration Rate 2023'].min()-3,m['Net Migration Rate 2023'].max()+3);xx=np.array([xmin,xmax]);a.plot(xx,-xx,ls='--',lw=1.5,c=orange,label='Natural change + migration = 0');a.axvline(0,c='#74838b',lw=1);a.axhline(0,c='#74838b',lw=1);a.set(xlabel='Natural change rate: births − deaths (per 1,000)',ylabel='Net migration rate (per 1,000)');a.legend(loc='upper right',fontsize=10,framealpha=.95);save(f,'06_migration_offset_scatter.png')
e[['FIPS Code','State','Area name','group',b0,b1,'gain']].to_csv(ROOT/'work/education_processed.csv',index=False);d.to_csv(ROOT/'work/life_recovery_processed.csv');gap.loc[:,1990:2023].to_csv(ROOT/'work/life_gap_processed.csv');m[['FIPS Code','State','Area name','Natural Change Rate 2023','Net Migration Rate 2023']].assign(offset=offset).to_csv(ROOT/'work/migration_processed.csv',index=False)
summary={'education_n':len(e),'education_medians':med.to_dict(),'groups_n':counts.to_dict(),'migration_n':len(m),'natural_decline_n':den,'offset_n':num,'recovery':d.to_dict(),'gap_endpoints':gap.loc[:,[1990,2023]].to_dict()}
import json
(ROOT/'work/summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
