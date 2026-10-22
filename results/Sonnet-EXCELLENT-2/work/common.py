import pandas as pd, numpy as np, re
ROOT='/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-EXCELLENT-2'
AGG_PAT=re.compile(r'(?:income|IDA|IBRD|dividend|small states|Arab World|Africa Eastern|Africa Western|Euro area|European Union|Europe & Central|East Asia|Latin America|Middle East|North America|OECD|South Asia|Sub-Saharan|World|Fragile|Heavily|Least developed|Central Europe|Caribbean small|Other small|Pacific island|Small states|Low & middle|High income|Middle income|Low income|Lower middle|Upper middle)')
def wb():
    w=pd.read_csv(f'{ROOT}/data/lifespan_dataset_1960.csv',index_col=0)
    p=w.pivot_table(index=['Country Name','Country Code','Year'],columns='Sex',values='Life Expectancy (years)').reset_index()
    p['gap']=p.Female-p.Male
    p['is_agg']=p['Country Name'].str.contains(AGG_PAT)
    return p
def census():
    d=pd.read_csv(f'{ROOT}/data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1')
    d=d[~d['FIPS Code'].str.endswith('000')].copy()
    return d
