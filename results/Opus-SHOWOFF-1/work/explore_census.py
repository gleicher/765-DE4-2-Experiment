import pandas as pd, numpy as np
c=pd.read_csv('data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1')
print(c.shape); c['fips']=c['FIPS Code'].str.zfill(5)
cty=c[~c.fips.str.endswith('000')].copy()
print(len(cty), cty['2023 Rural-urban Continuum Code'].value_counts(dropna=False).sort_index())
r=cty['2023 Rural-urban Continuum Code']
cty['grp']=np.select([r<=1,r<=3,r<=7,r>=8],['Large metro','Small metro','Nonmetro','Most rural'],'NA')
def rate(g,y): return 100*g[f'Unemployed {y}'].sum()/g[f'Civilian labor force {y}'].sum()
for gname,g in cty.groupby(r):
    print(gname, len(g), [round(rate(g,y),1) for y in range(2000,2024)])
# shocks
cty['rec']=cty['Unemployment rate 2010']-cty['Unemployment rate 2007']
cty['cov']=cty['Unemployment rate 2020']-cty['Unemployment rate 2019']
print(cty.groupby(r)[['rec','cov']].median())
print(cty[['rec','cov']].corr())
# natural change vs migration
for y in [2021,2022,2023]:
    print(y, cty.groupby(r)[[f'Natural Change Rate {y}',f'Net Migration Rate {y}',f'Domestic Migration Rate {y}',f'International Migration Rate {y}']].median().round(1))
print('nat<0 & mig>0 2023', ((cty['Natural Change Rate 2023']<0)&(cty['Net Migration Rate 2023']>0)).sum())
print('nat<0 share by year', [(cty[f'Natural Change Rate {y}']<0).mean().round(2) for y in [2021,2022,2023]])
