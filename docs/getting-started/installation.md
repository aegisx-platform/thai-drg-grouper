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

## Configuration

### Environment Variables

The API server can be configured using environment variables. Create a `.env` file in your working directory:

```bash
# Copy the example file
cp .env.example .env
```

Available configuration options:

#### CORS Configuration

Configure allowed origins for API requests (comma-separated):

```bash
# Development (default)
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# Production
CORS_ORIGINS=https://your-app.example.com,https://another-app.example.com
```

Default origins:
- `http://localhost:4200` - Angular development server
- `http://localhost:3000` - React/Vite development server

#### Server Configuration

```bash
# Server host and port (optional)
HOST=0.0.0.0
PORT=8000
```

### Example .env File

```bash
# CORS Configuration
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# Server Configuration
# HOST=0.0.0.0
# PORT=8000
```

## Next Steps

- Start grouping cases with the Python library or CLI
- Set up DRG versions using `thai-drg-grouper download`
