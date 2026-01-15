"""
Utility functions for SHACL Transformer
"""

import io
import os
from typing import Union, Optional, BinaryIO, TextIO
from pathlib import Path
import rdflib
from rdflib import Graph, Namespace
import json

# Common namespaces
SH = Namespace("http://www.w3.org/ns/shacl#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


def load_input(
    input_source: Union[str, Path, BinaryIO, TextIO, bytes], format: Optional[str] = None
) -> Union[Graph, dict, str, bytes]:
    """
    Load input from various sources (file path, stream, bytes).
    
    Args:
        input_source: File path, stream, or bytes
        format: Optional format hint (turtle, xml, json, etc.)
        
    Returns:
        Loaded data as Graph, dict, str, or bytes depending on format
    """
    # Handle file paths
    if isinstance(input_source, (str, Path)):
        path = Path(input_source)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {input_source}")
        
        # Infer format from extension if not provided
        if format is None:
            format = infer_format_from_extension(path)
        
        # Load RDF formats
        if format in ['turtle', 'ttl', 'xml', 'rdf', 'n3', 'nt', 'jsonld']:
            g = Graph()
            g.parse(str(path), format=normalize_rdf_format(format))
            return g
        
        # Load JSON
        elif format in ['json', 'json-schema']:
            with open(path, 'r') as f:
                return json.load(f)
        
        # Load as text
        elif format in ['txt', 'text', 'md', 'markdown']:
            with open(path, 'r') as f:
                return f.read()
        
        # Load as bytes
        else:
            with open(path, 'rb') as f:
                return f.read()
    
    # Handle streams
    elif hasattr(input_source, 'read'):
        content = input_source.read()
        
        # Try to parse as RDF
        if format in ['turtle', 'ttl', 'xml', 'rdf', 'n3', 'nt', 'jsonld']:
            g = Graph()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            g.parse(data=content, format=normalize_rdf_format(format))
            return g
        
        # Try to parse as JSON
        elif format in ['json', 'json-schema']:
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.loads(content)
        
        return content
    
    # Handle bytes
    elif isinstance(input_source, bytes):
        return input_source
    
    else:
        raise ValueError(f"Unsupported input source type: {type(input_source)}")


def save_output(
    data: Union[Graph, dict, str, bytes],
    output_dest: Union[str, Path, BinaryIO, TextIO, None],
    format: str = "turtle"
) -> Union[str, bytes]:
    """
    Save output to file or return as string/bytes.
    
    Args:
        data: Data to save
        output_dest: File path, stream, or None (return as string)
        format: Output format
        
    Returns:
        String or bytes if output_dest is None, otherwise None
    """
    # Serialize Graph
    if isinstance(data, Graph):
        serialized = data.serialize(format=normalize_rdf_format(format))
        if isinstance(serialized, bytes):
            serialized = serialized.decode('utf-8')
    
    # Serialize dict as JSON
    elif isinstance(data, dict):
        serialized = json.dumps(data, indent=2)
    
    # Handle string
    elif isinstance(data, str):
        serialized = data
    
    # Handle bytes
    elif isinstance(data, bytes):
        serialized = data
    
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")
    
    # Save to file
    if output_dest is not None:
        if isinstance(output_dest, (str, Path)):
            mode = 'w' if isinstance(serialized, str) else 'wb'
            with open(output_dest, mode) as f:
                f.write(serialized)
        elif hasattr(output_dest, 'write'):
            output_dest.write(serialized)
        return None
    
    # Return as string/bytes
    return serialized


def infer_format_from_extension(path: Path) -> str:
    """Infer format from file extension."""
    ext = path.suffix.lower()
    
    format_map = {
        '.ttl': 'turtle',
        '.rdf': 'xml',
        '.owl': 'xml',
        '.xml': 'xml',
        '.n3': 'n3',
        '.nt': 'nt',
        '.jsonld': 'jsonld',
        '.json': 'json',
        '.xsd': 'xml',
        '.csv': 'csv',
        '.xlsx': 'xlsx',
        '.docx': 'docx',
        '.pdf': 'pdf',
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image',
    }
    
    return format_map.get(ext, 'unknown')


def normalize_rdf_format(format: str) -> str:
    """Normalize RDF format names for rdflib."""
    format_map = {
        'ttl': 'turtle',
        'rdf': 'xml',
        'owl': 'xml',
        'n3': 'n3',
        'nt': 'nt',
        'ntriples': 'nt',
        'jsonld': 'json-ld',
        'json-ld': 'json-ld',
    }
    
    return format_map.get(format.lower(), format.lower())


def create_base_namespaces(graph: Graph) -> Graph:
    """Bind common namespaces to graph."""
    graph.bind('sh', SH)
    graph.bind('rdf', RDF)
    graph.bind('rdfs', RDFS)
    graph.bind('owl', OWL)
    graph.bind('xsd', XSD)
    graph.bind('skos', SKOS)
    graph.bind('dcterms', DCTERMS)
    return graph


def generate_iri(base: str, local_name: str) -> rdflib.URIRef:
    """Generate an IRI from base and local name."""
    # Clean local name
    local_name = local_name.replace(' ', '_')
    local_name = ''.join(c for c in local_name if c.isalnum() or c in '_-')
    
    if not base.endswith(('/', '#')):
        base += '/'
    
    return rdflib.URIRef(base + local_name)


def get_anthropic_api_key() -> Optional[str]:
    """Get Anthropic API key from environment."""
    return os.environ.get('ANTHROPIC_API_KEY')


def format_markdown_report(report_dict: dict) -> str:
    """Format validation report as Markdown."""
    md = ["# SHACL Validation Report\n"]
    
    md.append(f"**Conforms:** {report_dict.get('conforms', False)}\n")
    md.append(f"**Total Violations:** {len(report_dict.get('violations', []))}\n")
    
    if report_dict.get('violations'):
        md.append("\n## Violations\n")
        for i, violation in enumerate(report_dict['violations'], 1):
            md.append(f"### Violation {i}\n")
            md.append(f"- **Focus Node:** {violation.get('focusNode', 'N/A')}\n")
            md.append(f"- **Property:** {violation.get('path', 'N/A')}\n")
            md.append(f"- **Message:** {violation.get('message', 'N/A')}\n")
            md.append(f"- **Severity:** {violation.get('severity', 'Violation')}\n")
            md.append("\n")
    
    return ''.join(md)


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """Extract text from PDF file."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(pdf_path))
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return '\n'.join(text)
    except ImportError:
        raise ImportError("PyPDF2 required for PDF processing. Install with: pip install PyPDF2")


def extract_text_from_docx(docx_path: Union[str, Path]) -> str:
    """Extract text from DOCX file."""
    try:
        from docx import Document
        doc = Document(str(docx_path))
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        raise ImportError("python-docx required for DOCX processing. Install with: pip install python-docx")


def extract_text_from_image(image_path: Union[str, Path]) -> str:
    """Extract text from image using OCR."""
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(str(image_path))
        return pytesseract.image_to_string(img)
    except ImportError:
        raise ImportError("Pillow and pytesseract required for image processing. Install with: pip install Pillow pytesseract")


def parse_json_schema_to_dict(json_schema: dict) -> dict:
    """Parse JSON Schema to simplified dictionary."""
    result = {
        'type': json_schema.get('type', 'object'),
        'properties': {},
        'required': json_schema.get('required', []),
    }
    
    for prop_name, prop_def in json_schema.get('properties', {}).items():
        result['properties'][prop_name] = {
            'type': prop_def.get('type', 'string'),
            'description': prop_def.get('description', ''),
            'enum': prop_def.get('enum', []),
        }
    
    return result
