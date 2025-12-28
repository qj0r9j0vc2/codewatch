"""Tests for PatternRepository ABC interface."""

import pytest
from abc import ABC

from codewatch.domain.interfaces.repository import PatternRepository
from codewatch.domain.entities import Pattern, KeeperPattern, HandlerPattern
from codewatch.domain.enums import Framework, PatternType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName
from codewatch.domain.exceptions import StorageError


class InMemoryPatternRepository(PatternRepository):
    """In-memory mock repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._patterns: list[Pattern] = []

    def save_patterns(self, patterns: list[Pattern]) -> None:
        """Save patterns to in-memory storage."""
        # Store copies to ensure immutability
        self._patterns.extend(patterns)

    def find_by_type(self, pattern_type: PatternType) -> list[Pattern]:
        """Find patterns by type."""
        return [p for p in self._patterns if p.pattern_type == pattern_type]

    def execute_query(self, query: str) -> list[Pattern]:
        """Execute mock query (returns all patterns for simplicity)."""
        if "error" in query:
            raise StorageError(f"Query execution failed: {query}")
        return list(self._patterns)


class TestPatternRepositoryABC:
    """Tests for PatternRepository ABC interface."""

    def test_is_abstract_base_class(self) -> None:
        """Should be an ABC."""
        assert issubclass(PatternRepository, ABC)

    def test_cannot_instantiate_directly(self) -> None:
        """Should not be able to instantiate PatternRepository ABC directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PatternRepository()  # type: ignore

    def test_has_save_patterns_abstract_method(self) -> None:
        """Should have save_patterns as abstract method."""
        assert hasattr(PatternRepository, 'save_patterns')
        assert getattr(PatternRepository.save_patterns, '__isabstractmethod__', False)

    def test_has_find_by_type_abstract_method(self) -> None:
        """Should have find_by_type as abstract method."""
        assert hasattr(PatternRepository, 'find_by_type')
        assert getattr(PatternRepository.find_by_type, '__isabstractmethod__', False)

    def test_has_execute_query_abstract_method(self) -> None:
        """Should have execute_query as abstract method."""
        assert hasattr(PatternRepository, 'execute_query')
        assert getattr(PatternRepository.execute_query, '__isabstractmethod__', False)


class TestPatternRepositoryMockImplementation:
    """Tests for PatternRepository ABC with in-memory mock."""

    def test_can_create_mock_implementation(self) -> None:
        """Should be able to create concrete repository implementation."""
        repo = InMemoryPatternRepository()
        assert isinstance(repo, PatternRepository)

    def test_mock_repository_conforms_to_interface(self) -> None:
        """Mock repository should conform to PatternRepository interface."""
        repo = InMemoryPatternRepository()
        assert hasattr(repo, 'save_patterns')
        assert hasattr(repo, 'find_by_type')
        assert hasattr(repo, 'execute_query')
        assert callable(repo.save_patterns)
        assert callable(repo.find_by_type)
        assert callable(repo.execute_query)


class TestPatternRepositorySavePatterns:
    """Tests for PatternRepository.save_patterns()."""

    def test_can_save_patterns(self) -> None:
        """Should save patterns to repository."""
        repo = InMemoryPatternRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        repo.save_patterns([keeper])
        # Verify saved by retrieving
        patterns = repo.find_by_type(PatternType.KEEPER)
        assert len(patterns) == 1

    def test_save_patterns_accepts_list(self) -> None:
        """Should accept list of patterns."""
        repo = InMemoryPatternRepository()
        keeper1 = KeeperPattern(
            location=PatternLocation.at_line("keeper1.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper1", name="Keeper"),
            store_keys=("test1",),
            dependencies=()
        )
        keeper2 = KeeperPattern(
            location=PatternLocation.at_line("keeper2.go", 20),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper2", name="Keeper"),
            store_keys=("test2",),
            dependencies=()
        )
        repo.save_patterns([keeper1, keeper2])
        patterns = repo.find_by_type(PatternType.KEEPER)
        assert len(patterns) == 2

    def test_save_patterns_handles_empty_list(self) -> None:
        """Should handle empty list gracefully (no-op)."""
        repo = InMemoryPatternRepository()
        repo.save_patterns([])  # Should not raise
        patterns = repo.execute_query("all")
        assert patterns == []


class TestPatternRepositoryFindByType:
    """Tests for PatternRepository.find_by_type() returns list."""

    def test_find_by_type_returns_list(self) -> None:
        """Should return list (not generator)."""
        repo = InMemoryPatternRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        repo.save_patterns([keeper])
        patterns = repo.find_by_type(PatternType.KEEPER)
        assert isinstance(patterns, list)

    def test_find_by_type_returns_correct_type(self) -> None:
        """Should return only patterns of specified type."""
        repo = InMemoryPatternRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 20),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="test.handler", name="Handler"),
            handler_type="message",
            message_type=QualifiedName(package="test.types", name="MsgTest"),
            keeper_dependencies=()
        )
        repo.save_patterns([keeper, handler])

        keepers = repo.find_by_type(PatternType.KEEPER)
        assert len(keepers) == 1
        assert all(p.pattern_type == PatternType.KEEPER for p in keepers)

        handlers = repo.find_by_type(PatternType.MESSAGE_HANDLER)
        assert len(handlers) == 1
        assert all(p.pattern_type == PatternType.MESSAGE_HANDLER for p in handlers)


