"""Solutions for the Python and numerical tasks of the test assignment."""

from __future__ import annotations

from math import sqrt
from typing import Sequence


def is_isomorphic(s: str, t: str) -> bool:
    """Return True when strings have a one-to-one character mapping."""
    if len(s) != len(t):
        return False

    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}

    for source_char, target_char in zip(s, t):
        if source_char in s_to_t and s_to_t[source_char] != target_char:
            return False
        if target_char in t_to_s and t_to_s[target_char] != source_char:
            return False
        s_to_t[source_char] = target_char
        t_to_s[target_char] = source_char

    return True


def missing_number(nums: Sequence[int]) -> int:
    """Find the only missing value from 1..n, where n == len(nums) + 1."""
    n = len(nums) + 1
    missing = 0

    for expected_value in range(1, n + 1):
        missing ^= expected_value
    for value in nums:
        missing ^= value

    return missing


def prime_factors(n: int) -> list[int]:
    """Return the prime factors of a positive integer in ascending order."""
    if n < 1:
        raise ValueError("n must be a positive integer")

    factors: list[int] = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2

    if n > 1:
        factors.append(n)

    return factors


def expected_distinct_species(species_count: int = 6, visits: int = 6) -> float:
    """Expected number of species observed in independent uniform visits."""
    return species_count * (1 - ((species_count - 1) / species_count) ** visits)


def expected_two_round_winners(participant_count: int = 80) -> float:
    """Expected number of participants who win both independent pairings."""
    opponents = participant_count - 1
    return sum((weaker_opponents / opponents) ** 2 for weaker_opponents in range(participant_count))


def event_probability(base_probability: float, base_minutes: float, target_minutes: float) -> float:
    """Scale an at-least-one-event probability under a homogeneous Poisson process."""
    if not 0 <= base_probability < 1:
        raise ValueError("base_probability must be in [0, 1)")
    if base_minutes <= 0 or target_minutes < 0:
        raise ValueError("time intervals must be non-negative and base_minutes positive")
    return 1 - (1 - base_probability) ** (target_minutes / base_minutes)


def roc_auc_from_pairs(labels: Sequence[int], scores: Sequence[float]) -> float:
    """Compute ROC-AUC as the share of correctly ordered positive-negative pairs."""
    if len(labels) != len(scores):
        raise ValueError("labels and scores must have equal length")

    positive_scores = [score for label, score in zip(labels, scores) if label == 1]
    negative_scores = [score for label, score in zip(labels, scores) if label == 0]
    if not positive_scores or not negative_scores:
        raise ValueError("both classes must be present")

    concordant = sum(pos > neg for pos in positive_scores for neg in negative_scores)
    ties = sum(pos == neg for pos in positive_scores for neg in negative_scores)
    return (concordant + 0.5 * ties) / (len(positive_scores) * len(negative_scores))


def pearson_correlation(x: Sequence[float], y: Sequence[float]) -> float:
    """Compute Pearson's linear correlation coefficient."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must have equal length of at least two")

    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    cross_deviation = sum((x_i - x_mean) * (y_i - y_mean) for x_i, y_i in zip(x, y))
    x_squared_deviation = sum((x_i - x_mean) ** 2 for x_i in x)
    y_squared_deviation = sum((y_i - y_mean) ** 2 for y_i in y)

    denominator = sqrt(x_squared_deviation * y_squared_deviation)
    if denominator == 0:
        raise ValueError("correlation is undefined for a constant sequence")
    return cross_deviation / denominator


if __name__ == "__main__":
    print("Isomorphic:", is_isomorphic("paper", "title"))
    print("Missing number:", missing_number([1, 2, 3, 4, 5, 6, 8, 9, 10, 11]))
    print("Prime factors:", prime_factors(56))
