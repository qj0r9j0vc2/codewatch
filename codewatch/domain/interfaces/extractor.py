"""
Extractor interface for framework-specific pattern extraction.

This module provides the abstract Extractor interface for extracting
all patterns from a codebase for a specific blockchain framework.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities import Pattern
from ..enums import Framework


class Extractor(ABC):
    """
    Abstract interface for framework-specific pattern extraction.

    Extractors coordinate multiple detectors to extract all patterns from
    a codebase. Each extractor is specific to one blockchain framework.

    Implementations orchestrate file traversal, detector invocation, and
    result aggregation.

    Examples:
        >>> class CosmosSDKExtractor(Extractor):
        ...     def extract(self, codebase_path: str) -> list[Pattern]:
        ...         # Traverse codebase, apply detectors, aggregate results
        ...         return all_patterns
        ...     def supported_framework(self) -> Framework:
        ...         return Framework.COSMOS_SDK
    """

    @abstractmethod
    def extract(self, codebase_path: str) -> list[Pattern]:
        """
        Extract all patterns from codebase.

        Traverses the codebase, applies all relevant detectors, and aggregates
        results into a comprehensive pattern list.

        Args:
            codebase_path: Absolute path to the root of the codebase to analyze

        Returns:
            List of all detected patterns across all files.
            Returns empty list if no patterns found.
            Patterns are sorted by (file_path, line_number).

        Raises:
            ConfigurationError: If codebase_path doesn't exist or is not accessible
            ExtractionError: If extraction fails due to:
                - Invalid codebase structure
                - File reading errors
                - Detector failures (with aggregated error details)

        Notes:
            - Should skip non-source files (binaries, build artifacts)
            - Should handle file reading errors gracefully (log and continue)
            - Should aggregate detector results from all files
            - May use parallelization for performance (must be thread-safe)

        Examples:
            >>> extractor = CosmosSDKExtractor()
            >>> patterns = extractor.extract("/path/to/cosmos-sdk")
            >>> len(patterns)
            147
            >>> {p.pattern_type for p in patterns}
            {PatternType.KEEPER, PatternType.MESSAGE_HANDLER, PatternType.QUERY_HANDLER}
        """
        raise NotImplementedError

    @abstractmethod
    def supported_framework(self) -> Framework:
        """
        Return the framework this extractor supports.

        Returns:
            Framework enum value

        Examples:
            >>> extractor = CosmosSDKExtractor()
            >>> extractor.supported_framework()
            <Framework.COSMOS_SDK: 'cosmos_sdk'>
        """
        raise NotImplementedError
