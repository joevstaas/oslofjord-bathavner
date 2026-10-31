"""Supplerende utsnitt av hele fysiske anlegg, også når OSM-klyngen bare treffer en molo."""
import json
from pathlib import Path
from shapely.geometry import box
from PIL import Image
P=Path(__file__).parent;C={c['cid']:c for c in json.loads((P/'clusters.json').read_text())};rows=json.loads((P/'cluster-review-index.json').read_text());imgs=[json.loads(f.read_text()) for f in sorted((P/'images').glob('*.json'))]
for vid,cids,extra in [('V001',['C080','C163'],[40,40,40,40]),('V002',['C226','C227','C228'],[20,40,170,20]),('V003',['C164'],[90,40,25,25])]:
 bb=[C[c]['bounds'] for c in cids];a=min(b[0] for b in bb)-extra[0];b=min(b[1] for b in bb)-extra[1];c=max(b[2] for b in bb)+extra[2];d=max(b[3] for b in bb)+extra[3];fr=[a,b,c,d];ms=[m for m in imgs if box(*m['bbox']).covers(box(*fr))]
 if not ms:print('missing',vid);continue
 m=ms[0];A,B,E,F=m['bbox'];W,H=m['width'],m['height'];im=Image.open(P/'images'/(m['id']+'.jpg'));im.crop(((a-A)/(E-A)*W,(F-d)/(F-B)*H,(c-A)/(E-A)*W,(F-b)/(F-B)*H)).resize((500,500)).save(P/'qa'/(vid+'-clean.jpg'),quality=94)
 rows=[r for r in rows if r['cid']!=vid]+[dict(cid=vid,image_id=m['id'],review_bbox=fr,review_width=500,review_height=500)];print(vid,cids)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
