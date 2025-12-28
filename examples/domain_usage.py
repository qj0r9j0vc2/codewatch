"""
Example usage of the Codewatch Domain Layer.

This script demonstrates how to use all components of the domain layer:
- Value objects (PatternLocation, ConfidenceScore, QualifiedName)
- Entities (KeeperPattern, HandlerPattern, PatternRelation)
- Enumerations (Framework, PatternType, RelationType)
- Interfaces (Detector, Extractor, PatternRepository)
- Exception handling
"""

from pathlib import Path

from codewatch.domain import (
    # Value Objects
    ConfidenceScore,
    PatternLocation,
    QualifiedName,
    # Entities
    HandlerPattern,
    KeeperPattern,
    Pattern,
    PatternRelation,
    # Enumerations
    Framework,
    PatternType,
    RelationType,
    # Interfaces
    Detector,
    Extractor,
    PatternRepository,
    # Exceptions
    ExtractionError,
    InvalidConfidenceScoreError,
    InvalidLocationError,
    InvalidQualifiedNameError,
    StorageError,
)


def demonstrate_value_objects() -> None:
    """Demonstrate value object usage."""
    print("=" * 60)
    print("VALUE OBJECTS DEMONSTRATION")
    print("=" * 60)

    # PatternLocation: Source code locations
    print("\n1. PatternLocation - Source code locations")
    print("-" * 60)

    # Create location at specific line
    loc1 = PatternLocation.at_line("cosmos/bank/keeper.go", 142)
    print(f"Location at line: {loc1}")

    # Create location at specific point
    loc2 = PatternLocation.single_point("cosmos/bank/types.go", 25, 8)
    print(f"Location at point: {loc2}")

    # Create location with range
    loc3 = PatternLocation(
        file_path=Path("cosmos/bank/handler.go"),
        line_start=142,
        line_end=158,
        column_start=0,
        column_end=4,
    )
    print(f"Location with range: {loc3}")

    # Demonstrate immutability
    print(f"Location is hashable: {hash(loc1)}")
    print(f"Can use in set: {loc1 in {loc1, loc2}}")

    # ConfidenceScore: Confidence levels [0.0-1.0]
    print("\n2. ConfidenceScore - Confidence levels")
    print("-" * 60)

    # Factory methods
    high = ConfidenceScore.high()
    medium = ConfidenceScore.medium()
    low = ConfidenceScore.low()

    print(f"High confidence: {high} (value: {float(high)})")
    print(f"Medium confidence: {medium} (value: {float(medium)})")
    print(f"Low confidence: {low} (value: {float(low)})")

    # Custom confidence
    custom = ConfidenceScore(0.856)
    print(f"Custom confidence: {custom} (value: {float(custom)})")

    # Normalization
    normalized = ConfidenceScore(1.00001)  # Slightly above 1.0
    print(f"Normalized: {normalized} (was 1.00001)")

    # QualifiedName: Fully-qualified identifiers
    print("\n3. QualifiedName - Fully-qualified identifiers")
    print("-" * 60)

    # Parse from string
    qn1 = QualifiedName.parse("cosmos.bank.keeper.Keeper")
    print(f"Parsed name: {qn1}")
    print(f"  Package: {qn1.package}")
    print(f"  Name: {qn1.name}")

    # Create directly
    qn2 = QualifiedName(package="cosmos.auth.keeper", name="AccountKeeper")
    print(f"Direct creation: {qn2}")

    # Demonstrate validation
    try:
        QualifiedName(package="", name="Invalid")
    except InvalidQualifiedNameError as e:
        print(f"Validation error caught: {e}")


