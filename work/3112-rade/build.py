"""Bygg Råde rev. 1: GeoJSON, metadata-CSV, digitaliseringsgrunnlag, overlapp- og sammendragsfil.
Skriver bare til denne arbeidsmappen. Godkjenningsstatus settes alltid til til_godkjenning."""
import json, csv, collections, warnings
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import Polygon, shape, mapping
from shapely.geometry.polygon import orient
from shapely import ops
from digitize import rows

warnings.filterwarnings('ignore', category=DeprecationWarning)
P = Path(__file__).parent
CODE, NAME, REV, TODAY = '3112', 'Råde', 1, '2026-10-29'
F = Transformer.from_crs(4326, 25833, always_xy=True).transform
B = Transformer.from_crs(25833, 4326, always_xy=True).transform
boundary = ops.transform(F, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
ATTR = ('Kildeangitte operatører, Enhetsregisteret og Råde kommune; © Kartverket; imagery: Esri, Vantor, Earthstar Geographics '
        'and the GIS User Community; OSM © OpenStreetMap contributors (ODbL)')

groups, parts, features, projected = {}, collections.Counter(), [], []
for r in rows:
    hid = groups.setdefault(r['group'], f'{CODE}-H{len(groups) + 1:02d}')
    parts[hid] += 1
    fid = f'{hid}-B{parts[hid]:02d}'
    m = json.loads((P / 'images' / f"{r['image']}.json").read_text())
    a, b, c, d = r['frame']
    h = r['size'] * (d - b) / (c - a)
    g = Polygon([(a + x / r['size'] * (c - a), d - y / h * (d - b)) for x, y in r['pixels']])
    assert g.is_valid, (r['name'], 'ugyldig polygon')
    clipped = not boundary.covers(g)
    orig = g
    g = g.intersection(boundary)
    assert g.geom_type == 'Polygon' and g.area > 0.2 * orig.area, (r['name'], g.geom_type, g.area / orig.area)
    g = orient(g, sign=1)
    geo = ops.transform(B, g)
    q = geo.representative_point()
    sources = list(dict.fromkeys(r['sources'] + [f'https://www.openstreetmap.org/{o}' for o in r['osm_ids']] + [m['url']]))
    note = r['note'] + (' Vannmiljø: ' + r['water_body'] + '.' if r['water_body'] != 'saltvann' else '')
    if clipped:
        note += f' Klippet ved offisiell kommunegrense; {round(100 * g.area / orig.area)} % av det tegnede omrisset ligger i Råde.'
    cap = r['capacity']
    p = dict(
        id=fid, harbour_id=hid, candidate_id=r['candidate_id'], name=r['name'], name_is_descriptive=r['name_is_descriptive'],
        municipality=NAME, municipality_code=CODE,
        classification='mulig_smabathavn' if r['possible'] else 'smabathavn', classification_basis=r['basis'],
        approval_status='til_godkjenning', approved_utc=None, revision=REV, method_version='1.1', schema_version='1.1',
        geometry_role='brygger_batplasser_og_mellomliggende_sjo', method=r['tracing_method'],
        area_m2=round(g.area, 1), area_crs='EPSG:25833', longitude=round(q.x, 7), latitude=round(q.y, 7),
        sources=sources, osm_ids=r['osm_ids'], imagery_source=m['source'], imagery_retrieved_date=m['retrieved_date'],
        source_observation_date=None, image_resolution_m_per_pixel=round((m['bbox'][2] - m['bbox'][0]) / m['width'], 3),
        estimated_accuracy_m=None, needs_orthophoto_review=r['geometry_uncertain'], needs_dated_imagery_review=True,
        current_operation_verified=False, reviewed_date=TODAY,
        berth_count_published=cap, berth_count_source=r['capacity_source'] if cap is not None else None,
        berth_count_approximate=False if cap is not None else None,
        berth_count_scope='hele_havneanlegget' if cap is not None else None,
        berth_count_reference_period=r['capacity_period'] if cap is not None else None,
        source_register_objectid=None, source_register_number=None, source_register_members=r['source_register_members'],
        capacity_components=[],
        municipality_clipped=clipped, cross_municipality_group_id=r['cross_group'],
        attribution=ATTR, note=note,
        geometry_status='usikker_avgrensning' if r['geometry_uncertain'] else 'forelopig_avgrensning',
        water_body=r['water_body'], image_id=r['image'], image_sha256=m['sha256'])
    features.append(dict(type='Feature', properties=p, geometry=mapping(geo)))
    projected.append(g)

issues = []
for i, g in enumerate(projected):
    for j in range(i + 1, len(projected)):
        ar = g.intersection(projected[j]).area
        if ar >= 1:
            issues.append(dict(a=features[i]['properties']['id'], b=features[j]['properties']['id'], area_m2=round(ar, 2)))

fc = dict(type='FeatureCollection', name=f'{NAME} – småbåthavner, revisjon {REV}',
          description='Kommuneleveranse til godkjenning. Bilde- og kildebasert kartlegging; opptaksdato, posisjonsnøyaktighet, '
                      'fullstendighet og dagens drift er ikke generelt verifisert. Fysiske havneområder, ikke juridiske grenser.',
          method_version='1.1', schema_version='1.1', features=features)
(P / 'rade-bathavner.geojson').write_text(json.dumps(fc, ensure_ascii=False, indent=1) + '\n')
with (P / 'rade-metadata.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(features[0]['properties']), delimiter=';')
    w.writeheader()
    w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in x['properties'].items()} for x in features)
(P / 'manual-digitization.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n')
(P / 'overlap-issues.json').write_text(json.dumps(issues, indent=1) + '\n')
summary = dict(polygons=len(features), harbours=len(groups),
               possible_harbours=len({x['properties']['harbour_id'] for x in features if x['properties']['classification'] == 'mulig_smabathavn'}),
               uncertain_geometries=sum(x['properties']['needs_orthophoto_review'] for x in features),
               clipped=[x['properties']['id'] for x in features if x['properties']['municipality_clipped']], overlap_issues=issues,
               harbour_ids={k: v for k, v in groups.items()})
(P / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(summary, ensure_ascii=False))
