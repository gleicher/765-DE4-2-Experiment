from pathlib import Path
import re
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv');c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',low_memory=False)
c=c[(c['FIPS Code']%1000!=0)&c.State.ne('PR')].copy()
assert c['FIPS Code'].is_unique
assert not c.State.eq('PR').any()
print(f'County identifiers unique; {len(c):,} U.S. county records before complete-case filtering.')
selected=pd.read_csv(ROOT/'work/life_selected.csv')
assert not selected.duplicated(['Country Code','Year','Sex']).any()
assert len(selected)==6*34*3 and selected['Life Expectancy (years)'].notna().all()
metrics=pd.read_csv(ROOT/'work/life_endpoint_metrics.csv');assert (metrics.gain>0).all()
print('Six life-expectancy series: complete 34 years × 3 sex series; endpoint total gains all positive.')
k='2023 Rural-urban Continuum Code';cols=['Natural Change 2023','Domestic migration 2023','International Migration 2023'];v=c.dropna(subset=cols+[k,'Population Estimate 2022','Population Estimate 2023']);rates=pd.read_csv(ROOT/'work/growth_rates.csv',index_col=0)
assert len(v)==3106 and int(rates.n.sum())==3106
for code,d in v.groupby(k):
 den=(d['Population Estimate 2022'].sum()+d['Population Estimate 2023'].sum())/2
 for col in cols:assert np.isclose(rates.loc[code,col],d[col].sum()/den*1000)
 assert np.isclose(rates.loc[code,'Total'],rates.loc[code,cols].sum())
print('All nine growth groups independently recomputed; 3,106 complete cases; component totals match.')
s=pd.read_csv(ROOT/'work/education_shares.csv');assert np.allclose(s.iloc[:,3:].sum(axis=1),100)
assert s[s.period.eq('1990')]['count'].sum()==3087
for group,d in s.groupby('group'):assert d['count'].nunique()==1
p=s.pivot(index='group',columns='period',values='Bachelor+')
a=p.loc['Metro · codes 1–3','1990']-p.loc['Nonmetro · codes 8–9','1990'];b=p.loc['Metro · codes 1–3','2019-23']-p.loc['Nonmetro · codes 8–9','2019-23'];assert round(a,1)==11.9 and round(b,1)==18.0
print('Education shares sum to 100%; 3,087-county balanced panel; headline gap verified: 11.9 → 18.0 percentage points.')
r=pd.read_csv(ROOT/'work/recovery_metrics.csv');mapping={'Rwanda':'RWA','Russia':'RUS','Botswana':'BWA','Eswatini':'SWZ','South Africa':'ZAF'}
for row in r.itertuples():
 d=l[l['Country Code'].eq(mapping[row.name])&l.Sex.eq('Both')].set_index('Year')['Life Expectancy (years)'].loc[1990:2023]
 assert len(d)==34 and d.notna().all()
 assert row.trough==d.idxmin();assert np.isclose(row.trough_deficit,d.min()-d.loc[1990])
 crossings=[y for y in range(row.trough+1,2024) if d.loc[y]>=d.loc[1990]]
 assert row.recovery==min(crossings) and row.years_after_trough==row.recovery-row.trough
print('Recovery troughs, deficits, first subsequent threshold crossings, and durations independently verified.')
ps=sorted((ROOT/'answers/figures').glob('*.png'));assert len(ps)==6
sheet=Image.new('RGB',(1800,1800),'white')
for i,png in enumerate(ps):
 with Image.open(png) as im:
  assert im.size==(2850,1805);im.verify()
 with Image.open(png) as im:
  im.thumbnail((900,570));sheet.paste(im,((i%2)*900,(i//2)*600))
 ImageDraw.Draw(sheet).text(((i%2)*900+10,(i//2)*600+575),png.name,fill='black')
 assert png.with_suffix('.svg').exists()
sheet.save(ROOT/'work/contact_sheet.png')
answer=(ROOT/'answers/answer.md').read_text();assert re.findall(r'^## (\d+)\.',answer,re.M)==list(map(str,range(1,21)))
for png in ps:assert png.name in answer
print('Six valid 2850 × 1805 PNGs, six matching SVGs, and all 20 Canvas responses with correct upload references.')
print('PASS. Figure script also checks every visible text extent against the page boundary.')
