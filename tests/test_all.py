"""
Comprehensive tests for SHACL Transformer
"""

import pytest
import tempfile
import os
from pathlib import Path


# Fixtures

@pytest.fixture
def sample_json_schema():
    return {
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "email"]
    }


@pytest.fixture
def sample_json_data():
    return {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }


@pytest.fixture
def sample_rdf_turtle():
    return """
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    ex:person1 a ex:Person ;
        ex:name "Alice Smith" ;
        ex:age 25 ;
        ex:email "alice@example.com" .
    """


# Tests for utils

def test_infer_format_from_extension():
    from shacl_transformer.utils import infer_format_from_extension
    
    assert infer_format_from_extension(Path("test.ttl")) == "turtle"
    assert infer_format_from_extension(Path("test.owl")) == "xml"
    assert infer_format_from_extension(Path("test.json")) == "json"
    assert infer_format_from_extension(Path("test.xsd")) == "xml"


def test_normalize_rdf_format():
    from shacl_transformer.utils import normalize_rdf_format
    
    assert normalize_rdf_format("ttl") == "turtle"
    assert normalize_rdf_format("rdf") == "xml"
    assert normalize_rdf_format("jsonld") == "json-ld"


# Tests for convert_schema

def test_convert_schema_json_to_shacl_noai(sample_json_schema, tmp_path):
    """Test JSON Schema conversion without AI"""
    from shacl_transformer import convert_schema
    import json
    
    # Create temp file
    input_file = tmp_path / "schema.json"
    output_file = tmp_path / "output.ttl"
    
    with open(input_file, 'w') as f:
        json.dump(sample_json_schema, f)
    
    # Convert without AI
    result = convert_schema(
        input_file=str(input_file),
        output_file=str(output_file),
        input_format="json-schema",
        use_ai=False
    )
    
    # Check output file exists
    assert output_file.exists()
    
    # Verify it's valid Turtle
    from rdflib import Graph
    g = Graph()
    g.parse(str(output_file), format='turtle')
    assert len(g) > 0


def test_convert_schema_returns_string():
    """Test that convert_schema returns string when output_file is None"""
    from shacl_transformer import convert_schema
    import json
    import tempfile
    
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema, f)
        temp_file = f.name
    
    try:
        result = convert_schema(
            input_file=temp_file,
            output_file=None,
            input_format="json-schema",
            use_ai=False
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "@prefix" in result
    finally:
        os.unlink(temp_file)


# Tests for create_schema

def test_create_schema_from_json(sample_json_data, tmp_path):
    """Test schema creation from JSON data"""
    from shacl_transformer import create_schema
    import json
    
    input_file = tmp_path / "data.json"
    output_file = tmp_path / "schema.ttl"
    
    with open(input_file, 'w') as f:
        json.dump(sample_json_data, f)
    
    result = create_schema(
        source_data=str(input_file),
        output_file=str(output_file),
        use_ai=False
    )
    
    assert output_file.exists()


# Tests for validate_data

def test_validate_data_format_markdown(tmp_path, sample_rdf_turtle):
    """Test validation with markdown output"""
    from shacl_transformer import validate_data
    from rdflib import Graph
    
    # Create simple data and schema
    data_file = tmp_path / "data.ttl"
    schema_file = tmp_path / "schema.ttl"
    
    with open(data_file, 'w') as f:
        f.write(sample_rdf_turtle)
    
    # Simple schema
    simple_schema = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix ex: <http://example.org/> .
    
    ex:PersonShape a sh:NodeShape ;
        sh:targetClass ex:Person ;
        sh:property [
            sh:path ex:name ;
            sh:datatype xsd:string ;
            sh:minCount 1 ;
        ] .
    """
    
    with open(schema_file, 'w') as f:
        f.write(simple_schema)
    
    report = validate_data(
        data_file=str(data_file),
        schema_file=str(schema_file),
        output_format="markdown"
    )
    
    assert isinstance(report, str)
    assert "Validation Report" in report or "conforms" in report.lower()


# Tests for non_ai_transformer

def test_json_type_to_xsd():
    """Test JSON type mapping"""
    from shacl_transformer.non_ai_transformer import NonAITransformer
    from rdflib import XSD
    
    transformer = NonAITransformer()
    
    assert transformer._json_type_to_xsd('string') == XSD.string
    assert transformer._json_type_to_xsd('integer') == XSD.integer
    assert transformer._json_type_to_xsd('number') == XSD.decimal
    assert transformer._json_type_to_xsd('boolean') == XSD.boolean


# Integration tests

def test_full_workflow_json_to_validation(tmp_path, sample_json_schema, sample_json_data):
    """Test complete workflow: JSON Schema -> SHACL -> validate data"""
    from shacl_transformer import convert_schema, apply_schema, validate_data
    import json
    
    # Files
    json_schema_file = tmp_path / "schema.json"
    json_data_file = tmp_path / "data.json"
    shacl_schema_file = tmp_path / "shacl.ttl"
    rdf_data_file = tmp_path / "data.ttl"
    
    # Write files
    with open(json_schema_file, 'w') as f:
        json.dump(sample_json_schema, f)
    with open(json_data_file, 'w') as f:
        json.dump(sample_json_data, f)
    
    # Convert schema
    convert_schema(
        input_file=str(json_schema_file),
        output_file=str(shacl_schema_file),
        input_format="json-schema",
        use_ai=False
    )
    
    assert shacl_schema_file.exists()
    
    # Apply schema
    apply_schema(
        source_data=str(json_data_file),
        schema_file=str(shacl_schema_file),
        output_file=str(rdf_data_file),
        use_ai=False
    )
    
    assert rdf_data_file.exists()
    
    # Validate
    report = validate_data(
        data_file=str(rdf_data_file),
        schema_file=str(shacl_schema_file),
        output_format="json"
    )
    
    assert 'conforms' in report
    # May or may not conform depending on transformation


# Error handling tests

def test_convert_schema_file_not_found():
    """Test error handling for missing file"""
    from shacl_transformer import convert_schema
    
    with pytest.raises(FileNotFoundError):
        convert_schema(
            input_file="nonexistent_file.owl",
            output_file="output.ttl"
        )


def test_validate_data_invalid_format():
    """Test error handling for invalid format"""
    from shacl_transformer import validate_data
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ttl') as f:
        f.write("@prefix ex: <http://example.org/> .")
        f.flush()
        
        with pytest.raises(ValueError):
            validate_data(
                data_file=f.name,
                schema_file=f.name,
                output_format="invalid_format"
            )


# Mark tests that require AI

@pytest.mark.skipif(
    not os.environ.get('ANTHROPIC_API_KEY'),
    reason="ANTHROPIC_API_KEY not set"
)
def test_convert_schema_with_ai():
    """Test AI-powered conversion (requires API key)"""
    from shacl_transformer import convert_schema
    import json
    import tempfile
    
    schema = {"title": "Test", "type": "object", "properties": {"name": {"type": "string"}}}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(schema, f)
        temp_file = f.name
    
    try:
        result = convert_schema(
            input_file=temp_file,
            output_file=None,
            input_format="json-schema",
            use_ai=True
        )
        
        assert isinstance(result, str)
        assert "@prefix" in result
    finally:
        os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
