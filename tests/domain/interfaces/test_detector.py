"""Tests for Detector ABC interface."""

import pytest
from abc import ABC

from codewatch.domain.interfaces.detector import Detector
from codewatch.domain.entities import Pattern, KeeperPattern
from codewatch.domain.enums import Framework, PatternType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName
from codewatch.domain.exceptions import ExtractionError


class MockKeeperDetector(Detector):
    """Mock detector for testing Detector ABC."""

    def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        """Mock implementation that returns test patterns."""
        if "keeper" in source_code.lower():
            return [
                KeeperPattern(
                    location=PatternLocation.at_line(file_path, 10),
                    confidence=ConfidenceScore(0.9),
                    pattern_type=PatternType.KEEPER,
                    framework=Framework.COSMOS_SDK,
                    keeper_name=QualifiedName(package="test.keeper", name="Keeper"),
                    store_keys=("test",),
                    dependencies=()
                )
            ]
        return []

    def supported_pattern_type(self) -> PatternType:
        """Return KEEPER pattern type."""
        return PatternType.KEEPER


class MockMessageHandlerDetector(Detector):
    """Second mock detector for testing multiple detector implementations."""

    def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        """Mock implementation for message handlers."""
        return []

    def supported_pattern_type(self) -> PatternType:
        """Return MESSAGE_HANDLER pattern type."""
        return PatternType.MESSAGE_HANDLER


class TestDetectorABC:
    """Tests for Detector ABC interface."""

    def test_is_abstract_base_class(self) -> None:
        """Should be an ABC."""
        assert issubclass(Detector, ABC)

    def test_cannot_instantiate_directly(self) -> None:
        """Should not be able to instantiate Detector ABC directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Detector()  # type: ignore

    def test_has_detect_abstract_method(self) -> None:
        """Should have detect as abstract method."""
        assert hasattr(Detector, 'detect')
        assert getattr(Detector.detect, '__isabstractmethod__', False)

    def test_has_supported_pattern_type_abstract_method(self) -> None:
        """Should have supported_pattern_type as abstract method."""
        assert hasattr(Detector, 'supported_pattern_type')
        assert getattr(Detector.supported_pattern_type, '__isabstractmethod__', False)


class TestDetectorMockImplementation:
    """Tests for Detector ABC with mock implementation."""

    def test_can_create_mock_implementation(self) -> None:
        """Should be able to create concrete detector implementation."""
        detector = MockKeeperDetector()
        assert isinstance(detector, Detector)

    def test_mock_detector_conforms_to_interface(self) -> None:
        """Mock detector should conform to Detector interface."""
        detector = MockKeeperDetector()
        assert hasattr(detector, 'detect')
        assert hasattr(detector, 'supported_pattern_type')
        assert callable(detector.detect)
        assert callable(detector.supported_pattern_type)


class TestDetectorDetectMethod:
    """Tests for Detector.detect() return type (list of Pattern)."""

    def test_detect_returns_list_of_patterns(self) -> None:
        """Should return list of Pattern instances."""
        detector = MockKeeperDetector()
        source_code = "package keeper\ntype Keeper struct {}"
        patterns = detector.detect(source_code, "keeper.go")
        assert isinstance(patterns, list)
        assert all(isinstance(p, Pattern) for p in patterns)

    def test_detect_returns_empty_list_when_no_patterns(self) -> None:
        """Should return empty list when no patterns found."""
        detector = MockKeeperDetector()
        source_code = "package main"
        patterns = detector.detect(source_code, "main.go")
        assert patterns == []
        assert isinstance(patterns, list)

    def test_detect_accepts_source_code_and_file_path(self) -> None:
        """Should accept source_code and file_path parameters."""
        detector = MockKeeperDetector()
        patterns = detector.detect("package keeper", "test/keeper.go")
        assert len(patterns) == 1
        assert patterns[0].location.file_path.name == "keeper.go"

    def test_detect_patterns_have_correct_type(self) -> None:
        """Returned patterns should match supported_pattern_type."""
        detector = MockKeeperDetector()
        source_code = "package keeper\ntype Keeper struct {}"
        patterns = detector.detect(source_code, "keeper.go")
        for pattern in patterns:
            assert pattern.pattern_type == detector.supported_pattern_type()


class TestDetectorSupportedPatternType:
    """Tests for Detector.supported_pattern_type()."""

    def test_returns_pattern_type_enum(self) -> None:
        """Should return PatternType enum value."""
        detector = MockKeeperDetector()
        pattern_type = detector.supported_pattern_type()
        assert isinstance(pattern_type, PatternType)

    def test_returns_consistent_value(self) -> None:
        """Should return same value across multiple calls."""
        detector = MockKeeperDetector()
        type1 = detector.supported_pattern_type()
        type2 = detector.supported_pattern_type()
        assert type1 == type2

    def test_different_detectors_support_different_types(self) -> None:
        """Different detector implementations support different types."""
        keeper_detector = MockKeeperDetector()
        handler_detector = MockMessageHandlerDetector()
        assert keeper_detector.supported_pattern_type() == PatternType.KEEPER
        assert handler_detector.supported_pattern_type() == PatternType.MESSAGE_HANDLER
        assert keeper_detector.supported_pattern_type() != handler_detector.supported_pattern_type()


class TestMultipleDetectorImplementations:
    """Tests for multiple Detector implementations."""

    def test_can_create_multiple_detector_types(self) -> None:
        """Should support multiple detector implementations."""
        keeper_detector = MockKeeperDetector()
        handler_detector = MockMessageHandlerDetector()
        assert isinstance(keeper_detector, Detector)
        assert isinstance(handler_detector, Detector)

    def test_detectors_work_independently(self) -> None:
        """Each detector operates independently."""
        keeper_detector = MockKeeperDetector()
        handler_detector = MockMessageHandlerDetector()

        source_code = "package keeper"
        keeper_patterns = keeper_detector.detect(source_code, "keeper.go")
        handler_patterns = handler_detector.detect(source_code, "handler.go")

        # Keeper detector finds patterns in keeper code
        assert len(keeper_patterns) == 1
        # Handler detector finds nothing in keeper code
        assert len(handler_patterns) == 0

    def test_can_use_detectors_in_list(self) -> None:
        """Detectors can be stored and iterated in collections."""
        detectors: list[Detector] = [
            MockKeeperDetector(),
            MockMessageHandlerDetector()
        ]
        assert len(detectors) == 2
        for detector in detectors:
            assert isinstance(detector, Detector)
            pattern_type = detector.supported_pattern_type()
            assert isinstance(pattern_type, PatternType)


class FailingDetector(Detector):
    """Mock detector that raises ExtractionError."""

    def detect(self, source_code: str, file_path: str) -> list[Pattern]:
        """Raise ExtractionError."""
        raise ExtractionError(f"Failed to parse {file_path}")

    def supported_pattern_type(self) -> PatternType:
        """Return KEEPER type."""
        return PatternType.KEEPER


class TestDetectorErrorHandling:
    """Tests for Detector error handling."""

    def test_detector_can_raise_extraction_error(self) -> None:
        """Detector can raise ExtractionError for failures."""
        detector = FailingDetector()
        with pytest.raises(ExtractionError, match="Failed to parse"):
            detector.detect("invalid code", "test.go")
