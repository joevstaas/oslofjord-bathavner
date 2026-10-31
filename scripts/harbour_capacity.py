"""Published capacity per physical facility; never sum polygon or seasonal counts."""
from collections import defaultdict


def capacities(features, enrichment):
    groups = defaultdict(list)
    for feature in features:
        p = feature['properties']
        groups[p.get('cross_municipality_group_id') or p['harbour_id']].append(p)
    result = {}
    for gid, rows in groups.items():
        values = []
        for p in rows:
            record = enrichment.get('records', {}).get(p['harbour_id'])
            if record is not None:
                facts = [f for f in record['facts'] if f['field'] == 'berths_published']
                for f in facts:
                    values.append(dict(count=f['value'], source=f['sources'][0]['url'],
                                       period=f.get('reference_date') or 'Reference year unknown', approximate=f.get('approximate', False)))
            elif isinstance(p.get('berth_count_published'), (int, float)) and p.get('berth_count_source'):
                values.append(dict(count=p['berth_count_published'], source=p['berth_count_source'],
                                   period=p.get('berth_count_reference_period') or 'Reference year unknown',
                                   approximate=p.get('berth_count_approximate', False)))
        # Conflicting counts are unknown; identical values on several polygons count once.
        if values and len({v['count'] for v in values}) == 1:
            result[gid] = values[0]
    return result
