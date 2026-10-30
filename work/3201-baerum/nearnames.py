"""Nærmeste stedsnavn (Kartverket stedsnavn-API, punktsøk 400 m) for alle autokandidater. Lagrer raw/nearnames.json."""
import json, time, requests
from pathlib import Path
P = Path(__file__).parent
out = {}
for c in json.loads((P / 'auto-candidates.json').read_text()):
    try:
        r = requests.get('https://ws.geonorge.no/stedsnavn/v1/punkt', params=dict(nord=c['y'], ost=c['x'], koordsys=25833, radius=400, utkoordsys=25833, treffPerSide=8), timeout=30).json()
        out[c['cid']] = [f"{n['stedsnavn'][0]['skrivemåte']} ({n['navneobjekttype']})" for n in r.get('navn', [])
                         if n['navneobjekttype'] not in ('Adressenavn', 'Bruk', 'Bolighus', 'Fritidsbolig', 'Gard')][:5]
    except Exception as e:
        out[c['cid']] = ['FEIL ' + repr(e)[:40]]
    time.sleep(0.1)
(P / 'raw/nearnames.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items(): print(k, '; '.join(v))
