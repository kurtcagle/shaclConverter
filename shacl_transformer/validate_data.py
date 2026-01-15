"""
Validate Data - Validate data against SHACL schemas
"""

from typing import Union, Optional, BinaryIO, TextIO, Dict, Any
from pathlib import Path
from rdflib import Graph

from .non_ai_transformer import NonAITransformer
from .utils import load_input, save_output, format_markdown_report


def validate_data(
    data_file: Union[str, Path, BinaryIO, TextIO],
    schema_file: Union[str, Path, BinaryIO, TextIO],
    output_file: Union[str, Path, BinaryIO, TextIO, None] = None,
    output_format: str = "markdown",
    inference: str = "rdfs"
) -> Union[Dict[str, Any], str, None]:
    """
    Validate data against SHACL schema.
    
    Args:
        data_file: Data file/stream to validate
        schema_file: SHACL schema file/stream
        output_file: Output file/stream (None returns report)
        output_format: Report format (markdown, turtle, json)
        inference: Inference type (none, rdfs, owlrl)
        
    Returns:
        Validation report (dict if json, string if markdown/turtle)
        
    Example:
        >>> # Validate and get markdown report
        >>> report = validate_data(
        ...     data_file="my_data.ttl",
        ...     schema_file="schema.ttl",
        ...     output_format="markdown"
        ... )
        >>> print(report)
        
        >>> # Save report to file
        >>> validate_data(
        ...     data_file="data.ttl",
        ...     schema_file="schema.ttl",
        ...     output_file="validation_report.md"
        ... )
    """
    # Load data and schema
    data_graph = load_input(data_file, 'turtle')
    schema_graph = load_input(schema_file, 'turtle')
    
    # Validate
    non_ai = NonAITransformer()
    report = non_ai.validate_shacl(data_graph, schema_graph, inference)
    
    # Format output
    if output_format == "json":
        result = report
    elif output_format == "markdown":
        result = format_markdown_report(report)
    elif output_format == "turtle":
        result = report['results_graph']
    else:
        raise ValueError(f"Unsupported output format: {output_format}")
    
    # Save or return
    if output_file is not None:
        save_output(result, output_file, output_format)
        return None
    
    return result
