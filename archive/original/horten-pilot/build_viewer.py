"""Build an offline review map: original cartography + separate vector overlays."""
import sys,json,pathlib,base64,io
ROOT=pathlib.Path(__file__).parent
sys.path.insert(0,str(ROOT/'deps'))
from PIL import Image
from pyproj import Transformer,CRS
from shapely.geometry import shape,mapping
from shapely.ops import transform
features=json.loads((ROOT/'bathavner-alle-forslag.geojson').read_text())
boundary=json.loads((ROOT/'kommunegrense.geojson').read_text())
grid=json.loads((ROOT/'dekningsruter.geojson').read_text())
followup=json.loads((ROOT/'oppfolgingspunkter.geojson').read_text())
to_utm=Transformer.from_crs(4326,25833,always_xy=True)
to_merc=Transformer.from_crs(4326,3857,always_xy=True)
def project(f):
    o=dict(f)
    if f['geometry']:
        o['utm']=mapping(transform(to_utm.transform,shape(f['geometry'])))
        o['merc']=mapping(transform(to_merc.transform,shape(f['geometry'])))
    return o
keys=['kommuneoversikt']+list(dict.fromkeys(f['properties']['source_image'].split('/')[-1][:-4] for f in features['features']))+['lovoya','indre-havn','indre-vest']
images={}
for key in keys:
    m=json.loads((ROOT/'images'/f'{key}.json').read_text())
    # A compact display copy; original unmodified PNG and request metadata stay in the bundle.
    im=Image.open(ROOT/'images'/f'{key}.png').convert('RGB');im.thumbnail((1800,1800))
    buf=io.BytesIO();im.save(buf,format='JPEG',quality=86)
    m['data']='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
    images[key]=m
# Complete world files and projection sidecars for opening the source PNGs in GIS.
for p in (ROOT/'images').glob('*.json'):
    m=json.loads(p.read_text());b=m['bbox'];dx=(b[2]-b[0])/m['width'];dy=(b[3]-b[1])/m['height']
    p.with_suffix('.pgw').write_text('\n'.join(map(str,[dx,0,0,-dy,b[0]+dx/2,b[3]-dy/2]))+'\n')
    p.with_suffix('.prj').write_text(CRS.from_user_input(m['crs']).to_wkt(version='WKT1_GDAL'))
payload=dict(features=[project(f) for f in features['features']],boundary=project(boundary['features'][0]),grid=[project(f) for f in grid['features']],followup=[project(f) for f in followup['features']],images=images,download=features,report=(ROOT/'rapport.txt').read_text())
template=(ROOT/'viewer-template.html').read_text()
(ROOT/'horten-kart.html').write_text(template.replace('/*PAYLOAD*/',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))
print('Viewer bytes:',(ROOT/'horten-kart.html').stat().st_size)
