"""Setup configuration for iOS Performance Image Generator."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ios-perf-image-generator",
    version="1.0.0",
    author="Performance Testing Team",
    description="Generate test images for iOS framework performance benchmarking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ios-perf-image-generator",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Pillow>=10.1.0",
        "cairosvg>=2.7.0",
        "svgwrite>=1.4.3",
        "reportlab>=4.0.7",
        "numpy>=1.24.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "pylint>=3.0.2",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "perf-image-gen=src.image_generator.cli:main",
        ],
    },
)
