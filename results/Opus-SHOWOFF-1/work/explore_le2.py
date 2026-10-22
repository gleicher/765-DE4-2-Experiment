import pandas as pd, numpy as np
w=pd.read_csv('data/lifespan_dataset_1960.csv',index_col=0); w.columns=['name','code','sex','year','le']
p=w.pivot_table(index=['name','year'],columns='sex',values='le').reset_index(); p['gap']=p.Female-p.Male
C=['China','India','United States','Indonesia','Pakistan','Nigeria','Brazil','Bangladesh','Russian Federation','Mexico','Japan','Ethiopia','Philippines','Egypt, Arab Rep.','Viet Nam','Congo, Dem. Rep.','Turkiye','Iran, Islamic Rep.','Germany','Thailand','United Kingdom','France','Italy','South Africa','Tanzania','Kenya','Korea, Rep.','Colombia','Spain','Argentina','Ukraine','Poland','Canada','Morocco','Saudi Arabia','Peru','Australia','Sweden','Nepal','Sri Lanka','Kazakhstan','Chile','Netherlands','Afghanistan','Ghana','Algeria','Iraq','Malaysia']
for c in C:
    s=p[p.name==c].set_index('year').gap
    if len(s)==0: print('MISSING',c); continue
    sm=s.rolling(5,center=True,min_periods=3).mean()
    print(f"{c:22s} 1960={s.loc[1960]:5.1f} peak={sm.idxmax()} ({sm.max():4.1f}) 2023={s.iloc[-1]:5.1f} min={s.min():5.1f} n={s.notna().sum()}")
