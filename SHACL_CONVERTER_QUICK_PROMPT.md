# SHACL 1.2 Converter - Quick Prompt

Convert the provided schema or data to SHACL 1.2 following these rules:

## Input:
[Schema: OWL/SHACL/XSD/JSON Schema/URL] OR [Data: JSON/XML/Turtle/CSV/Office docs/web page]

## Output: Both RDF Turtle AND JSON-LD

## Requirements Checklist:

✓ **Named IRIs for all shapes** (no blank nodes)
✓ **sh:name** - human labels ("Person Name")
✓ **sh:codeIdentifier** - code names ("personName")
✓ **sh:description** - comprehensive descriptions
✓ **sh:in with IRIs only** - define SKOS concepts, never use string literals
✓ **SKOS taxonomies** - ConceptScheme + Concepts for controlled vocabularies
✓ **Prefer IRIs** - use sh:class & sh:nodeKind sh:IRI for entities
✓ **UI elements** - dash:editor, dash:viewer, sh:order
✓ **Node expressions** - sh:expression, sh:values, sh:rule where useful
✓ **Validation** - sh:minCount, sh:maxCount, sh:pattern, sh:minLength, etc.

## Quick Template:

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dash: <http://datashapes.org/dash#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# Node Shape (named IRI)
<http://example.org/shapes/EntityShape>
  sh:targetClass schema:Entity ;
  sh:name "Entity"@en ;
  sh:description "..."@en ;
  sh:property <http://example.org/shapes/EntityPropertyShape> .

# Property Shape (named IRI)
<http://example.org/shapes/EntityPropertyShape>
  sh:path schema:property ;
  sh:name "Property Label"@en ;
  sh:codeIdentifier "propertyName" ;
  sh:description "..."@en ;
  sh:datatype xsd:string ;
  sh:minCount 1 ;
  sh:order 1 ;
  dash:editor dash:TextFieldEditor .

# Taxonomy (for sh:in)
<http://example.org/concepts/ConceptScheme>
  a skos:ConceptScheme ;
  skos:prefLabel "..."@en .

<http://example.org/concepts/Concept1>
  a skos:Concept ;
  skos:prefLabel "Active"@en ;
  skos:inScheme <http://example.org/concepts/ConceptScheme> .

# Use in shape
sh:in ( <http://example.org/concepts/Concept1> ... ) .
```

## Common Editors:
- Text: `dash:TextFieldEditor`, `dash:TextAreaEditor`
- Numbers: `dash:IntegerEditor`, `dash:DecimalEditor`
- Dates: `dash:DatePickerEditor`
- Enums: `dash:EnumSelectEditor`
- Booleans: `dash:BooleanSelectEditor`
- IRIs: `dash:URIEditor`, `dash:InstancesSelectEditor`

## Remember:
- All shapes = named IRIs
- All sh:in values = IRIs (with SKOS definitions)
- All properties = sh:name + sh:codeIdentifier + sh:description
- Output = Turtle + JSON-LD
