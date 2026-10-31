"""Uavhengige bildesøk-kandidater uten OSM-pirer. Pikselrammer fra originalbildene."""
import json
from pathlib import Path
from PIL import Image
P=Path(__file__).parent;rows=json.loads((P/'cluster-review-index.json').read_text())
for cid,img,px in [('G001','coast-254700-6614100',(30,35,210,215)),('G002','coast-254700-6607800',(300,600,750,1200))]:
 m=json.loads((P/'images'/(img+'.json')).read_text());a,b,c,d=m['bbox'];x0,y0,x1,y1=px;W,H=m['width'],m['height'];fr=[a+x0/W*(c-a),d-y1/H*(d-b),a+x1/W*(c-a),d-y0/H*(d-b)]
 rows=[r for r in rows if r['cid']!=cid]+[dict(cid=cid,image_id=img,review_bbox=fr,review_width=500,review_height=500)]
 Image.open(P/'images'/(img+'.jpg')).crop(px).resize((500,500)).save(P/'qa'/(cid+'-clean.jpg'),quality=94)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
# Extra north-basin review frame: imagery extends beyond the OSM cluster envelope.
m=json.loads((P/'images/coast-255600-6606000.json').read_text());a,b,c,d=m['bbox'];fr=[255900,6606350,256300,6606850];W,H=m['width'],m['height']
rows=[r for r in rows if r['cid']!='V001']+[dict(cid='V001',image_id=m['id'],review_bbox=fr,review_width=500,review_height=500)]
Image.open(P/'images'/(m['id']+'.jpg')).crop(((fr[0]-a)/(c-a)*W,(d-fr[3])/(d-b)*H,(fr[2]-a)/(c-a)*W,(d-fr[1])/(d-b)*H)).resize((500,500)).save(P/'qa/V001-clean.jpg',quality=94)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
fr=[255780,6606200,256080,6606500]
rows=[r for r in rows if r['cid']!='V002']+[dict(cid='V002',image_id=m['id'],review_bbox=fr,review_width=500,review_height=500)]
Image.open(P/'images'/(m['id']+'.jpg')).crop(((fr[0]-a)/(c-a)*W,(d-fr[3])/(d-b)*H,(fr[2]-a)/(c-a)*W,(d-fr[1])/(d-b)*H)).resize((500,500)).save(P/'qa/V002-clean.jpg',quality=94)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1))
