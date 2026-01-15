# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of SHACL Transformer
- `convert_schema()` function for schema conversion
- `create_schema()` function for schema generation from data
- `apply_schema()` function for data transformation
- `validate_data()` function for SHACL validation
- `generate_data()` function for synthetic data generation
- AI Transformer using Claude API
- Non-AI Transformer for deterministic processing
- Support for OWL, XSD, JSON Schema, database schemas
- Support for RDF, JSON, XML, CSV, Office formats, PDF, images
- Comprehensive documentation and examples
- Test suite with pytest
- CLI interface for common operations
- GitHub Actions CI/CD workflow

### Features
- SHACL 1.2 compliance
- SKOS conversion for enumerations
- UI annotations (sh:group, sh:order)
- SHACL Rules support
- Node expressions
- Multiple output formats (Turtle, JSON-LD)
- Stream and file I/O
- Validation reports (Markdown, RDF, JSON)
- Extensible architecture
