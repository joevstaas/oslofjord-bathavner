"""Bygg Asker rev. 1 fra auto-kandidater + decisions.py: GeoJSON, metadata-CSV, kandidatlogg, sammendrag.
Skriver bare til arbeidsmappen. approval_status settes alltid til til_godkjenning."""
import json, csv, collections, warnings
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, box, Polygon, mapping
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import ops

warnings.filterwarnings('ignore')
P = Path(__file__).parent
CODE, NAME, REV, TODAY = '3203', 'Asker', 1, '2026-10-29'
F = Transformer.from_crs(4326, 25833, always_xy=True).transform
B = Transformer.from_crs(25833, 4326, always_xy=True).transform
bnd = ops.transform(F, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
ns = {}; exec((P / 'decisions.py').read_text(), ns); D = ns['D']
cands = {c['cid']: c for c in json.loads((P / 'auto-candidates.json').read_text())}
ATTR = ('Kildeangitte operatører, Enhetsregisteret; © Kartverket; imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; '
        'OSM © OpenStreetMap contributors (ODbL)')
imgs = []
for f in (P / 'images').glob('*.json'):
    m = json.loads(f.read_text())
    if m.get('source', '').startswith('Esri'): imgs.append((m['bbox'][2] - m['bbox'][0]) / m['width'] and ((m['bbox'][2] - m['bbox'][0]) / m['width'], f.stem, m))
imgs.sort(key=lambda t: t[0])

def best_image(g):
    for r, k, m in imgs:
        if box(*m['bbox']).contains(g): return k, m
    return max(((k, m) for r, k, m in imgs), key=lambda t: box(*t[1]['bbox']).intersection(g).area)

rows = []  # (decision, geometry, candidate id, osm piers)
for cid, dd in D.items():
    if dd['action'] == 'exc': continue
    c = cands.get(cid)
    if dd['action'] == 'man':
        rows.append((dd, Polygon(dd['coords']), cid, [], 'manuell_digitalisering_georeferert_flybilde')); continue
    g = shape(c['geom'])
    meth = 'osm_pirer_bufret_og_klippet_mot_kartvann_bildekontrollert'
    if dd['action'] == 'clip': g = g.intersection(box(*dd['box']))
    if dd['action'] == 'add': g = unary_union([g, Polygon(dd['extra']).intersection(bnd)]); meth += '_med_manuelt_tillegg'
    if dd['action'] == 'split':
        for part in dd['parts']:
            gp = g.intersection(box(*part['box'])) if 'box' in part else g.difference(box(*part['minus']))
            rows.append((part, gp, cid, c['osm_piers'], meth))
        continue
    rows.append((dd, g, cid, c['osm_piers'], meth))

groups, parts, feats, proj = {}, collections.Counter(), [], []
order = sorted(rows, key=lambda r: (round(r[1].centroid.x / 2000), -r[1].centroid.y))
for dd, g, cid, piers, meth in order:
    raw_g = g
    g = g.intersection(bnd).buffer(0)
    polys = [p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'Polygon' and p.area >= 100 and not any(box(*b).contains(p.representative_point()) for b in dd.get('drop', []))]
    for poly in polys:
        hid = groups.setdefault(dd['group'], f"{CODE}-H{len(groups) + 1:02d}")
        parts[hid] += 1
        fid = f'{hid}-B{parts[hid]:02d}'
        poly = orient(poly, sign=1); geo = ops.transform(B, poly); q = geo.representative_point()
        key, m = best_image(poly)
        cap = dd.get('capacity')
        srcs = list(dict.fromkeys(dd.get('sources', []) + [f'https://www.openstreetmap.org/{o}' for o in dd.get('osm', []) + piers] + [m['url']]))
        clipped = not bnd.buffer(0.01).covers(raw_g)
        p = dict(id=fid, harbour_id=hid, candidate_id=cid, name=dd['name'], name_is_descriptive=dd.get('descr', True),
                 municipality=NAME, municipality_code=CODE, classification=dd['cls'], classification_basis=dd['basis'],
                 approval_status='til_godkjenning', approved_utc=None, revision=REV, method_version='1.2', schema_version='1.1',
                 geometry_role='brygger_batplasser_og_mellomliggende_sjo', method=meth,
                 area_m2=round(poly.area, 1), area_crs='EPSG:25833', longitude=round(q.x, 7), latitude=round(q.y, 7),
                 sources=srcs, osm_ids=list(dict.fromkeys(dd.get('osm', []) + piers)), imagery_source=m['source'], imagery_retrieved_date=m['retrieved_date'],
                 source_observation_date=None, image_resolution_m_per_pixel=round((m['bbox'][2] - m['bbox'][0]) / m['width'], 3),
                 estimated_accuracy_m=None, needs_orthophoto_review=dd.get('unc', False), needs_dated_imagery_review=True,
                 current_operation_verified=False, reviewed_date=TODAY,
                 berth_count_published=cap, berth_count_source=dd.get('cap_source') if cap else None,
                 berth_count_approximate=dd.get('cap_approx', False) if cap else None,
                 berth_count_scope='hele_havneanlegget' if cap else None,
                 berth_count_reference_period='ukjent_referanseperiode_nettside_lest_2026-10-29' if cap else None,
                 source_register_objectid=None, source_register_number=None, source_register_members=[], capacity_components=[],
                 municipality_clipped=clipped, cross_municipality_group_id=dd.get('cross'),
                 attribution=ATTR, note=dd.get('note', '') + (f' Delpolygon {parts[hid]} av havnegruppen.' if len(polys) > 1 else ''),
                 geometry_status='usikker_avgrensning' if dd.get('unc') else 'forelopig_avgrensning',
                 water_body='saltvann_eller_brakkvann', image_id=key, image_sha256=m.get('sha256'))
        feats.append(dict(type='Feature', properties=p, geometry=mapping(geo))); proj.append(poly)

issues = [dict(a=feats[i]['properties']['id'], b=feats[j]['properties']['id'], area_m2=round(proj[i].intersection(proj[j]).area, 2))
          for i in range(len(proj)) for j in range(i + 1, len(proj)) if proj[i].intersection(proj[j]).area >= 1]
fc = dict(type='FeatureCollection', name=f'{NAME} – småbåthavner, revisjon {REV}',
          description='Kommuneleveranse til godkjenning. Bilde- og kildebasert kartlegging; opptaksdato, posisjonsnøyaktighet, fullstendighet og dagens drift er ikke generelt verifisert. Fysiske havneområder, ikke juridiske grenser.',
          method_version='1.2', schema_version='1.1', features=feats)
(P / 'asker-bathavner.geojson').write_text(json.dumps(fc, ensure_ascii=False, indent=1) + '\n')
with (P / 'asker-metadata.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(feats[0]['properties']), delimiter=';'); w.writeheader()
    w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in x['properties'].items()} for x in feats)
