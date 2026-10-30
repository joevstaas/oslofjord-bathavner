import sys,json,re,urllib.request,concurrent.futures,xml.etree.ElementTree as E
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from shapely.geometry import shape,mapping
from shapely.ops import transform
from pyproj import Transformer
x=json.loads((P/'raw/kommunegrense-response.json').read_text());g=shape(x['omrade']);wgs=transform(Transformer.from_crs(4258,4326,always_xy=True).transform,g);(P/'kommunegrense.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','properties':{'name':'Larvik','municipality_code':'3909','source':'Kartverket kommuneinfo','source_crs':'EPSG:4258'},'geometry':mapping(wgs)}]}));print('bounds',wgs.bounds,flush=True)
links=sorted(set(re.findall(r'href="([^"]*osm-(?:node|way|relation)-\d+[^\"]*)"',(P/'raw/sjosett.html').read_text())));(P/'raw/candidate-links.json').write_text(json.dumps(links,indent=2))
def f(l):
 t,n=re.search('osm-(node|way|relation)-(\\d+)',l).groups();u=f'https://api.openstreetmap.org/api/0.6/{t}/{n}'+('/full' if t!='node' else '')
 try:
  b=urllib.request.urlopen(u,timeout=25).read();(P/'raw'/f'osm-{t}-{n}.osm').write_bytes(b);r=E.fromstring(b);e=r.find(t+f"[@id='{n}']");tags={z.get('k'):z.get('v') for z in e.findall('tag')};ns=r.findall('node');lon=sum(float(z.get('lon')) for z in ns)/len(ns);lat=sum(float(z.get('lat')) for z in ns)/len(ns);return dict(osm_id=f'{t}/{n}',name=tags.get('name',''),lon=lon,lat=lat,tags=tags,url='https://www.sjosett.com'+l)
 except Exception as e:return dict(error=str(e),link=l)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:out=list(ex.map(f,[l for l in links if '/gjestehavner/' in l]))
(P/'osm-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('OSM marina candidates',len(out),flush=True)
for i,q in enumerate(out):print(i,q.get('osm_id'),q.get('name'),q.get('lon'),q.get('lat'),flush=True)
