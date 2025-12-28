# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-12-29

### Added
- **API Reference Documentation**: Complete REST API and Python API documentation
  - REST API Reference with all endpoints, request/response schemas, examples
  - Python API Reference with detailed class and method documentation
  - Interactive examples in Python, JavaScript, and cURL
- **Environment Variable Configuration**: CORS and server configuration via .env file
  - Configurable CORS origins for production and development
  - Server host and port configuration
  - Docker environment variable support
- **Thai Language Documentation**: Comprehensive documentation in Thai
  - Complete installation guide in Thai
  - 10 detailed usage examples covering common scenarios
  - Thai translations of main documentation pages
- **Buy Me a Coffee Integration**: Support links in README and documentation

### Changed
- Improved documentation structure with clear navigation
- Enhanced installation guide with configuration section
- Updated all documentation links to point to existing files

### Fixed
- Broken documentation links in navigation menu
- Relative path issues in Thai documentation
- MkDocs strict mode build failures
- Documentation deployment workflow

## [2.0.0] - 2024-12-28

### Added
- Multi-version DRG support with version manager
- FastAPI REST API with auto-generated OpenAPI documentation
- Docker support with multi-platform builds (amd64, arm64)
- Comprehensive CLI with commands: list, add, download, remove, group, compare, serve, stats
- Batch processing support for multiple cases
- Version comparison functionality across all installed versions
- Cross-platform support (Linux, Mac, Windows)
- DBF file auto-detection with flexible naming
- CC/MCC exclusion rules support
- Patient Complexity Level (PCL) calculation (0-4)
- Adjusted RW calculation based on Length of Stay
- Comprehensive test suite with pytest
- CI/CD workflows with GitHub Actions:
  - Automated testing on multiple Python versions
  - Code quality checks (black, ruff)
  - Docker image builds and publishing
  - PyPI package publishing on release
  - Documentation deployment to GitHub Pages
- Complete documentation with MkDocs Material theme
- CLAUDE.md for AI-assisted development

### Changed
- Refactored from single-version to multi-version architecture
- Improved error handling with detailed error messages
- Enhanced type hints using dataclasses
- Optimized DBF file loading with lazy initialization
- Better code normalization for ICD-10 and procedure codes

### Fixed
- DBF file encoding handling (Windows-874 for Thai characters)
- ICD-10 code normalization and lookup fallback
- Procedure code lookup with multiple formats (with/without dots)
- CC exclusion logic for PDx-SDx relationships
- RW adjustment calculation for long-stay cases

### Security
- Implemented safe GitHub Actions workflows without command injection risks
- Added proper input validation for API endpoints

## [1.0.0] - Initial Release

### Added
- Basic DRG grouping functionality
- Single version support
- Simple command-line interface

[2.1.0]: https://github.com/aegisx-platform/thai-drg-grouper/releases/tag/v2.1.0
[2.0.0]: https://github.com/aegisx-platform/thai-drg-grouper/releases/tag/v2.0.0
[1.0.0]: https://github.com/aegisx-platform/thai-drg-grouper/releases/tag/v1.0.0