def demonstrate_entities() -> None:
    """Demonstrate entity usage."""
    print("\n" + "=" * 60)
    print("ENTITIES DEMONSTRATION")
    print("=" * 60)

    # KeeperPattern: Cosmos SDK Keepers
    print("\n1. KeeperPattern - Cosmos SDK Keepers")
    print("-" * 60)

    bank_keeper = KeeperPattern(
        location=PatternLocation.at_line("cosmos/bank/keeper.go", 142),
        confidence=ConfidenceScore.high(),
        pattern_type=PatternType.KEEPER,
        framework=Framework.COSMOS_SDK,
        keeper_name=QualifiedName.parse("cosmos.bank.keeper.Keeper"),
        store_keys=("bank", "supply"),
        dependencies=(
            QualifiedName.parse("cosmos.auth.keeper.AccountKeeper"),
            QualifiedName.parse("cosmos.params.keeper.Keeper"),
        ),
    )

    print(f"Keeper: {bank_keeper.keeper_name}")
    print(f"  Location: {bank_keeper.location}")
    print(f"  Confidence: {bank_keeper.confidence}")
    print(f"  Store keys: {bank_keeper.store_keys}")
    print(f"  Dependencies: {bank_keeper.dependencies}")

    # Validate keeper
    bank_keeper.validate()  # Should pass
    print("  Validation: PASSED")

    # Demonstrate immutability and hashability
    print(f"  Is hashable: {hash(bank_keeper)}")
    keepers_set = {bank_keeper}
    print(f"  Can use in set: {bank_keeper in keepers_set}")

    # HandlerPattern: Message/Query handlers
    print("\n2. HandlerPattern - Message/Query handlers")
    print("-" * 60)

    send_handler = HandlerPattern(
        location=PatternLocation.at_line("cosmos/bank/handler.go", 25),
        confidence=ConfidenceScore(0.85),
        pattern_type=PatternType.MESSAGE_HANDLER,
        framework=Framework.COSMOS_SDK,
        handler_name=QualifiedName.parse("cosmos.bank.handler.SendHandler"),
        handler_type="message",
        message_type=QualifiedName.parse("cosmos.bank.types.MsgSend"),
        keeper_dependencies=(QualifiedName.parse("cosmos.bank.keeper.Keeper"),),
    )

    print(f"Handler: {send_handler.handler_name}")
    print(f"  Location: {send_handler.location}")
    print(f"  Handler type: {send_handler.handler_type}")
    print(f"  Message type: {send_handler.message_type}")
    print(f"  Keeper deps: {send_handler.keeper_dependencies}")

    # Query handler
    query_handler = HandlerPattern(
        location=PatternLocation.at_line("cosmos/bank/query.go", 42),
        confidence=ConfidenceScore.medium(),
        pattern_type=PatternType.QUERY_HANDLER,
        framework=Framework.COSMOS_SDK,
        handler_name=QualifiedName.parse("cosmos.bank.query.BalanceHandler"),
        handler_type="query",
        message_type=QualifiedName.parse("cosmos.bank.types.QueryBalance"),
        keeper_dependencies=(QualifiedName.parse("cosmos.bank.keeper.Keeper"),),
    )

    print(f"\nQuery handler: {query_handler.handler_name}")
    print(f"  Handler type: {query_handler.handler_type}")

    # PatternRelation: Relationships between patterns
    print("\n3. PatternRelation - Relationships between patterns")
    print("-" * 60)

    relation = PatternRelation(
        source=send_handler,
        target=bank_keeper,
        relation_type=RelationType.DEPENDS_ON,
        metadata={
            "reason": "requires bank keeper for balance operations",
            "confidence": "high",
        },
    )

    print(f"Relation: {relation.relation_type.value}")
    print(f"  Source: {relation.source.pattern_type.value} at {relation.source.location}")
    print(f"  Target: {relation.target.pattern_type.value} at {relation.target.location}")
    print(f"  Metadata: {relation.metadata}")

    # Demonstrate validation: source != target
    try:
        invalid_relation = PatternRelation(
            source=bank_keeper,
            target=bank_keeper,  # Same as source
            relation_type=RelationType.CALLS,
            metadata={},
        )
    except ExtractionError as e:
        print(f"  Validation error caught: {e}")


