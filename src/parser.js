import fs from 'fs/promises';
import axios from 'axios';
import xlsx from 'xlsx';
import pdfParse from 'pdf-parse';
import mime from 'mime-types';
import path from 'path';

/**
 * File parser and data loader for various formats
 */
export class FileParser {
  /**
   * Detect file type from extension or content
   */
  static detectFileType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const typeMap = {
      '.owl': 'owl',
      '.rdf': 'rdf',
      '.ttl': 'turtle',
      '.xsd': 'xsd',
      '.xml': 'xml',
      '.json': 'json',
      '.jsonld': 'jsonld',
      '.xlsx': 'excel',
      '.xls': 'excel',
      '.csv': 'csv',
      '.pdf': 'pdf',
      '.txt': 'text'
    };
    return typeMap[ext] || 'unknown';
  }

  /**
   * Load content from file path
   */
  static async loadFile(filePath) {
    const content = await fs.readFile(filePath, 'utf-8');
    const fileType = this.detectFileType(filePath);
    return { content, fileType };
  }

  /**
   * Load content from URL
   */
  static async loadUrl(url) {
    const response = await axios.get(url, {
      responseType: 'arraybuffer',
      headers: {
        'User-Agent': 'SHACL-Converter/1.0'
      }
    });

    const contentType = response.headers['content-type'];
    const mimeType = contentType ? contentType.split(';')[0] : null;
    
    // Determine file type from MIME type or URL
    let fileType = 'unknown';
    if (url.endsWith('.owl') || mimeType === 'application/rdf+xml') {
      fileType = 'owl';
    } else if (url.endsWith('.xsd') || url.endsWith('.xml')) {
      fileType = url.endsWith('.xsd') ? 'xsd' : 'xml';
    } else if (url.endsWith('.ttl') || mimeType === 'text/turtle') {
      fileType = 'turtle';
    } else if (url.endsWith('.json') || mimeType === 'application/json') {
      fileType = 'json';
    } else if (url.endsWith('.jsonld') || mimeType === 'application/ld+json') {
      fileType = 'jsonld';
    } else if (url.endsWith('.pdf')) {
      fileType = 'pdf';
    }

    const content = Buffer.from(response.data).toString('utf-8');
    return { content, fileType };
  }

  /**
   * Parse Excel file to JSON
   */
  static async parseExcel(filePath) {
    const buffer = await fs.readFile(filePath);
    const workbook = xlsx.read(buffer, { type: 'buffer' });
    
    const result = {};
    workbook.SheetNames.forEach(sheetName => {
      const worksheet = workbook.Sheets[sheetName];
      result[sheetName] = xlsx.utils.sheet_to_json(worksheet);
    });

    return JSON.stringify(result, null, 2);
  }

  /**
   * Parse PDF file to text
   */
  static async parsePdf(filePath) {
    const buffer = await fs.readFile(filePath);
    const data = await pdfParse(buffer);
    return data.text;
  }

  /**
   * Determine if the content is a schema or data
   */
  static isSchema(content, fileType) {
    const schemaTypes = ['owl', 'xsd', 'jsonschema'];
    
    if (schemaTypes.includes(fileType)) {
      return true;
    }

    // Check for schema keywords in JSON
    if (fileType === 'json') {
      try {
        const parsed = JSON.parse(content);
        if (parsed.$schema || parsed.properties || parsed.definitions) {
          return 'jsonschema';
        }
      } catch (e) {
        // Not valid JSON
      }
    }

    // Check for SHACL content
    if (fileType === 'turtle' || fileType === 'rdf') {
      if (content.includes('sh:NodeShape') || content.includes('sh:PropertyShape')) {
        return 'shacl1';
      }
    }

    return false;
  }

  /**
   * Get appropriate format string for data sources
   */
  static getDataFormat(fileType) {
    const formatMap = {
      'json': 'JSON',
      'jsonld': 'JSON-LD',
      'xml': 'XML',
      'turtle': 'RDF Turtle',
      'rdf': 'RDF/XML',
      'excel': 'Excel',
      'csv': 'CSV',
      'pdf': 'PDF Text',
      'text': 'Plain Text'
    };
    return formatMap[fileType] || 'Unknown';
  }
}
