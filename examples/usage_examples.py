"""
Example usage of SHACL Transformer
"""

from shacl_transformer import (
    convert_schema,
    create_schema,
    apply_schema,
    validate_data,
    generate_data
)

# Example 1: Convert OWL to SHACL
def example_convert_owl():
    """Convert OWL ontology to SHACL schema"""
    result = convert_schema(
        input_file="example_owl_schema.ttl",
        output_file="converted_schema.ttl",
        use_ai=False
    )
    print("Converted OWL to SHACL")


# Example 2: Create schema from JSON data
def example_create_from_json():
    """Generate SHACL schema from JSON data"""
    json_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    
    # Would write json_data to file first
    # result = create_schema("data.json", "inferred_schema.ttl")
    print("Created schema from data")


# Example 3: Validate data
def example_validate():
    """Validate RDF data against SHACL schema"""
    report = validate_data(
        data_file="my_data.ttl",
        schema_file="my_schema.ttl",
        output_format="markdown"
    )
    print(report)


# Example 4: Generate sample data
def example_generate():
    """Generate sample data from schema"""
    data = generate_data(
        schema_file="person_schema.ttl",
        prompt="Create 10 people with diverse names and ages between 20-60",
        count=10,
        output_file="generated_people.ttl"
    )
    print("Generated sample data")


if __name__ == "__main__":
    print("SHACL Transformer Examples")
    print("See function definitions for usage examples")
