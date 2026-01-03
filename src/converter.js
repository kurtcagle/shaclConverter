import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * SHACL Converter using Claude Opus 4.5
 */
export class ShaclConverter {
  constructor(apiKey) {
    if (!apiKey) {
      throw new Error('Anthropic API key is required');
    }
    this.client = new Anthropic({ apiKey });
    this.modelName = 'claude-opus-4-20250514';
  }

  /**
   * Load a prompt template from the prompts directory
   */
  async loadPrompt(templateName) {
    const promptPath = path.join(__dirname, '..', 'prompts', `${templateName}.txt`);
    return await fs.readFile(promptPath, 'utf-8');
  }

  /**
   * Call Claude API to convert content using a specific prompt template
   */
  async convert(input, templateName, format = null) {
    const promptTemplate = await this.loadPrompt(templateName);
    let prompt = promptTemplate.replace('{input}', input);
    
    if (format) {
      prompt = prompt.replace('{format}', format);
    }

    const message = await this.client.messages.create({
      model: this.modelName,
      max_tokens: 4096,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    });

    return message.content[0].text;
  }

  /**
   * Convert OWL ontology to SHACL 1.2
   */
  async owlToShacl(owlContent) {
    return await this.convert(owlContent, 'owl-to-shacl');
  }

  /**
   * Convert XSD schema to SHACL 1.2
   */
  async xsdToShacl(xsdContent) {
    return await this.convert(xsdContent, 'xsd-to-shacl');
  }

  /**
   * Convert JSON Schema to SHACL 1.2
   */
  async jsonSchemaToShacl(jsonSchemaContent) {
    return await this.convert(jsonSchemaContent, 'jsonschema-to-shacl');
  }

  /**
   * Upgrade SHACL 1.0 to SHACL 1.2
   */
  async shacl1ToShacl12(shacl1Content) {
    return await this.convert(shacl1Content, 'shacl1-to-shacl12');
  }

  /**
   * Generate SHACL 1.2 from data source
   */
  async dataToShacl(dataContent, format) {
    return await this.convert(dataContent, 'data-to-shacl', format);
  }
}
