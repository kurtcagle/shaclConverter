"""
Command-line interface for SHACL Transformer
"""

import click
from pathlib import Path
from .convert_schema import convert_schema
from .create_schema import create_schema
from .validate_data import validate_data


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', '-f', default=None, help='Input format')
@click.option('--no-ai', is_flag=True, help='Disable AI transformer')
def convert_cli(input_file, output_file, format, no_ai):
    """Convert schema to SHACL 1.2"""
    try:
        convert_schema(
            input_file=input_file,
            output_file=output_file,
            input_format=format,
            use_ai=not no_ai
        )
        click.echo(f"✓ Converted {input_file} → {output_file}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@click.command()
@click.argument('data_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--base-schema', '-b', type=click.Path(exists=True), help='Base schema to extend')
@click.option('--no-ai', is_flag=True, help='Disable AI transformer')
def create_cli(data_file, output_file, base_schema, no_ai):
    """Create SHACL schema from data"""
    try:
        create_schema(
            source_data=data_file,
            output_file=output_file,
            base_schema=base_schema,
            use_ai=not no_ai
        )
        click.echo(f"✓ Created schema: {output_file}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@click.command()
@click.argument('data_file', type=click.Path(exists=True))
@click.argument('schema_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for report')
@click.option('--format', '-f', default='markdown', type=click.Choice(['markdown', 'turtle', 'json']))
def validate_cli(data_file, schema_file, output, format):
    """Validate data against SHACL schema"""
    try:
        report = validate_data(
            data_file=data_file,
            schema_file=schema_file,
            output_file=output,
            output_format=format
        )
        
        if output is None:
            if format == 'markdown':
                click.echo(report)
            elif format == 'json':
                import json
                click.echo(json.dumps(report, indent=2))
        else:
            click.echo(f"✓ Validation report saved: {output}")
            
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    convert_cli()
