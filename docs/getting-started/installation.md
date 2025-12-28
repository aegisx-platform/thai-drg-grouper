# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation Methods

### PyPI (Recommended)

Install from Python Package Index:

```bash
pip install thai-drg-grouper
```

### With Optional Dependencies

Install with API support (FastAPI + Uvicorn):

```bash
pip install thai-drg-grouper[api]
```

Install with development tools:

```bash
pip install thai-drg-grouper[dev]
```

Install with documentation tools:

```bash
pip install thai-drg-grouper[docs]
```

Install everything:

```bash
pip install thai-drg-grouper[all]
```

### From Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/aegisx-platform/thai-drg-grouper.git
cd thai-drg-grouper
pip install -e .[all]
```

## Verification

Verify the installation:

```bash
thai-drg-grouper --version
```

List available commands:

```bash
thai-drg-grouper --help
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Start grouping cases
- [Configuration](configuration.md) - Set up DRG versions
