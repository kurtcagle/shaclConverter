"""
Non-AI Transformer - Handles deterministic rule-based transformations
"""

from typing import Optional, Dict, Any, List
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, BNode
from pyshacl import validate
import json

from .utils import (
    SH, XSD, SKOS, DCTERMS,
    create_base_namespaces,
    generate_iri
)


class NonAITransformer:
    """
    Deterministic transformer for rule-based SHACL processing,
    validation, and data transformation.
    """
    
    def __init__(self):
        """Initialize Non-AI Transformer."""
        self.base_iri = "http://example.org/shapes/"
    
    def validate_shacl(
        self,
        data_graph: Graph,
        shapes_graph: Graph,
        inference: str = 'rdfs'
    ) -> Dict[str, Any]:
        """
        Validate data against SHACL shapes.
        
        Args:
            data_graph: RDF graph containing data
            shapes_graph: RDF graph containing SHACL shapes
            inference: Inference type ('none', 'rdfs', 'owlrl')
            
        Returns:
            Validation report as dictionary
        """
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference=inference,
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True
        )
        
        # Parse results into structured format
        violations = self._parse_validation_results(results_graph)
        
        return {
            'conforms': conforms,
            'violations': violations,
            'results_text': results_text,
            'results_graph': results_graph
        }
    
    def apply_shacl_rules(
        self,
        data_graph: Graph,
        shapes_graph: Graph
    ) -> Graph:
        """
        Apply SHACL rules to derive new triples.
        
        Args:
            data_graph: Input data graph
            shapes_graph: SHACL shapes with rules
            
        Returns:
            Enhanced data graph with inferred triples
        """
        # Extract SHACL rules from shapes graph
        rules = list(shapes_graph.subjects(RDF.type, SH.SPARQLRule))
        
        for rule in rules:
            # Get CONSTRUCT query from rule
            construct_query = shapes_graph.value(rule, SH.construct)
            if construct_query:
                # Execute CONSTRUCT query on data graph
                try:
                    inferred = data_graph.query(str(construct_query))
                    for triple in inferred:
                        data_graph.add(triple)
                except Exception as e:
                    print(f"Warning: Could not execute rule {rule}: {e}")
        
        return data_graph
    
    def convert_owl_to_shacl(
        self,
        owl_graph: Graph,
        base_iri: Optional[str] = None
    ) -> Graph:
        """
        Convert OWL ontology to SHACL shapes.
        
        Args:
            owl_graph: OWL ontology graph
            base_iri: Base IRI for generated shapes
            
        Returns:
            SHACL shapes graph
        """
        shapes_graph = Graph()
        create_base_namespaces(shapes_graph)
        
        base = base_iri or self.base_iri
        
        # Convert OWL Classes to NodeShapes
        for owl_class in owl_graph.subjects(RDF.type, OWL.Class):
            if isinstance(owl_class, BNode):
                continue
            
            shape_iri = generate_iri(base, str(owl_class).split('/')[-1] + 'Shape')
            
            # Create NodeShape
            shapes_graph.add((shape_iri, RDF.type, SH.NodeShape))
            shapes_graph.add((shape_iri, SH.targetClass, owl_class))
            
            # Add label
            label = owl_graph.value(owl_class, RDFS.label)
            if label:
                shapes_graph.add((shape_iri, SH.name, label))
            
            # Add description
            comment = owl_graph.value(owl_class, RDFS.comment)
            if comment:
                shapes_graph.add((shape_iri, SH.description, comment))
        
        # Convert OWL Properties to PropertyShapes
        for owl_prop in owl_graph.subjects(RDF.type, OWL.ObjectProperty):
            if isinstance(owl_prop, BNode):
                continue
            
            # Get domain and range
            domain = owl_graph.value(owl_prop, RDFS.domain)
            range_val = owl_graph.value(owl_prop, RDFS.range)
            
            if domain:
                domain_shape = generate_iri(base, str(domain).split('/')[-1] + 'Shape')
                prop_shape = generate_iri(
                    base,
                    str(domain).split('/')[-1] + '_' + str(owl_prop).split('/')[-1] + 'PropertyShape'
                )
                
                # Create PropertyShape
                shapes_graph.add((prop_shape, RDF.type, SH.PropertyShape))
                shapes_graph.add((prop_shape, SH.path, owl_prop))
                
                if range_val:
                    shapes_graph.add((prop_shape, SH['class'], range_val))
                
                # Link to NodeShape
                shapes_graph.add((domain_shape, SH.property, prop_shape))
        
        return shapes_graph
    
    def convert_json_schema_to_shacl(
        self,
        json_schema: dict,
        base_iri: Optional[str] = None
    ) -> Graph:
        """
        Convert JSON Schema to SHACL shapes.
        
        Args:
            json_schema: JSON Schema as dictionary
            base_iri: Base IRI for generated shapes
            
        Returns:
            SHACL shapes graph
        """
        shapes_graph = Graph()
        create_base_namespaces(shapes_graph)
        
        base = base_iri or self.base_iri
        
        # Create main NodeShape
        schema_name = json_schema.get('title', 'Schema')
        shape_iri = generate_iri(base, schema_name + 'Shape')
        
        shapes_graph.add((shape_iri, RDF.type, SH.NodeShape))
        shapes_graph.add((shape_iri, SH.name, Literal(schema_name, lang='en')))
        
        if 'description' in json_schema:
            shapes_graph.add((shape_iri, SH.description, Literal(json_schema['description'], lang='en')))
        
        # Convert properties
        for prop_name, prop_def in json_schema.get('properties', {}).items():
            prop_shape_iri = generate_iri(base, f"{schema_name}_{prop_name}PropertyShape")
            
            shapes_graph.add((prop_shape_iri, RDF.type, SH.PropertyShape))
            shapes_graph.add((prop_shape_iri, SH.path, generate_iri(base, prop_name)))
            shapes_graph.add((prop_shape_iri, SH.name, Literal(prop_name.replace('_', ' ').title(), lang='en')))
            
            # Add datatype
            json_type = prop_def.get('type', 'string')
            xsd_type = self._json_type_to_xsd(json_type)
            shapes_graph.add((prop_shape_iri, SH.datatype, xsd_type))
            
            # Add cardinality
            if prop_name in json_schema.get('required', []):
                shapes_graph.add((prop_shape_iri, SH.minCount, Literal(1)))
            
            # Add enum as SKOS concepts
            if 'enum' in prop_def:
                concept_scheme = generate_iri(base, f"{prop_name}Scheme")
                shapes_graph.add((concept_scheme, RDF.type, SKOS.ConceptScheme))
                
                concepts = []
                for enum_val in prop_def['enum']:
                    concept_iri = generate_iri(base, f"{prop_name}_{enum_val}")
                    shapes_graph.add((concept_iri, RDF.type, SKOS.Concept))
                    shapes_graph.add((concept_iri, SKOS.inScheme, concept_scheme))
                    shapes_graph.add((concept_iri, SKOS.prefLabel, Literal(enum_val, lang='en')))
                    concepts.append(concept_iri)
                
                # Add sh:in constraint
                from rdflib.collection import Collection
                shapes_graph.add((prop_shape_iri, SH['in'], BNode()))
                Collection(shapes_graph, shapes_graph.value(prop_shape_iri, SH['in']), concepts)
            
            # Link to NodeShape
            shapes_graph.add((shape_iri, SH.property, prop_shape_iri))
        
        return shapes_graph
    
    def transform_data_to_rdf(
        self,
        data: Any,
        format: str,
        base_iri: Optional[str] = None
    ) -> Graph:
        """
        Transform various data formats to RDF.
        
        Args:
            data: Input data
            format: Data format
            base_iri: Base IRI for generated resources
            
        Returns:
            RDF graph
        """
        graph = Graph()
        create_base_namespaces(graph)
        
        base = base_iri or self.base_iri
        
        if format == 'json':
            return self._json_to_rdf(data, base, graph)
        elif format == 'csv':
            return self._csv_to_rdf(data, base, graph)
        else:
            raise ValueError(f"Unsupported format for transformation: {format}")
    
    def _json_to_rdf(self, data: dict, base: str, graph: Graph) -> Graph:
        """Convert JSON to RDF."""
        if isinstance(data, list):
            for i, item in enumerate(data):
                self._json_object_to_rdf(item, base, f"item{i}", graph)
        elif isinstance(data, dict):
            self._json_object_to_rdf(data, base, "root", graph)
        
        return graph
    
    def _json_object_to_rdf(self, obj: dict, base: str, identifier: str, graph: Graph):
        """Convert JSON object to RDF triples."""
        subject = generate_iri(base, identifier)
        
        for key, value in obj.items():
            predicate = generate_iri(base, key)
            
            if isinstance(value, (str, int, float, bool)):
                graph.add((subject, predicate, Literal(value)))
            elif isinstance(value, dict):
                obj_iri = generate_iri(base, f"{identifier}_{key}")
                graph.add((subject, predicate, obj_iri))
                self._json_object_to_rdf(value, base, f"{identifier}_{key}", graph)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, (str, int, float, bool)):
                        graph.add((subject, predicate, Literal(item)))
                    else:
                        item_iri = generate_iri(base, f"{identifier}_{key}_{i}")
                        graph.add((subject, predicate, item_iri))
                        self._json_object_to_rdf(item, base, f"{identifier}_{key}_{i}", graph)
    
    def _parse_validation_results(self, results_graph: Graph) -> List[Dict[str, Any]]:
        """Parse SHACL validation results into structured format."""
        violations = []
        
        for result in results_graph.subjects(RDF.type, SH.ValidationResult):
            violation = {
                'focusNode': str(results_graph.value(result, SH.focusNode) or ''),
                'path': str(results_graph.value(result, SH.resultPath) or ''),
                'message': str(results_graph.value(result, SH.resultMessage) or ''),
                'severity': str(results_graph.value(result, SH.resultSeverity) or 'Violation'),
                'value': str(results_graph.value(result, SH.value) or ''),
            }
            violations.append(violation)
        
        return violations
    
    def _json_type_to_xsd(self, json_type: str) -> URIRef:
        """Map JSON Schema types to XSD datatypes."""
        type_map = {
            'string': XSD.string,
            'integer': XSD.integer,
            'number': XSD.decimal,
            'boolean': XSD.boolean,
            'null': XSD.string,
        }
        return type_map.get(json_type, XSD.string)
