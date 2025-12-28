"""Tests for KeeperPattern entity."""

import pytest

from codewatch.domain.entities.keeper import KeeperPattern
from codewatch.domain.enums import Framework, PatternType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName
from codewatch.domain.exceptions import ExtractionError


class TestKeeperPatternCreation:
    """Tests for KeeperPattern creation with valid attributes."""

    def test_create_with_single_store_key(self) -> None:
        """Should create keeper with single store key."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        assert keeper.keeper_name == QualifiedName(package="cosmos.bank.keeper", name="Keeper")
        assert keeper.store_keys == ("bank",)
        assert keeper.dependencies == ()

    def test_create_with_multiple_store_keys(self) -> None:
        """Should create keeper with multiple store keys."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank", "supply", "params"),
            dependencies=()
        )
        assert keeper.store_keys == ("bank", "supply", "params")

    def test_create_with_dependencies(self) -> None:
        """Should create keeper with keeper dependencies."""
        auth_keeper = QualifiedName(package="cosmos.auth.keeper", name="AccountKeeper")
        params_keeper = QualifiedName(package="cosmos.params.keeper", name="Keeper")
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=(auth_keeper, params_keeper)
        )
        assert keeper.dependencies == (auth_keeper, params_keeper)

    def test_create_with_no_dependencies(self) -> None:
        """Should create keeper with no dependencies."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        assert keeper.dependencies == ()


class TestKeeperPatternValidation:
    """Tests for KeeperPattern validation."""

    def test_reject_empty_store_keys(self) -> None:
        """Should reject keeper with no store keys."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=(),
            dependencies=()
        )
        with pytest.raises(ExtractionError, match="must have at least one store key"):
            keeper.validate()

    def test_validate_passes_with_store_keys(self) -> None:
        """Should pass validation with at least one store key."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keeper.validate()  # Should not raise


class TestKeeperPatternImmutability:
    """Tests for KeeperPattern immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            keeper.store_keys = ("other",)  # type: ignore


class TestKeeperPatternHashability:
    """Tests for KeeperPattern hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        hash(keeper)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        keeper1 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keeper2 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keepers = {keeper1, keeper2}
        assert len(keepers) == 1  # Equal values


class TestKeeperPatternEquality:
    """Tests for KeeperPattern equality."""

    def test_equal_keepers(self) -> None:
        """Should compare equal keepers."""
        keeper1 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keeper2 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        assert keeper1 == keeper2

    def test_unequal_keepers_different_name(self) -> None:
        """Should compare unequal keepers with different names."""
        keeper1 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keeper2 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.auth.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        assert keeper1 != keeper2

    def test_unequal_keepers_different_store_keys(self) -> None:
        """Should compare unequal keepers with different store keys."""
        keeper1 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank",),
            dependencies=()
        )
        keeper2 = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 142),
            confidence=ConfidenceScore(0.95),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName(package="cosmos.bank.keeper", name="Keeper"),
            store_keys=("bank", "supply"),
            dependencies=()
        )
        assert keeper1 != keeper2
