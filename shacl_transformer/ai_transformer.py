"""
AI Transformer - Handles AI-powered schema and data transformations
"""

import os
from typing import Optional, Union, Dict, Any
from pathlib import Path
import json

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from .utils import get_anthropic_api_key


class AITransformer:
    """
    AI-powered transformer using Claude API for semantic understanding
    and intelligent schema/data transformations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Transformer.
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        if Anthropic is None:
            raise ImportError(
                "anthropic package required for AI features. "
                "Install with: pip install anthropic"
            )
        
        self.api_key = api_key or get_anthropic_api_key()
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def transform_schema_to_shacl(
        self,
        source_schema: str,
        source_format: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Transform schema to SHACL 1.2 using AI understanding.
        
        Args:
            source_schema: Source schema as string
            source_format: Format (owl, xsd, json-schema, etc.)
            parameters: Optional transformation parameters
            
        Returns:
            SHACL 1.2 schema as Turtle string
        """
        # Load the comprehensive prompt from earlier in the conversation
        system_prompt = self._get_shacl_generation_prompt()
        
        user_prompt = f"""
Please convert the following {source_format} schema to SHACL 1.2 format.

SOURCE SCHEMA:
{source_schema}

REQUIREMENTS:
- Full SHACL 1.2 compliance (https://www.w3.org/TR/shacl12-core/)
- Include SHACL Core constraints
- Add node expressions where appropriate
- Create SHACL Rules for calculated properties
- Use sh:name and sh:codeIdentifier
- Convert enumerations to SKOS concepts
- Add comprehensive sh:description for all shapes
- Use IRIs for all shapes (no blank nodes)
- Include UI annotations (sh:group, sh:order, shui:* predicates)
- All classes and property shape identifiers should use descriptive IRIs rather than blank nodes
- Schema conversion sources that include imports should incorporate those imports before conversion to SHACL
- Include sh:message and sh:severity fields within properties, with severity determined contextually
- Be as descriptive as possible for sh:description fields
- Include sh:nodeKind statements in shape properties
- Create namespaces based upon classes (i.e., PREFIX Person: <http://www.example.com/ns/Person#> )
- Parameters can include a base namespace (baseNamespace) that is used to construct namespaces, which should be terminated with a "/" character. The default base namespace is "http://example.com/ns/".
- Class and property shapes should incorporate xsh:altLabel, xsh:acronym, and xsh:soundsLike, where xsh: = <http:/example.com/ns/xsh#>. All of these should be lower case.
- The xsh:soundsLike predicate uses the double-homophone encoding to create sounds-like representation of the primary and secondary labels.

OUTPUT FORMAT: Turtle (.ttl)
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )
        
        return self._extract_turtle_from_response(response.content[0].text)
    
    def analyze_data_for_schema(
        self,
        source_data: str,
        source_format: str,
        base_schema: Optional[str] = None
    ) -> str:
        """
        Analyze data and generate/extend SHACL schema.
        
        Args:
            source_data: Source data as string
            source_format: Data format (json, xml, csv, etc.)
            base_schema: Optional base SHACL schema to extend
            
        Returns:
            SHACL 1.2 schema as Turtle string
        """
        system_prompt = self._get_shacl_generation_prompt()
        
        if base_schema:
            user_prompt = f"""
Please analyze the following {source_format} data and EXTEND the provided base schema.

BASE SCHEMA:
{base_schema}

SOURCE DATA:
{source_data}

REQUIREMENTS:
- Extend the base schema with additional shapes as needed
- Infer data types, cardinalities, and constraints from data
- Create new SKOS concepts for any enumerations
- Maintain consistency with base schema
- Add sh:description based on data patterns
"""
        else:
            user_prompt = f"""
Please analyze the following {source_format} data and CREATE a complete SHACL 1.2 schema.

SOURCE DATA:
{source_data}

REQUIREMENTS:
- Full SHACL 1.2 compliance
- Infer data types, cardinalities, and constraints from data
- Identify enumerations and convert to SKOS
- Add comprehensive documentation
- Include appropriate SHACL Rules for derived properties
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )
        
        return self._extract_turtle_from_response(response.content[0].text)
    
    def map_data_to_schema(
        self,
        source_data: str,
        source_format: str,
        target_schema: str
    ) -> str:
        """
        Map source data to target SHACL schema.
        
        Args:
            source_data: Source data as string
            source_format: Data format
            target_schema: Target SHACL schema
            
        Returns:
            Mapped data as Turtle string
        """
        user_prompt = f"""
Please map the following {source_format} data to conform to the target SHACL schema.

TARGET SCHEMA:
{target_schema}

SOURCE DATA:
{source_data}

REQUIREMENTS:
- Transform data to match schema structure
- Apply type conversions as needed
- Generate IRIs for entities
- Ensure all constraints are satisfied
- Output as RDF Turtle
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )
        
        return self._extract_turtle_from_response(response.content[0].text)
    
    def generate_sample_data(
        self,
        schema: str,
        prompt: str,
        count: int = 10
    ) -> str:
        """
        Generate sample data based on schema and prompt.
        
        Args:
            schema: SHACL schema
            prompt: Natural language description of desired data
            count: Number of instances to generate
            
        Returns:
            Generated data as Turtle string
        """
        user_prompt = f"""
Please generate {count} instances of sample data conforming to the SHACL schema below.

SCHEMA:
{schema}

DATA REQUIREMENTS:
{prompt}

REQUIREMENTS:
- All instances must validate against the schema
- Generate realistic, diverse data
- Include all required properties
- Output as RDF Turtle
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )
        
        return self._extract_turtle_from_response(response.content[0].text)
    
    def _get_shacl_generation_prompt(self) -> str:
        """Get comprehensive SHACL generation system prompt."""
        # This would ideally load from the prompt file created earlier
        return """You are an expert in W3C semantic web technologies specializing in SHACL 1.2 schema generation, OWL ontology processing, and SPARQL query development. Your task is to generate comprehensive, specification-compliant SHACL schemas with associated documentation.

Generate schemas compliant with https://www.w3.org/TR/shacl12-core/ including:

- SHACL Core constraints (sh:datatype, sh:minCount, sh:maxCount, sh:pattern, etc.)
- Node Expressions (sh:and, sh:or, sh:not, sh:xone)
- SHACL Rules for calculated properties
- UI Annotations (sh:group, sh:order, sh:defaultValue)
- ALL shape nodes MUST use IRIs (no blank nodes)
- sh:name, sh:codeIdentifier, and sh:description for all shapes
- Use SKOS for enumerations
- Link to external vocabularies (Wikidata, DBpedia, etc.) where appropriate

Output format: Valid RDF Turtle that can be parsed by rdflib."""
    
    def _extract_turtle_from_response(self, response_text: str) -> str:
        """Extract Turtle content from Claude's response."""
        # Remove markdown code fences if present
        text = response_text.strip()
        
        if '```turtle' in text:
            start = text.find('```turtle') + 9
            end = text.find('```', start)
            text = text[start:end].strip()
        elif '```ttl' in text:
            start = text.find('```ttl') + 6
            end = text.find('```', start)
            text = text[start:end].strip()
        elif '```' in text:
            start = text.find('```') + 3
            end = text.find('```', start)
            text = text[start:end].strip()
        
        return text
