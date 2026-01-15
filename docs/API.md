# API Reference

## Core Functions

### convert_schema()

Convert various schema formats to SHACL 1.2.

```python
convert_schema(
    input_file: Union[str, Path, BinaryIO, TextIO, bytes],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    input_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None,
    parameters: Optional[dict] = None
) -> Union[str, None]
```

**Supported Input Formats:**
- OWL (RDF/XML, Turtle)
- XSD (XML Schema)
- JSON Schema
- Database schemas (SQL DDL)
- SHACL 1.0/1.1 (upgrade to 1.2)

**Example:**
```python
from shacl_transformer import convert_schema

# Convert OWL to SHACL
shacl = convert_schema(
    input_file="ontology.owl",
    output_file="schema.ttl"
)

# Get as string
shacl_str = convert_schema(
    input_file="schema.xsd",
    output_file=None
)
```

---

### create_schema()

Generate SHACL 1.2 schemas from data documents.

```python
create_schema(
    source_data: Union[str, Path, BinaryIO, TextIO, bytes],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    base_schema: Union[str, Path, BinaryIO, TextIO, None] = None,
    data_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None
) -> Union[str, None]
```

**Supported Data Formats:**
- RDF (Turtle, RDF/XML, N-Triples, JSON-LD)
- JSON
- XML
- CSV
- Office formats (DOCX, XLSX, PPTX)
- PDF
- Images (with OCR)

**Example:**
```python
# Create schema from JSON data
schema = create_schema(
    source_data="data.json",
    output_file="schema.ttl"
)

# Extend existing schema
extended = create_schema(
    source_data="new_data.json",
    base_schema="existing_schema.ttl",
    output_file="extended_schema.ttl"
)
```

---

### apply_schema()

Map data to SHACL schemas.

```python
apply_schema(
    source_data: Union[str, Path, BinaryIO, TextIO, bytes],
    schema_file: Union[str, Path, BinaryIO, TextIO],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    data_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None
) -> Union[str, None]
```

**Example:**
```python
# Transform JSON to RDF following schema
rdf_data = apply_schema(
    source_data="input.json",
    schema_file="schema.ttl",
    output_file="output.ttl"
)
```

---

### validate_data()

Validate data against SHACL schemas.

```python
validate_data(
    data_file: Union[str, Path, BinaryIO, TextIO],
    schema_file: Union[str, Path, BinaryIO, TextIO],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    output_format: str = "markdown",
    inference: str = "rdfs"
) -> Union[Dict[str, Any], str, None]
```

**Output Formats:**
- `markdown`: Human-readable validation report
- `turtle`: RDF validation results
- `json`: Structured validation results

**Example:**
```python
# Get markdown report
report = validate_data(
    data_file="my_data.ttl",
    schema_file="schema.ttl",
    output_format="markdown"
)
print(report)

# Save to file
validate_data(
    data_file="data.ttl",
    schema_file="schema.ttl",
    output_file="validation_report.md"
)
```

---

### generate_data()

Generate sample data from schemas.

```python
generate_data(
    schema_file: Union[str, Path, BinaryIO, TextIO],
    prompt: str,
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    count: int = 10,
    output_format: str = "turtle",
    api_key: Optional[str] = None
) -> Union[str, None]
```

**Example:**
```python
# Generate person data
data = generate_data(
    schema_file="person_schema.ttl",
    prompt="Create diverse people from different countries with ages 25-65",
    count=20,
    output_file="sample_people.ttl"
)
```

---

## Configuration

### API Key

Set Anthropic API key for AI features:

```python
import os
os.environ['ANTHROPIC_API_KEY'] = 'your-api-key'
```

Or pass directly:

```python
convert_schema("schema.owl", api_key="your-api-key")
```

### AI vs Non-AI Mode

```python
# AI-powered (default)
result = convert_schema("schema.owl", use_ai=True)

# Deterministic rules only
result = convert_schema("schema.owl", use_ai=False)
```

---

## Error Handling

```python
try:
    schema = convert_schema("input.owl")
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid format: {e}")
except Exception as e:
    print(f"Conversion failed: {e}")
```
