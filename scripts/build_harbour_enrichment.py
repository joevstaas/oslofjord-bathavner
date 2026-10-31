"""Build the public, source-attributed Moss card overlay without changing approved data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / 'data/berikelse/3103-moss/pilot-01'
OUTPUT = ROOT / 'site/labs/oslofjord-bathavner/data/enrichment.json'
LABELS = {
    'operator_name': 'Operator / association',
    'berths_published': 'Reported boat places',
    'guest_berths_published': 'Dedicated guest places',
    'dinghy_berths_published': 'Dinghy places',
    'winter_storage_berths_published': 'Winter storage on land',
    'land_storage_reported': 'Storage on land',
    'lifting_reported': 'Boat lifting',
    'ramp_reported': 'Launching ramp',
}
SCOPES = {
    'published_berth_capacity_guest_inclusion_unknown': 'Whether guest places are included is not specified.',
    'operator_published_berths_separately_lists_7_guest': 'Guest places are reported separately; counts are not added.',
    'boats_afloat_capacity': 'Capacity afloat; storage on land is separate.',
    'operator_published_berths_guest_use_of_members_places': 'Guests use available member places; not additional capacity.',
    'ordinary_berths_excluding_separately_reported_dinghy_berths': 'Ordinary places; dinghy places are separate.',
    'whole_shared_facility': 'Capacity for the whole shared facility.',
    'dedicated_guest_berths': 'Dedicated guest places, kept separate from other counts.',
    'children_dinghy_berths': 'Children’s dinghy places; kept separate from ordinary places.',
    'land_winter_storage': 'Capacity on land, not boat places afloat.',
    'bay_shared_ramp_location_not_digitised': 'Shared ramp in the bay; its location has not been mapped separately.',
}
SOURCE_TYPES = {
    'operator': 'Operator website', 'operator_historical': 'Historical operator website',
    'sales_listing': 'Property listing', 'municipal_plan_mirror_historical': 'Historical waste plan',
}

def read(path):
    return json.loads(path.read_text())

def build(pilot=PILOT, approved=None):
    harbours = read(pilot / 'harbours.json')
    observations = read(pilot / 'observations.json')
    sources = {s['source_id']: s for s in read(pilot / 'sources.json')}
    approved = approved if approved is not None else read(ROOT / 'data/samlet/oslofjorden-bathavner-samlet.geojson')
    moss_ids = {f['properties']['harbour_id'] for f in approved['features'] if f['properties'].get('municipality_code') == '3103'}
    if {r['harbour_id'] for r in harbours} != moss_ids:
        raise ValueError('Enrichment must cover exactly the approved Moss harbour IDs')
    if len(harbours) != len(moss_ids):
        raise ValueError('Duplicate harbour IDs in enrichment')
    records = {}
    for row in harbours:
        hid = row['harbour_id']
        evidence = [o for o in observations if o['subject_id'] == hid]
        facts = []
        for field, label in LABELS.items():
            value = row[field]
            if value is None:
                continue
            matches = [o for o in evidence if o['field'] == field and o['value'] == value and o['status'] == 'published_undated']
            if len(matches) != 1:
                raise ValueError(f'{hid}: {field} requires one matching published observation')
            o = matches[0]
            source_ids = [o['source_id']]
            if field == 'operator_name' and row['operator_link_status'] == 'multiple_operators_internal_boundaries_unresolved':
                source_ids += [x['source_id'] for x in evidence if x['field'] == 'operator_component']
                value = 'Vindsteg AS; Arbeidernes Båtforening Moss; third operator unresolved'
            refs = []
            for sid in dict.fromkeys(source_ids):
                s = sources[sid]
                if s['retrieval_status'] != 'retrieved' or not s['url'].startswith('https://'):
                    raise ValueError(f'Unpublishable source {sid}')
                refs.append({'title': s['title'], 'url': s['url'], 'type': SOURCE_TYPES.get(s['source_type'], 'Published source'), 'accessed_date': s['accessed_utc'][:10]})
            qualifier = SCOPES.get(o['scope'], '')
            if field == 'operator_name':
                qualifier = {
                    'operator_published_baseline_location': 'Published operator identity; operating boundaries have not been surveyed.',
                    'historical_operator_baseline_geographic_link': 'Historical website posts from 2010–2011; current operation is not verified.',
                    'sales_listing_and_baseline_location': 'Identity reported in a property listing; not confirmed directly with the operator.',
                    'multiple_operators_internal_boundaries_unresolved': 'Several operators share this harbour group; internal boundaries are unresolved.',
                }.get(row['operator_link_status'], '')
            elif field == 'land_storage_reported' and o['source_id'] == 'S04':
                qualifier = 'Service link on the operator website; capacity and land area are not documented.'
            if isinstance(value, (int, float)) and not isinstance(value, bool) and o['approximate'] is None:
                qualifier += ' Precision is not specified by the source.'
            if field == 'berths_published' and o['source_id'] == 'S17':
                qualifier += ' Reported in a property listing, not verified with the operator.'
            facts.append({'field': field, 'label': label, 'value': value, 'approximate': o['approximate'], 'reference_date': o['reference_date'], 'qualifier': qualifier, 'sources': refs})
        records[hid] = {
            'reviewed_date': row['reviewed_date'], 'water_environment': row['water_environment'],
            'facts': facts, 'current_operation_verified': row['current_operation_verified'],
            'wastewater_treatment_current': row['wastewater_treatment_current'],
            'baseline_capacities': row['baseline_berth_values'],
        }
    return {'schema_version': 1, 'status': 'source_review_pilot', 'records': records}

def main():
    payload = build()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'Enrichment: {len(payload["records"])} Moss harbours -> {OUTPUT.relative_to(ROOT)}')

if __name__ == '__main__':
    main()
