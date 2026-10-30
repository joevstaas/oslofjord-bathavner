"""Hent OSM-havneobjekter i delruter (store spørringer gir 504). Lagrer raw/overpass-<i>.json og samlet raw/overpass-lier.json."""
import json, time, requests
from pathlib import Path
P = Path(__file__).parent
URLS = ['https://maps.mail.ru/osm/tools/overpass/api/interpreter', 'https://overpass.private.coffee/api/interpreter', 'https://overpass-api.de/api/interpreter']
_c = json.loads((P / 'raw/kommunegrense-4326.json').read_text())['omrade']['coordinates']
_xs = [q[0] for poly in _c for ring in poly for q in ring]; _ys = [q[1] for poly in _c for ring in poly for q in ring]
lat0, lon0, lat1, lon1 = min(_ys) - 0.005, min(_xs) - 0.01, max(_ys) + 0.005, max(_xs) + 0.01
n = 3
els = {}
for i in range(n):
    for j in range(n):
        f = P / 'raw' / f'overpass-{i}{j}.json'
        if f.exists():
            d = json.loads(f.read_text())
        else:
            a, b = lat0 + (lat1 - lat0) * i / n, lon0 + (lon1 - lon0) * j / n
            B = f'{a:.4f},{b:.4f},{a + (lat1 - lat0) / n:.4f},{b + (lon1 - lon0) / n:.4f}'
            q = (f'[out:json][timeout:90];(nwr["leisure"="marina"]({B});nwr["harbour"]({B});nwr["mooring"]({B});'
                 f'nwr["leisure"="slipway"]({B});way["man_made"="pier"]({B});way["man_made"="breakwater"]({B}););out geom tags;')
            d = None
            for k in range(6):
                u = URLS[k % 3]
                try:
                    r = requests.post(u, data={'data': q}, timeout=120, headers={'User-Agent': 'oslofjord-bathavner/1.0 (research)'})
                    if r.status_code == 200 and r.text.startswith('{'):
                        d = r.json(); break
                    print(i, j, u, r.status_code)
                except Exception as e:
                    print(i, j, u, repr(e)[:80])
                time.sleep(4)
            if d is None:
                print('FEIL', i, j); continue
            f.write_text(json.dumps(d))
        for e in d['elements']:
            els[(e['type'], e['id'])] = e
(P / 'raw/overpass-lier.json').write_text(json.dumps(dict(elements=list(els.values()))))
print('elementer', len(els))
