"""Reproducible Kartverket WMS downloads; bounding boxes are EPSG:25833."""
import sys, json, pathlib, urllib.request, urllib.parse, concurrent.futures, time
sys.path.insert(0, str(pathlib.Path(__file__).parent/'deps'))
from pyproj import Transformer
from PIL import Image
ROOT=pathlib.Path(__file__).parent
TO_UTM=Transformer.from_crs(4326,25833,always_xy=True)
def centered(key, lon, lat, ground_width, ground_height=None, resolution=0.5):
    x,y=TO_UTM.transform(lon,lat); h=ground_height or ground_width
    return dict(id=key,bbox=[x-ground_width/2,y-h/2,x+ground_width/2,y+h/2],width=round(ground_width/resolution),height=round(h/resolution))
def fetch(spec):
    p=ROOT/'images'/f"{spec['id']}.png"
    params=dict(service='WMS',version='1.3.0',request='GetMap',layers='topo',styles='',crs='EPSG:25833',bbox=','.join(map(str,spec['bbox'])),width=spec['width'],height=spec['height'],format='image/png',transparent='false')
    url='https://wms.geonorge.no/skwms1/wms.topo?'+urllib.parse.urlencode(params)
    meta=dict(spec,crs='EPSG:25833',url=url,source='© Kartverket, Topografisk norgeskart',retrieved='2026-10-28',source_observation_date=None)
    if not p.exists():
        data=urllib.request.urlopen(url,timeout=60).read()
        if not data.startswith(b'\x89PNG'): raise ValueError(data[:500])
        p.write_bytes(data)
    with Image.open(p) as im:
        if im.size!=(spec['width'],spec['height']): raise ValueError('Wrong dimensions')
    p.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    # Pixel centers: world file follows A,D,B,E,C,F convention.
    b=spec['bbox']; dx=(b[2]-b[0])/spec['width']; dy=(b[3]-b[1])/spec['height']
    p.with_suffix('.pgw').write_text('\n'.join(map(str,[dx,0,0,-dy,b[0]+dx/2,b[3]-dy/2]))+'\n')
    return spec['id'],p.stat().st_size
if __name__=='__main__':
    specs=json.loads((ROOT/sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        tasks={ex.submit(fetch,s):s['id'] for s in specs}
        for f in concurrent.futures.as_completed(tasks):
            try: print(f.result(),flush=True)
            except Exception as e: print(tasks[f],repr(e),flush=True)
