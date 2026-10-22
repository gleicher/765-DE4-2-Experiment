import sys; sys.path.insert(0,'work')
from common import *
c=load_census(); r='Rural Urban Continuum Code 2023'; c=c.dropna(subset=[r])
grp={1:'A',2:'B',3:'B',4:'C',6:'C',8:'C',5:'D',7:'D',9:'D'}; c['g']=c[r].map(grp)
pd.set_option('display.width',200)
t=pd.DataFrame({y:c.groupby('g').apply(lambda s:s['Unemployed %d'%y].sum()/s['Civilian labor force %d'%y].sum()*100) for y in range(2005,2024)}).T
print(t.round(2)); 
print(c[['Unemployed 2000','Civilian labor force 2000','Unemployed 2020']].isna().sum())
