"""Tests for Extractor ABC interface."""

import pytest
from abc import ABC

from codewatch.domain.interfaces.extractor import Extractor
from codewatch.domain.interfaces.detector import Detector
from codewatch.domain.entities import Pattern, KeeperPattern
from codewatch.domain.enums import Framework, PatternType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName
from codewatch.domain.exceptions import ConfigurationError, ExtractionError


class MockDetector(Detector):
    """Mock detector for testing."""

    def __init__(self, patterns_to_return: list[Pattern]) -> None:
        """Initialize with patterns to return."""
        self._patterns = patterns_to_return

    def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        """Return mock patterns."""
        return self._patterns

    def supported_pattern_type(self) -> PatternType:
        """Return KEEPER type."""
        return PatternType.KEEPER


class MockCosmosExtractor(Extractor):
    """Mock extractor for Cosmos SDK."""

    def __init__(self, detectors: list[Detector] | None = None) -> None:
        """Initialize with optional detectors."""
        self._detectors = detectors or []

    def extract(self, codebase_path: str) -> list[Pattern]:
        """Mock extraction that aggregates detector results."""
        # Simulate simple extraction
        all_patterns: list[Pattern] = []
        for detector in self._detectors:
            patterns = detector.detect("mock code", f"{codebase_path}/file.go")
            all_patterns.extend(patterns)
        return all_patterns

    def supported_framework(self) -> Framework:
        """Return COSMOS_SDK framework."""
        return Framework.COSMOS_SDK


class MockEthereumExtractor(Extractor):
    """Mock extractor for Ethereum."""

    def extract(self, codebase_path: str) -> list[Pattern]:
        """Mock extraction returning empty list."""
        return []

    def supported_framework(self) -> Framework:
        """Return ETHEREUM framework."""
        return Framework.ETHEREUM


class TestExtractorABC:
    """Tests for Extractor ABC interface."""

    def test_is_abstract_base_class(self) -> None:
        """Should be an ABC."""
        assert issubclass(Extractor, ABC)

    def test_cannot_instantiate_directly(self) -> None:
        """Should not be able to instantiate Extractor ABC directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Extractor()  # type: ignore

    def test_has_extract_abstract_method(self) -> None:
        """Should have extract as abstract method."""
        assert hasattr(Extractor, 'extract')
        assert getattr(Extractor.extract, '__isabstractmethod__', False)

    def test_has_supported_framework_abstract_method(self) -> None:
        """Should have supported_framework as abstract method."""
        assert hasattr(Extractor, 'supported_framework')
        assert getattr(Extractor.supported_framework, '__isabstractmethod__', False)


class TestExtractorMockImplementation:
    """Tests for Extractor ABC with mock implementation."""

    def test_can_create_mock_implementation(self) -> None:
        """Should be able to create concrete extractor implementation."""
        extractor = MockCosmosExtractor()
        assert isinstance(extractor, Extractor)

    def test_mock_extractor_conforms_to_interface(self) -> None:
        """Mock extractor should conform to Extractor interface."""
        extractor = MockCosmosExtractor()
        assert hasattr(extractor, 'extract')
        assert hasattr(extractor, 'supported_framework')
        assert callable(extractor.extract)
        assert callable(extractor.supported_framework)


class TestExtractorExtractMethod:
    """Tests for Extractor.extract() return type (list of Pattern)."""

    def test_extract_returns_list_of_patterns(self) -> None:
        """Should return list of Pattern instances."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore(0.9),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
            store_keys=("test",),
            dependencies=()
        )
        detector = MockDetector([keeper])
        extractor = MockCosmosExtractor([detector])
        patterns = extractor.extract("/path/to/codebase")
        assert isinstance(patterns, list)
        assert all(isinstance(p, Pattern) for p in patterns)

    def test_extract_returns_empty_list_when_no_patterns(self) -> None:
        """Should return empty list when no patterns found."""
        extractor = MockCosmosExtractor([])
        patterns = extractor.extract("/path/to/codebase")
        assert patterns == []
        assert isinstance(patterns, list)

    def test_extract_accepts_codebase_path(self) -> None:
        """Should accept codebase_path parameter."""
        extractor = MockCosmosExtractor()
        patterns = extractor.extract("/some/path")
        assert isinstance(patterns, list)


