# SHACL Converter Quick Start

## Prerequisites

1. Install Node.js (v14 or higher)
2. Get an Anthropic API key with Claude Opus 4.5 access

## Setup

```bash
# Install dependencies
npm install

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Basic Usage

### Convert JSON Schema to SHACL 1.2

```bash
node cli.js jsonschema examples/person-schema.json -o output.ttl
```

### Convert XSD to SHACL 1.2

```bash
node cli.js xsd examples/book-schema.xsd -o output.ttl
```

### Generate SHACL from Data

```bash
node cli.js data examples/employees.json -o output.ttl
```

### Upgrade SHACL 1.0 to 1.2

```bash
node cli.js upgrade examples/person-shacl1.ttl -o output.ttl
```

### Auto-detect and Convert

```bash
node cli.js convert examples/person-schema.json -o output.ttl
```

## Programmatic Usage

```javascript
import { ShaclConverter } from './index.js';
import fs from 'fs/promises';

const converter = new ShaclConverter(process.env.ANTHROPIC_API_KEY);

// Convert JSON Schema
const schema = await fs.readFile('examples/person-schema.json', 'utf-8');
const result = await converter.jsonSchemaToShacl(schema);
console.log(result);
```

## Input Sources

The tool supports:
- **Local files**: Any supported file format
- **URLs**: HTTP/HTTPS resources
- **Excel files**: .xlsx, .xls (auto-parsed to JSON)
- **PDF files**: .pdf (auto-parsed to text)

## Output

All conversions produce SHACL 1.2 in Turtle format (.ttl), which can be:
- Saved to a file using `-o` option
- Printed to stdout (default)
- Used programmatically in your applications

## Tips

1. **Specify type explicitly** if auto-detection fails:
   ```bash
   node cli.js convert file.txt -t xsd -o output.ttl
   ```

2. **Specify data format** for better schema inference:
   ```bash
   node cli.js data file.json -f JSON -o output.ttl
   ```

3. **Use URLs** for remote resources:
   ```bash
   node cli.js convert https://example.com/schema.xsd -o output.ttl
   ```
