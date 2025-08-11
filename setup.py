"""
SRTA: Semantic Responsibility Trace Architecture
Setup configuration for PyPI distribution
"""

from setuptools import setup, find_packages
import os

# Read README.md for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements.txt for dependencies
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith("#"):
                    requirements.append(line)
    return requirements

setup(
    name="srta-ai-accountability",
    version="0.1.0",
    
    # Author information
    author="Takayuki Takagi",
    author_email="contact.via.github@srta-research.org",
    
    # Project description
    description="Revolutionary AI Accountability Framework based on Formal Causation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    
    # Project URLs
    url="https://github.com/ubunturbo/srta-ai-accountability",
    project_urls={
        "Bug Reports": "https://github.com/ubunturbo/srta-ai-accountability/issues",
        "Source": "https://github.com/ubunturbo/srta-ai-accountability",
        "Documentation": "https://github.com/ubunturbo/srta-ai-accountability/docs",
        "Research Paper": "https://github.com/ubunturbo/srta-ai-accountability/docs/paper",
    },
    
    # Package discovery
    packages=find_packages(exclude=["tests*", "docs*"]),
    
    # Requirements
    python_requires=">=3.8",
    install_requires=read_requirements(),
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
        "research": [
            "torch>=1.9.0",
            "transformers>=4.11.0",
            "datasets>=1.12.0",
        ],
        "api": [
            "fastapi>=0.68.0",
            "uvicorn>=0.15.0",
            "pydantic>=1.8.0",
        ]
    },
    
    # Package metadata
    classifiers=[
        # Development Status
        "Development Status :: 3 - Alpha",
        
        # Intended Audience
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Operating System
        "Operating System :: OS Independent",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        
        # Topic
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Security",
        
        # Research specific
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Sociology :: Genealogy/Gen",
    ],
    
    # Keywords for discovery
    keywords=[
        "ai-accountability", "explainable-ai", "xai", "formal-causation",
        "perichoretic-synthesis", "ai-governance", "eu-ai-act", 
        "responsibility-attribution", "audit-trails", "regulatory-compliance",
        "machine-learning", "artificial-intelligence", "transparency",
        "interpretability", "ethics", "fairness", "bias-detection"
    ],
    
    # Entry points for CLI tools
    entry_points={
        "console_scripts": [
            "srta=srta.cli:main",
        ],
    },
    
    # Include additional files
    include_package_data=True,
    package_data={
        "srta": [
            "data/*.json",
            "templates/*.yaml",
            "configs/*.toml",
        ],
    },
    
    # Zip safety
    zip_safe=False,
    
    # Platform specification
    platforms=["any"],
    
    # License
    license="MIT",
    
    # Maintainer information
    maintainer="Takayuki Takagi",
    maintainer_email="contact.via.github@srta-research.org",
)
