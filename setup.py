# WARNING: template code, may need edits
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paragraph_checker",
    version="0.1.0",
    author="Your Name",
    description="A simple grammar and writing analysis tool for learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "spacy>=3.7.0",
        "language-tool-python>=2.7.1",
        "pyspellchecker>=0.7.2",
        "textstat>=0.7.3",
        "colorama>=0.4.6",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "paragraph-checker=src.main:main",
        ],
    },
)
