"""
Pattern entities for representing detected code patterns.

This module provides the abstract Pattern base class and PatternRelation
for representing relationships between patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..enums import Framework, PatternType, RelationType
from ..exceptions import ExtractionError
from ..value_objects import ConfidenceScore, PatternLocation


@dataclass(frozen=True, slots=True, kw_only=True)
class Pattern(ABC):
    """
    Abstract base for all blockchain code patterns.

    All pattern subclasses must provide location, confidence, type, and framework.
    Subclasses must implement the validate() method for pattern-specific validation.

    Attributes:
        location: Source code location of the pattern
        confidence: Detection confidence score [0.0, 1.0]
        pattern_type: Type of pattern (KEEPER, MESSAGE_HANDLER, etc.)
        framework: Blockchain framework (COSMOS_SDK, ETHEREUM, etc.)

    Examples:
        >>> class ConcretePattern(Pattern):
        ...     def validate(self) -> None:
        ...         pass
        >>> pattern = ConcretePattern(
        ...     location=PatternLocation.at_line("keeper.go", 142),
        ...     confidence=ConfidenceScore(0.95),
        ...     pattern_type=PatternType.KEEPER,
        ...     framework=Framework.COSMOS_SDK
        ... )
    """

    location: PatternLocation
    confidence: ConfidenceScore
    pattern_type: PatternType
    framework: Framework

    @abstractmethod
    def validate(self) -> None:
        """
        Validate pattern-specific constraints.

        Raises:
            ExtractionError: If validation fails
        """
        pass


@dataclass(frozen=True, slots=True, kw_only=True)
class PatternRelation:
    """
    Relationship between two patterns.

    Represents dependencies, calls, inheritance, and other relationships
    between detected code patterns.

    Attributes:
        source: Source pattern (the one initiating the relationship)
        target: Target pattern (the one being related to)
        relation_type: Type of relationship (CALLS, DEPENDS_ON, etc.)
        metadata: Additional relationship metadata (must be JSON-serializable)

    Raises:
        ExtractionError: If source and target are the same pattern

    Examples:
        >>> relation = PatternRelation(
        ...     source=handler_pattern,
        ...     target=keeper_pattern,
        ...     relation_type=RelationType.DEPENDS_ON,
        ...     metadata={"reason": "requires bank keeper for balance checks"}
        ... )

    Note:
        metadata dict values should be JSON-serializable primitives
        (str, int, float, bool, None, list, dict) for future persistence.
    """

    source: Pattern
    target: Pattern
    relation_type: RelationType
    metadata: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate relation constraints."""
        # Validate: Source and target must be different patterns
        if self.source is self.target:
            raise ExtractionError(
                "Pattern relation source and target cannot be the same pattern"
            )
