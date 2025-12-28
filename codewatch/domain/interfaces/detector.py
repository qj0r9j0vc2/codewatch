"""
Detector interface for pattern detection.

This module provides the abstract Detector interface for detecting
specific pattern types in source code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities import Pattern
from ..enums import PatternType


class Detector(ABC):
    """
    Abstract interface for pattern detection.

    Detectors analyze source code to find instances of a specific pattern type.
    Each detector focuses on one pattern type (e.g., KeeperDetector finds Keepers).

    Implementations must be stateless and thread-safe.

    Examples:
        >>> class KeeperDetector(Detector):
        ...     def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        ...         # Implementation that finds Keeper patterns
        ...         return found_patterns
        ...     def supported_pattern_type(self) -> PatternType:
        ...         return PatternType.KEEPER
    """

    @abstractmethod
    def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        """
        Detect all instances of the pattern in source code.

        This method analyzes the provided source code and returns all detected
        instances of the pattern type this detector supports.

        Args:
            source_code: Source code content to analyze
            file_path: Path to the source file (for location context in results)

        Returns:
            List of detected patterns with confidence scores.
            Returns empty list if no patterns found.
            Patterns are sorted by location (file path, then line number).

        Raises:
            ExtractionError: If detection fails due to parsing errors,
                            invalid source code, or detector-specific issues.
                            Should include details about what failed.

        Notes:
            - Implementations must be thread-safe (no shared mutable state)
            - Confidence scores should reflect detection certainty
            - All returned patterns must have valid locations within the file

        Examples:
            >>> detector = KeeperDetector()
            >>> patterns = detector.detect(source_code, "cosmos/bank/keeper.go")
            >>> len(patterns)
            3
            >>> patterns[0].pattern_type
            <PatternType.KEEPER: 'keeper'>
        """
        raise NotImplementedError

    @abstractmethod
    def supported_pattern_type(self) -> PatternType:
        """
        Return the pattern type this detector finds.

        Returns:
            PatternType enum value representing the pattern this detector finds.

        Examples:
            >>> detector = KeeperDetector()
            >>> detector.supported_pattern_type()
            <PatternType.KEEPER: 'keeper'>
        """
        raise NotImplementedError
