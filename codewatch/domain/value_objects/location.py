"""
PatternLocation value object for representing source code locations.

This module provides an immutable value object for source code locations
with file path, line numbers, and column offsets.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from ..exceptions import InvalidLocationError


@dataclass(frozen=True, slots=True)
class PatternLocation:
    """
    Source code location.

    Represents a position in source code with file path, line/column coordinates.
    All fields are validated on construction.

    Attributes:
        file_path: Path to source file (absolute or relative)
        line_start: Starting line number (1-indexed, must be positive)
        line_end: Ending line number (1-indexed, must be >= line_start)
        column_start: Starting column offset (0-indexed, must be non-negative)
        column_end: Ending column offset (0-indexed, must be >= column_start on same line)

    Raises:
        InvalidLocationError: If validation fails

    Examples:
        >>> loc = PatternLocation(Path("keeper.go"), 142, 158, 0, 4)
        >>> str(loc)
        'keeper.go:142:0-158:4'

        >>> loc = PatternLocation.at_line("test.go", 42)
        >>> str(loc)
        'test.go:42:0-0'
    """

    file_path: Path
    line_start: int
    line_end: int
    column_start: int
    column_end: int

    def __post_init__(self) -> None:
        """Validate location invariants."""
        # Normalize: Convert string paths to Path objects
        if isinstance(self.file_path, str):
            object.__setattr__(self, 'file_path', Path(self.file_path))

        # Validate: Line numbers must be positive (1-indexed)
        if self.line_start < 1:
            raise InvalidLocationError(
                f"Line start must be positive, got {self.line_start}"
            )
        if self.line_end < 1:
            raise InvalidLocationError(
                f"Line end must be positive, got {self.line_end}"
            )

        # Validate: End >= Start
        if self.line_end < self.line_start:
            raise InvalidLocationError(
                f"Line end ({self.line_end}) must be >= line start ({self.line_start})"
            )

        # Validate: Column offsets must be non-negative (0-indexed)
        if self.column_start < 0:
            raise InvalidLocationError(
                f"Column start must be non-negative, got {self.column_start}"
            )
        if self.column_end < 0:
            raise InvalidLocationError(
                f"Column end must be non-negative, got {self.column_end}"
            )

        # Validate: If single line, column_end >= column_start
        if self.line_start == self.line_end and self.column_end < self.column_start:
            raise InvalidLocationError(
                f"Column end ({self.column_end}) must be >= column start ({self.column_start}) on single line"
            )

        # Validate: File path must have at least one component
        if not self.file_path.parts:
            raise InvalidLocationError("File path cannot be empty")

    @classmethod
    def at_line(cls, file_path: Path | str, line_number: int) -> Self:
        """
        Create location spanning entire line.

        Args:
            file_path: Path to source file
            line_number: Line number (1-indexed)

        Returns:
            Location spanning the line from column 0 to 0

        Examples:
            >>> loc = PatternLocation.at_line("test.go", 42)
            >>> loc.line_start == loc.line_end == 42
            True
        """
        return cls(
            file_path=file_path,
            line_start=line_number,
            line_end=line_number,
            column_start=0,
            column_end=0
        )

    @classmethod
    def single_point(cls, file_path: Path | str, line: int, column: int) -> Self:
        """
        Create location at single point.

        Args:
            file_path: Path to source file
            line: Line number (1-indexed)
            column: Column offset (0-indexed)

        Returns:
            Location at single point

        Examples:
            >>> loc = PatternLocation.single_point("test.go", 42, 8)
            >>> (loc.line_start, loc.column_start)
            (42, 8)
        """
        return cls(
            file_path=file_path,
            line_start=line,
            line_end=line,
            column_start=column,
            column_end=column
        )

    def __str__(self) -> str:
        """
        Return human-readable location string.

        Returns:
            Location string in format "file:line:col-col" or "file:line:col-line:col"

        Examples:
            >>> loc = PatternLocation(Path("test.go"), 10, 10, 5, 8)
            >>> str(loc)
            'test.go:10:5-8'
        """
        if self.line_start == self.line_end:
            return f"{self.file_path}:{self.line_start}:{self.column_start}-{self.column_end}"
        return f"{self.file_path}:{self.line_start}:{self.column_start}-{self.line_end}:{self.column_end}"
