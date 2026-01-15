# Architecture

## Overview

SHACL Transformer implements a dual-stage transformation architecture combining AI-powered semantic understanding with deterministic rule-based processing.

```
Input → AI Transformer → Non-AI Transformer → Output
  ↓            ↓                ↑
Schema + Parameters + Data ─────┘
```

## Components

### AI Transformer

**Technology:** Claude (Anthropic API)

**Responsibilities:**
- Semantic understanding of schemas and data
- Natural language prompt interpretation
- Intelligent schema mapping
- Context-aware transformations
- Data generation from descriptions

**Advantages:**
- Handles ambiguous or incomplete schemas
- Understands domain context
- Generates human-quality documentation
- Adapts to diverse input formats

### Non-AI Transformer

**Technology:** RDFLib + pySHACL

**Responsibilities:**
- SHACL 1.2 validation
- RDF parsing and serialization
- Deterministic schema transformations
- SPARQL query execution
- Format conversions

**Advantages:**
- Predictable, repeatable results
- No API dependencies
- Fast processing
- Standards-compliant

## Data Flow

### 1. Convert Schema

```
OWL/XSD/JSON Schema
    ↓
[AI: Understand schema structure]
    ↓
[Non-AI: Apply SHACL 1.2 rules]
    ↓
SHACL 1.2 Turtle
```

### 2. Create Schema

```
Data Document (JSON/PDF/etc)
    ↓
[AI: Analyze structure and infer constraints]
    ↓
[Non-AI: Generate SHACL shapes]
    ↓
SHACL 1.2 Schema
```

### 3. Apply Schema

```
Data + SHACL Schema
    ↓
[AI: Understand mapping requirements]
    ↓
[Non-AI: Transform and validate]
    ↓
Conformant RDF Data
```

### 4. Validate Data

```
Data + SHACL Schema
    ↓
[Non-AI: pySHACL validation]
    ↓
Validation Report (RDF/Markdown/JSON)
```

### 5. Generate Data

```
SHACL Schema + Prompt
    ↓
[AI: Generate realistic instances]
    ↓
[Non-AI: Validate against schema]
    ↓
Sample RDF Data
```

## Design Decisions

### Why Dual Architecture?

1. **AI for Complexity**: Handles ambiguous, incomplete, or complex transformations
2. **Non-AI for Reliability**: Ensures standards compliance and repeatability
3. **Flexibility**: Users can choose AI or non-AI mode
4. **Validation**: Non-AI validation ensures AI output is correct

### SHACL 1.2 Focus

- Latest W3C specification
- Enhanced features (UI annotations, code identifiers)
- Backwards compatible with SHACL 1.0/1.1
- Industry-standard validation

### Modular Design

- Each function is self-contained
- Transformers are reusable
- Easy to extend with new formats
- Simple to test components independently

## Performance

### AI Mode
- **Speed**: 2-10 seconds per transformation
- **Cost**: API calls to Anthropic
- **Quality**: High semantic understanding

### Non-AI Mode
- **Speed**: < 1 second per transformation
- **Cost**: None (local processing)
- **Quality**: Rules-based, predictable

## Future Enhancements

1. Caching of AI transformations
2. Streaming for large files
3. Parallel processing
4. Custom AI model support
5. GUI interface
6. Additional format support
