# SHACL Transformer - Complete Usage Guide

## Installation

```bash
pip install shacl-transformer
```

Or from source:
```bash
git clone https://github.com/yourusername/shacl-transformer.git
cd shacl-transformer
pip install -e .
```

## Configuration

### Set API Key for AI Features

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or in Python:
```python
import os
os.environ['ANTHROPIC_API_KEY'] = 'your-api-key'
```

## Usage Examples

### 1. Convert Schema (OWL/XSD/JSON Schema → SHACL 1.2)

#### Convert OWL to SHACL

```python
from shacl_transformer import convert_schema

# AI-powered conversion (recommended)
shacl = convert_schema(
    input_file="my_ontology.owl",
    output_file="generated_schema.ttl",
    use_ai=True
)

# Deterministic conversion (no API key needed)
shacl = convert_schema(
    input_file="my_ontology.owl",
    output_file="generated_schema.ttl",
    use_ai=False
)
```

#### Convert JSON Schema to SHACL

```python
# From file
convert_schema(
    input_file="api_schema.json",
    output_file="api_shapes.ttl",
    input_format="json-schema"
)

# From stream
import io
json_stream = io.StringIO('{"type": "object", ...}')
result = convert_schema(
    input_file=json_stream,
    input_format="json-schema",
    output_file=None  # Returns as string
)
```

#### Convert XSD to SHACL

```python
convert_schema(
    input_file="database_schema.xsd",
    output_file="db_shapes.ttl"
)
```

### 2. Create Schema from Data

#### Create from JSON Data

```python
from shacl_transformer import create_schema

# Create new schema
schema = create_schema(
    source_data="sample_data.json",
    output_file="inferred_schema.ttl"
)

# Extend existing schema
extended = create_schema(
    source_data="additional_data.json",
    base_schema="existing_schema.ttl",
    output_file="extended_schema.ttl"
)
```

#### Create from PDF Document

```python
# Extracts text and generates schema
schema = create_schema(
    source_data="specification.pdf",
    output_file="spec_schema.ttl",
    data_format="pdf"
)
```

#### Create from Office Documents

```python
# From DOCX
schema = create_schema(
    source_data="requirements.docx",
    output_file="requirements_schema.ttl"
)

# From XLSX
schema = create_schema(
    source_data="data_dictionary.xlsx",
    output_file="dictionary_schema.ttl"
)
```

#### Create from Image (OCR)

```python
# Requires pytesseract
schema = create_schema(
    source_data="diagram.png",
    output_file="diagram_schema.ttl",
    data_format="image"
)
```

### 3. Apply Schema to Data

#### Transform JSON to RDF

```python
from shacl_transformer import apply_schema

# Transform and validate
rdf_data = apply_schema(
    source_data="input_data.json",
    schema_file="schema.ttl",
    output_file="output_data.ttl"
)
```

#### Transform CSV to RDF

```python
rdf_data = apply_schema(
    source_data="data.csv",
    schema_file="schema.ttl",
    output_file="data_rdf.ttl",
    data_format="csv"
)
```

#### Get Result as String

```python
rdf_string = apply_schema(
    source_data="data.json",
    schema_file="schema.ttl",
    output_file=None  # Returns as string
)
print(rdf_string)
```

### 4. Validate Data

#### Basic Validation

```python
from shacl_transformer import validate_data

# Get markdown report
report = validate_data(
    data_file="my_data.ttl",
    schema_file="schema.ttl",
    output_format="markdown"
)

print(report)
# Output:
# # SHACL Validation Report
# **Conforms:** False
# **Total Violations:** 2
# ...
```

#### Save Report to File

```python
validate_data(
    data_file="my_data.ttl",
    schema_file="schema.ttl",
    output_file="validation_report.md",
    output_format="markdown"
)
```

#### Get Structured Report

```python
# JSON format
report = validate_data(
    data_file="my_data.ttl",
    schema_file="schema.ttl",
    output_format="json"
)

print(f"Conforms: {report['conforms']}")
for violation in report['violations']:
    print(f"  - {violation['message']}")
```

#### RDF Validation Results

```python
# Get validation results as RDF
validate_data(
    data_file="my_data.ttl",
    schema_file="schema.ttl",
    output_file="validation_results.ttl",
    output_format="turtle"
)
```

### 5. Generate Sample Data

#### Generate from Schema and Prompt

```python
from shacl_transformer import generate_data

# Generate person data
data = generate_data(
    schema_file="person_schema.ttl",
    prompt="Create 10 diverse people with realistic names, ages 25-65, from different countries",
    count=10,
    output_file="sample_people.ttl"
)
```

#### Generate Complex Data

```python
# Generate product catalog
products = generate_data(
    schema_file="product_schema.ttl",
    prompt="""
    Create electronics products including:
    - 5 laptops with prices $800-2000
    - 5 smartphones with prices $400-1200
    - Include realistic brands, specifications, and release dates
    """,
    count=10,
    output_file="products.ttl"
)
```

#### Generate and Validate

