# Thai DRG Grouper

[![PyPI version](https://badge.fury.io/py/thai-drg-grouper.svg)](https://pypi.org/project/thai-drg-grouper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Multi-version Thai DRG (Diagnosis Related Group) Grouper for Linux, Mac, and Windows.

> 🇹🇭 **[เอกสารภาษาไทย (Thai Documentation)](th/index.md)** - Complete documentation in Thai with detailed examples

## Features

- ✅ **Cross-platform** - Works on Linux, Mac, Windows
- ✅ **Multi-version** - Run multiple DRG versions simultaneously
- ✅ **Easy updates** - Add new versions with one command
- ✅ **REST API** - FastAPI included with auto-generated docs
- ✅ **CLI** - Full-featured command-line interface
- ✅ **Batch processing** - Process multiple cases at once
- ✅ **Version comparison** - Compare results across versions

## Quick Start

### Installation

```bash
pip install thai-drg-grouper

# With API support
pip install thai-drg-grouper[api]
```

### Python Library

```python
from thai_drg_grouper import ThaiDRGGrouperManager

# Initialize with versions directory
manager = ThaiDRGGrouperManager('./data/versions')

# Group a case (uses default version)
result = manager.group_latest(
    pdx='S82201D',        # Principal diagnosis
    sdx=['E119', 'I10'],  # Secondary diagnoses
    procedures=['7936'],   # ICD-9-CM procedures
    age=25,
    sex='M',
    los=5
)

print(f"DRG: {result.drg}")      # 08172
print(f"RW: {result.rw}")        # 5.0602
print(f"AdjRW: {result.adjrw}")  # 5.0602
```

### CLI

```bash
# List installed versions
thai-drg-grouper list

# Group a case
thai-drg-grouper group --pdx S82201D --sdx E119,I10 --proc 7936 --los 5

# Start API server
thai-drg-grouper serve --port 8000
```

### REST API

```bash
# Start server
thai-drg-grouper serve --port 8000

# Or with uvicorn
uvicorn thai_drg_grouper.api:app --port 8000

# Or with Docker
docker run -p 8000:8000 ghcr.io/aegisx-platform/thai-drg-grouper:latest
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

## Documentation

- **[Getting Started](getting-started/installation.md)** - Installation and configuration
- **[Thai Documentation](th/index.md)** - Complete documentation in Thai
- **[Thai Examples](th/examples/basic.md)** - 10 detailed usage examples in Thai
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (run server first)
- **[Contributing](contributing.md)** - How to contribute
- **[Changelog](changelog.md)** - Version history

## Support This Project

If you find this project helpful, consider supporting its development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/sathit)

Your support helps maintain and improve this project! ☕

## Disclaimer

This is an implementation based on DBF files from Thai CaseMix Centre, **not the official grouper**. Always validate results against official TGrp software before production use.

## License

MIT License - See [LICENSE](https://github.com/aegisx-platform/thai-drg-grouper/blob/main/LICENSE) for details.
