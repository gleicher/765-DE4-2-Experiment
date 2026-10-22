from common import *
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_rows',200)
d=census()
b90="Percent of adults with a bachelor's degree or higher, 1990"
d=d[d[b90].notna()&(d[b90]>0)]
d['q']=pd.qcut(d[b90],4,labels=['Q1 lowest','Q2','Q3','Q4 highest'])
rows=[]
for y in range(2000,2024):
    for q,s in d.groupby('q',observed=True):
        s=s.dropna(subset=[f'Unemployed {y}',f'Civilian labor force {y}'])
        rows.append((y,q,s[f'Unemployed {y}'].sum()/s[f'Civilian labor force {y}'].sum()*100,s[f'Unemployment rate {y}'].median()))
r=pd.DataFrame(rows,columns=['y','q','pooled','med'])
print(r.pivot(index='y',columns='q',values='pooled').round(2))
print(d.groupby('q',observed=True)['Census Population 2020'].agg(['sum','median','count']))
print(d.groupby('q',observed=True)['2023 Rural-urban Continuum Code'].mean())
w=wb(); c=w[~w.is_agg]
pp=c.pivot(index='Country Name',columns='Year',values='Both')
x=pd.DataFrame({'l19':pp[2019],'l21':pp[2021],'l23':pp[2023]})
x['drop']=x.l21-x.l19; x['rec']=x.l23-x.l21; x['net']=x.l23-x.l19
print(x.sort_values('drop').head(25).round(1))
print(x.sort_values('net').head(20).round(1))
print((x.net>=0).mean(), x.net.describe())
