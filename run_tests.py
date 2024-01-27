import unittest
from bitwarden_dedup import dedup

class MyTestCase(unittest.TestCase):
    def test_dedup(self):
        dedup("./test_resources/fake_bitwarden_export_2024.json", "./test_resources/computed_deduped.json")

        with open("./test_resources/computed_deduped.json", 'r') as f:
            computed_deduped = f.read()

        with open("./test_resources/expected_deduped.json", 'r') as f:
            expected_deduped = f.read()

        self.assertEqual(computed_deduped, expected_deduped)

if __name__ == '__main__':
    unittest.main()
