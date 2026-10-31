import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from harbour_capacity import capacities


def feature(count=None, hid='h', gid=None):
    return {'properties': dict(harbour_id=hid, cross_municipality_group_id=gid,
                               berth_count_published=count, berth_count_source='https://example.org')}


class CapacityTest(unittest.TestCase):
    def test_threshold_and_unknown(self):
        rows = [feature(199, 'a'), feature(200, 'b'), feature(None, 'c')]
        actual = capacities(rows, {})
        self.assertEqual([k for k, v in actual.items() if v['count'] >= 200], ['b'])
        self.assertNotIn('c', actual)

    def test_boundary_group_and_duplicate_polygons_are_not_added(self):
        actual = capacities([feature(220, 'a', 'shared'), feature(220, 'b', 'shared'), feature(220, 'b', 'shared')], {})
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual['shared']['count'], 220)

    def test_conflict_is_unknown(self):
        self.assertEqual(capacities([feature(199), feature(220)], {}), {})

    def test_review_supersedes_old_capacity_and_unknown_is_not_fallback(self):
        self.assertEqual(capacities([feature(300)], {'records': {'h': {'facts': []}}}), {})
        record = {'records': {'h': {'facts': [dict(field='berths_published', value=199, sources=[{'url': 'https://example.org/new'}])]}}}
        self.assertEqual(capacities([feature(300)], record)['h']['count'], 199)
