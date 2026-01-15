# SHACL Transformer - Project Summary

## Overview

SHACL Transformer is a comprehensive Python library implementing a dual-stage transformation architecture for SHACL 1.2 schema conversion, generation, validation, and data transformation.

### Architecture

```
Input (Schema/Data/Parameters)
        ↓
  AI Transformer (Claude API)
        ↓
  Non-AI Transformer (RDFLib/pySHACL)
        ↓
   Output (SHACL/RDF/Reports)
```

## Project Structure

```
shacl-transformer/
├── shacl_transformer/           # Main package
│   ├── __init__.py             # Package initialization & exports
│   ├── convert_schema.py       # Schema conversion function
│   ├── create_schema.py        # Schema generation function
│   ├── apply_schema.py         # Data transformation function
│   ├── validate_data.py        # Validation function
│   ├── generate_data.py        # Data generation function
│   ├── ai_transformer.py       # AI-powered transformer (Claude)
│   ├── non_ai_transformer.py   # Deterministic transformer
│   ├── utils.py                # Utility functions
│   └── cli.py                  # Command-line interface
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_convert_schema.py
│   └── test_all.py             # Comprehensive tests
├── examples/                    # Usage examples
│   ├── usage_examples.py
│   └── example_json_schema.json
├── docs/                        # Documentation
│   ├── API.md                  # API reference
│   └── ARCHITECTURE.md         # Architecture details
├── .github/workflows/           # CI/CD
│   └── tests.yml               # GitHub Actions workflow
├── README.md                    # Main documentation
├── USAGE_GUIDE.md              # Complete usage guide
├── PROJECT_SUMMARY.md          # This file
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
├── setup.py                    # Package setup
├── requirements.txt            # Dependencies
├── pytest.ini                  # Pytest configuration
└── .gitignore                  # Git ignore rules
```

## Core Functions

### 1. convert_schema()

**Purpose:** Convert various schema formats to SHACL 1.2

**Inputs:**
- OWL (RDF/XML, Turtle)
- XSD (XML Schema)
- JSON Schema
- Database schemas (SQL DDL)
- SHACL 1.0/1.1

**Outputs:**
- SHACL 1.2 (Turtle, JSON-LD)

**Key Features:**
- SHACL Core constraints
- Node expressions (sh:and, sh:or, sh:not)
- SHACL Rules for calculated properties
- SKOS concepts for enumerations
- UI annotations (sh:group, sh:order)
- Comprehensive sh:description

**Usage:**
```python
from shacl_transformer import convert_schema

shacl = convert_schema(
    input_file="ontology.owl",
    output_file="schema.ttl",
    use_ai=True
)
```

### 2. create_schema()

**Purpose:** Generate SHACL schemas from data documents

**Inputs:**
- RDF (Turtle, RDF/XML, N-Triples, JSON-LD)
- JSON
- XML
- CSV
- Office formats (DOCX, XLSX, PPTX)
- PDF (with text extraction)
- Images (with OCR)

**Outputs:**
- SHACL 1.2 schema

**Key Features:**
- Infers constraints from data
- Extends existing schemas
- Generates enumerations as SKOS
- Creates appropriate datatypes
- Infers cardinality

**Usage:**
```python
from shacl_transformer import create_schema

schema = create_schema(
    source_data="data.json",
    output_file="schema.ttl",
    base_schema="base_schema.ttl"  # Optional
)
```

### 3. apply_schema()

**Purpose:** Transform data to conform to SHACL schema

**Inputs:**
- Source data (JSON, XML, CSV, etc.)
- SHACL schema

**Outputs:**
- RDF data conforming to schema

**Key Features:**
- Intelligent type conversion
- IRI generation
- Structure mapping
- Validation during transformation

**Usage:**
```python
from shacl_transformer import apply_schema

rdf = apply_schema(
    source_data="input.json",
    schema_file="schema.ttl",
    output_file="output.ttl"
)
```

### 4. validate_data()

**Purpose:** Validate RDF data against SHACL schema

**Inputs:**
- RDF data
- SHACL schema

**Outputs:**
- Validation report (Markdown, RDF, JSON)

**Key Features:**
- Full SHACL validation
- Detailed violation reports
- Multiple output formats
- RDFS/OWL inference support

**Usage:**
```python
from shacl_transformer import validate_data

report = validate_data(
    data_file="data.ttl",
    schema_file="schema.ttl",
    output_format="markdown"
)
```

### 5. generate_data()

**Purpose:** Generate synthetic data from schema

**Inputs:**
- SHACL schema
- Natural language prompt
- Count of instances

**Outputs:**
- Generated RDF data

**Key Features:**
- AI-powered generation
- Realistic data
- Schema-compliant
- Customizable via prompts

**Usage:**
```python
from shacl_transformer import generate_data

data = generate_data(
    schema_file="person_schema.ttl",
    prompt="Create diverse people aged 25-65",
    count=20,
    output_file="sample_data.ttl"
)
```

## AI Transformer

**Technology:** Claude (Anthropic) API

**Capabilities:**
- Semantic understanding of schemas
- Context-aware transformations
- Natural language interpretation
- Intelligent schema mapping
- Realistic data generation

**Configuration:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## Non-AI Transformer

**Technology:** RDFLib + pySHACL

**Capabilities:**
- SHACL validation
- RDF parsing/serialization
- Deterministic transformations
- SPARQL query execution
- Format conversions

**Advantages:**
- No API dependencies
- Predictable results
- Fast processing
- Standards-compliant

## Installation

```bash
# From PyPI (when published)
pip install shacl-transformer

# From source
git clone https://github.com/yourusername/shacl-transformer.git
cd shacl-transformer
pip install -e .

# With all optional dependencies
pip install -e .[all]

# Development mode
pip install -e .[dev]
```

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=shacl_transformer

