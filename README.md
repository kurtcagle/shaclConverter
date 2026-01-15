# SHACL Transformer

A comprehensive Python library for converting, creating, applying, validating, and generating SHACL 1.2 compliant schemas and data.

## Overview

SHACL Transformer implements a dual-stage transformation architecture combining AI-powered semantic understanding with deterministic rule-based processing to handle schema transformations and data validation.

```
Schema + Parameters → AI Transformer → Non-AI Transformer → Output
                              ↓              ↑
                            Data ────────────┘
```

## Features

- **Convert Schema**: Transform OWL, XSD, JSON Schema, database schemas, and other formats to SHACL 1.2
- **Create Schema**: Generate SHACL 1.2 schemas from data documents (RDF, JSON, XML, PDF, images)
- **Apply Schema**: Map data to SHACL schemas with automatic transformation
- **Validate Data**: Comprehensive validation with detailed reports in RDF and Markdown
- **Generate Data**: AI-powered data generation based on schema and natural language prompts

## Installation

```bash
pip install shacl-transformer
```

Or install from source:

```bash
git clone https://github.com/yourusername/shacl-transformer.git
cd shacl-transformer
pip install -e .
```

## Quick Start

```python
from shacl_transformer import (
    convert_schema,
    create_schema,
    apply_schema,
    validate_data,
    generate_data
)

# Convert an OWL schema to SHACL 1.2
shacl_output = convert_schema(
    input_file="my_ontology.owl",
    output_format="turtle"
)

# Create a SHACL schema from data
new_schema = create_schema(
    source_data="my_data.json",
    output_file="generated_schema.ttl"
)

# Validate data against a schema
validation_report = validate_data(
    data_file="my_data.ttl",
    schema_file="my_schema.ttl",
    output_format="markdown"
)

# Generate sample data from schema
sample_data = generate_data(
    schema_file="my_schema.ttl",
    prompt="Create 10 person records with realistic names and ages",
    output_file="generated_data.ttl"
)
```

## Architecture

### AI Transformer
Uses Claude (Anthropic) API for:
- Semantic understanding of schemas and data
- Natural language prompt interpretation
- Intelligent schema mapping
- Data generation from descriptions

### Non-AI Transformer
Deterministic processing for:
- SHACL 1.2 validation rules
- RDF parsing and serialization
- Schema transformation rules
- Data format conversions

## Supported Formats

### Input Schemas
- OWL (RDF/XML, Turtle)
- SHACL 1.0/1.1
- XSD (XML Schema)
- JSON Schema
- Database schemas (SQL DDL)
- CSV with headers

### Input Data
- RDF (Turtle, RDF/XML, N-Triples, JSON-LD)
- JSON
- XML
- CSV
- Office formats (DOCX, XLSX, PPTX)
- PDF
- Images (OCR + extraction)

### Output Formats
- SHACL 1.2 (Turtle, JSON-LD)
- Validation reports (RDF, Markdown, JSON)
- Generated data (Turtle, JSON-LD)

## Key Features

### SHACL 1.2 Compliance
- Complete SHACL Core support
- Node expressions (sh:and, sh:or, sh:not, sh:xone)
- SHACL Rules (SPARQLRule, TripleRule)
- UI annotations (sh:group, sh:order, sh:defaultValue)
- Code identifiers for programmatic access

### SKOS Integration
- Automatic enumeration → SKOS conversion
- External vocabulary linking (Wikidata, DBpedia, etc.)
- Concept scheme generation
- Notation and preferred labels

### Provenance & Metadata
- Full dcterms annotations
- Transformation history tracking
- Source attribution
- Version control

## API Documentation

See [docs/API.md](docs/API.md) for complete API reference.

## Examples

See [examples/](examples/) directory for:
- Converting various schema formats
- Creating schemas from data
- Applying schemas to transform data
- Validating with detailed reports
- Generating synthetic data

## Development

### Running Tests

```bash
pytest tests/
```

### Building Documentation

```bash
cd docs
make html
```

## Requirements

- Python 3.8+
- rdflib >= 6.0.0
- pyshacl >= 0.20.0
- anthropic >= 0.7.0 (for AI features)
- requests >= 2.28.0

See [requirements.txt](requirements.txt) for complete list.

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{shacl_transformer,
  title = {SHACL Transformer: AI-Powered Schema Transformation and Validation},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/yourusername/shacl-transformer}
}
```

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/shacl-transformer/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/shacl-transformer/discussions)

## Acknowledgments

Built on the foundations of:
- [rdflib](https://github.com/RDFLib/rdflib)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [Anthropic Claude API](https://www.anthropic.com/)

Based on SHACL 1.2 specification: https://www.w3.org/TR/shacl12-core/
