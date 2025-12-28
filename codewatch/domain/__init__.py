"""
Codewatch Domain Layer.

This module provides the core domain layer for the Codewatch blockchain code
analysis system. It defines immutable entities, value objects, and interfaces
following Clean Architecture and Domain-Driven Design principles.

The domain layer is the innermost layer of the application, containing all
business logic and domain concepts. It has zero external dependencies and
uses only Python standard library.

## Architecture

### Entities
Immutable pattern entities representing detected code patterns:
- Pattern: Abstract base class for all patterns
- KeeperPattern: Cosmos SDK Keeper patterns
- HandlerPattern: Message/Query handler patterns
- PatternRelation: Relationships between patterns

### Value Objects
Immutable, validated value objects for domain concepts:
- PatternLocation: Source code location with file path and line/column coordinates
- ConfidenceScore: Confidence level [0.0-1.0] with percentage formatting
- QualifiedName: Fully-qualified identifiers (package.name)

### Enumerations
Type-safe enumerations for domain concepts:
- Framework: Blockchain frameworks (COSMOS_SDK, ETHEREUM, POLKADOT)
- PatternType: Pattern types (KEEPER, MESSAGE_HANDLER, QUERY_HANDLER, VALIDATOR)
- RelationType: Relationship types (CALLS, DEPENDS_ON, IMPLEMENTS, INHERITS_FROM)

### Interfaces
Abstract interfaces for infrastructure implementations:
- Detector: Pattern detection interface
- Extractor: Framework-specific extraction interface
- PatternRepository: Pattern persistence interface

### Exceptions
Typed exception hierarchy for domain errors:
- CodewatchError: Base exception
- ValueObjectError: Value object validation errors
- InvalidLocationError, InvalidConfidenceScoreError, InvalidQualifiedNameError
- ExtractionError: Pattern extraction failures
- StorageError: Repository operation failures
- ConfigurationError: Configuration validation failures

## Design Principles

1. **Immutability**: All entities and value objects are immutable (frozen dataclasses)
2. **Type Safety**: 100% type hints, mypy strict mode compliant
3. **Validation**: All validation in __post_init__() with object.__setattr__()
4. **Hashability**: All entities and value objects are hashable (usable in sets/dicts)
5. **Zero Dependencies**: Pure Python stdlib only, no external packages

## Example Usage

```python
from codewatch.domain import (
    # Value Objects
    PatternLocation,
    ConfidenceScore,
    QualifiedName,
    # Entities
    KeeperPattern,
    HandlerPattern,
    PatternRelation,
    # Enums
    Framework,
    PatternType,
    RelationType,
    # Interfaces
    Detector,
    Extractor,
    PatternRepository,
)

# Create a keeper pattern
keeper = KeeperPattern(
    location=PatternLocation.at_line("keeper.go", 142),
    confidence=ConfidenceScore.high(),
    pattern_type=PatternType.KEEPER,
    framework=Framework.COSMOS_SDK,
    keeper_name=QualifiedName.parse("cosmos.bank.keeper.Keeper"),
    store_keys=("bank", "supply"),
    dependencies=()
)

# Create a handler pattern
handler = HandlerPattern(
    location=PatternLocation.at_line("handler.go", 25),
    confidence=ConfidenceScore(0.85),
    pattern_type=PatternType.MESSAGE_HANDLER,
    framework=Framework.COSMOS_SDK,
    handler_name=QualifiedName.parse("cosmos.bank.handler.SendHandler"),
    handler_type="message",
    message_type=QualifiedName.parse("cosmos.bank.types.MsgSend"),
    keeper_dependencies=(QualifiedName.parse("cosmos.bank.keeper.Keeper"),)
)

# Create a relationship
relation = PatternRelation(
    source=handler,
    target=keeper,
    relation_type=RelationType.DEPENDS_ON,
    metadata={"reason": "requires bank keeper"}
)
```

## Module Organization

```
codewatch/domain/
├── __init__.py              # This file (public API)
├── entities/                # Immutable domain entities
│   ├── pattern.py          # Pattern ABC and PatternRelation
│   ├── keeper.py           # KeeperPattern
│   └── handler.py          # HandlerPattern
├── value_objects/          # Immutable value objects
│   ├── location.py         # PatternLocation
│   ├── confidence.py       # ConfidenceScore
│   └── qualified_name.py   # QualifiedName
├── enums.py                # Domain enumerations
├── exceptions.py           # Domain exception hierarchy
└── interfaces/             # Abstract interfaces for infrastructure
    ├── detector.py         # Detector ABC
    ├── extractor.py        # Extractor ABC
    └── repository.py       # PatternRepository ABC
```

## Testing

All domain components have 95%+ test coverage with comprehensive test suites:
- tests/domain/test_enums.py
- tests/domain/test_exceptions.py
- tests/domain/value_objects/
- tests/domain/entities/
- tests/domain/interfaces/

## Type Safety

All code passes mypy strict mode:
```bash
mypy --strict codewatch/domain/
```

## Standards Compliance

This module follows:
- Clean Architecture (innermost layer, zero dependencies)
- Domain-Driven Design (rich domain model)
- Python 3.11+ dataclass features (frozen, slots, kw_only)
- PEP 8 code style
- Google docstring format
"""

from .entities import (
    HandlerPattern,
    KeeperPattern,
    Pattern,
    PatternRelation,
)
from .enums import (
    Framework,
    PatternType,
    RelationType,
)
from .exceptions import (
    CodewatchError,
    ConfigurationError,
    ExtractionError,
    InvalidConfidenceScoreError,
    InvalidLocationError,
    InvalidQualifiedNameError,
    StorageError,
    ValueObjectError,
)
from .interfaces import (
    Detector,
    Extractor,
    PatternRepository,
)
from .value_objects import (
    ConfidenceScore,
    PatternLocation,
    QualifiedName,
)

__all__ = [
    # Entities
    "HandlerPattern",
    "KeeperPattern",
    "Pattern",
    "PatternRelation",
    # Value Objects
    "ConfidenceScore",
    "PatternLocation",
    "QualifiedName",
    # Enumerations
    "Framework",
    "PatternType",
    "RelationType",
    # Interfaces
    "Detector",
    "Extractor",
    "PatternRepository",
    # Exceptions
    "CodewatchError",
    "ConfigurationError",
    "ExtractionError",
    "InvalidConfidenceScoreError",
    "InvalidLocationError",
    "InvalidQualifiedNameError",
    "StorageError",
    "ValueObjectError",
]
