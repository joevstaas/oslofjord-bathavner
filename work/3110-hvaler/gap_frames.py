import json
from pathlib import Path
from PIL import Image
from shapely.geometry import box
P=Path(__file__).parent;rows=json.loads((P/'cluster-review-index.json').read_text());F={r['cid']:r for r in rows};imgs=[json.loads(f.read_text()) for f in sorted((P/'images').glob('*.json'))]
for vid,cid,side in [('V004','C033',550),('V005','C114',350),('V006','C118',400),('V007','C012',700)]:
 a,b,c,d=F[cid]['review_bbox'];x=(a+c)/2;y=(b+d)/2;fr=[x-side/2,y-side/2,x+side/2,y+side/2];ms=[m for m in imgs if box(*m['bbox']).covers(box(*fr))]
 if not ms: print('missing',vid);continue
 m=ms[0];A,B,C,E=m['bbox'];W,H=m['width'],m['height'];im=Image.open(P/'images'/(m['id']+'.jpg'));im.crop(((fr[0]-A)/(C-A)*W,(E-fr[3])/(E-B)*H,(fr[2]-A)/(C-A)*W,(E-fr[1])/(E-B)*H)).resize((500,500)).save(P/'qa'/(vid+'-clean.jpg'))
 rows=[r for r in rows if r['cid']!=vid]+[dict(cid=vid,image_id=m['id'],review_bbox=fr,review_width=500,review_height=500)]
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
