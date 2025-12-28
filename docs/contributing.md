# Contributing

Thank you for your interest in contributing to Thai DRG Grouper! This document provides guidelines for contributing to the project.

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/thai-drg-grouper.git
cd thai-drg-grouper
```

### 2. Install Dependencies

```bash
pip install -e .[all]
```

### 3. Run Tests

```bash
pytest tests/ -v
```

## Development Workflow

### Code Style

We use `black` for formatting and `ruff` for linting:

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/
```

### Testing

Write tests for all new features:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=thai_drg_grouper --cov-report=html

# Run specific test
pytest tests/test_grouper.py::TestGrouper::test_group_fracture -v
```

### Documentation

Update documentation for new features:

```bash
# Build docs locally
mkdocs serve

# View at http://localhost:8000
```

## Pull Request Process

1. **Create a Branch**: `git checkout -b feature/your-feature-name`
2. **Make Changes**: Follow code style guidelines
3. **Add Tests**: Ensure test coverage for new code
4. **Update Docs**: Document new features
5. **Commit**: Use clear commit messages
6. **Push**: `git push origin feature/your-feature-name`
7. **Open PR**: Create pull request on GitHub

### Commit Message Guidelines

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test updates
- `chore:` Maintenance tasks
- `refactor:` Code refactoring

Example:
```
feat: add support for DRG version 6.5

- Add version 6.5 DBF file support
- Update version detection logic
- Add tests for version 6.5
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Reporting Issues

Use GitHub Issues to report bugs or request features:

- **Bug Report**: Describe the issue, steps to reproduce, expected vs actual behavior
- **Feature Request**: Describe the feature and use case
- **Question**: Ask questions about usage or implementation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
