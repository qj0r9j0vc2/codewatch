"""
PatternRepository interface for pattern persistence.

This module provides the abstract PatternRepository interface for
storing and retrieving patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities import Pattern
from ..enums import PatternType


class PatternRepository(ABC):
    """
    Abstract interface for pattern persistence.

    Repositories handle storing and retrieving patterns. Implementations
    provide different storage backends (in-memory, file-based, graph database).

    Contract guarantees:
    - All methods return lists (not generators) to prevent exhaustion issues
    - All methods are thread-safe
    - Patterns are immutable (repository stores copies, not references)

    Examples:
        >>> class InMemoryPatternRepository(PatternRepository):
        ...     def save_patterns(self, patterns: list[Pattern]) -> None:
        ...         self._store.extend(patterns)
        ...     def find_by_type(self, pattern_type: PatternType) -> list[Pattern]:
        ...         return [p for p in self._store if p.pattern_type == pattern_type]
        ...     def execute_query(self, query: str) -> list[Pattern]:
        ...         # Execute implementation-specific query
        ...         return matching_patterns
    """

    @abstractmethod
    def save_patterns(self, patterns: list[Pattern]) -> None:
        """
        Persist patterns to storage.

        Stores all provided patterns. Existing patterns with same identity
        (location + type) may be overwritten depending on implementation.

        Args:
            patterns: List of patterns to save

        Raises:
            StorageError: If persistence fails due to:
                - Storage backend connection issues
                - Serialization errors
                - Permission issues
                Should include details about what failed.

        Notes:
            - Implementations must handle empty list gracefully (no-op)
            - Patterns are stored immutably (implementation stores copies)
            - May batch operations for performance
            - Should be atomic where possible (all or nothing)

        Examples:
            >>> repo = InMemoryPatternRepository()
            >>> repo.save_patterns([keeper1, keeper2, handler1])
            # Patterns now stored in repository
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_type(self, pattern_type: PatternType) -> list[Pattern]:
        """
        Retrieve all patterns of a specific type.

        Args:
            pattern_type: Pattern type to filter by

        Returns:
            List of patterns matching the type.
            Returns empty list if no matches found.
            List (not generator) to prevent exhaustion issues.

        Raises:
            StorageError: If retrieval fails due to:
                - Storage backend connection issues
                - Deserialization errors
                Should include details about what failed.

        Notes:
            - Result is a new list (not a view or generator)
            - Patterns in result are independent of stored instances
            - No ordering guaranteed unless implementation specifies

        Examples:
            >>> repo = InMemoryPatternRepository()
            >>> keepers = repo.find_by_type(PatternType.KEEPER)
            >>> len(keepers)
            5
            >>> all(p.pattern_type == PatternType.KEEPER for p in keepers)
            True
        """
        raise NotImplementedError

    @abstractmethod
    def execute_query(self, query: str) -> list[Pattern]:
        """
        Execute custom query and return matching patterns.

        Args:
            query: Implementation-specific query string.
                   - For Cypher backend: Cypher query
                   - For SQL backend: SQL query
                   - For in-memory: JSONPath or similar

        Returns:
            List of patterns matching the query.
            Returns empty list if no matches found.
            List (not generator) to prevent exhaustion issues.

        Raises:
            StorageError: If query execution fails due to:
                - Invalid query syntax
                - Storage backend errors
                - Query timeout
                Should include query and error details.

        Notes:
            - Query language is implementation-specific
            - Implementations should document supported query syntax
            - Result is always a list (not generator)
            - No ordering guaranteed unless query specifies

        Examples:
            >>> repo = CypherPatternRepository()
            >>> query = "MATCH (p:Pattern {framework: 'cosmos_sdk'}) RETURN p"
            >>> patterns = repo.execute_query(query)
            >>> all(p.framework == Framework.COSMOS_SDK for p in patterns)
            True
        """
        raise NotImplementedError
