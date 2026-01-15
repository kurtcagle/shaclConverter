"""
SHACL Transformer
=================

A comprehensive Python library for SHACL 1.2 schema transformation and validation.

Main Functions:
    - convert_schema: Convert various schema formats to SHACL 1.2
    - create_schema: Generate SHACL schemas from data
    - apply_schema: Map data to SHACL schemas
    - validate_data: Validate data against SHACL schemas
    - generate_data: Generate synthetic data from schemas

Architecture:
    Schema + Parameters → AI Transformer → Non-AI Transformer → Output
                                  ↓              ↑
                                Data ────────────┘
"""

from .convert_schema import convert_schema
from .create_schema import create_schema
from .apply_schema import apply_schema
from .validate_data import validate_data
from .generate_data import generate_data

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "convert_schema",
    "create_schema",
    "apply_schema",
    "validate_data",
    "generate_data",
]
