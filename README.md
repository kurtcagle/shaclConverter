# SHACL Converter

Convert ontologies and data sources to SHACL 1.2 using Claude Opus 4.5

## Overview

This tool uses Claude Opus 4.5 to convert various schema formats and data sources to SHACL 1.2 (Shapes Constraint Language). It supports:

### Schema Conversions
- **OWL Ontologies** → SHACL 1.2
- **XSD Schemas** → SHACL 1.2
- **JSON Schema** → SHACL 1.2
- **SHACL 1.0** → SHACL 1.2 (upgrade)

### Data Source Analysis
Generate SHACL 1.2 schemas from data sources:
- **Excel documents** (.xlsx, .xls)
- **PDF files** (.pdf)
- **JSON data** (.json)
- **XML data** (.xml)
- **RDF/Turtle** (.ttl, .rdf)
- **URLs** to online data sources

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file with your Anthropic API key:

```bash
cp .env.example .env
# Edit .env and add your API key
```

Or set the environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

The tool provides several commands:

#### General Convert Command

```bash
node cli.js convert <source> [options]
```

Options:
- `-o, --output <file>` - Output file path (default: stdout)
- `-t, --type <type>` - Force input type (owl, xsd, jsonschema, shacl1, data)
- `-f, --format <format>` - Data format for data sources
- `-k, --api-key <key>` - Anthropic API key

#### Specific Conversion Commands

**Convert OWL to SHACL 1.2:**
```bash
node cli.js owl <source> [-o output.ttl]
```

**Convert XSD to SHACL 1.2:**
```bash
node cli.js xsd <source> [-o output.ttl]
```

**Convert JSON Schema to SHACL 1.2:**
```bash
node cli.js jsonschema <source> [-o output.ttl]
```

**Upgrade SHACL 1.0 to SHACL 1.2:**
```bash
node cli.js upgrade <source> [-o output.ttl]
```

**Generate SHACL from Data:**
```bash
node cli.js data <source> [-o output.ttl] [-f format]
```

### Examples

**From a JSON Schema file:**
```bash
node cli.js jsonschema examples/person-schema.json -o output/person-shape.ttl
```

**From a data file:**
```bash
node cli.js data examples/employees.json -o output/employee-shape.ttl
```

**From a URL:**
```bash
node cli.js convert https://example.com/schema.xsd -o output.ttl
```

**Upgrade SHACL 1.0:**
```bash
node cli.js upgrade examples/person-shacl1.ttl -o output/person-shacl12.ttl
```

**From an Excel file:**
```bash
node cli.js data data.xlsx -o output/data-shape.ttl -f Excel
```

## Programmatic Usage

```javascript
import { ShaclConverter } from './src/converter.js';

const converter = new ShaclConverter(process.env.ANTHROPIC_API_KEY);

// Convert OWL to SHACL
const owlContent = await fs.readFile('ontology.owl', 'utf-8');
const shaclOutput = await converter.owlToShacl(owlContent);

// Convert JSON Schema to SHACL
const jsonSchemaContent = await fs.readFile('schema.json', 'utf-8');
const shaclOutput = await converter.jsonSchemaToShacl(jsonSchemaContent);

// Generate SHACL from data
const dataContent = await fs.readFile('data.json', 'utf-8');
const shaclOutput = await converter.dataToShacl(dataContent, 'JSON');
```

## How It Works

1. **Input Processing**: The tool loads and parses the input file or URL
2. **Type Detection**: Automatically detects the input type (OWL, XSD, JSON Schema, data, etc.)
3. **Prompt Selection**: Selects the appropriate conversion prompt template
4. **AI Conversion**: Sends the content to Claude Opus 4.5 with specialized prompts
5. **Output**: Returns SHACL 1.2 in Turtle format

## Supported Input Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| OWL | .owl, .rdf | Web Ontology Language |
| XSD | .xsd | XML Schema Definition |
| JSON Schema | .json | JSON Schema files |
| SHACL 1.0 | .ttl, .rdf | SHACL shapes to upgrade |
| JSON Data | .json | JSON data files |
| XML Data | .xml | XML data files |
| Excel | .xlsx, .xls | Excel spreadsheets |
| PDF | .pdf | PDF documents |
| Turtle | .ttl | RDF Turtle format |

## Features

- ✅ Automatic format detection
- ✅ URL support for remote resources
- ✅ Excel and PDF parsing
- ✅ Intelligent schema inference from data
- ✅ SHACL 1.2 compliant output
- ✅ Claude Opus 4.5 powered conversions
- ✅ Comprehensive error handling

## Requirements

- Node.js 14 or higher
- Anthropic API key (Claude Opus 4.5 access)

## License

ISC
