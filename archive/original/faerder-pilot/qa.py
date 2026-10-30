import sys,json,math
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
F=Transformer.from_crs(4326,25833,always_xy=True)
fs=json.loads((P/'faerder-bathavner.geojson').read_text())['features']
can=None
for i,f in enumerate(fs):
 p=f['properties']; key=p['image_id'];m=json.loads((P/'images'/f'{key}.json').read_text());im=Image.open(P/'images'/f'{key}.jpg').convert('RGB').resize((1000,1000));d=ImageDraw.Draw(im);x0,y0,x1,y1=m['bbox'];pts=[]
 for lon,lat in f['geometry']['coordinates'][0]:
  x,y=F.transform(lon,lat);pts.append(((x-x0)/(x1-x0)*1000,(y1-y)/(y1-y0)*1000))
 d.line(pts,fill='red',width=3);xs,ys=zip(*pts);box=(max(0,int(min(xs))-30),max(0,int(min(ys))-30),min(1000,int(max(xs))+30),min(1000,int(max(ys))+30));tile=im.crop(box);tile.thumbnail((390,300));panel=Image.new('RGB',(400,340),'white');panel.paste(tile,((400-tile.width)//2,30));ImageDraw.Draw(panel).text((4,5),p['id']+' '+p['name'][:43],fill='black')
 if i%9==0:can=Image.new('RGB',(1200,1020),'white')
 can.paste(panel,((i%3)*400,((i%9)//3)*340))
 if i%9==8 or i==len(fs)-1:can.save(P/'images'/f'qa-{i//9}.jpg')
print('4 QA sheets generated from exported GeoJSON')
