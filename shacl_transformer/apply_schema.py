"""
Apply Schema - Map data to SHACL schemas
"""

from typing import Union, Optional, BinaryIO, TextIO
from pathlib import Path
from rdflib import Graph

from .ai_transformer import AITransformer
from .non_ai_transformer import NonAITransformer
from .utils import load_input, save_output, infer_format_from_extension


def apply_schema(
    source_data: Union[str, Path, BinaryIO, TextIO, bytes],
    schema_file: Union[str, Path, BinaryIO, TextIO],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    data_format: Optional[str] = None,
    output_format: str = "turtle",
    use_ai: bool = True,
    api_key: Optional[str] = None
) -> Union[str, None]:
    """
    Apply SHACL schema to data, transforming it to conform.
    
    Args:
        source_data: Source data file/stream
        schema_file: SHACL schema file/stream
        output_file: Output file/stream (None returns as string)
        data_format: Data format (auto-detected if None)
        output_format: Output format (turtle, jsonld)
        use_ai: Use AI for intelligent mapping
        api_key: Anthropic API key
        
    Returns:
        Transformed data as string if output_file is None
        
    Example:
        >>> # Transform JSON to RDF following schema
        >>> rdf_data = apply_schema(
        ...     source_data="input.json",
        ...     schema_file="schema.ttl",
        ...     output_file="output.ttl"
        ... )
    """
    # Infer format
    if data_format is None and isinstance(source_data, (str, Path)):
        data_format = infer_format_from_extension(Path(source_data))
    
    # Load schema
    schema_graph = load_input(schema_file, 'turtle')
    schema_text = schema_graph.serialize(format='turtle')
    
    # Load data
    data_input = load_input(source_data, data_format)
    if isinstance(data_input, Graph):
        data_text = data_input.serialize(format='turtle')
    elif isinstance(data_input, dict):
        import json
        data_text = json.dumps(data_input, indent=2)
    else:
        data_text = str(data_input)
    
    # Apply schema
    if use_ai:
        ai = AITransformer(api_key)
        mapped_text = ai.map_data_to_schema(
            data_text,
            data_format or 'text',
            schema_text
        )
        result_graph = Graph()
        result_graph.parse(data=mapped_text, format='turtle')
    else:
        non_ai = NonAITransformer()
        if isinstance(data_input, dict):
            result_graph = non_ai.transform_data_to_rdf(
                data_input,
                'json'
            )
        else:
            raise ValueError("Non-AI mapping requires structured data")
    
    # Save output
    result = save_output(result_graph, output_file, output_format)
    return result
