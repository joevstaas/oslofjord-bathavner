import sys,json
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
import numpy as np,rasterio.features
from rasterio.transform import from_bounds
from PIL import Image
from shapely.geometry import shape,box
from shapely.ops import transform
from pyproj import Transformer
m=json.loads((P/'images/oversikt.json').read_text());im=np.asarray(Image.open(P/'images/oversikt.png').convert('RGB')).astype(int);h,w=im.shape[:2];bbox=m['bbox'];g=shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']);T=Transformer.from_crs(4326,25833,always_xy=True).transform;g=transform(T,g)
mask=rasterio.features.rasterize([(g,1)],out_shape=(h,w),transform=from_bounds(*bbox,w,h),fill=0).astype(bool)
r,gr,b=im[:,:,0],im[:,:,1],im[:,:,2];land=(b<220)&(r>115)&(gr>130)&(gr>r-35)&mask
specs=[]
for i,x in enumerate(range(232000,252001,3600)):
 for j,y in enumerate(range(6540000,6580001,3600)):
  b=[x,y,x+4000,y+4000]
  if not g.intersects(box(*b)):continue
  l=max(0,int((x-bbox[0])/(bbox[2]-bbox[0])*w));rr=min(w,int((x+4000-bbox[0])/(bbox[2]-bbox[0])*w)+1);top=max(0,int((bbox[3]-y-4000)/(bbox[3]-bbox[1])*h));bot=min(h,int((bbox[3]-y)/(bbox[3]-bbox[1])*h)+1)
  n=int(land[top:bot,l:rr].sum())
  if n>0:specs.append(dict(id=f'scan-{i}-{j}',bbox=b,width=2000,height=2000,land_pixels_overview=n))
(P/'scan-maps.json').write_text(json.dumps(specs,indent=2));print(len(specs),'tiles')