```python
# Generate data
generated = generate_data(
    schema_file="schema.ttl",
    prompt="Create test data",
    output_file="test_data.ttl",
    count=5
)

# Validate generated data
report = validate_data(
    data_file="test_data.ttl",
    schema_file="schema.ttl"
)

if report['conforms']:
    print("Generated data is valid!")
```

## Advanced Usage

### Working with Streams

```python
import io
from shacl_transformer import convert_schema

# Input stream
owl_content = """
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
...
"""
input_stream = io.StringIO(owl_content)

# Convert
result = convert_schema(
    input_file=input_stream,
    input_format="turtle",
    output_file=None
)

print(result)
```

### Custom Parameters

```python
# Convert with custom parameters
result = convert_schema(
    input_file="schema.owl",
    output_file="schema.ttl",
    parameters={
        'include_rules': True,
        'ui_annotations': True,
        'generate_examples': True
    }
)
```

### Using Non-AI Mode

```python
# Faster, deterministic, no API key needed
result = convert_schema(
    input_file="schema.owl",
    output_file="schema.ttl",
    use_ai=False
)
```

## Complete Workflow Example

```python
from shacl_transformer import (
    convert_schema,
    generate_data,
    validate_data
)

# 1. Convert JSON Schema to SHACL
print("Converting JSON Schema to SHACL 1.2...")
shacl = convert_schema(
    input_file="api_schema.json",
    output_file="shacl_schema.ttl",
    input_format="json-schema"
)

# 2. Generate sample data
print("Generating sample data...")
sample_data = generate_data(
    schema_file="shacl_schema.ttl",
    prompt="Create 20 realistic API records with diverse values",
    count=20,
    output_file="sample_api_data.ttl"
)

# 3. Validate generated data
print("Validating data...")
report = validate_data(
    data_file="sample_api_data.ttl",
    schema_file="shacl_schema.ttl",
    output_file="validation_report.md"
)

print(f"Validation complete. Conforms: {report['conforms']}")
```

## Error Handling

```python
from shacl_transformer import convert_schema

try:
    result = convert_schema(
        input_file="schema.owl",
        output_file="output.ttl"
    )
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid format or parameters: {e}")
except ImportError as e:
    print(f"Missing dependency: {e}")
except Exception as e:
    print(f"Conversion failed: {e}")
```

## Command Line Interface

```bash
# Convert schema
shacl-convert input.owl output.ttl

# Create schema from data
shacl-create data.json schema.ttl

# Validate data
shacl-validate data.ttl schema.ttl --output report.md
```

## Performance Tips

1. **Use Non-AI mode for simple conversions** (OWL to SHACL)
2. **Batch similar operations** to reuse API connections
3. **Cache generated schemas** for repeated use
4. **Use streaming** for large files
5. **Validate incrementally** during development

## Troubleshooting

### API Key Issues

```python
import os
print(os.environ.get('ANTHROPIC_API_KEY'))  # Should not be None
```

### Format Detection

```python
# Explicitly specify format if auto-detection fails
convert_schema(
    input_file="ambiguous_file.txt",
    input_format="turtle",  # Force format
    output_file="output.ttl"
)
```

### Validation Failures

```python
# Get detailed report
report = validate_data(
    data_file="data.ttl",
    schema_file="schema.ttl",
    output_format="json"
)

for violation in report['violations']:
    print(f"Node: {violation['focusNode']}")
    print(f"Path: {violation['path']}")
    print(f"Message: {violation['message']}")
```

## Best Practices

1. **Version control your schemas** - Track changes in git
2. **Document schema intent** - Use sh:description liberally
3. **Test with sample data** - Generate and validate before production
4. **Use SKOS for enumerations** - Better than raw strings
5. **Include UI annotations** - Makes schemas more usable
6. **Validate early and often** - Catch issues during development
7. **Keep schemas modular** - Use base schemas and extend

## Integration Examples

### With Flask API

```python
from flask import Flask, request, jsonify
from shacl_transformer import validate_data
import tempfile

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.files['data']
    schema = request.files['schema']
    
    with tempfile.NamedTemporaryFile() as data_file, \
         tempfile.NamedTemporaryFile() as schema_file:
        
        data.save(data_file.name)
        schema.save(schema_file.name)
        
        report = validate_data(
            data_file=data_file.name,
            schema_file=schema_file.name,
            output_format="json"
        )
        
        return jsonify(report)
```

### With Pandas

```python
import pandas as pd
from shacl_transformer import create_schema
import json

# Create schema from DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [30, 25],
    'email': ['alice@example.com', 'bob@example.com']
})

# Convert to JSON
with open('temp_data.json', 'w') as f:
    json.dump(df.to_dict('records'), f)

# Generate schema
schema = create_schema(
    source_data='temp_data.json',
    output_file='dataframe_schema.ttl'
)
```

## Support

- Documentation: https://shacl-transformer.readthedocs.io/
- Issues: https://github.com/yourusername/shacl-transformer/issues
- Discussions: https://github.com/yourusername/shacl-transformer/discussions
