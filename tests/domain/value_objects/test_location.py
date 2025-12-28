"""Tests for PatternLocation value object."""

import pytest
from pathlib import Path

from codewatch.domain.value_objects.location import PatternLocation
from codewatch.domain.exceptions import InvalidLocationError


class TestPatternLocationCreation:
    """Tests for PatternLocation creation with valid inputs."""

    def test_create_with_valid_inputs(self) -> None:
        """Should create location with valid inputs."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=10,
            line_end=20,
            column_start=0,
            column_end=5
        )
        assert loc.file_path == Path("test.go")
        assert loc.line_start == 10
        assert loc.line_end == 20
        assert loc.column_start == 0
        assert loc.column_end == 5

    def test_create_with_string_path(self) -> None:
        """Should normalize string paths to Path objects."""
        loc = PatternLocation(
            file_path="test.go",
            line_start=10,
            line_end=10,
            column_start=0,
            column_end=0
        )
        assert isinstance(loc.file_path, Path)
        assert loc.file_path == Path("test.go")

    def test_create_single_line_location(self) -> None:
        """Should create location on single line."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=42,
            line_end=42,
            column_start=8,
            column_end=15
        )
        assert loc.line_start == 42
        assert loc.line_end == 42


class TestPatternLocationValidation:
    """Tests for PatternLocation validation."""

    def test_reject_negative_line_start(self) -> None:
        """Should reject negative line start."""
        with pytest.raises(InvalidLocationError, match="Line start must be positive"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=-1,
                line_end=10,
                column_start=0,
                column_end=0
            )

    def test_reject_zero_line_start(self) -> None:
        """Should reject zero line start (1-indexed)."""
        with pytest.raises(InvalidLocationError, match="Line start must be positive"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=0,
                line_end=10,
                column_start=0,
                column_end=0
            )

    def test_reject_negative_line_end(self) -> None:
        """Should reject negative line end."""
        with pytest.raises(InvalidLocationError, match="Line end must be positive"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=1,
                line_end=-1,
                column_start=0,
                column_end=0
            )

    def test_reject_line_end_before_start(self) -> None:
        """Should reject line_end < line_start."""
        with pytest.raises(InvalidLocationError, match="Line end.*must be >= line start"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=20,
                line_end=10,
                column_start=0,
                column_end=0
            )

    def test_reject_negative_column_start(self) -> None:
        """Should reject negative column start."""
        with pytest.raises(InvalidLocationError, match="Column start must be non-negative"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=10,
                line_end=10,
                column_start=-1,
                column_end=0
            )

    def test_reject_negative_column_end(self) -> None:
        """Should reject negative column end."""
        with pytest.raises(InvalidLocationError, match="Column end must be non-negative"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=10,
                line_end=10,
                column_start=0,
                column_end=-1
            )

    def test_reject_column_end_before_start_on_same_line(self) -> None:
        """Should reject column_end < column_start on single line."""
        with pytest.raises(InvalidLocationError, match="Column end.*must be >= column start"):
            PatternLocation(
                file_path=Path("test.go"),
                line_start=10,
                line_end=10,
                column_start=15,
                column_end=8
            )

    def test_accept_column_end_before_start_on_different_lines(self) -> None:
        """Should accept column_end < column_start on different lines."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=10,
            line_end=20,
            column_start=15,
            column_end=5
        )
        assert loc.column_start == 15
        assert loc.column_end == 5

    def test_reject_empty_file_path(self) -> None:
        """Should reject empty file path."""
        with pytest.raises(InvalidLocationError, match="File path cannot be empty"):
            PatternLocation(
                file_path=Path(""),
                line_start=1,
                line_end=1,
                column_start=0,
                column_end=0
            )


class TestPatternLocationFactoryMethods:
    """Tests for PatternLocation factory methods."""

    def test_at_line_factory(self) -> None:
        """Should create location at start of line."""
        loc = PatternLocation.at_line(Path("test.go"), 42)
        assert loc.file_path == Path("test.go")
        assert loc.line_start == 42
        assert loc.line_end == 42
        assert loc.column_start == 0
        assert loc.column_end == 0

    def test_at_line_with_string_path(self) -> None:
        """Should accept string path in at_line factory."""
        loc = PatternLocation.at_line("test.go", 42)
        assert isinstance(loc.file_path, Path)
        assert loc.file_path == Path("test.go")

    def test_single_point_factory(self) -> None:
        """Should create location at single point."""
        loc = PatternLocation.single_point(Path("test.go"), 42, 8)
        assert loc.file_path == Path("test.go")
        assert loc.line_start == 42
        assert loc.line_end == 42
        assert loc.column_start == 8
        assert loc.column_end == 8


class TestPatternLocationImmutability:
    """Tests for PatternLocation immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=10,
            line_end=10,
            column_start=0,
            column_end=0
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            loc.line_start = 20  # type: ignore


class TestPatternLocationHashability:
    """Tests for PatternLocation hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=10,
            line_end=10,
            column_start=0,
            column_end=0
        )
        hash(loc)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        loc1 = PatternLocation.at_line(Path("test.go"), 10)
        loc2 = PatternLocation.at_line(Path("test.go"), 10)
        locations = {loc1, loc2}
        assert len(locations) == 1  # Equal values

    def test_can_be_used_as_dict_key(self) -> None:
        """Should be usable as dict key."""
        loc = PatternLocation.at_line(Path("test.go"), 10)
        cache = {loc: "data"}
        assert cache[loc] == "data"


class TestPatternLocationStringRepresentation:
    """Tests for PatternLocation string representation."""

    def test_str_single_line(self) -> None:
        """Should format single line location."""
        loc = PatternLocation(
            file_path=Path("test.go"),
            line_start=42,
            line_end=42,
            column_start=8,
            column_end=15
        )
        assert str(loc) == "test.go:42:8-15"

    def test_str_multi_line(self) -> None:
        """Should format multi-line location."""
        loc = PatternLocation(
            file_path=Path("keeper.go"),
            line_start=142,
            line_end=158,
            column_start=0,
            column_end=4
        )
        assert str(loc) == "keeper.go:142:0-158:4"


class TestPatternLocationEquality:
    """Tests for PatternLocation equality."""

    def test_equal_locations(self) -> None:
        """Should compare equal locations."""
        loc1 = PatternLocation.at_line(Path("test.go"), 10)
        loc2 = PatternLocation.at_line("test.go", 10)
        assert loc1 == loc2

    def test_unequal_locations(self) -> None:
        """Should compare unequal locations."""
        loc1 = PatternLocation.at_line(Path("test.go"), 10)
        loc2 = PatternLocation.at_line(Path("test.go"), 20)
        assert loc1 != loc2
