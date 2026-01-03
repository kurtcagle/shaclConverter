#!/usr/bin/env node

import { Command } from 'commander';
import fs from 'fs/promises';
import dotenv from 'dotenv';
import { ShaclConverter } from './src/converter.js';
import { FileParser } from './src/parser.js';

dotenv.config();

const program = new Command();

program
  .name('shacl-convert')
  .description('Convert ontologies and data sources to SHACL 1.2 using Claude Opus 4.5')
  .version('1.0.0');

program
  .command('convert')
  .description('Convert a file or URL to SHACL 1.2')
  .argument('<source>', 'File path or URL to convert')
  .option('-o, --output <file>', 'Output file path (default: stdout)')
  .option('-t, --type <type>', 'Force input type (owl, xsd, jsonschema, shacl1, data)')
  .option('-f, --format <format>', 'Data format for data sources (JSON, XML, etc.)')
  .option('-k, --api-key <key>', 'Anthropic API key (or set ANTHROPIC_API_KEY env var)')
  .action(async (source, options) => {
    try {
      const apiKey = options.apiKey || process.env.ANTHROPIC_API_KEY;
      if (!apiKey) {
        console.error('Error: Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or use --api-key option.');
        process.exit(1);
      }

      console.error('Loading source...');
      let content, fileType;

      // Load from URL or file
      if (source.startsWith('http://') || source.startsWith('https://')) {
        const result = await FileParser.loadUrl(source);
        content = result.content;
        fileType = result.fileType;
        
        // Parse binary types after loading
        if (fileType === 'excel') {
          // For URL-loaded Excel, content is already a buffer
          const xlsx = (await import('xlsx')).default;
          const workbook = xlsx.read(content, { type: 'buffer' });
          const parsed = {};
          workbook.SheetNames.forEach(sheetName => {
            const worksheet = workbook.Sheets[sheetName];
            parsed[sheetName] = xlsx.utils.sheet_to_json(worksheet);
          });
          content = JSON.stringify(parsed, null, 2);
        } else if (fileType === 'pdf') {
          // For URL-loaded PDF, content is already a buffer
          const pdfParse = (await import('pdf-parse')).default;
          const data = await pdfParse(content);
          content = data.text;
        }
      } else {
        const result = await FileParser.loadFile(source);
        content = result.content;
        fileType = result.fileType;
        
        // Parse binary types that were loaded as buffers
        if (fileType === 'excel') {
          content = await FileParser.parseExcel(source);
        } else if (fileType === 'pdf') {
          content = await FileParser.parsePdf(source);
        }
        }
      }

      // Override type if specified
      if (options.type) {
        fileType = options.type;
      }

      console.error(`Detected type: ${fileType}`);
      console.error('Converting with Claude Opus 4.5...');

      const converter = new ShaclConverter(apiKey);
      let result;

      // Determine conversion type
      const schemaType = FileParser.isSchema(content, fileType);
      
      if (schemaType === 'jsonschema' || fileType === 'jsonschema') {
        result = await converter.jsonSchemaToShacl(content);
      } else if (fileType === 'owl') {
        result = await converter.owlToShacl(content);
      } else if (fileType === 'xsd') {
        result = await converter.xsdToShacl(content);
      } else if (schemaType === 'shacl1' || fileType === 'shacl1') {
        result = await converter.shacl1ToShacl12(content);
      } else {
        // Treat as data source
        const format = options.format || FileParser.getDataFormat(fileType);
        result = await converter.dataToShacl(content, format);
      }

      // Output result
      if (options.output) {
        await fs.writeFile(options.output, result);
        console.error(`Output written to ${options.output}`);
      } else {
        console.log(result);
      }

      console.error('Conversion complete!');
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('owl')
  .description('Convert OWL ontology to SHACL 1.2')
  .argument('<source>', 'OWL file path or URL')
  .option('-o, --output <file>', 'Output file path')
  .option('-k, --api-key <key>', 'Anthropic API key')
  .action(async (source, options) => {
    await runConversion(source, 'owl', options);
  });

program
  .command('xsd')
  .description('Convert XSD schema to SHACL 1.2')
  .argument('<source>', 'XSD file path or URL')
  .option('-o, --output <file>', 'Output file path')
  .option('-k, --api-key <key>', 'Anthropic API key')
  .action(async (source, options) => {
    await runConversion(source, 'xsd', options);
  });

program
  .command('jsonschema')
  .description('Convert JSON Schema to SHACL 1.2')
  .argument('<source>', 'JSON Schema file path or URL')
  .option('-o, --output <file>', 'Output file path')
  .option('-k, --api-key <key>', 'Anthropic API key')
  .action(async (source, options) => {
    await runConversion(source, 'jsonschema', options);
  });

program
  .command('upgrade')
  .description('Upgrade SHACL 1.0 to SHACL 1.2')
  .argument('<source>', 'SHACL 1.0 file path or URL')
  .option('-o, --output <file>', 'Output file path')
  .option('-k, --api-key <key>', 'Anthropic API key')
  .action(async (source, options) => {
    await runConversion(source, 'shacl1', options);
  });

program
  .command('data')
  .description('Generate SHACL 1.2 schema from data source')
  .argument('<source>', 'Data file path or URL')
  .option('-o, --output <file>', 'Output file path')
  .option('-f, --format <format>', 'Data format (JSON, XML, Excel, etc.)')
  .option('-k, --api-key <key>', 'Anthropic API key')
  .action(async (source, options) => {
    await runConversion(source, 'data', options);
  });

async function runConversion(source, type, options) {
  try {
    const apiKey = options.apiKey || process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      console.error('Error: Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or use --api-key option.');
      process.exit(1);
    }

    console.error('Loading source...');
    let content, fileType;

    if (source.startsWith('http://') || source.startsWith('https://')) {
      const result = await FileParser.loadUrl(source);
      content = result.content;
      fileType = result.fileType;
      
      // Parse binary types after loading
      if (fileType === 'excel') {
        const xlsx = (await import('xlsx')).default;
        const workbook = xlsx.read(content, { type: 'buffer' });
        const parsed = {};
        workbook.SheetNames.forEach(sheetName => {
          const worksheet = workbook.Sheets[sheetName];
          parsed[sheetName] = xlsx.utils.sheet_to_json(worksheet);
        });
        content = JSON.stringify(parsed, null, 2);
      } else if (fileType === 'pdf') {
        const pdfParse = (await import('pdf-parse')).default;
        const data = await pdfParse(content);
        content = data.text;
      }
    } else {
      const result = await FileParser.loadFile(source);
      fileType = result.fileType;
      
      if (fileType === 'excel') {
        content = await FileParser.parseExcel(source);
      } else if (fileType === 'pdf') {
        content = await FileParser.parsePdf(source);
      } else {
        content = result.content;
      }
    }

    console.error('Converting with Claude Opus 4.5...');
    const converter = new ShaclConverter(apiKey);
    let result;

    switch (type) {
      case 'owl':
        result = await converter.owlToShacl(content);
        break;
      case 'xsd':
        result = await converter.xsdToShacl(content);
        break;
      case 'jsonschema':
        result = await converter.jsonSchemaToShacl(content);
        break;
      case 'shacl1':
        result = await converter.shacl1ToShacl12(content);
        break;
      case 'data':
        const format = options.format || 'JSON';
        result = await converter.dataToShacl(content, format);
        break;
      default:
        throw new Error(`Unknown type: ${type}`);
    }

    if (options.output) {
      await fs.writeFile(options.output, result);
      console.error(`Output written to ${options.output}`);
    } else {
      console.log(result);
    }

    console.error('Conversion complete!');
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

program.parse();
