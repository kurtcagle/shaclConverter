"""
Convert Schema - Transform various schema formats to SHACL 1.2
"""

from typing import Union, Optional, BinaryIO, TextIO
from pathlib import Path
from rdflib import Graph

from .ai_transformer import AITransformer
from .non_ai_transformer import NonAITransformer
from .utils import load_input, save_output, infer_format_from_extension


def convert_schema(
    input_file: Union[str, Path, BinaryIO, TextIO, bytes],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    input_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None,
    parameters: Optional[dict] = None,
    prompt: Optional[str] = None
) -> Union[str, None]:
    """
    Convert various schema formats to SHACL 1.2 compliant schemas.
    
    Supports: OWL (RDF/XML, Turtle), XSD, JSON Schema, database schemas, etc.
    
    Args:
        input_file: Input schema file/stream
        output_file: Output file/stream (None returns as string)
        input_format: Input format (auto-detected if None)
        output_format: Output format (turtle, jsonld)
        use_ai: Use AI transformer for enhanced conversion
        api_key: Anthropic API key (for AI mode)
        parameters: Optional conversion parameters
        prompt: Additional prompt instructions
        
    Returns:
        SHACL schema as string if output_file is None, otherwise None
        
    Example:
        >>> # Convert OWL to SHACL
        >>> shacl = convert_schema("ontology.owl", "schema.ttl")
        
        >>> # Convert JSON Schema to SHACL
        >>> shacl = convert_schema(
        ...     input_file="api-schema.json",
        ...     output_file="api-shapes.ttl",
        ...     input_format="json-schema"
        ... )
        
        >>> # Get as string
        >>> shacl_str = convert_schema("schema.xsd", output_file=None)
    """
    # Infer input format if not provided
    if input_format is None and isinstance(input_file, (str, Path)):
        input_format = infer_format_from_extension(Path(input_file))
    
    # Load input
    input_data = load_input(input_file, input_format)
    
    # Initialize transformers
    non_ai = NonAITransformer()
    
    # Determine processing path based on input format
    if isinstance(input_data, Graph):
        # RDF-based schema (OWL, SHACL 1.0/1.1)
        if use_ai:
            # AI-enhanced conversion
            ai = AITransformer(api_key)
            source_text = input_data.serialize(format='turtle')
            shacl_text = ai.transform_schema_to_shacl(
                source_text,
                input_format or 'owl',
                parameters
            )
            shapes_graph = Graph()
            shapes_graph.parse(data=shacl_text, format='turtle')
        else:
            # Non-AI conversion (deterministic rules)
            if input_format in ['owl', 'rdf', 'xml']:
                shapes_graph = non_ai.convert_owl_to_shacl(input_data)
            else:
                shapes_graph = input_data  # Already SHACL
    
    elif isinstance(input_data, dict):
        # JSON-based schema
        if use_ai:
            ai = AITransformer(api_key)
            import json
            source_text = json.dumps(input_data, indent=2)
            shacl_text = ai.transform_schema_to_shacl(
                source_text,
                'json-schema',
                parameters
            )
            shapes_graph = Graph()
            shapes_graph.parse(data=shacl_text, format='turtle')
        else:
            shapes_graph = non_ai.convert_json_schema_to_shacl(input_data)
    
    elif isinstance(input_data, (str, bytes)):
        # Text-based schema (XSD, SQL DDL, etc.)
        if not use_ai:
            raise ValueError(
                f"Non-AI conversion not supported for format: {input_format}. "
                "Set use_ai=True or provide supported format."
            )
        
        ai = AITransformer(api_key)
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8')
        
        shacl_text = ai.transform_schema_to_shacl(
            input_data,
            input_format or 'text',
            parameters
        )
        shapes_graph = Graph()
        shapes_graph.parse(data=shacl_text, format='turtle')
    
    else:
        raise ValueError(f"Unsupported input type: {type(input_data)}")
    
    # Save output
    result = save_output(shapes_graph, output_file, output_format)
    
    return result
