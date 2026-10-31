"""Hent georefererte bilder. Bruk: fetch_images.py <specs.json> topo|esri"""
import json, sys, time, hashlib, datetime, concurrent.futures, urllib.parse
from pathlib import Path
import requests
from PIL import Image

P = Path(__file__).parent
specs = json.loads((P / sys.argv[1]).read_text())
provider = sys.argv[2]
ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export'
TOPO = 'https://wms.geonorge.no/skwms1/wms.topo'
TODAY = datetime.date.today().isoformat()


def get(url, **kw):
    for n in range(3):
        try:
            r = requests.get(url, timeout=60, **kw)
            r.raise_for_status()
            return r
        except Exception:
            if n == 2:
                raise
            time.sleep(2 * (n + 1))


def fetch(s):
    t0 = time.monotonic()
    key = s['id']
    f = P / 'images' / f"{key}.{'png' if provider == 'topo' else 'jpg'}"
    meta = f.with_suffix('.json')
    if f.exists() and meta.exists():
        return key, 'cached'
    bb = ','.join(map(str, s['bbox']))
    if provider == 'topo':
        q = dict(service='WMS', version='1.3.0', request='GetMap', layers='topo', crs='EPSG:25833',
                 bbox=bb, width=s['width'], height=s['height'], format='image/png')
        u = TOPO + '?' + urllib.parse.urlencode(q)
        r = get(u)
        if not r.headers.get('content-type', '').startswith('image'):
            raise ValueError('ikke bilde: ' + r.text[:200])
        d = r.content
        m = dict(s, url=u, requested_bbox=s['bbox'], actual_bbox=s['bbox'], crs='EPSG:25833',
                 source='Kartverket Topografisk norgeskart (WMS topo)', attribution='© Kartverket')
    else:
        q = dict(f='pjson', bbox=bb, bboxSR=25833, imageSR=25833, size=f"{s['width']},{s['height']}", format='jpg')
        u = ESRI + '?' + urllib.parse.urlencode(q)
        res = get(u).json()
        (P / 'raw' / f'{key}-export.json').write_text(json.dumps(res, indent=1))
        if 'error' in res:
            raise ValueError(res['error'])
        img_url = res.get('href') or ESRI + '?' + urllib.parse.urlencode(dict(q, f='image'))
        d = get(img_url).content
        e = res['extent']
        actual = [e['xmin'], e['ymin'], e['xmax'], e['ymax']]
        m = dict(s, url=u, image_url=img_url, requested_bbox=s['bbox'], bbox=actual, actual_bbox=actual,
                 width=res.get('width') or s['width'], height=res.get('height') or s['height'], crs='EPSG:25833',
                 source='Esri World Imagery',
                 attribution='Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community')
    f.write_bytes(d)
    with Image.open(f) as im:
        assert im.size == (m['width'], m['height']), (key, im.size)
    m.update(retrieved_date=TODAY, retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
             source_observation_date=None, sha256=hashlib.sha256(d).hexdigest(),
             elapsed_seconds=round(time.monotonic() - t0, 2), bytes=len(d))
    meta.write_text(json.dumps(m, ensure_ascii=False, indent=1))
    return key, len(d)


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    fs = {ex.submit(fetch, s): s['id'] for s in specs}
    for fu in concurrent.futures.as_completed(fs):
        try:
            print(fu.result(), flush=True)
        except Exception as e:
            print(fs[fu], 'ERROR', repr(e)[:300], flush=True)
