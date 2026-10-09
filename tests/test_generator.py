import unittest
from password_generator import apply_rules, generate_patterns


class GeneratorTests(unittest.TestCase):
    def test_leet_rule_g_to_6(self):
        self.assertEqual(apply_rules("Gato", {"g": "6"}), "6ato")

    def test_existing_exact_match_can_be_filtered(self):
        config = {
            "length": {"min": 1, "max": 30},
            "leet_rules": {},
            "special_rules": {},
            "separators": ["."],
            "patterns": ["{WORD}{SEP}{YEAR}", "{YEAR}{SEP}{WORD}"],
        }
        results, _ = generate_patterns(["Colombia"], "2026", config)
        self.assertIn("Colombia.2026", results)
        existing = {"Colombia.2026"}
        self.assertNotIn("Colombia.2026", results - existing)

    def test_separator_configuration(self):
        config = {
            "length": {"min": 1, "max": 30},
            "leet_rules": {},
            "special_rules": {},
            "separators": ["/"],
            "patterns": ["{WORD}{SEP}{YEAR}"],
        }
        results, _ = generate_patterns(["Forense"], "2026", config)
        self.assertIn("Forense/2026", results)


if __name__ == "__main__":
    unittest.main()
