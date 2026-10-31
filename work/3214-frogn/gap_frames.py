import json
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
rows=json.loads((P/'cluster-review-index.json').read_text());m=json.loads((P/'images/coast-251100-6623100.json').read_text());a,b,c,d=m['bbox']
# Reproducible manual gap frame: original 1500px image, island north and south guest piers.
for cid,px in [('G003',(500,650,750,900)),('G004',(660,940,960,1240))]:
 x0,y0,x1,y1=px;fr=[a+x0/1500*(c-a),d-y1/1500*(d-b),a+x1/1500*(c-a),d-y0/1500*(d-b)]
 rows=[r for r in rows if r['cid']!=cid]+[dict(cid=cid,image_id=m['id'],review_bbox=fr,review_width=500,review_height=500)]
 Image.open(P/'images'/f"{m['id']}.jpg").crop(px).resize((500,500)).save(P/'qa'/f'{cid}-clean.jpg',quality=94)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
