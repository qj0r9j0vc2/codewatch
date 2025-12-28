"""Tests for domain enumerations."""

import pytest

from codewatch.domain.enums import Framework, PatternType, RelationType


class TestFramework:
    """Tests for Framework enum."""

    def test_framework_values_defined(self) -> None:
        """Should define all framework values."""
        assert Framework.COSMOS_SDK.value == "cosmos_sdk"
        assert Framework.ETHEREUM.value == "ethereum"
        assert Framework.POLKADOT.value == "polkadot"

    def test_framework_string_representation(self) -> None:
        """Should have string representation."""
        assert str(Framework.COSMOS_SDK) == "cosmos_sdk"
        assert str(Framework.ETHEREUM) == "ethereum"

    def test_framework_equality(self) -> None:
        """Should support equality comparison."""
        assert Framework.COSMOS_SDK == Framework.COSMOS_SDK
        assert Framework.COSMOS_SDK != Framework.ETHEREUM

    def test_framework_iteration(self) -> None:
        """Should be iterable."""
        frameworks = list(Framework)
        assert Framework.COSMOS_SDK in frameworks
        assert Framework.ETHEREUM in frameworks
        assert Framework.POLKADOT in frameworks

    def test_framework_membership(self) -> None:
        """Should support membership testing."""
        assert "cosmos_sdk" in [f.value for f in Framework]


class TestPatternType:
    """Tests for PatternType enum."""

    def test_pattern_type_values_defined(self) -> None:
        """Should define all pattern type values."""
        assert PatternType.KEEPER.value == "keeper"
        assert PatternType.MESSAGE_HANDLER.value == "message_handler"
        assert PatternType.QUERY_HANDLER.value == "query_handler"
        assert PatternType.VALIDATOR.value == "validator"

    def test_pattern_type_string_representation(self) -> None:
        """Should have string representation."""
        assert str(PatternType.KEEPER) == "keeper"
        assert str(PatternType.MESSAGE_HANDLER) == "message_handler"

    def test_pattern_type_equality(self) -> None:
        """Should support equality comparison."""
        assert PatternType.KEEPER == PatternType.KEEPER
        assert PatternType.KEEPER != PatternType.MESSAGE_HANDLER

    def test_pattern_type_iteration(self) -> None:
        """Should be iterable."""
        types = list(PatternType)
        assert PatternType.KEEPER in types
        assert PatternType.MESSAGE_HANDLER in types
        assert PatternType.QUERY_HANDLER in types
        assert PatternType.VALIDATOR in types

    def test_pattern_type_serialization(self) -> None:
        """Should serialize to string value."""
        assert PatternType.KEEPER.value == "keeper"


class TestRelationType:
    """Tests for RelationType enum."""

    def test_relation_type_values_defined(self) -> None:
        """Should define all relation type values."""
        assert RelationType.CALLS.value == "calls"
        assert RelationType.DEPENDS_ON.value == "depends_on"
        assert RelationType.IMPLEMENTS.value == "implements"
        assert RelationType.INHERITS_FROM.value == "inherits_from"

    def test_relation_type_string_representation(self) -> None:
        """Should have string representation."""
        assert str(RelationType.CALLS) == "calls"
        assert str(RelationType.DEPENDS_ON) == "depends_on"

    def test_relation_type_equality(self) -> None:
        """Should support equality comparison."""
        assert RelationType.CALLS == RelationType.CALLS
        assert RelationType.CALLS != RelationType.DEPENDS_ON

    def test_relation_type_iteration(self) -> None:
        """Should be iterable."""
        types = list(RelationType)
        assert RelationType.CALLS in types
        assert RelationType.DEPENDS_ON in types
        assert RelationType.IMPLEMENTS in types
        assert RelationType.INHERITS_FROM in types
