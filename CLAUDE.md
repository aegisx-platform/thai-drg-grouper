# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Thai DRG Grouper** is a Python package for grouping Thai DRG (Diagnosis Related Groups) cases. It supports multiple DRG versions simultaneously and provides a CLI, Python library, and REST API interface.

### Key Architecture Components

1. **ThaiDRGGrouper** (`src/thai_drg_grouper/grouper.py`): Core grouping logic for a single DRG version
   - Loads DBF files (ICD-10 codes, procedures, DRG definitions, CC exclusions)
   - Implements the grouping algorithm (MDC assignment, PCL calculation, DRG selection)
   - Handles CC/MCC detection and exclusions
   - Calculates adjusted relative weights based on LOS

2. **ThaiDRGGrouperManager** (`src/thai_drg_grouper/manager.py`): Multi-version orchestrator
   - Manages multiple DRG versions in `data/versions/` directory
   - Lazy-loads groupers on demand (caches instances)
   - Handles version adding/removing/downloading from TCMC
   - Provides comparison across all versions

3. **Types** (`src/thai_drg_grouper/types.py`): Data models
   - `GrouperResult`: Output with DRG, RW, MDC, PCL, etc.
   - `VersionInfo`: Metadata for each version
   - MDC name mappings (English and Thai)

4. **CLI** (`src/thai_drg_grouper/cli.py`): Command-line interface
   - Commands: list, add, download, remove, group, compare, serve, stats
   - Entry point: `thai-drg-grouper` command

5. **API** (`src/thai_drg_grouper/api.py`): FastAPI REST endpoints
   - Endpoints: `/group`, `/group/{version}`, `/group/compare`, `/group/batch`, `/versions`
   - Auto-generated OpenAPI docs at `/docs`

## Development Commands

### Setup

```bash
# Install in development mode with all dependencies
pip install -e .[all]

# Or install specific extras
pip install -e .[api]     # API only
pip install -e .[dev]     # Dev tools only
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=thai_drg_grouper --cov-report=html

# Run specific test file
pytest tests/test_grouper.py

# Run specific test
pytest tests/test_grouper.py::TestGrouper::test_group_fracture -v
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/

# Auto-fix ruff issues
ruff check --fix src/ tests/

# Type checking (if implemented)
mypy src/
```

### Building

```bash
# Build package
python -m build

# Install locally from build
pip install dist/thai_drg_grouper-*.whl
```

### Running Locally

```bash
# CLI - List versions
thai-drg-grouper list

# CLI - Group a case
thai-drg-grouper group --pdx S82201D --sdx E119,I10 --proc 7936 --los 5 --age 25

# API - Start server
thai-drg-grouper serve --port 8000

# Or with uvicorn directly
uvicorn thai_drg_grouper.api:app --reload --port 8000
```

### Docker

```bash
# Build Docker image
docker build -t thai-drg-grouper:latest .

# Run container
docker run -p 8000:8000 thai-drg-grouper:latest

# Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## Data Version Management

The `data/versions/` directory contains multiple DRG versions:

```
data/versions/
├── config.json              # Stores default version
├── 6.3/
│   ├── version.json         # Version metadata
│   └── data/
│       ├── c63i10.dbf       # ICD-10 codes with MDC, CC flags
│       ├── c63proc.dbf      # Procedures with OR flags
│       ├── c63drg.dbf       # DRG definitions with RW
│       └── c63ccex.dbf      # CC exclusion rules
└── 6.3.4/
    └── ...
```

### Adding New Versions

When TCMC releases a new DRG version:

1. Download the TGrp zip file from https://www.tcmc.or.th/tdrg
2. Run: `thai-drg-grouper add --version 6.4 --source TGrp64.zip --set-default`
3. The manager will extract DBF files and create version.json

The grouper auto-detects DBF files by naming pattern (i10, proc, drg, ccex).

## Grouping Algorithm Flow

1. **Input Validation**: Check PDX format, age, sex, LOS
2. **ICD-10 Lookup**: Get MDC, PDC, CC flags from i10.dbf
3. **Procedure Analysis**: Detect OR procedures from proc.dbf
4. **CC/MCC Detection**:
   - Check secondary diagnoses for CC/MCC flags
   - Apply CC exclusion rules (ccex.dbf)
   - Calculate PCL (Patient Complexity Level 0-4)
5. **DRG Selection**:
   - Filter by MDC + DC (disease cluster)
   - Match OR/non-OR, age, sex, PCL criteria
   - Select best matching DRG
6. **RW Adjustment**: Adjust RW based on LOS (daycase, normal, long stay)

## Project Structure Notes

- **DBF File Reading**: Uses `dbfread` library (not DBF writer, read-only)
- **Encoding**: DBF files use Windows-874 (Thai) encoding
- **Lazy Loading**: Manager only loads groupers when needed to save memory
- **Version Comparison**: `group_all_versions()` runs same case across all versions
- **Error Handling**: Returns `GrouperResult` with `is_valid=False` and error messages

## Configuration Files

- `pyproject.toml`: Package metadata, dependencies, build config, tool settings
- `docker-compose.yml`: Single-service setup for API
- `Dockerfile`: Multi-stage build (currently single stage)
- `.github/workflows/ci.yml`: CI pipeline

## API Authentication

Currently no authentication implemented. Add authentication middleware in `api.py` if deploying to production.

## Database Format

DBF files are dBASE III/IV format (legacy format from DOS era). Thai TCMC uses these for official distribution. The grouper reads them directly without conversion.

## Important Constraints

- This is NOT the official grouper - it's an implementation based on DBF files
- Always validate results against official TGrp software before production use
- DRG versions have different logic - cannot mix DBF files across versions
- Thai ICD-10-TM codes may differ from WHO ICD-10
