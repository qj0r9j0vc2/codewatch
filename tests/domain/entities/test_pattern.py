"""Tests for Pattern ABC and PatternRelation entity."""

import pytest
from abc import ABC

from codewatch.domain.entities.pattern import Pattern, PatternRelation
from codewatch.domain.enums import Framework, PatternType, RelationType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName
from codewatch.domain.exceptions import ExtractionError


class TestPatternABC:
    """Tests for Pattern abstract base class."""

    def test_cannot_instantiate_directly(self) -> None:
        """Should not be able to instantiate Pattern ABC directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Pattern(  # type: ignore
                location=PatternLocation.at_line("test.go", 10),
                confidence=ConfidenceScore(0.9),
                pattern_type=PatternType.KEEPER,
                framework=Framework.COSMOS_SDK
            )

    def test_is_abstract_base_class(self) -> None:
        """Should be an ABC."""
        assert issubclass(Pattern, ABC)

    def test_has_validate_abstract_method(self) -> None:
        """Should have validate as abstract method."""
        assert hasattr(Pattern, 'validate')
        assert getattr(Pattern.validate, '__isabstractmethod__', False)


class ConcretePattern(Pattern):
    """Concrete implementation for testing Pattern ABC."""

    def validate(self) -> None:
        """Implement abstract validate method."""
        pass


class TestPatternCommonAttributes:
    """Tests for Pattern common attributes."""

    def test_has_location_attribute(self) -> None:
        """Should have location attribute."""
        loc = PatternLocation.at_line("test.go", 42)
        pattern = ConcretePattern(
            location=loc,
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        assert pattern.location == loc

    def test_has_confidence_attribute(self) -> None:
        """Should have confidence attribute."""
        conf = ConfidenceScore(0.85)
        pattern = ConcretePattern(
            location=PatternLocation.at_line("test.go", 42),
            confidence=conf,
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        assert pattern.confidence == conf

    def test_has_pattern_type_attribute(self) -> None:
        """Should have pattern_type attribute."""
        pattern = ConcretePattern(
            location=PatternLocation.at_line("test.go", 42),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK
        )
        assert pattern.pattern_type == PatternType.MESSAGE_HANDLER

    def test_has_framework_attribute(self) -> None:
        """Should have framework attribute."""
        pattern = ConcretePattern(
            location=PatternLocation.at_line("test.go", 42),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.ETHEREUM
        )
        assert pattern.framework == Framework.ETHEREUM

    def test_kw_only_constructor(self) -> None:
        """Should require keyword arguments."""
        with pytest.raises(TypeError):
            ConcretePattern(  # type: ignore
                PatternLocation.at_line("test.go", 42),
                ConfidenceScore(0.9),
                PatternType.KEEPER,
                Framework.COSMOS_SDK
            )


class TestPatternRelationCreation:
    """Tests for PatternRelation creation."""

    def test_create_with_valid_patterns(self) -> None:
        """Should create relation between different patterns."""
        source = ConcretePattern(
            location=PatternLocation.at_line("handler.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("keeper.go", 20),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        relation = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.DEPENDS_ON,
            metadata={"reason": "requires keeper"}
        )
        assert relation.source is source
        assert relation.target is target
        assert relation.relation_type == RelationType.DEPENDS_ON
        assert relation.metadata == {"reason": "requires keeper"}

    def test_create_with_empty_metadata(self) -> None:
        """Should accept empty metadata dict."""
        source = ConcretePattern(
            location=PatternLocation.at_line("handler.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("keeper.go", 20),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        relation = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.CALLS,
            metadata={}
        )
        assert relation.metadata == {}

    def test_create_with_different_relation_types(self) -> None:
        """Should support all relation types."""
        source = ConcretePattern(
            location=PatternLocation.at_line("a.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("b.go", 20),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )

        for rel_type in [RelationType.CALLS, RelationType.DEPENDS_ON,
                         RelationType.IMPLEMENTS, RelationType.INHERITS_FROM]:
            relation = PatternRelation(
                source=source,
                target=target,
                relation_type=rel_type,
                metadata={}
            )
            assert relation.relation_type == rel_type


class TestPatternRelationValidation:
    """Tests for PatternRelation validation."""

    def test_reject_same_source_and_target(self) -> None:
        """Should reject relation where source and target are the same."""
        pattern = ConcretePattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        with pytest.raises(ExtractionError, match="source and target cannot be the same"):
            PatternRelation(
                source=pattern,
                target=pattern,
                relation_type=RelationType.CALLS,
                metadata={}
            )


class TestPatternRelationImmutability:
    """Tests for PatternRelation immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        source = ConcretePattern(
            location=PatternLocation.at_line("a.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("b.go", 20),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        relation = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.DEPENDS_ON,
            metadata={}
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            relation.relation_type = RelationType.CALLS  # type: ignore


class TestPatternRelationHashability:
    """Tests for PatternRelation hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        source = ConcretePattern(
            location=PatternLocation.at_line("a.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("b.go", 20),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        relation = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.DEPENDS_ON,
            metadata={}
        )
        hash(relation)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        source = ConcretePattern(
            location=PatternLocation.at_line("a.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        target = ConcretePattern(
            location=PatternLocation.at_line("b.go", 20),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK
        )
        rel1 = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.DEPENDS_ON,
            metadata={}
        )
        rel2 = PatternRelation(
            source=source,
            target=target,
            relation_type=RelationType.DEPENDS_ON,
            metadata={}
        )
        relations = {rel1, rel2}
        assert len(relations) == 1  # Equal values
