"""
Domain enumerations for the Codewatch blockchain code analysis system.

This module defines type-safe enumerations for frameworks, pattern types,
and relationship types. All enums inherit from str for JSON serialization.
"""

from enum import Enum


class Framework(str, Enum):
    """
    Supported blockchain frameworks.

    Examples:
        >>> framework = Framework.COSMOS_SDK
        >>> str(framework)
        'cosmos_sdk'
    """

    COSMOS_SDK = "cosmos_sdk"
    ETHEREUM = "ethereum"
    POLKADOT = "polkadot"

    def __str__(self) -> str:
        return self.value


class PatternType(str, Enum):
    """
    Pattern categories for blockchain code patterns.

    Examples:
        >>> pattern_type = PatternType.KEEPER
        >>> str(pattern_type)
        'keeper'
    """

    KEEPER = "keeper"
    MESSAGE_HANDLER = "message_handler"
    QUERY_HANDLER = "query_handler"
    VALIDATOR = "validator"

    def __str__(self) -> str:
        return self.value


class RelationType(str, Enum):
    """
    Relationship types between patterns.

    Examples:
        >>> relation = RelationType.DEPENDS_ON
        >>> str(relation)
        'depends_on'
    """

    CALLS = "calls"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    INHERITS_FROM = "inherits_from"

    def __str__(self) -> str:
        return self.value
