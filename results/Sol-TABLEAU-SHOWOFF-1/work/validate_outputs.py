"""Check source identities, plotted subsets, figure existence, and stated counts."""
from pathlib import Path
import pandas as pd
from PIL import Image
root=Path(__file__).resolve().parents[1]
l=pd.read_csv(root/'data/lifespan_dataset_1960.csv')
assert not l.duplicated(['Country Code','Sex','Year']).any()
c=pd.read_csv(root/'work/county_patterns.csv',dtype={'FIPS Code':str})
assert c['FIPS Code'].is_unique and len(c)==3106
assert c['County group'].value_counts().to_dict()=={'Nonmetro':1949,'Metro':1157}
x=c['Natural Change Rate 2023'];y=c['Net Migration Rate 2023']
clipped=c[~x.between(-20,20)|~y.between(-40,80)]
assert clipped['County group'].value_counts().to_dict()=={'Nonmetro':11,'Metro':1}
st=pd.read_csv(root/'work/state_unemployment.csv',index_col=0)
assert st.shape==(50,17) and not st.isna().any().any()
assert st.to_numpy().max()<=15
images=list((root/'answers/figures').glob('*.png'))
assert len(images)==6
for p in sorted(images):
 im=Image.open(p);im.verify();print(p.name)
text=(root/'answers/answer.md').read_text()
for q in range(1,21):assert f'## {q}. ' in text
print('Checks passed: unique keys, denominators, clipped counts, matrix completeness, PNG integrity, and all 20 answers.')
