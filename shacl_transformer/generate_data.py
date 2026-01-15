"""
Generate Data - Generate sample data from schemas
"""

from typing import Union, Optional, BinaryIO, TextIO
from pathlib import Path
from rdflib import Graph

from .ai_transformer import AITransformer
from .utils import load_input, save_output


def generate_data(
    schema_file: Union[str, Path, BinaryIO, TextIO],
    prompt: str,
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    count: int = 10,
    output_format: str = "turtle",
    api_key: Optional[str] = None
) -> Union[str, None]:
    """
    Generate sample data based on SHACL schema and prompt.
    
    Args:
        schema_file: SHACL schema file/stream
        prompt: Natural language description of desired data
        output_file: Output file/stream (None returns as string)
        count: Number of instances to generate
        output_format: Output format (turtle, jsonld)
        api_key: Anthropic API key
        
    Returns:
        Generated data as string if output_file is None
        
    Example:
        >>> # Generate person data
        >>> data = generate_data(
        ...     schema_file="person_schema.ttl",
        ...     prompt="Create diverse people from different countries",
        ...     count=20,
        ...     output_file="sample_people.ttl"
        ... )
        
        >>> # Generate and return as string
        >>> data_str = generate_data(
        ...     schema_file="product_schema.ttl",
        ...     prompt="Electronics products with realistic prices",
        ...     output_file=None
        ... )
    """
    # Load schema
    schema_graph = load_input(schema_file, 'turtle')
    schema_text = schema_graph.serialize(format='turtle')
    
    # Generate data using AI
    ai = AITransformer(api_key)
    generated_text = ai.generate_sample_data(
        schema_text,
        prompt,
        count
    )
    
    # Parse generated data
    data_graph = Graph()
    data_graph.parse(data=generated_text, format='turtle')
    
    # Save output
    result = save_output(data_graph, output_file, output_format)
    return result
