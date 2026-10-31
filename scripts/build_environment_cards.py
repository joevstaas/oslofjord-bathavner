"""Build a separate public environmental-card overlay. Never modifies approved harbours."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / 'data/miljokort/pilot-01'
OUT = ROOT / 'site/labs/oslofjord-bathavner/data/environment-cards.json'

def build():
    data = json.loads((PILOT / 'cards.json').read_text())
    sources = {s['id']: s for s in json.loads((PILOT / 'sources.json').read_text())}
    approved = json.loads((ROOT / 'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())
    ids = {f['properties']['harbour_id'] for f in approved['features']}
    features = []
    for card in data['cards']:
        link = card['map_link']
        assert set(link['harbour_ids']) <= ids
        assert len(link['coordinates']) == 2 and all(isinstance(x, (int, float)) for x in link['coordinates'])
        used = set(card['source_ids'] + link['source_ids'])
        assert all(set(o['source_ids']) <= sources.keys() for o in card['observations'])
        assert used <= sources.keys()
        public = dict(card)
        public['regulatory_context'] = json.loads((PILOT / 'regulatory-context.json').read_text())
        public['sources'] = [{k: sources[sid].get(k) for k in ('id', 'url', 'title', 'publisher', 'source_type', 'published_or_updated', 'retrieved_utc')} for sid in sorted(used)]
        features.append(dict(type='Feature', geometry=dict(type='Point', coordinates=link['coordinates']), properties=public))
    return dict(type='FeatureCollection', schema_version=1, status='source_review_pilot', features=features)

def main():
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f"Built {len(data['features'])} environmental cards; approved harbour data unchanged.")

if __name__ == '__main__':
    main()
