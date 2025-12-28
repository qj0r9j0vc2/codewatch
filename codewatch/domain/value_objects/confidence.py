"""
ConfidenceScore value object for representing confidence levels.

This module provides an immutable value object for confidence scores
with range validation and normalization for floating-point precision errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ..exceptions import InvalidConfidenceScoreError


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    """
    Confidence score for pattern detection.

    Represents confidence level as a float in range [0.0, 1.0].
    Values slightly outside this range (±0.00001) are normalized to handle
    floating-point precision errors.

    Attributes:
        value: Confidence score in range [0.0, 1.0]

    Raises:
        InvalidConfidenceScoreError: If value is outside valid range

    Examples:
        >>> score = ConfidenceScore(0.85)
        >>> str(score)
        '85.00%'

        >>> high = ConfidenceScore.high()
        >>> high.value
        0.9
    """

    value: float

    def __post_init__(self) -> None:
        """Validate and normalize confidence score."""
        # Normalization tolerance for floating-point errors
        EPSILON = 0.00001

        # Normalize: Handle floating-point precision errors
        normalized_value = self.value
        if -EPSILON <= self.value < 0.0:
            normalized_value = 0.0
        elif 1.0 < self.value <= 1.0 + EPSILON:
            normalized_value = 1.0

        # Apply normalization if needed
        if normalized_value != self.value:
            object.__setattr__(self, 'value', normalized_value)

        # Validate: Must be in range [0.0, 1.0]
        if not (0.0 <= self.value <= 1.0):
            raise InvalidConfidenceScoreError(
                f"Confidence score must be between 0.0 and 1.0, got {self.value}"
            )

    @classmethod
    def high(cls) -> Self:
        """
        Create high confidence score.

        Returns:
            ConfidenceScore with value 0.9

        Examples:
            >>> score = ConfidenceScore.high()
            >>> score.value
            0.9
        """
        return cls(0.9)

    @classmethod
    def medium(cls) -> Self:
        """
        Create medium confidence score.

        Returns:
            ConfidenceScore with value 0.5

        Examples:
            >>> score = ConfidenceScore.medium()
            >>> score.value
            0.5
        """
        return cls(0.5)

    @classmethod
    def low(cls) -> Self:
        """
        Create low confidence score.

        Returns:
            ConfidenceScore with value 0.3

        Examples:
            >>> score = ConfidenceScore.low()
            >>> score.value
            0.3
        """
        return cls(0.3)

    def __str__(self) -> str:
        """
        Return percentage representation.

        Returns:
            Formatted percentage string with 2 decimal places

        Examples:
            >>> str(ConfidenceScore(0.856))
            '85.60%'
        """
        return f"{self.value * 100:.2f}%"

    def __float__(self) -> float:
        """
        Convert to float.

        Returns:
            Raw confidence value as float

        Examples:
            >>> float(ConfidenceScore(0.85))
            0.85
        """
        return self.value
