#!/usr/bin/env python3
"""
TMA-SRTA: Three-Module Architecture for Self-Regulating Transparent AI
Setup configuration for Structural Design Pattern Theory implementation

This package provides the world's first computational implementation of
classical four-cause design patterns in modern AI systems.
"""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
def get_version():
    version_file = os.path.join('src', 'tma', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
            version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
            if version_match:
                return version_match.group(1)
    return "1.0.0"

# Read long description from README
def get_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "TMA-SRTA: Three-Module Architecture for Self-Regulating Transparent AI"

# Core dependencies
CORE_REQUIREMENTS = [
    'dataclasses>=0.8; python_version < "3.7"',
    'typing-extensions>=3.7.4',
    'pandas>=1.3.0',
    'numpy>=1.21.0',
    'scipy>=1.7.0',
    'scikit-learn>=1.0.0',
    'pydantic>=1.8.0',
    'requests>=2.25.1',
    'matplotlib>=3.4.0',
    'loguru>=0.5.3'
]

# Development dependencies
DEV_REQUIREMENTS = [
    'pytest>=6.2.0',
    'pytest-cov>=2.12.0',
    'pytest-asyncio>=0.15.0',
    'hypothesis>=6.14.0',
    'black>=21.7.0',
    'flake8>=3.9.0',
    'mypy>=0.910',
    'pre-commit>=2.15.0'
]

# Documentation dependencies
DOCS_REQUIREMENTS = [
    'sphinx>=4.1.0',
    'sphinx-rtd-theme>=0.5.2',
    'mkdocs>=1.2.0',
    'mkdocs-material>=7.2.0'
]

# Experimental dependencies
EXPERIMENTAL_REQUIREMENTS = [
    'torch>=1.9.0',
    'transformers>=4.12.0',
    'anthropic>=0.7.0',
    'openai>=0.27.0'
]

# All optional dependencies
ALL_REQUIREMENTS = DEV_REQUIREMENTS + DOCS_REQUIREMENTS + EXPERIMENTAL_REQUIREMENTS

setup(
    # Basic package information
    name="tma-srta",
    version=get_version(),
    description="Three-Module Architecture for Self-Regulating Transparent AI",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    
    # Author and project information
    author="TMA-SRTA Research Team",
    author_email="research@tma-srta.org",
    url="https://github.com/ubunturbo/srta-ai-accountability",
    project_urls={
        "Bug Tracker": "https://github.com/ubunturbo/srta-ai-accountability/issues",
        "Documentation": "https://github.com/ubunturbo/srta-ai-accountability/docs",
        "Source Code": "https://github.com/ubunturbo/srta-ai-accountability",
        "Research Paper": "https://github.com/ubunturbo/srta-ai-accountability/docs/paper",
    },
    
    # Package discovery and structure
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    
    # Python version support
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=CORE_REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
        "docs": DOCS_REQUIREMENTS,
        "experimental": EXPERIMENTAL_REQUIREMENTS,
        "all": ALL_REQUIREMENTS,
    },
    
    # Package classification
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",
        
        # Intended audience
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        
        # Topic classification
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Programming language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # Operating systems
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        
        # Framework
        "Framework :: AsyncIO",
        "Framework :: Pytest",
        
        # Natural language
        "Natural Language :: English",
        
        # Environment
        "Environment :: Console",
        "Environment :: Web Environment",
    ],
    
    # Keywords for discovery
    keywords=[
        "ai-accountability",
        "transparent-ai", 
        "ethical-ai",
        "four-cause-design",
        "structural-design-patterns",
        "three-module-architecture",
        "tma-srta",
        "ai-governance",
        "explainable-ai",
        "responsible-ai"
    ],
    
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "tma-srta=src.tma.cli:main",
            "tma-validate=tools.design_validator:main",
            "tma-profile=tools.performance_profiler:main",
        ]
    },
    
    # Package data
    package_data={
        "tma": [
            "data/*.json",
            "data/*.yaml", 
            "templates/*.txt",
            "schemas/*.json"
        ]
    },
    
    # Data files
    data_files=[
        ("docs", ["README.md", "CONTRIBUTING.md"]),
        ("examples", ["examples/basic_tma_usage.py"]),
    ],
    
    # Test configuration
    test_suite="tests",
    tests_require=DEV_REQUIREMENTS,
    
    # Zip safety
    zip_safe=False,
    
    # Additional metadata
    platforms=["any"],
    license="MIT",
    
    # Project maturity indicators
    download_url="https://github.com/ubunturbo/srta-ai-accountability/archive/v1.0.0.tar.gz",
    
    # Maintainer information
    maintainer="TMA-SRTA Research Team",
    maintainer_email="research@tma-srta.org",
    
    # Additional options
    options={
        "build": {
            "build_base": "build"
        },
        "sdist": {
            "formats": ["zip", "gztar"]
        },
        "bdist_wheel": {
            "universal": False
        }
    }
)

# Post-installation message
print("""
🎉 TMA-SRTA Installation Complete!

Three-Module Architecture for Self-Regulating Transparent AI
===============================================================================

You've just installed the world's first computational implementation of 
classical four-cause design patterns in modern AI systems!

📚 Getting Started:
   python -c "from src.tma import TMAArchitecture; print('TMA-SRTA Ready!')"

📖 Documentation: 
   See README.md and docs/ directory

🧪 Run Examples:
   python examples/basic_tma_usage.py

🔬 Validation:
   python experiments/proof_of_concept/tma_validation.py

⚡ Quick Test:
   python -m pytest tests/test_tma_architecture.py

For more information: https://github.com/ubunturbo/srta-ai-accountability

Welcome to the Aristotelian revolution in AI design! 🏛️✨
===============================================================================
""")