class TestExtractorSupportedFramework:
    """Tests for Extractor.supported_framework()."""

    def test_returns_framework_enum(self) -> None:
        """Should return Framework enum value."""
        extractor = MockCosmosExtractor()
        framework = extractor.supported_framework()
        assert isinstance(framework, Framework)

    def test_returns_consistent_value(self) -> None:
        """Should return same value across multiple calls."""
        extractor = MockCosmosExtractor()
        fw1 = extractor.supported_framework()
        fw2 = extractor.supported_framework()
        assert fw1 == fw2

    def test_different_extractors_support_different_frameworks(self) -> None:
        """Different extractor implementations support different frameworks."""
        cosmos_extractor = MockCosmosExtractor()
        ethereum_extractor = MockEthereumExtractor()
        assert cosmos_extractor.supported_framework() == Framework.COSMOS_SDK
        assert ethereum_extractor.supported_framework() == Framework.ETHEREUM
        assert cosmos_extractor.supported_framework() != ethereum_extractor.supported_framework()


class TestExtractorComposingDetectors:
    """Tests for Extractor composing multiple Detectors."""

    def test_extractor_can_compose_multiple_detectors(self) -> None:
        """Extractor can coordinate multiple detectors."""
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
        detector1 = MockDetector([keeper1])
        detector2 = MockDetector([keeper2])
        extractor = MockCosmosExtractor([detector1, detector2])

        patterns = extractor.extract("/path/to/codebase")
        assert len(patterns) == 2
        assert keeper1 in patterns
        assert keeper2 in patterns

    def test_extractor_aggregates_detector_results(self) -> None:
        """Extractor aggregates results from all detectors."""
        patterns_set1 = [
            KeeperPattern(
                location=PatternLocation.at_line("a.go", 10),
                confidence=ConfidenceScore(0.9),
                pattern_type=PatternType.KEEPER,
                framework=Framework.COSMOS_SDK,
                keeper_name=QualifiedName(package="a", name="Keeper"),
                store_keys=("a",),
                dependencies=()
            )
        ]
        patterns_set2 = [
            KeeperPattern(
                location=PatternLocation.at_line("b.go", 20),
                confidence=ConfidenceScore(0.85),
                pattern_type=PatternType.KEEPER,
                framework=Framework.COSMOS_SDK,
                keeper_name=QualifiedName(package="b", name="Keeper"),
                store_keys=("b",),
                dependencies=()
            )
        ]
        detector1 = MockDetector(patterns_set1)
        detector2 = MockDetector(patterns_set2)
        extractor = MockCosmosExtractor([detector1, detector2])

        all_patterns = extractor.extract("/codebase")
        assert len(all_patterns) == 2

    def test_extractor_works_with_no_detectors(self) -> None:
        """Extractor can work with empty detector list."""
        extractor = MockCosmosExtractor([])
        patterns = extractor.extract("/codebase")
        assert patterns == []


class FailingExtractor(Extractor):
    """Mock extractor that raises ConfigurationError."""

    def extract(self, codebase_path: str) -> list[Pattern]:
        """Raise ConfigurationError."""
        raise ConfigurationError(f"Codebase path '{codebase_path}' does not exist")

    def supported_framework(self) -> Framework:
        """Return COSMOS_SDK."""
        return Framework.COSMOS_SDK


class TestExtractorErrorHandling:
    """Tests for Extractor error handling."""

    def test_extractor_can_raise_configuration_error(self) -> None:
        """Extractor can raise ConfigurationError for invalid paths."""
        extractor = FailingExtractor()
        with pytest.raises(ConfigurationError, match="does not exist"):
            extractor.extract("/nonexistent/path")
