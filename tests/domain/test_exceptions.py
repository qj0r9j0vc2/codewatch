"""Tests for domain exception hierarchy."""

import pytest

from codewatch.domain.exceptions import (
    CodewatchError,
    ConfigurationError,
    ExtractionError,
    InvalidConfidenceScoreError,
    InvalidLocationError,
    InvalidQualifiedNameError,
    StorageError,
    ValueObjectError,
)


class TestCodewatchError:
    """Tests for CodewatchError base exception."""

    def test_can_instantiate_with_message(self) -> None:
        """Should instantiate with error message."""
        error = CodewatchError("Test error")
        assert str(error) == "Test error"

    def test_is_exception(self) -> None:
        """Should be an Exception subclass."""
        error = CodewatchError("Test")
        assert isinstance(error, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """Should be raisable and catchable."""
        with pytest.raises(CodewatchError, match="Test error"):
            raise CodewatchError("Test error")


class TestValueObjectError:
    """Tests for ValueObjectError."""

    def test_inherits_from_codewatch_error(self) -> None:
        """Should inherit from CodewatchError."""
        error = ValueObjectError("Test")
        assert isinstance(error, CodewatchError)

    def test_inherits_from_value_error(self) -> None:
        """Should inherit from ValueError."""
        error = ValueObjectError("Test")
        assert isinstance(error, ValueError)

    def test_can_be_caught_polymorphically(self) -> None:
        """Should be catchable via CodewatchError."""
        with pytest.raises(CodewatchError):
            raise ValueObjectError("Test error")


class TestInvalidLocationError:
    """Tests for InvalidLocationError."""

    def test_inherits_from_value_object_error(self) -> None:
        """Should inherit from ValueObjectError."""
        error = InvalidLocationError("Test")
        assert isinstance(error, ValueObjectError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Line number must be positive, got -5"
        error = InvalidLocationError(msg)
        assert str(error) == msg

    def test_can_be_caught_as_codewatch_error(self) -> None:
        """Should be catchable via CodewatchError."""
        with pytest.raises(CodewatchError):
            raise InvalidLocationError("Test")


class TestInvalidConfidenceScoreError:
    """Tests for InvalidConfidenceScoreError."""

    def test_inherits_from_value_object_error(self) -> None:
        """Should inherit from ValueObjectError."""
        error = InvalidConfidenceScoreError("Test")
        assert isinstance(error, ValueObjectError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Confidence score must be between 0.0 and 1.0, got 1.500000"
        error = InvalidConfidenceScoreError(msg)
        assert str(error) == msg


class TestInvalidQualifiedNameError:
    """Tests for InvalidQualifiedNameError."""

    def test_inherits_from_value_object_error(self) -> None:
        """Should inherit from ValueObjectError."""
        error = InvalidQualifiedNameError("Test")
        assert isinstance(error, ValueObjectError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Qualified name cannot contain consecutive dots: 'cosmos..bank'"
        error = InvalidQualifiedNameError(msg)
        assert str(error) == msg


class TestExtractionError:
    """Tests for ExtractionError."""

    def test_inherits_from_codewatch_error(self) -> None:
        """Should inherit from CodewatchError."""
        error = ExtractionError("Test")
        assert isinstance(error, CodewatchError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Failed to parse Go source file 'keeper.go' at line 42"
        error = ExtractionError(msg)
        assert str(error) == msg

    def test_can_include_context(self) -> None:
        """Should support error context."""
        try:
            raise ValueError("Parse error")
        except ValueError as e:
            extraction_error = ExtractionError(f"Pattern detection failed: {e}")
            assert "Parse error" in str(extraction_error)


class TestStorageError:
    """Tests for StorageError."""

    def test_inherits_from_codewatch_error(self) -> None:
        """Should inherit from CodewatchError."""
        error = StorageError("Test")
        assert isinstance(error, CodewatchError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Failed to save patterns to database"
        error = StorageError(msg)
        assert str(error) == msg


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_inherits_from_codewatch_error(self) -> None:
        """Should inherit from CodewatchError."""
        error = ConfigurationError("Test")
        assert isinstance(error, CodewatchError)

    def test_preserves_error_message(self) -> None:
        """Should preserve error message."""
        msg = "Invalid configuration: codebase_path does not exist"
        error = ConfigurationError(msg)
        assert str(error) == msg


class TestExceptionHierarchy:
    """Tests for exception hierarchy relationships."""

    def test_all_exceptions_catchable_via_base(self) -> None:
        """Should be able to catch all exceptions via CodewatchError."""
        exceptions = [
            ValueObjectError("test"),
            InvalidLocationError("test"),
            InvalidConfidenceScoreError("test"),
            InvalidQualifiedNameError("test"),
            ExtractionError("test"),
            StorageError("test"),
            ConfigurationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, CodewatchError)

    def test_value_object_errors_catchable_via_value_error(self) -> None:
        """Should be able to catch value object errors via ValueError."""
        value_object_errors = [
            ValueObjectError("test"),
            InvalidLocationError("test"),
            InvalidConfidenceScoreError("test"),
            InvalidQualifiedNameError("test"),
        ]

        for exc in value_object_errors:
            assert isinstance(exc, ValueError)
