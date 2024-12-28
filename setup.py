from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="altercycle",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A specialized data structure for handling alternating binary states in cyclic sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/altercycle",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing_extensions>=4.0.0;python_version<'3.8'",  # For Python 3.7 compatibility
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "mypy>=0.900",
            "pylint>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/altercycle/issues",
        "Source": "https://github.com/yourusername/altercycle",
        "Documentation": "https://altercycle.readthedocs.io/",
    },
    keywords=[
        "data-structure",
        "binary-state",
        "state-alternation",
        "cyclic-patterns",
        "dna-analysis",
        "protocol-validation",
        "pattern-detection",
        "concurrent",
        "thread-safe",
    ],
)
