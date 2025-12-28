"""
Domain exception hierarchy for the Codewatch blockchain code analysis system.

This module defines a typed exception hierarchy with CodewatchError as the base
and specific subtypes for different error categories.

Example:
    >>> try:
    ...     raise ExtractionError("Failed to parse source code")
    ... except CodewatchError as e:
    ...     print(f"Domain error: {e}")
    Domain error: Failed to parse source code
"""


class CodewatchError(Exception):
    """
    Base exception for all Codewatch errors.

    All domain-specific exceptions inherit from this class, enabling
    polymorphic exception handling.
    """

    pass


class ValueObjectError(CodewatchError, ValueError):
    """
    Base exception for value object validation errors.

    Inherits from both CodewatchError (for domain error handling) and
    ValueError (for Python built-in compatibility).
    """

    pass


class InvalidLocationError(ValueObjectError):
    """
    Raised when PatternLocation validation fails.

    Examples:
        Negative line numbers, invalid column offsets, empty file paths.
    """

    pass


class InvalidConfidenceScoreError(ValueObjectError):
    """
    Raised when ConfidenceScore validation fails.

    Examples:
        Scores outside the range [0.0, 1.0].
    """

    pass


class InvalidQualifiedNameError(ValueObjectError):
    """
    Raised when QualifiedName validation fails.

    Examples:
        Empty names, consecutive dots, invalid identifier format.
    """

    pass


class ExtractionError(CodewatchError):
    """
    Pattern extraction failures.

    Raised when pattern detection or code analysis fails.

    Examples:
        Parsing errors, invalid source code, detector failures.
    """

    pass


class StorageError(CodewatchError):
    """
    Repository operation failures.

    Raised when pattern persistence or retrieval fails.

    Examples:
        Database connection errors, serialization failures.
    """

    pass


class ConfigurationError(CodewatchError):
    """
    Configuration validation failures.

    Raised when system configuration is invalid.

    Examples:
        Missing codebase paths, invalid settings.
    """

    pass
