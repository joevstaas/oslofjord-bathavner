import json,runpy,sys
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;D=runpy.run_path(str(P/'decisions.py'))['D'];batch=sys.argv[1]
rows=[r for r in json.loads((P/'cluster-review-index.json').read_text()) if r['cid'].startswith('C') and r['cid'] not in D];C={c['cid']:c for c in json.loads((P/'clusters.json').read_text())}
for k in range(0,len(rows),6):
 can=Image.new('RGB',(1500,1050),'white')
 for i,r in enumerate(rows[k:k+6]):
  cid=r['cid'];im=Image.open(P/'qa'/(cid+'-clean.jpg'));c=C[cid];a,b,d,e=r['review_bbox'];px=lambda x,y:((x-a)/(d-a)*500,(e-y)/(e-b)*500);dr=ImageDraw.Draw(im)
  for p in c['piers']:dr.line([px(*z) for z in p['geometry']['coordinates']],fill='red',width=1)
  x=i%3*500;y=i//3*525;can.paste(im,(x,y+25));ImageDraw.Draw(can).text((x+3,y+3),cid+' '+','.join(m['tags'].get('name','?') for m in c['marks'])[:60],fill='black')
 can.save(P/'qa'/f'pending-{batch}-{k//6}.jpg',quality=93)
(P/'qa'/f'pending-{batch}.json').write_text(json.dumps([r['cid'] for r in rows]));print(len(rows),'new',[(r['cid']) for r in rows])
