import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_harbour_enrichment import build, PILOT, OUTPUT

class HarbourEnrichmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = build()

    def facts(self, hid):
        return {f['field']: f for f in self.payload['records'][hid]['facts']}

    def test_exact_moss_coverage_and_no_open_candidates(self):
        self.assertEqual(set(self.payload['records']), {f'3103-H{i:02}' for i in range(1, 23)})
        self.assertFalse(any(k.startswith('C-') for k in self.payload['records']))

    def test_fiske_uses_new_source_without_erasing_baseline(self):
        fact = self.facts('3103-H01')['berths_published']
        self.assertEqual(fact['value'], 376)
        self.assertIsNone(fact['reference_date'])
        self.assertIn('fiske-baatforening.no', fact['sources'][0]['url'])
        self.assertEqual(self.payload['records']['3103-H01']['baseline_capacities'][0]['value'], 384)

    def test_categories_and_precision_are_preserved(self):
        vansjo = self.facts('3103-H11')
        self.assertEqual(vansjo['berths_published']['value'], 168)
        self.assertEqual(vansjo['dinghy_berths_published']['value'], 16)
        self.assertEqual(self.payload['records']['3103-H11']['water_environment'], 'freshwater')
        self.assertEqual(self.facts('3103-H05')['winter_storage_berths_published']['value'], 200)
        self.assertTrue(self.facts('3103-H05')['berths_published']['approximate'])
        self.assertTrue(self.facts('3103-H03')['berths_published']['approximate'])

    def test_unresolved_operator_groups_do_not_gain_capacity(self):
        self.assertNotIn('berths_published', self.facts('3103-H16'))
        self.assertNotIn('operator_name', self.facts('3103-H17'))
        self.assertNotIn('berths_published', self.facts('3103-H17'))
        self.assertIn('historical website', self.facts('3103-H07')['operator_name']['qualifier'].lower())

    def test_historical_wash_claim_is_not_published_as_current(self):
        for record in self.payload['records'].values():
            self.assertIsNone(record['current_operation_verified'])
            self.assertIsNone(record['wastewater_treatment_current'])
            self.assertFalse(any('wash' in f['field'] or 'treatment' in f['field'] for f in record['facts']))

    def test_every_fact_has_public_sources_and_access_dates(self):
        for record in self.payload['records'].values():
            for fact in record['facts']:
                self.assertTrue(fact['sources'])
                for source in fact['sources']:
                    self.assertTrue(source['url'].startswith('https://'))
                    self.assertEqual(source['accessed_date'], '2026-10-31')

    def fixture(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        dest = Path(directory.name)
        for filename in ['harbours.json', 'observations.json', 'sources.json']:
            shutil.copyfile(PILOT / filename, dest / filename)
        return dest

    def test_unsubstantiated_value_is_rejected(self):
        dest = self.fixture()
        rows = json.loads((dest / 'harbours.json').read_text())
        rows[0]['berths_published'] = 377
        (dest / 'harbours.json').write_text(json.dumps(rows))
        with self.assertRaisesRegex(ValueError, 'matching published observation'):
            build(dest)

    def test_duplicate_harbour_is_rejected(self):
        dest = self.fixture()
        rows = json.loads((dest / 'harbours.json').read_text())
        rows.append(rows[0])
        (dest / 'harbours.json').write_text(json.dumps(rows))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            build(dest)

    def test_generated_bundle_matches_reviewed_records(self):
        self.assertEqual(json.loads(OUTPUT.read_text()), self.payload)

if __name__ == '__main__':
    unittest.main()
