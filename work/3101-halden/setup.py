"""Start Halden review and save official boundary and imagery metadata."""
import datetime,hashlib,json,pathlib,time,urllib.request
from shapely.geometry import shape,mapping
from shapely.ops import transform
from pyproj import Transformer
P=pathlib.Path(__file__).parent;ROOT=P.parents[1]
for name in ['raw','images','qa']:(P/name).mkdir(parents=True,exist_ok=True)
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'oslofjord-bathavner/1.0 (public research)'}),timeout=40) as r:return r.read()
def save(name,d): (P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if not (P/'run.json').exists():save('run.json',dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),started_unix=time.time(),municipality='Halden',code='3101',revision=1,method_version='1.2',schema_version='1.1',approved_baseline_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/samlet').glob('*') if p.is_file()}))
urls={'kommunegrense-4326.json':'https://api.kartverket.no/kommuneinfo/v1/kommuner/3101/omrade?utkoordsys=4326','esri-service.json':'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer?f=pjson'}
for name,url in urls.items():
 raw=get(url);(P/'raw'/name).write_bytes(raw);save('raw/'+name+'.provenance.json',dict(url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest()));print(name,len(raw),flush=True)
j=json.loads((P/'raw/kommunegrense-4326.json').read_text());g=shape(j['omrade']);save('kommunegrense.geojson',dict(type='FeatureCollection',features=[dict(type='Feature',properties=dict(code='3101',name='Halden',source=urls['kommunegrense-4326.json']),geometry=mapping(g))]))
F=Transformer.from_crs(4326,25833,always_xy=True).transform
print('Boundary WGS84',g.bounds,'EPSG25833',transform(F,g).bounds,flush=True)
