"""Tests for QualifiedName value object."""

import pytest

from codewatch.domain.value_objects.qualified_name import QualifiedName
from codewatch.domain.exceptions import InvalidQualifiedNameError


class TestQualifiedNameCreation:
    """Tests for QualifiedName creation with valid inputs."""

    def test_create_with_valid_package_and_name(self) -> None:
        """Should create qualified name with package and name."""
        qn = QualifiedName(
            package="github.com/cosmos/cosmos-sdk/x/bank/keeper",
            name="Keeper"
        )
        assert qn.package == "github.com/cosmos/cosmos-sdk/x/bank/keeper"
        assert qn.name == "Keeper"

    def test_create_with_simple_package(self) -> None:
        """Should create qualified name with simple package."""
        qn = QualifiedName(package="main", name="App")
        assert qn.package == "main"
        assert qn.name == "App"

    def test_create_with_nested_package(self) -> None:
        """Should create qualified name with deeply nested package."""
        qn = QualifiedName(
            package="github.com/org/repo/internal/pkg/subpkg",
            name="Handler"
        )
        assert qn.package == "github.com/org/repo/internal/pkg/subpkg"
        assert qn.name == "Handler"


class TestQualifiedNameValidation:
    """Tests for QualifiedName validation."""

    def test_reject_empty_package(self) -> None:
        """Should reject empty package."""
        with pytest.raises(InvalidQualifiedNameError, match="Package cannot be empty"):
            QualifiedName(package="", name="Keeper")

    def test_reject_whitespace_only_package(self) -> None:
        """Should reject whitespace-only package."""
        with pytest.raises(InvalidQualifiedNameError, match="Package cannot be empty"):
            QualifiedName(package="   ", name="Keeper")

    def test_reject_empty_name(self) -> None:
        """Should reject empty name."""
        with pytest.raises(InvalidQualifiedNameError, match="Name cannot be empty"):
            QualifiedName(package="main", name="")

    def test_reject_whitespace_only_name(self) -> None:
        """Should reject whitespace-only name."""
        with pytest.raises(InvalidQualifiedNameError, match="Name cannot be empty"):
            QualifiedName(package="main", name="   ")

    def test_reject_both_empty(self) -> None:
        """Should reject both package and name empty."""
        with pytest.raises(InvalidQualifiedNameError):
            QualifiedName(package="", name="")


class TestQualifiedNameNormalization:
    """Tests for QualifiedName normalization (whitespace trimming)."""

    def test_trim_package_whitespace(self) -> None:
        """Should trim leading/trailing whitespace from package."""
        qn = QualifiedName(package="  main  ", name="App")
        assert qn.package == "main"

    def test_trim_name_whitespace(self) -> None:
        """Should trim leading/trailing whitespace from name."""
        qn = QualifiedName(package="main", name="  App  ")
        assert qn.name == "App"

    def test_trim_both_whitespace(self) -> None:
        """Should trim whitespace from both fields."""
        qn = QualifiedName(package="  main  ", name="  App  ")
        assert qn.package == "main"
        assert qn.name == "App"


class TestQualifiedNameFactoryMethods:
    """Tests for QualifiedName factory methods."""

    def test_parse_full_qualified_name(self) -> None:
        """Should parse full qualified name string."""
        qn = QualifiedName.parse("github.com/cosmos/cosmos-sdk/x/bank/keeper.Keeper")
        assert qn.package == "github.com/cosmos/cosmos-sdk/x/bank/keeper"
        assert qn.name == "Keeper"

    def test_parse_simple_qualified_name(self) -> None:
        """Should parse simple qualified name."""
        qn = QualifiedName.parse("main.App")
        assert qn.package == "main"
        assert qn.name == "App"

    def test_parse_with_multiple_dots_in_package(self) -> None:
        """Should handle multiple dots in package path."""
        qn = QualifiedName.parse("com.example.package.subpackage.Class")
        assert qn.package == "com.example.package.subpackage"
        assert qn.name == "Class"

    def test_parse_rejects_no_separator(self) -> None:
        """Should reject qualified name without separator."""
        with pytest.raises(InvalidQualifiedNameError, match="must contain at least one"):
            QualifiedName.parse("NoPackage")

    def test_parse_rejects_empty_string(self) -> None:
        """Should reject empty string."""
        with pytest.raises(InvalidQualifiedNameError, match="cannot be empty"):
            QualifiedName.parse("")

    def test_parse_rejects_only_dots(self) -> None:
        """Should reject string with only dots."""
        with pytest.raises(InvalidQualifiedNameError):
            QualifiedName.parse("...")

    def test_parse_handles_whitespace(self) -> None:
        """Should trim whitespace when parsing."""
        qn = QualifiedName.parse("  main.App  ")
        assert qn.package == "main"
        assert qn.name == "App"


