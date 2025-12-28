# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-28

### Added
- Multi-version DRG support with version manager
- FastAPI REST API with auto-generated documentation
- Docker support with multi-platform builds
- Comprehensive CLI with commands: list, add, download, remove, group, compare, serve, stats
- Batch processing support
- Version comparison functionality
- Cross-platform support (Linux, Mac, Windows)
- DBF file auto-detection
- CC/MCC exclusion rules support
- Patient Complexity Level (PCL) calculation
- Adjusted RW calculation based on LOS
- Comprehensive test suite
- CI/CD workflows with GitHub Actions
- Documentation with MkDocs Material

### Changed
- Refactored from single-version to multi-version architecture
- Improved error handling and validation
- Enhanced type hints and dataclasses

### Fixed
- DBF file encoding handling (Windows-874 for Thai)
- ICD-10 code normalization
- Procedure code lookup with multiple formats

## [1.0.0] - Initial Release

- Basic DRG grouping functionality
- Single version support
- Command-line interface

[2.0.0]: https://github.com/aegisx-platform/thai-drg-grouper/releases/tag/v2.0.0
[1.0.0]: https://github.com/aegisx-platform/thai-drg-grouper/releases/tag/v1.0.0
