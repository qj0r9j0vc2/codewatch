"""Tests for HandlerPattern entity."""

import pytest

from codewatch.domain.entities.handler import HandlerPattern
from codewatch.domain.enums import Framework, PatternType
from codewatch.domain.value_objects import ConfidenceScore, PatternLocation, QualifiedName


class TestHandlerPatternCreation:
    """Tests for HandlerPattern creation with message and query types."""

    def test_create_message_handler(self) -> None:
        """Should create message handler."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        assert handler.handler_name == QualifiedName(package="cosmos.bank.handler", name="SendHandler")
        assert handler.handler_type == "message"
        assert handler.message_type == QualifiedName(package="cosmos.bank.types", name="MsgSend")
        assert handler.keeper_dependencies == ()

    def test_create_query_handler(self) -> None:
        """Should create query handler."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("query.go", 42),
            confidence=ConfidenceScore(0.90),
            pattern_type=PatternType.QUERY_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.query", name="BalanceHandler"),
            handler_type="query",
            message_type=QualifiedName(package="cosmos.bank.types", name="QueryBalance"),
            keeper_dependencies=()
        )
        assert handler.handler_type == "query"

    def test_create_with_keeper_dependencies(self) -> None:
        """Should create handler with keeper dependencies."""
        bank_keeper = QualifiedName(package="cosmos.bank.keeper", name="Keeper")
        auth_keeper = QualifiedName(package="cosmos.auth.keeper", name="AccountKeeper")
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=(bank_keeper, auth_keeper)
        )
        assert handler.keeper_dependencies == (bank_keeper, auth_keeper)

    def test_create_with_no_keeper_dependencies(self) -> None:
        """Should create handler with no keeper dependencies."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        assert handler.keeper_dependencies == ()


class TestHandlerPatternHandlerTypeValidation:
    """Tests for HandlerPattern handler_type validation (Literal)."""

    def test_accept_message_type(self) -> None:
        """Should accept 'message' as handler_type."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        assert handler.handler_type == "message"

    def test_accept_query_type(self) -> None:
        """Should accept 'query' as handler_type."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("query.go", 42),
            confidence=ConfidenceScore(0.90),
            pattern_type=PatternType.QUERY_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.query", name="BalanceHandler"),
            handler_type="query",
            message_type=QualifiedName(package="cosmos.bank.types", name="QueryBalance"),
            keeper_dependencies=()
        )
        assert handler.handler_type == "query"


class TestHandlerPatternImmutability:
    """Tests for HandlerPattern immutability."""

    def test_is_immutable(self) -> None:
        """Should be immutable (frozen dataclass)."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            handler.handler_type = "query"  # type: ignore


class TestHandlerPatternHashability:
    """Tests for HandlerPattern hashability."""

    def test_is_hashable(self) -> None:
        """Should be hashable."""
        handler = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        hash(handler)  # Should not raise

    def test_can_be_used_in_set(self) -> None:
        """Should be usable in sets."""
        handler1 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        handler2 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        handlers = {handler1, handler2}
        assert len(handlers) == 1  # Equal values


class TestHandlerPatternEquality:
    """Tests for HandlerPattern equality."""

    def test_equal_handlers(self) -> None:
        """Should compare equal handlers."""
        handler1 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        handler2 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        assert handler1 == handler2

    def test_unequal_handlers_different_type(self) -> None:
        """Should compare unequal handlers with different handler_type."""
        handler1 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        handler2 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.QUERY_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="query",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        assert handler1 != handler2

    def test_unequal_handlers_different_message_type(self) -> None:
        """Should compare unequal handlers with different message_type."""
        handler1 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgSend"),
            keeper_dependencies=()
        )
        handler2 = HandlerPattern(
            location=PatternLocation.at_line("handler.go", 25),
            confidence=ConfidenceScore(0.85),
            pattern_type=PatternType.MESSAGE_HANDLER,
            framework=Framework.COSMOS_SDK,
            handler_name=QualifiedName(package="cosmos.bank.handler", name="SendHandler"),
            handler_type="message",
            message_type=QualifiedName(package="cosmos.bank.types", name="MsgMultiSend"),
            keeper_dependencies=()
        )
        assert handler1 != handler2