# Run specific test
pytest tests/test_convert_schema.py -v

# Skip AI tests (no API key needed)
pytest tests/ -m "not ai"
```

## Command-Line Interface

```bash
# Convert schema
shacl-convert input.owl output.ttl

# Create schema from data
shacl-create data.json schema.ttl --base-schema existing.ttl

# Validate data
shacl-validate data.ttl schema.ttl --output report.md --format markdown
```

## Dependencies

### Core
- rdflib >= 7.0.0 (RDF processing)
- pyshacl >= 0.25.0 (SHACL validation)
- anthropic >= 0.7.0 (AI features)
- requests >= 2.31.0

### Data Processing
- pandas >= 2.0.0
- openpyxl >= 3.1.0 (Excel files)
- python-docx >= 1.1.0 (Word documents)
- python-pptx >= 0.6.23 (PowerPoint)
- PyPDF2 >= 3.0.0 (PDF extraction)
- Pillow >= 10.0.0 (Images)
- pytesseract >= 0.3.10 (OCR)

### Development
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- flake8 >= 6.0.0
- mypy >= 1.5.0

## SHACL 1.2 Compliance

This library generates schemas compliant with:
https://www.w3.org/TR/shacl12-core/

**Features:**
- All SHACL Core constraints
- Node expressions (sh:and, sh:or, sh:not, sh:xone)
- Property shapes with sh:path
- SHACL Rules (SPARQLRule, TripleRule)
- UI annotations (sh:group, sh:order, sh:defaultValue)
- Code identifiers (sh:codeIdentifier)
- SKOS integration
- Comprehensive documentation (sh:name, sh:description)

**Best Practices:**
- All shapes use IRIs (no blank nodes)
- Property shapes include class names in IRI
- Enumerations converted to SKOS ConceptSchemes
- Triple compatibility (sh:classShape + sh:NodeShape + sh:targetClass)
- Complete sh:description for all shapes

## Use Cases

### 1. Schema Migration
Convert legacy schemas (OWL, XSD) to modern SHACL 1.2

### 2. Data Validation
Validate RDF data against business rules expressed in SHACL

### 3. API Development
Generate SHACL schemas from JSON Schema for semantic APIs

### 4. Data Integration
Transform heterogeneous data to conform to standard schemas

### 5. Testing
Generate realistic test data from schemas

### 6. Documentation
Create well-documented schemas with AI assistance

## Performance

### AI Mode
- **Speed:** 2-10 seconds per transformation
- **Quality:** High semantic understanding
- **Use Case:** Complex schemas, ambiguous inputs

### Non-AI Mode
- **Speed:** < 1 second per transformation
- **Quality:** Rules-based, predictable
- **Use Case:** Simple conversions, high throughput

## Roadmap

### v1.1
- [ ] Additional schema formats (Protobuf, Avro)
- [ ] Streaming support for large files
- [ ] Caching of AI transformations
- [ ] Enhanced CLI with interactive mode

### v1.2
- [ ] GUI interface
- [ ] Schema visualization
- [ ] Batch processing
- [ ] Custom AI model support

### v2.0
- [ ] Real-time validation API
- [ ] Schema registry integration
- [ ] Multi-language support
- [ ] Advanced analytics

## Support

- **Documentation:** See docs/ directory
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@example.com

## License

MIT License - see LICENSE file

## Citation

```bibtex
@software{shacl_transformer,
  title = {SHACL Transformer: AI-Powered Schema Transformation},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/yourusername/shacl-transformer},
  version = {1.0.0}
}
```

## Acknowledgments

- Built on RDFLib and pySHACL
- Powered by Claude (Anthropic)
- Based on SHACL 1.2 W3C Specification
- Inspired by semantic web community

## Quick Start

```python
# 1. Install
pip install shacl-transformer

# 2. Set API key
import os
os.environ['ANTHROPIC_API_KEY'] = 'your-key'

# 3. Convert schema
from shacl_transformer import convert_schema
shacl = convert_schema("ontology.owl", "schema.ttl")

# 4. Validate data
from shacl_transformer import validate_data
report = validate_data("data.ttl", "schema.ttl")

print(f"Valid: {report['conforms']}")
```

## Complete Example Workflow

```python
from shacl_transformer import (
    convert_schema,
    generate_data,
    validate_data
)

# Step 1: Convert JSON Schema to SHACL
print("Converting schema...")
shacl_schema = convert_schema(
    input_file="api_schema.json",
    output_file="shacl_schema.ttl",
    input_format="json-schema"
)

# Step 2: Generate sample data
print("Generating sample data...")
sample_data = generate_data(
    schema_file="shacl_schema.ttl",
    prompt="Create 20 realistic API records",
    count=20,
    output_file="sample_data.ttl"
)

# Step 3: Validate
print("Validating...")
report = validate_data(
    data_file="sample_data.ttl",
    schema_file="shacl_schema.ttl",
    output_file="report.md"
)

print(f"✓ Complete! Validation: {report['conforms']}")
```

## Troubleshooting

### Import Errors
```bash
pip install -e .[all]  # Install all dependencies
```

### API Key Issues
```python
import os
print(os.environ.get('ANTHROPIC_API_KEY'))  # Should not be None
```

### Validation Failures
```python
# Get detailed report
report = validate_data("data.ttl", "schema.ttl", output_format="json")
for violation in report['violations']:
    print(f"Error: {violation['message']}")
```

## Contact

- GitHub: https://github.com/yourusername/shacl-transformer
- Email: support@example.com
- Documentation: https://shacl-transformer.readthedocs.io
