import sys; sys.path.insert(0,'work')
from common import *
c=load_census();B=lambda y:"Percent of adults with a bachelor's degree or higher, %s"%y
d=c.dropna(subset=[B('1990'),B('2019-23')]);d=d.assign(g=d[B('2019-23')]-d[B('1990')],x=d[B('1990')])
for lo,hi in [(0,10),(10,15),(15,20),(20,30),(30,80)]:
    s=d[(d.x>=lo)&(d.x<hi)].g; print(lo,hi,len(s),s.quantile([.1,.5,.9]).round(1).tolist())
print((d.g<0).sum())
