"""
Create Schema - Generate SHACL 1.2 schemas from data documents
"""

from typing import Union, Optional, BinaryIO, TextIO
from pathlib import Path
from rdflib import Graph

from .ai_transformer import AITransformer
from .non_ai_transformer import NonAITransformer
from .utils import (
    load_input, save_output, infer_format_from_extension,
    extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
)


def create_schema(
    source_data: Union[str, Path, BinaryIO, TextIO, bytes],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    base_schema: Union[str, Path, BinaryIO, TextIO, None] = None,
    data_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None
) -> Union[str, None]:
    """
    Generate SHACL 1.2 schema from data documents.
    
    Can create new schema or extend existing base schema.
    Supports: RDF, JSON, XML, CSV, Office formats, PDF, images.
    
    Args:
        source_data: Source data file/stream
        output_file: Output file/stream (None returns as string)
        base_schema: Optional base SHACL schema to extend
        data_format: Data format (auto-detected if None)
        output_format: Output format (turtle, jsonld)
        use_ai: Use AI for schema generation
        api_key: Anthropic API key
        
    Returns:
        SHACL schema as string if output_file is None
        
    Example:
        >>> # Create schema from JSON data
        >>> schema = create_schema("data.json", "schema.ttl")
        
        >>> # Extend existing schema
        >>> schema = create_schema(
        ...     source_data="new_data.json",
        ...     base_schema="existing_schema.ttl",
        ...     output_file="extended_schema.ttl"
        ... )
        
        >>> # Create from PDF
        >>> schema = create_schema("document.pdf", output_file=None)
    """
    # Infer format
    if data_format is None and isinstance(source_data, (str, Path)):
        data_format = infer_format_from_extension(Path(source_data))
    
    # Load data
    if data_format == 'pdf':
        data_text = extract_text_from_pdf(source_data)
    elif data_format == 'docx':
        data_text = extract_text_from_docx(source_data)
    elif data_format in ['image', 'png', 'jpg', 'jpeg']:
        data_text = extract_text_from_image(source_data)
    else:
        data_input = load_input(source_data, data_format)
        if isinstance(data_input, Graph):
            data_text = data_input.serialize(format='turtle')
        elif isinstance(data_input, dict):
            import json
            data_text = json.dumps(data_input, indent=2)
        else:
            data_text = str(data_input)
    
    # Load base schema if provided
    base_schema_text = None
    if base_schema is not None:
        base_input = load_input(base_schema, 'turtle')
        if isinstance(base_input, Graph):
            base_schema_text = base_input.serialize(format='turtle')
    
    # Generate schema
    if use_ai:
        ai = AITransformer(api_key)
        shacl_text = ai.analyze_data_for_schema(
            data_text,
            data_format or 'text',
            base_schema_text
        )
        shapes_graph = Graph()
        shapes_graph.parse(data=shacl_text, format='turtle')
    else:
        non_ai = NonAITransformer()
        # Basic schema generation from data structure
        if isinstance(data_input, dict):
            # Infer schema from JSON structure
            inferred_schema = _infer_schema_from_json(data_input)
            shapes_graph = non_ai.convert_json_schema_to_shacl(inferred_schema)
        else:
            raise ValueError("Non-AI schema creation requires structured data (JSON)")
    
    # Save output
    result = save_output(shapes_graph, output_file, output_format)
    return result


def _infer_schema_from_json(data: dict) -> dict:
    """Infer JSON Schema from JSON data."""
    schema = {
        'type': 'object',
        'properties': {},
        'required': []
    }
    
    for key, value in data.items():
        prop_type = type(value).__name__
        type_map = {
            'str': 'string',
            'int': 'integer',
            'float': 'number',
            'bool': 'boolean',
            'list': 'array',
            'dict': 'object'
        }
        schema['properties'][key] = {
            'type': type_map.get(prop_type, 'string')
        }
    
    return schema
