"""Tests for ConfidenceScore value object."""

import pytest

from codewatch.domain.value_objects.confidence import ConfidenceScore
from codewatch.domain.exceptions import InvalidConfidenceScoreError


class TestConfidenceScoreCreation:
    """Tests for ConfidenceScore creation with valid values."""

    def test_create_with_valid_value(self) -> None:
        """Should create score with valid value."""
        score = ConfidenceScore(0.85)
        assert score.value == 0.85

    def test_accept_zero(self) -> None:
        """Should accept 0.0."""
        score = ConfidenceScore(0.0)
        assert score.value == 0.0

    def test_accept_one(self) -> None:
        """Should accept 1.0."""
        score = ConfidenceScore(1.0)
        assert score.value == 1.0

    def test_accept_mid_range_values(self) -> None:
        """Should accept values in mid-range."""
        scores = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
        for val in scores:
            score = ConfidenceScore(val)
            assert score.value == val


class TestConfidenceScoreValidation:
    """Tests for ConfidenceScore validation (range [0.0, 1.0])."""

    def test_reject_negative_value(self) -> None:
        """Should reject negative values."""
        with pytest.raises(InvalidConfidenceScoreError, match="between 0.0 and 1.0"):
            ConfidenceScore(-0.1)

    def test_reject_value_above_one(self) -> None:
        """Should reject values above 1.0."""
        with pytest.raises(InvalidConfidenceScoreError, match="between 0.0 and 1.0"):
            ConfidenceScore(1.5)

    def test_reject_large_negative(self) -> None:
        """Should reject large negative values."""
        with pytest.raises(InvalidConfidenceScoreError):
            ConfidenceScore(-10.0)

    def test_reject_large_positive(self) -> None:
        """Should reject large positive values."""
        with pytest.raises(InvalidConfidenceScoreError):
            ConfidenceScore(100.0)


class TestConfidenceScoreNormalization:
    """Tests for ConfidenceScore normalization (floating-point errors)."""

    def test_normalize_slightly_below_zero(self) -> None:
        """Should normalize values slightly below zero due to float errors."""
        score = ConfidenceScore(-0.00001)
        assert score.value == 0.0

    def test_normalize_slightly_above_one(self) -> None:
        """Should normalize values slightly above 1.0 due to float errors."""
        score = ConfidenceScore(1.00001)
        assert score.value == 1.0

    def test_no_normalize_clearly_invalid_negative(self) -> None:
        """Should not normalize clearly invalid negative values."""
        with pytest.raises(InvalidConfidenceScoreError):
            ConfidenceScore(-0.001)

    def test_no_normalize_clearly_invalid_positive(self) -> None:
        """Should not normalize clearly invalid positive values."""
        with pytest.raises(InvalidConfidenceScoreError):
            ConfidenceScore(1.001)


class TestConfidenceScoreFactoryMethods:
    """Tests for ConfidenceScore factory methods."""

    def test_high_factory(self) -> None:
        """Should create high confidence score (0.9)."""
        score = ConfidenceScore.high()
        assert score.value == 0.9

    def test_medium_factory(self) -> None:
        """Should create medium confidence score (0.5)."""
        score = ConfidenceScore.medium()
        assert score.value == 0.5

    def test_low_factory(self) -> None:
        """Should create low confidence score (0.3)."""
        score = ConfidenceScore.low()
        assert score.value == 0.3


class TestConfidenceScoreImmutability:
    """Tests for ConfidenceScore immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        score = ConfidenceScore(0.85)
        with pytest.raises(Exception):  # FrozenInstanceError
            score.value = 0.9  # type: ignore


class TestConfidenceScoreHashability:
    """Tests for ConfidenceScore hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        score = ConfidenceScore(0.85)
        hash(score)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        score1 = ConfidenceScore(0.85)
        score2 = ConfidenceScore(0.85)
        scores = {score1, score2}
        assert len(scores) == 1  # Equal values

    def test_can_be_used_as_dict_key(self) -> None:
        """Should be usable as dict key."""
        score = ConfidenceScore(0.85)
        cache = {score: "high confidence"}
        assert cache[score] == "high confidence"


class TestConfidenceScoreStringRepresentation:
    """Tests for ConfidenceScore string representation and float conversion."""

    def test_str_representation(self) -> None:
        """Should format as percentage."""
        score = ConfidenceScore(0.856)
        assert str(score) == "85.60%"

    def test_str_zero(self) -> None:
        """Should format zero as percentage."""
        score = ConfidenceScore(0.0)
        assert str(score) == "0.00%"

    def test_str_one(self) -> None:
        """Should format one as percentage."""
        score = ConfidenceScore(1.0)
        assert str(score) == "100.00%"

    def test_float_conversion(self) -> None:
        """Should convert to float."""
        score = ConfidenceScore(0.85)
        assert float(score) == 0.85

    def test_float_conversion_preserves_value(self) -> None:
        """Should preserve exact value in float conversion."""
        original = 0.123456
        score = ConfidenceScore(original)
        assert float(score) == original


class TestConfidenceScoreEquality:
    """Tests for ConfidenceScore equality."""

    def test_equal_scores(self) -> None:
        """Should compare equal scores."""
        score1 = ConfidenceScore(0.85)
        score2 = ConfidenceScore(0.85)
        assert score1 == score2

    def test_unequal_scores(self) -> None:
        """Should compare unequal scores."""
        score1 = ConfidenceScore(0.85)
        score2 = ConfidenceScore(0.86)
        assert score1 != score2

    def test_factory_equality(self) -> None:
        """Should compare factory-created scores."""
        high1 = ConfidenceScore.high()
        high2 = ConfidenceScore.high()
        assert high1 == high2
