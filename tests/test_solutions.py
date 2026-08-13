import unittest

from solutions import (
    event_probability,
    expected_distinct_species,
    expected_two_round_winners,
    is_isomorphic,
    missing_number,
    pearson_correlation,
    prime_factors,
    roc_auc_from_pairs,
)


class TestPythonTasks(unittest.TestCase):
    def test_isomorphic_example(self):
        self.assertTrue(is_isomorphic("paper", "title"))

    def test_isomorphic_rejects_many_to_one_mapping(self):
        self.assertFalse(is_isomorphic("ab", "aa"))

    def test_isomorphic_rejects_inconsistent_mapping(self):
        self.assertFalse(is_isomorphic("foo", "bar"))

    def test_isomorphic_handles_empty_and_unicode_strings(self):
        self.assertTrue(is_isomorphic("", ""))
        self.assertTrue(is_isomorphic("топот", "довод"))

    def test_missing_number_in_middle(self):
        self.assertEqual(missing_number([1, 2, 3, 4, 5, 6, 8, 9, 10, 11]), 7)

    def test_missing_number_at_boundary(self):
        self.assertEqual(missing_number([1, 2, 3]), 4)

    def test_missing_number_from_single_value_range(self):
        self.assertEqual(missing_number([]), 1)

    def test_prime_factors(self):
        self.assertEqual(prime_factors(56), [2, 2, 2, 7])
        self.assertEqual(prime_factors(97), [97])
        self.assertEqual(prime_factors(1), [])
        with self.assertRaises(ValueError):
            prime_factors(0)


class TestNumericalTasks(unittest.TestCase):
    def test_probability_answers(self):
        self.assertAlmostEqual(expected_distinct_species(), 3.9906121399)
        self.assertAlmostEqual(expected_two_round_winners(), 26.8354430380)
        self.assertAlmostEqual(event_probability(0.95, 30, 10), 0.6315968501)
        self.assertAlmostEqual(event_probability(0.95, 30, 27), 0.9325358576)

    def test_probability_input_validation(self):
        with self.assertRaises(ValueError):
            expected_distinct_species(0, 6)
        with self.assertRaises(ValueError):
            expected_two_round_winners(3)
        with self.assertRaises(ValueError):
            event_probability(1.0, 30, 10)

    def test_roc_auc(self):
        labels = [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0]
        scores = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25]
        self.assertAlmostEqual(roc_auc_from_pairs(labels, scores), 0.75)

    def test_roc_auc_ties_and_invalid_labels(self):
        self.assertAlmostEqual(roc_auc_from_pairs([1, 0], [0.5, 0.5]), 0.5)
        with self.assertRaises(ValueError):
            roc_auc_from_pairs([1, 2], [0.8, 0.2])

    def test_pearson_correlation(self):
        coffee = [1, 1, 2, 2, 2, 2, 3, 3, 3, 4]
        scores = [85, 88, 79, 81, 84, 65, 67, 58, 76, 49]
        self.assertAlmostEqual(pearson_correlation(coffee, scores), -0.8492696877)

    def test_pearson_rejects_constant_input(self):
        with self.assertRaises(ValueError):
            pearson_correlation([1, 1], [2, 3])


if __name__ == "__main__":
    unittest.main()
