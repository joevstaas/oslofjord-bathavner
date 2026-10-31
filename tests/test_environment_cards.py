"""Evidence traceability and approved-geometry invariants for the public overlay."""
import csv
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / 'data/miljokort/pilot-01'
spec = importlib.util.spec_from_file_location('environment_builder', ROOT / 'scripts/build_environment_cards.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class EnvironmentCardsTest(unittest.TestCase):
    def test_public_overlay_matches_evidence_and_does_not_change_baseline(self):
        overlay = builder.build()
        self.assertEqual(overlay, json.loads(builder.OUT.read_text()))
        self.assertEqual(len(overlay['features']), 6)
        observations = [o for f in overlay['features'] for o in f['properties']['observations']]
        self.assertEqual(len(observations), 25)
        for f in overlay['features']:
            p = f['properties']
            refs = {s['id'] for s in p['sources']}
            self.assertEqual([row[0] for row in p['presentation']['rows']], ['Spylevann', 'Båtpuss', 'Arbeidsavfall'])
            self.assertFalse(p['regulatory_context']['compliance_assessed'])
            self.assertFalse(p['regulatory_context']['applicability_assessed'])
            self.assertFalse(p['map_link']['operating_boundaries_verified'])
            self.assertFalse(p['ecological_effect_verified'])
            self.assertTrue(set(p['map_link']['source_ids']) <= refs)
            for o in p['observations']:
                self.assertTrue(set(o['source_ids']) <= refs)
                self.assertTrue(o['missing_evidence'])
                self.assertIsNone(o['measured_effect'])
                self.assertFalse(o['confirmed_measure_gap'])
        baseline = json.loads((PILOT / 'baseline.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT / baseline['path']).read_bytes()).hexdigest(), baseline['sha256'])
        # Snapshots are a separate local archive, not required in a clean checkout.
        for s in json.loads((PILOT / 'sources.json').read_text()):
            path = PILOT / s['snapshot']
            if path.exists():
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), s['sha256'])
        with (PILOT / 'observations.csv').open(encoding='utf-8-sig', newline='') as h:
            rows = list(csv.DictReader(h, delimiter=';'))
        self.assertEqual(len(rows), len(observations))
        for row, o in zip(rows, observations):
            for key, value in o.items():
                self.assertEqual(row[key], json.dumps(value, ensure_ascii=False) if isinstance(value, list) else '' if value is None else str(value))

if __name__ == '__main__':
    unittest.main()
