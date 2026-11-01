import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from estimate_harbour_capacity import estimate, cross_validate, fit, predict
ROOT = Path(__file__).resolve().parents[1]


def rows():
    return [dict(gid=f'{m}-{i}', municipality=m, municipalities=[m], area=1000 * i,
                 count=10 * i) for m in ['A', 'B', 'C', 'D'] for i in [1, 2, 3]]


class EstimateTests(unittest.TestCase):
    def test_recovers_power_relation(self):
        parameters = fit(rows())
        self.assertAlmostEqual(predict(parameters, 4000), 40)

    def test_held_out_municipality_does_not_leak(self):
        original = rows()
        expected = cross_validate(original, 'balanced_log')[0]['predicted']
        changed = copy.deepcopy(original)
        for row in changed:
            if row['municipality'] == 'A':
                row['count'] *= 100
        self.assertAlmostEqual(cross_validate(changed, 'balanced_log')[0]['predicted'], expected)

    def test_shared_facility_excludes_both_municipalities(self):
        original = rows()
        original[0]['municipalities'] = ['A', 'B']
        expected = cross_validate(original, 'balanced_log')[0]['predicted']
        changed = copy.deepcopy(original)
        for row in changed:
            if row['municipality'] == 'B':
                row['count'] *= 100
        self.assertAlmostEqual(cross_validate(changed, 'balanced_log')[0]['predicted'], expected)

    def test_real_dataset_published_wins_and_groups_are_unique(self):
        features = json.loads((ROOT / 'site/labs/oslofjord-bathavner/data/harbours.geojson').read_text())['features']
        estimates, report = estimate(features)
        self.assertEqual(report['training_groups'], 98)
        self.assertEqual(len(estimates), 567)
        self.assertEqual(report['training_groups'] + len(estimates), 665)
        for f in features:
            p = f['properties']
            self.assertEqual(p['capacity_estimate'], estimates.get(p['gid']))
            if p['capacity']:
                self.assertNotIn(p['gid'], estimates)
        for e in estimates.values():
            self.assertLessEqual(e['low'], e['count'])
            self.assertLessEqual(e['count'], e['high'])
            if e['outside_training_range'] or e['possible_harbour']:
                self.assertEqual(e['category'], 'uncertain')
        self.assertTrue(all(p['gid'] not in {r['gid'] for r in report['training'] if set(r['municipalities']).isdisjoint(p['held_out_municipalities'])}
                            for p in report['held_out_predictions']))