def demonstrate_interfaces() -> None:
    """Demonstrate interface usage with mock implementations."""
    print("\n" + "=" * 60)
    print("INTERFACES DEMONSTRATION")
    print("=" * 60)

    # Mock Detector implementation
    class MockKeeperDetector(Detector):
        """Mock detector for demonstration."""

        def detect(self, source_code: str, file_path: str) -> list[Pattern]:
            """Mock detection returning sample keeper."""
            if "keeper" in source_code.lower():
                return [
                    KeeperPattern(
                        location=PatternLocation.at_line(file_path, 10),
                        confidence=ConfidenceScore.high(),
                        pattern_type=PatternType.KEEPER,
                        framework=Framework.COSMOS_SDK,
                        keeper_name=QualifiedName.parse("example.keeper.Keeper"),
                        store_keys=("example",),
                        dependencies=(),
                    )
                ]
            return []

        def supported_pattern_type(self) -> PatternType:
            """Return KEEPER type."""
            return PatternType.KEEPER

    # Mock Extractor implementation
    class MockCosmosExtractor(Extractor):
        """Mock extractor for demonstration."""

        def __init__(self, detectors: list[Detector]) -> None:
            """Initialize with detectors."""
            self._detectors = detectors

        def extract(self, codebase_path: str) -> list[Pattern]:
            """Mock extraction."""
            all_patterns: list[Pattern] = []
            # Simulate processing files
            mock_code = "package keeper\ntype Keeper struct {}"
            for detector in self._detectors:
                patterns = detector.detect(mock_code, f"{codebase_path}/keeper.go")
                all_patterns.extend(patterns)
            return all_patterns

        def supported_framework(self) -> Framework:
            """Return COSMOS_SDK."""
            return Framework.COSMOS_SDK

    # Mock Repository implementation
    class InMemoryRepository(PatternRepository):
        """Mock in-memory repository for demonstration."""

        def __init__(self) -> None:
            """Initialize storage."""
            self._patterns: list[Pattern] = []

        def save_patterns(self, patterns: list[Pattern]) -> None:
            """Save patterns to memory."""
            self._patterns.extend(patterns)

        def find_by_type(self, pattern_type: PatternType) -> list[Pattern]:
            """Find patterns by type."""
            return [p for p in self._patterns if p.pattern_type == pattern_type]

        def execute_query(self, query: str) -> list[Pattern]:
            """Execute mock query."""
            return list(self._patterns)

    # Demonstrate detector
    print("\n1. Detector Interface")
    print("-" * 60)

    detector = MockKeeperDetector()
    print(f"Detector type: {detector.supported_pattern_type()}")

    source_code = "package keeper\ntype Keeper struct {}"
    patterns = detector.detect(source_code, "keeper.go")
    print(f"Detected {len(patterns)} pattern(s)")
    for pattern in patterns:
        print(f"  - {pattern.pattern_type.value} at {pattern.location}")

    # Demonstrate extractor
    print("\n2. Extractor Interface")
    print("-" * 60)

    extractor = MockCosmosExtractor([detector])
    print(f"Extractor framework: {extractor.supported_framework()}")

    all_patterns = extractor.extract("/path/to/cosmos-sdk")
    print(f"Extracted {len(all_patterns)} pattern(s)")
    for pattern in all_patterns:
        print(f"  - {pattern.pattern_type.value} at {pattern.location}")

    # Demonstrate repository
    print("\n3. PatternRepository Interface")
    print("-" * 60)

    repo = InMemoryRepository()

    # Save patterns
    repo.save_patterns(all_patterns)
    print(f"Saved {len(all_patterns)} pattern(s)")

    # Find by type
    keepers = repo.find_by_type(PatternType.KEEPER)
    print(f"Found {len(keepers)} keeper(s)")

    # Execute query
    all_stored = repo.execute_query("all")
    print(f"Query returned {len(all_stored)} pattern(s)")


def demonstrate_enumerations() -> None:
    """Demonstrate enumeration usage."""
    print("\n" + "=" * 60)
    print("ENUMERATIONS DEMONSTRATION")
    print("=" * 60)

    print("\n1. Framework Enumeration")
    print("-" * 60)
    print(f"COSMOS_SDK: {Framework.COSMOS_SDK}")
    print(f"ETHEREUM: {Framework.ETHEREUM}")
    print(f"POLKADOT: {Framework.POLKADOT}")

    print("\n2. PatternType Enumeration")
    print("-" * 60)
    print(f"KEEPER: {PatternType.KEEPER}")
    print(f"MESSAGE_HANDLER: {PatternType.MESSAGE_HANDLER}")
    print(f"QUERY_HANDLER: {PatternType.QUERY_HANDLER}")
    print(f"VALIDATOR: {PatternType.VALIDATOR}")

    print("\n3. RelationType Enumeration")
    print("-" * 60)
    print(f"CALLS: {RelationType.CALLS}")
    print(f"DEPENDS_ON: {RelationType.DEPENDS_ON}")
    print(f"IMPLEMENTS: {RelationType.IMPLEMENTS}")
    print(f"INHERITS_FROM: {RelationType.INHERITS_FROM}")


def demonstrate_error_handling() -> None:
    """Demonstrate exception handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMONSTRATION")
    print("=" * 60)

    print("\n1. Invalid value object validation")
    print("-" * 60)

    # Invalid location
    try:
        PatternLocation.at_line("test.go", -1)  # Negative line number
    except InvalidLocationError as e:
        print(f"InvalidLocationError: {e}")

    # Invalid confidence score
    try:
        ConfidenceScore(1.5)  # Above 1.0
    except InvalidConfidenceScoreError as e:
        print(f"InvalidConfidenceScoreError: {e}")

    # Invalid qualified name
    try:
        QualifiedName(package="", name="Test")  # Empty package
    except InvalidQualifiedNameError as e:
        print(f"InvalidQualifiedNameError: {e}")

    print("\n2. Entity validation")
    print("-" * 60)

    # Keeper without store keys
    try:
        invalid_keeper = KeeperPattern(
            location=PatternLocation.at_line("keeper.go", 10),
            confidence=ConfidenceScore.high(),
            pattern_type=PatternType.KEEPER,
            framework=Framework.COSMOS_SDK,
            keeper_name=QualifiedName.parse("test.keeper.Keeper"),
            store_keys=(),  # Empty store keys
            dependencies=(),
        )
        invalid_keeper.validate()
    except ExtractionError as e:
        print(f"ExtractionError: {e}")


def main() -> None:
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("CODEWATCH DOMAIN LAYER - EXAMPLE USAGE")
    print("=" * 60)

    demonstrate_value_objects()
    demonstrate_entities()
    demonstrate_interfaces()
    demonstrate_enumerations()
    demonstrate_error_handling()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
