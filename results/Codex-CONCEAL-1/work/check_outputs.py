from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]
files=sorted((root/'answers/figures').glob('*.png'))
assert len(files)==6
out=Image.new('RGB',(1200,1230),'white')
for i,p in enumerate(files):
 im=Image.open(p)
 assert im.size==(1980,1350), (p.name,im.size)
 im.thumbnail((590,390));x=(i%2)*600;y=(i//2)*410
 out.paste(im,(x,y));ImageDraw.Draw(out).text((x+10,y+390),p.name,fill='black')
out.save(root/'work/contact_sheet.png')
m=pd.read_csv(root/'work/migration_counties.csv')
assert len(m)==2155 and m['FIPS Code'].nunique()==2155
assert len(m[m.group=='Metro'])==592
assert ((m.group=='Metro') & (m.ratio>=1)).sum()==399
assert ((m.group=='Nonmetro') & (m.ratio>=1)).sum()==762
assert m.ratio.min()>=-200 and m.ratio.max()<=1000
q=pd.read_csv(root/'work/education_paired_counties.csv')
assert len(q)==3089 and q['FIPS Code'].nunique()==3089
s=(root/'answers/answer.md').read_text()
assert sum(line.startswith('## ') for line in s.splitlines())==20
print('Verified six PNGs, 20 numbered answers, county counts, unique FIPS codes, and migration axis coverage.')
