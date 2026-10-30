"""Skriv coverage/source-notes/timing for én kommune i batch-kjøringen. Bruk: finalize_batch.py <mappe> <start_utc> <merknad om dekning>"""
import json, sys, datetime, glob
from pathlib import Path
d = Path(sys.argv[1]); start = sys.argv[2]; cov_note = sys.argv[3]
end = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ'); sec = int((f(end) - f(start)).total_seconds())
imgs = list((d / 'images').glob('*.json'))
(d / 'timing.json').write_text(json.dumps(dict(run_id=d.name + '-rev01', method_version='1.2', schema_version='1.1', started_utc=start, finished_utc=end,
    elapsed_wall_seconds=sec, elapsed_wall_minutes=round(sec / 60, 1), image_count=len(imgs), actual_input_tokens=None, actual_output_tokens=None, actual_cost=None,
    note='Batchkjøring (Bærum–Asker–Lier–Drammen–Oslo): starttid er når analysen av denne kommunen begynte; bildenedlasting skjedde delvis parallelt i bakgrunnen for flere kommuner. Tokens og kostnad ikke målt.'), ensure_ascii=False, indent=1) + '\n')
det = json.loads((d / 'detail-esri.json').read_text())
(d / 'coverage.json').write_text(json.dumps(dict(boundary_source=f"https://api.kartverket.no/kommuneinfo/v1/kommuner/{d.name[:4]}/omrade?utkoordsys=4326", working_crs='EPSG:25833',
    overview_tiles=len(json.loads((d / 'scan-topo.json').read_text())), detail_tiles=len(det), images_total=len(imgs),
    candidate_generation='Metode 1.2: OSM-pirer klynget, bufret, lukket og klippet mot kartvann; hver kandidat vurdert visuelt.',
    sweep=cov_note), ensure_ascii=False, indent=1) + '\n')
src = dict(osm='raw/overpass-??.json', brreg='raw/brreg-*.json; utvalg raw/brreg-utvalg.json', stedsnavn='raw/nearnames.json')
for extra in ['raw/lokalhistoriewiki-bathavner.json', 'raw/kildelister.json']:
    if (d / extra).exists(): src['kildelister'] = extra
(d / 'source-notes.json').write_text(json.dumps(src, ensure_ascii=False, indent=1) + '\n')
print(d.name, round(sec / 60, 1), 'min')
