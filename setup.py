from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shacl-transformer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered SHACL 1.2 schema transformation and validation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shacl-transformer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "sphinx>=5.0.0",
        ],
        "all": [
            "pandas>=1.5.0",
            "openpyxl>=3.0.0",
            "python-docx>=0.8.11",
            "python-pptx>=0.6.21",
            "PyPDF2>=3.0.0",
            "Pillow>=9.0.0",
            "pytesseract>=0.3.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "shacl-convert=shacl_transformer.cli:convert_cli",
            "shacl-create=shacl_transformer.cli:create_cli",
            "shacl-validate=shacl_transformer.cli:validate_cli",
        ],
    },
    include_package_data=True,
    package_data={
        "shacl_transformer": ["prompts/*.txt", "templates/*.ttl"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/shacl-transformer/issues",
        "Source": "https://github.com/yourusername/shacl-transformer",
        "Documentation": "https://shacl-transformer.readthedocs.io/",
    },
)