class TestPatternRepositoryExecuteQuery:
    """Tests for PatternRepository.execute_query() returns list."""

    def test_execute_query_returns_list(self) -> None:
        """Should return list (not generator)."""
        repo = InMemoryPatternRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        repo.save_patterns([keeper])
        patterns = repo.execute_query("all")
        assert isinstance(patterns, list)

    def test_execute_query_accepts_query_string(self) -> None:
        """Should accept query string parameter."""
        repo = InMemoryPatternRepository()
        patterns = repo.execute_query("MATCH (p:Pattern) RETURN p")
        assert isinstance(patterns, list)


class TestPatternRepositoryEmptyResults:
    """Tests for PatternRepository empty results (empty list)."""

    def test_find_by_type_returns_empty_list_when_no_matches(self) -> None:
        """Should return empty list when no patterns match."""
        repo = InMemoryPatternRepository()
        patterns = repo.find_by_type(PatternType.KEEPER)
        assert patterns == []
        assert isinstance(patterns, list)

    def test_execute_query_returns_empty_list_when_no_matches(self) -> None:
        """Should return empty list when query has no matches."""
        repo = InMemoryPatternRepository()
        patterns = repo.execute_query("no matches")
        assert patterns == []
        assert isinstance(patterns, list)

    def test_empty_results_are_not_none(self) -> None:
        """Empty results should be empty list, not None."""
        repo = InMemoryPatternRepository()
        patterns = repo.find_by_type(PatternType.KEEPER)
        assert patterns is not None
        assert patterns == []


class TestPatternRepositoryMultiplePatternTypes:
    """Tests for PatternRepository with multiple pattern types."""

    def test_repository_handles_multiple_pattern_types(self) -> None:
        """Repository should handle different pattern types."""
        repo = InMemoryPatternRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 20),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="test.handler", name="Handler"),
            handler_type="message",
            message_type=QualifiedName(package="test.types", name="MsgTest"),
            keeper_dependencies=()
        )
        repo.save_patterns([keeper, handler])

        all_patterns = repo.execute_query("all")
        assert len(all_patterns) == 2

        keepers = repo.find_by_type(PatternType.KEEPER)
        handlers = repo.find_by_type(PatternType.MESSAGE_HANDLER)
        assert len(keepers) == 1
        assert len(handlers) == 1

    def test_repository_preserves_pattern_types(self) -> None:
        """Repository should preserve pattern type information."""
        repo = InMemoryPatternRepository()
        patterns_to_save = [
            KeeperPattern(
                location=PatternLocation.at_line("keeper.go", 10),
                confidence=ConfidenceScore(0.9),
                pattern_type=PatternType.KEEPER,
                framework=Framework.COSMOS_SDK,
                keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
                store_keys=("test",),
                dependencies=()
            ),
            HandlerPattern(
                location=PatternLocation.at_line("handler.go", 20),
                confidence=ConfidenceScore(0.85),
                pattern_type=PatternType.MESSAGE_HANDLER,
                framework=Framework.COSMOS_SDK,
                handler_name=QualifiedName(package="test.handler", name="Handler"),
                handler_type="message",
                message_type=QualifiedName(package="test.types", name="MsgTest"),
                keeper_dependencies=()
            )
        ]
        repo.save_patterns(patterns_to_save)

        retrieved = repo.execute_query("all")
        assert len(retrieved) == 2
        assert isinstance(retrieved[0], Pattern)
        assert isinstance(retrieved[1], Pattern)


class FailingRepository(PatternRepository):
    """Mock repository that raises StorageError."""

    def save_patterns(self, patterns: list[Pattern]) -> None:
        """Raise StorageError."""
        raise StorageError("Failed to connect to storage backend")

    def find_by_type(self, pattern_type: PatternType) -> list[Pattern]:
        """Raise StorageError."""
        raise StorageError("Failed to retrieve patterns")

    def execute_query(self, query: str) -> list[Pattern]:
        """Raise StorageError."""
        raise StorageError(f"Query execution failed: {query}")


class TestPatternRepositoryErrorHandling:
    """Tests for PatternRepository error handling."""

    def test_save_patterns_can_raise_storage_error(self) -> None:
        """save_patterns can raise StorageError."""
        repo = FailingRepository()
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        with pytest.raises(StorageError, match="Failed to connect"):
            repo.save_patterns([keeper])

    def test_find_by_type_can_raise_storage_error(self) -> None:
        """find_by_type can raise StorageError."""
        repo = FailingRepository()
        with pytest.raises(StorageError, match="Failed to retrieve"):
            repo.find_by_type(PatternType.KEEPER)

    def test_execute_query_can_raise_storage_error(self) -> None:
        """execute_query can raise StorageError."""
        repo = FailingRepository()
        with pytest.raises(StorageError, match="Query execution failed"):
            repo.execute_query("invalid query")