class TestQualifiedNameImmutability:
    """Tests for QualifiedName immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        qn = QualifiedName(package="main", name="App")
        with pytest.raises(Exception):  # FrozenInstanceError
            qn.package = "other"  # type: ignore


class TestQualifiedNameHashability:
    """Tests for QualifiedName hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        qn = QualifiedName(package="main", name="App")
        hash(qn)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        qn1 = QualifiedName(package="main", name="App")
        qn2 = QualifiedName(package="main", name="App")
        names = {qn1, qn2}
        assert len(names) == 1  # Equal values

    def test_can_be_used_as_dict_key(self) -> None:
        """Should be usable as dict key."""
        qn = QualifiedName(package="main", name="App")
        cache = {qn: "metadata"}
        assert cache[qn] == "metadata"


class TestQualifiedNameStringRepresentation:
    """Tests for QualifiedName string representation."""

    def test_str_representation(self) -> None:
        """Should format as package.name."""
        qn = QualifiedName(
            package="github.com/cosmos/cosmos-sdk/x/bank/keeper",
            name="Keeper"
        )
        assert str(qn) == "github.com/cosmos/cosmos-sdk/x/bank/keeper.Keeper"

    def test_str_simple_name(self) -> None:
        """Should format simple name."""
        qn = QualifiedName(package="main", name="App")
        assert str(qn) == "main.App"

    def test_str_round_trip_with_parse(self) -> None:
        """Should round-trip through str() and parse()."""
        original = QualifiedName(package="pkg.subpkg", name="Class")
        parsed = QualifiedName.parse(str(original))
        assert parsed == original


class TestQualifiedNameEquality:
    """Tests for QualifiedName equality."""

    def test_equal_names(self) -> None:
        """Should compare equal names."""
        qn1 = QualifiedName(package="main", name="App")
        qn2 = QualifiedName(package="main", name="App")
        assert qn1 == qn2

    def test_unequal_package(self) -> None:
        """Should compare unequal packages."""
        qn1 = QualifiedName(package="main", name="App")
        qn2 = QualifiedName(package="other", name="App")
        assert qn1 != qn2

    def test_unequal_name(self) -> None:
        """Should compare unequal names."""
        qn1 = QualifiedName(package="main", name="App")
        qn2 = QualifiedName(package="main", name="Handler")
        assert qn1 != qn2

    def test_factory_equality(self) -> None:
        """Should compare factory-created names."""
        qn1 = QualifiedName.parse("main.App")
        qn2 = QualifiedName.parse("main.App")
        assert qn1 == qn2


class TestQualifiedNameComponents:
    """Tests for QualifiedName component extraction."""

    def test_package_path_components(self) -> None:
        """Should preserve package path structure."""
        qn = QualifiedName(
            package="github.com/org/repo/pkg",
            name="Class"
        )
        # Package path can be split for directory resolution
        assert "/" in qn.package or "." in qn.package

    def test_simple_name_component(self) -> None:
        """Should provide simple name for symbol lookup."""
        qn = QualifiedName(package="main", name="App")
        assert qn.name == "App"
