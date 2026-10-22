import pandas as pd, numpy as np
w=pd.read_csv('data/lifespan_dataset_1960.csv',index_col=0)
w.columns=['name','code','sex','year','le']
p=w.pivot_table(index=['name','code','year'],columns='sex',values='le').reset_index()
p['gap']=p.Female-p.Male
print(p[p.year==2023].sort_values('gap').tail(15)[['name','Male','Female','gap']])
print(p[p.year==2023].sort_values('gap').head(10)[['name','Male','Female','gap']])
wld=p[p.name=='World'];print(wld[['year','Both','gap']].iloc[::5])
for c in ['Russian Federation','Japan','United States','Korea, Rep.','China','India','Bangladesh','Ukraine','Belarus','Nigeria','Sweden','United Kingdom','Brazil','Pakistan','Nepal']:
    s=p[p.name==c].set_index('year'); print(c, s.loc[[1960,1980,2000,2019,2023],'gap'].round(1).tolist(), 'max', s.gap.idxmax(), round(s.gap.max(),1))
print('----')
agg=set(['World'])
cc=p[p.code.str.len()==3]
# WB aggregates identification: codes list
names=p.name.unique()
print([n for n in names if any(k in n for k in ['income','IDA','IBRD','Asia','Africa','Europe','America','World','dividend','states','Euro','OECD','members','Arab','Fragile','Heavily','Least','Small','Middle','Caribbean','Pacific','Sub-Saharan'])])
p['lebin']=(p.Both//5)*5
print(p.groupby('lebin').gap.describe()[['count','25%','50%','75%']])
# peak year distribution for countries
