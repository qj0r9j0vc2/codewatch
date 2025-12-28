"""
KeeperPattern entity for Cosmos SDK Keeper patterns.

This module provides the KeeperPattern entity for representing
Cosmos SDK Keepers with their store keys and dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import ExtractionError
from ..value_objects import QualifiedName
from .pattern import Pattern


@dataclass(frozen=True, slots=True, kw_only=True)
class KeeperPattern(Pattern):
    """
    Cosmos SDK Keeper pattern.

    Keepers manage module state and business logic in Cosmos SDK.
    Must have at least one store key to be considered valid.

    Attributes:
        keeper_name: Fully qualified name of the keeper
        store_keys: Tuple of store keys the keeper accesses
        dependencies: Tuple of other keepers this keeper depends on

    Raises:
        ExtractionError: If validation fails (e.g., no store keys)

    Examples:
        >>> keeper = KeeperPattern(
        ...     location=PatternLocation.at_line("keeper.go", 142),
        ...     confidence=ConfidenceScore(0.95),
        ...     pattern_type=PatternType.KEEPER,
        ...     framework=Framework.COSMOS_SDK,
        ...     keeper_name=QualifiedName("cosmos.bank.keeper.Keeper"),
        ...     store_keys=("bank", "supply"),
        ...     dependencies=(QualifiedName("cosmos.auth.keeper.AccountKeeper"),)
        ... )
    """

    keeper_name: QualifiedName
    store_keys: tuple[str, ...]
    dependencies: tuple[QualifiedName, ...]

    def validate(self) -> None:
        """
        Validate keeper-specific constraints.

        Raises:
            ExtractionError: If keeper has no store keys
        """
        # Keeper must have at least one store key
        if not self.store_keys:
            raise ExtractionError(
                f"Keeper '{self.keeper_name}' must have at least one store key"
            )

        # All dependencies must be valid qualified names (already validated by QualifiedName)
        # No additional validation needed beyond type checking
