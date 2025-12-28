"""
HandlerPattern entity for message and query handler patterns.

This module provides the HandlerPattern entity for representing
message handlers and query handlers in blockchain applications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..value_objects import QualifiedName
from .pattern import Pattern


@dataclass(frozen=True, slots=True, kw_only=True)
class HandlerPattern(Pattern):
    """
    Message or Query Handler pattern.

    Handlers process messages or queries in blockchain applications.
    The handler_type distinguishes between message handlers and query handlers.

    Attributes:
        handler_name: Fully qualified name of the handler
        handler_type: Either 'message' or 'query'
        message_type: Qualified name of the message/query type being handled
        keeper_dependencies: Tuple of keepers this handler depends on

    Examples:
        >>> handler = HandlerPattern(
        ...     location=PatternLocation.at_line("handler.go", 25),
        ...     confidence=ConfidenceScore(0.85),
        ...     pattern_type=PatternType.MESSAGE_HANDLER,
        ...     framework=Framework.COSMOS_SDK,
        ...     handler_name=QualifiedName("cosmos.bank.handler.SendHandler"),
        ...     handler_type="message",
        ...     message_type=QualifiedName("cosmos.bank.types.MsgSend"),
        ...     keeper_dependencies=(QualifiedName("cosmos.bank.keeper.Keeper"),)
        ... )
    """

    handler_name: QualifiedName
    handler_type: Literal['message', 'query']
    message_type: QualifiedName
    keeper_dependencies: tuple[QualifiedName, ...]

    def validate(self) -> None:
        """
        Validate handler-specific constraints.

        Handler type is already constrained by Literal type hint.
        Message type and keeper dependencies are validated by QualifiedName class.
        No additional validation needed beyond type checking.
        """
        # Handler type already constrained by Literal['message', 'query']
        # Message type is valid QualifiedName (validated by QualifiedName class)
        # No additional validation needed beyond type checking
        pass