# kandidatlogg
fid_by_c = collections.defaultdict(list)
for x in feats: fid_by_c[x['properties']['candidate_id']].append(x['properties']['id'])
L = []
for cid, dd in D.items():
    c = cands.get(cid, {})
    L.append(dict(candidate_id=cid, x_25833=c.get('x'), y_25833=c.get('y'), osm_ids=c.get('osm_piers', []) + [m['id'] for m in c.get('marks', [])],
                  decision='utelatt' if dd['action'] == 'exc' else 'inkludert_' + (dd.get('cls') or 'flere_deler'),
                  reason=dd.get('why') or dd.get('basis') or 'delt_i_to_havner', feature_ids=fid_by_c.get(cid, []), reviewed_date=TODAY))
(P / 'candidate-ledger.json').write_text(json.dumps(L, ensure_ascii=False, indent=1) + '\n')
with (P / 'candidate-ledger.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(L[0]), delimiter=';'); w.writeheader()
    w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in r.items()} for r in L)
summary = dict(polygons=len(feats), harbours=len(groups),
               possible_harbours=len({x['properties']['harbour_id'] for x in feats if x['properties']['classification'] == 'mulig_smabathavn'}),
               uncertain_geometries=sum(x['properties']['needs_orthophoto_review'] for x in feats),
               candidates_total=len(L), candidates_included=sum(1 for r in L if r['feature_ids']), overlap_issues=issues)
(P / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(summary, ensure_ascii=False))
