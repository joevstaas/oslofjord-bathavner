import json
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import shape,box
from shapely.ops import transform
from pyproj import Transformer
P=Path(__file__).parent
B=transform(Transformer.from_crs(4326,25833,always_xy=True).transform,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
for family in ['coast','inland']:
 fs=sorted((P/'images').glob(f'{family}-*.jpg'))
 for n in range(0,len(fs),6):
  canvas=Image.new('RGB',(1500,1040),'white')
  for i,f in enumerate(fs[n:n+6]):
   im=Image.open(f);im.load();im=im.resize((500,500));d=ImageDraw.Draw(im);a,b,c,e=json.loads(f.with_suffix('.json').read_text())['bbox']
   bound=B.boundary.intersection(box(a,b,c,e))
   for line in getattr(bound,'geoms',[bound]):
    if line.geom_type=='LineString':d.line([((x-a)/(c-a)*500,(e-y)/(e-b)*500) for x,y in line.coords],fill='yellow',width=2)
   x=i%3*500;y=i//3*520;canvas.paste(im,(x,y+20));ImageDraw.Draw(canvas).text((x+4,y+3),f.stem,fill='black')
  canvas.save(P/'qa'/f'{family}-sheet-{n//6}.jpg',quality=92)
print('done')
