import json,sys,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
P=Path('.');sys.path.insert(0,'deps');from pyproj import Transformer
T=Transformer.from_crs(4326,25833,always_xy=True);ss=[]
for k,lon,lat in [('fuglevik-jeloy',10.64169,59.46681)]:
 x,y=T.transform(lon,lat);ss.append(dict(id=k,bbox=[x-600,y-600,x+600,y+600],width=1500,height=1500))
def f(n):
 u='https://ws.geonorge.no/stedsnavn/v1/navn?'+urllib.parse.urlencode(dict(sok=n,treffPerSide=100));d=json.load(urllib.request.urlopen(u,timeout=15));(P/'raw'/f'name-{n}.json').write_text(json.dumps(d));return n,[(x['skrivemåte'],x['representasjonspunkt']) for x in d.get('navn',[]) if any(z['kommunenummer']=='3103' for z in x.get('kommuner',[]))]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for n,pts in ex.map(f,['Rødstranda','Tollstranda','Billmannsbakken']):
  print(n,pts)
  if pts:
   q=pts[0][1];x,y=T.transform(q['øst'],q['nord']);ss.append(dict(id='place-'+n,bbox=[x-500,y-500,x+500,y+500],width=1500,height=1500))
(P/'extras4.json').write_text(json.dumps(ss))
