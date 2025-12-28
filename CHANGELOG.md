# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Core domain layer implementation
  - Domain enumerations: Framework, PatternType, RelationType
  - Exception hierarchy with 8 typed exceptions
  - Value objects: PatternLocation, ConfidenceScore, QualifiedName
  - Entities: Pattern (ABC), KeeperPattern, HandlerPattern, PatternRelation
  - Interfaces: Detector, Extractor, PatternRepository
- Type-safe domain model with 100% type hints
- Immutable frozen dataclasses with validation
- Comprehensive test suite with 95%+ coverage
- Example usage script demonstrating all components
- Project configuration: mypy.ini, pytest.ini, .gitignore

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
