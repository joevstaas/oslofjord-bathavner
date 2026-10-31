"""Full detaljgjennomgang: 500 m-celler langs hele OSM-kystlinjen, satt sammen fra kystflisene i opprinnelig oppløsning (ca. 0,73 m/px).
Eksisterende polygoner (rød), kommunegrense (gul), 100 m-rutenett. Lager qa/sweep-NN.jpg (2 x 2 celler) og sweep-index.json."""
import json,warnings
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import shape,LineString,box
from shapely.ops import transform,unary_union
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];S=500;PX=685
T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
coast=unary_union([transform(T,LineString([(v['lon'],v['lat']) for v in e['geometry']])).intersection(B.buffer(20)) for e in json.loads((P/'raw/overpass-bamble.json').read_text())['elements'] if e.get('tags',{}).get('natural')=='coastline'])
polys=[(f['properties']['id'],transform(T,shape(f['geometry']))) for f in json.loads((R/'data/kommuner/4012-bamble/rev-01/bathavner.geojson').read_text())['features']]
tiles=[(f,json.loads(f.with_suffix('.json').read_text())) for f in sorted((P/'images').glob('coast-*.jpg'))]
x0,y0,x1,y1=coast.bounds;cells=[]
for y in range(int(y1//S)*S,int(y0//S)*S-S,-S):
 for x in range(int(x0//S)*S,int(x1)+S,S):
  if not coast.intersection(box(x,y,x+S,y+S)).is_empty:cells.append((x,y))
idx=[];panels=[]
for k,(x,y) in enumerate(cells):
 cid=f'G{k+1:03}';fr=(x,y,x+S,y+S);can=Image.new('RGB',(PX,PX),'black');used=[]
 for f,m in tiles:
  a,b,c,d=m['bbox'];ov=box(a,b,c,d).intersection(box(*fr))
  if ov.is_empty or ov.area<1:continue
  ox0,oy0,ox1,oy1=ov.bounds;W,H=m['width'],m['height'];im=Image.open(f)
  crop=im.crop(((ox0-a)/(c-a)*W,(d-oy1)/(d-b)*H,(ox1-a)/(c-a)*W,(d-oy0)/(d-b)*H))
  tw,th=round((ox1-ox0)/S*PX),round((oy1-oy0)/S*PX)
  if tw<1 or th<1:continue
  can.paste(crop.resize((tw,th)),(round((ox0-x)/S*PX),round((y+S-oy1)/S*PX)));used.append(f.stem)
 dr=ImageDraw.Draw(can);px=lambda X,Y:((X-x)/S*PX,(y+S-Y)/S*PX)
 for g in range(100,S,100):dr.line([px(x+g,y),px(x+g,y+S)],fill=(255,255,255));dr.line([px(x,y+g),px(x+S,y+g)],fill=(255,255,255))
 bl=B.boundary.intersection(box(*fr))
 for ln in getattr(bl,'geoms',[bl]):
  if ln.geom_type=='LineString':dr.line([px(*q) for q in ln.coords],fill='yellow',width=2)
 for pid,g in polys:
  if g.intersects(box(*fr)):dr.line([px(*q) for q in g.exterior.coords],fill='red',width=2)
 pn=Image.new('RGB',(PX,PX+20),'white');pn.paste(can,(0,20));ImageDraw.Draw(pn).text((4,4),f'{cid}  x={x} y={y}  (500 m, rutenett 100 m)',fill='black');panels.append(pn)
 idx.append(dict(cell=cid,bbox=list(fr),tiles=used,sheet=k//4))
for n in range(0,len(panels),4):
 sh=Image.new('RGB',(2*PX,2*(PX+20)),'white')
 for i,p in enumerate(panels[n:n+4]):sh.paste(p,(i%2*PX,i//2*(PX+20)))
 sh.save(P/'qa'/f'sweep-{n//4:02}.jpg',quality=88)
(P/'sweep-index.json').write_text(json.dumps(idx,indent=1));print(len(cells),'celler',(len(panels)+3)//4,'ark')
