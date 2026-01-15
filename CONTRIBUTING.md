# Contributing to SHACL Transformer

Thank you for considering contributing to SHACL Transformer!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/shacl-transformer.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature`
8. Create a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/shacl-transformer.git
cd shacl-transformer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8
- Use Black for formatting: `black shacl_transformer tests`
- Use isort for imports: `isort shacl_transformer tests`
- Run flake8: `flake8 shacl_transformer tests`
- Add type hints where possible

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use pytest fixtures for reusable test components

## Documentation

- Update README.md for new features
- Add docstrings to all functions (Google style)
- Update USAGE_GUIDE.md with examples
- Update API.md for API changes

## Pull Request Guidelines

1. Update CHANGELOG.md
2. Add tests for new features
3. Ensure CI passes
4. Update documentation
5. Keep commits atomic and well-described
6. Reference related issues

## Reporting Bugs

Use GitHub Issues with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Example code/data if applicable

## Feature Requests

- Check existing issues first
- Provide use cases
- Explain why feature is needed
- Consider implementation approach

## Questions

- Use GitHub Discussions for questions
- Check documentation first
- Provide context and examples
