from common import *
d=census()
print(len(d))
b90="Percent of adults with a bachelor's degree or higher, 1990"; b23="Percent of adults with a bachelor's degree or higher, 2019-23"; b00="Percent of adults with a bachelor's degree or higher, 2000"
d['rucc']=d['2023 Rural-urban Continuum Code']
print(d.groupby('rucc')[[b90,b00,b23,'Census Population 2020']].agg({b90:'median',b00:'median',b23:'median','Census Population 2020':['median','count']}))
print(d[[b90,b23]].corr())
d['gain']=d[b23]-d[b90]
print(d.groupby('rucc').gain.describe())
print(d.sort_values('gain').tail(8)[['State','Area name',b90,b23,'rucc']])
print(d.sort_values('gain').head(5)[['State','Area name',b90,b23,'rucc']])
# unemployment trajectories by education tercile (2019-23 bach)
u=[f'Unemployment rate {y}' for y in range(2000,2024)]
d['q']=pd.qcut(d[b90],4,labels=False)
print(d.groupby('q')[u].median().T.round(1).iloc[::2])
d['qp']=pd.qcut(d['Census Population 2020'],4,labels=False)
print(d.groupby('qp')[u].median().T.round(1).iloc[::3])
