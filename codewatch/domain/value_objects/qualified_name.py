"""
QualifiedName value object for representing fully-qualified identifiers.

This module provides an immutable value object for fully-qualified names
with package path and symbol name components.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ..exceptions import InvalidQualifiedNameError


@dataclass(frozen=True, slots=True)
class QualifiedName:
    """
    Fully-qualified identifier.

    Represents a symbol with its complete package path, such as
    "github.com/cosmos/cosmos-sdk/x/bank/keeper.Keeper".

    Attributes:
        package: Package or module path (cannot be empty after trimming)
        name: Symbol name (cannot be empty after trimming)

    Raises:
        InvalidQualifiedNameError: If validation fails

    Examples:
        >>> qn = QualifiedName("github.com/cosmos/cosmos-sdk/x/bank/keeper", "Keeper")
        >>> str(qn)
        'github.com/cosmos/cosmos-sdk/x/bank/keeper.Keeper'

        >>> qn = QualifiedName.parse("main.App")
        >>> qn.package
        'main'
        >>> qn.name
        'App'
    """

    package: str
    name: str

    def __post_init__(self) -> None:
        """Validate and normalize qualified name."""
        # Normalize: Trim whitespace from both components
        normalized_package = self.package.strip()
        normalized_name = self.name.strip()

        # Apply normalization if needed
        if normalized_package != self.package:
            object.__setattr__(self, 'package', normalized_package)
        if normalized_name != self.name:
            object.__setattr__(self, 'name', normalized_name)

        # Validate: Package cannot be empty
        if not self.package:
            raise InvalidQualifiedNameError("Package cannot be empty")

        # Validate: Name cannot be empty
        if not self.name:
            raise InvalidQualifiedNameError("Name cannot be empty")

    @classmethod
    def parse(cls, qualified_name: str) -> Self:
        """
        Parse qualified name from string.

        Parses a string in format "package.name" or "package/path.name"
        into package and name components. The last dot separates the
        package from the name.

        Args:
            qualified_name: Qualified name string (e.g., "main.App")

        Returns:
            Parsed QualifiedName

        Raises:
            InvalidQualifiedNameError: If parsing fails

        Examples:
            >>> qn = QualifiedName.parse("main.App")
            >>> (qn.package, qn.name)
            ('main', 'App')

            >>> qn = QualifiedName.parse("github.com/cosmos/cosmos-sdk/x/bank.Keeper")
            >>> qn.package
            'github.com/cosmos/cosmos-sdk/x/bank'
        """
        # Normalize: Trim whitespace
        qualified_name = qualified_name.strip()

        # Validate: Cannot be empty
        if not qualified_name:
            raise InvalidQualifiedNameError("Qualified name cannot be empty")

        # Parse: Split on last dot
        if '.' not in qualified_name:
            raise InvalidQualifiedNameError(
                f"Qualified name must contain at least one '.' separator, got '{qualified_name}'"
            )

        # Split on last dot to separate package from name
        last_dot_index = qualified_name.rfind('.')
        package = qualified_name[:last_dot_index]
        name = qualified_name[last_dot_index + 1:]

        return cls(package=package, name=name)

    def __str__(self) -> str:
        """
        Return fully-qualified name string.

        Returns:
            Qualified name in format "package.name"

        Examples:
            >>> str(QualifiedName("main", "App"))
            'main.App'
        """
        return f"{self.package}.{self.name}"
