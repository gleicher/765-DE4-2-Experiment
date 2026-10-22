import pandas as pd, numpy as np
c=pd.read_csv('data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1').copy()
c['fips']=c['FIPS Code'].str.zfill(5); cty=c[~c.fips.str.endswith('000')].copy()
r=cty['2023 Rural-urban Continuum Code']
Y=[2021,2022,2023]
for k,col in [('nat','Natural Change'),('dom','Domestic migration'),('intl','International Migration'),('net','Net Migration'),('chg','Population Change')]:
    cty[k]=sum(cty[f'{col} {y}'] for y in Y)
cty['base']=cty['Population Estimate 2020']
g=cty.groupby(r)[['nat','dom','intl','net','chg','base']].sum()
print((g[['nat','dom','intl','net','chg']].div(g.base,axis=0)*1000/3).round(2))
print(g.base)
cty['natr']=cty.nat/cty.base*1000/3; cty['netr']=cty.net/cty.base*1000/3
q=pd.crosstab(r,[cty.natr<0,cty.netr>0],normalize='index').round(2); print(q)
print(pd.crosstab(cty.natr<0,cty.netr>0))
print(cty[['natr','netr']].describe())
print('PR?',cty[cty.State=='PR'].shape, cty[r.isna()][['State','Area name']])
# check rate columns vs computed
cty['nr23']=cty['Natural Change Rate 2023']; print(cty[['nr23']].describe())
