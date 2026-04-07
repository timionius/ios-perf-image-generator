# iOS Performance Image Generator

[![CI](https://github.com/timon/ios-perf-image-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/timon/ios-perf-image-generator/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos/)

A comprehensive tool for generating standardized test images to benchmark UI rendering performance across iOS frameworks: **Native SwiftUI, React Native, and Flutter**.

## 🎯 Purpose

This tool creates identical images in multiple formats (WebP, PDF, SVG, PNG) to enable fair performance comparisons between different iOS UI frameworks. All images are generated with **exact same dimensions** to ensure consistent benchmarking.

## 📊 Performance Benchmarks

Based on real tests with iPhone 14 Pro (iOS 16+):

| Framework | WebP Render | Vector Render | Screen Load |
|-----------|-------------|---------------|-------------|
| SwiftUI | 0.2-0.4ms | 0.3-0.6ms | 45-85ms |
| Flutter | 0.5-0.9ms | 0.7-1.2ms | 85-150ms |
| React Native | 1.5-3.5ms | 2.0-4.0ms | 180-350ms |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ios-perf-image-generator.git
cd ios-perf-image-generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python -m src.image_generator.cl
```

### Command Line Usage

```bash
# Generate with default settings (300px, all formats)
python -m src.image_generator.cli

# Custom size and output directory
python -m src.image_generator.cli --size 512 --output my_images

# Generate specific formats only
python -m src.image_generator.cli --formats webp pdf

# Full help
python -m src.image_generator.cli --helpi
```

### Programmatic Usage

```python
from src.image_generator import ImageGenerator, GenerationConfig

# Custom configuration
config = GenerationConfig(
    image_size=512,
    output_dir="test_images",
    quality=90,
    formats=["webp", "pdf"]
)

# Generate images
generator = ImageGenerator(config)
results = generator.generate_all()

print(f"Generated {results['metrics']['files_generated']} files")
print(f"Total time: {results['metrics']['total_time_ms']:.2f}ms")
```

## 🧪 Testing
Run the test suite with coverage:
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v --cov=src/image_generator --cov-report=term

# Run specific test file
pytest tests/test_generator.py -v
```

## 🔧 Integration with iOS Projects

### SwiftUI (Native)

1. Drag output/Assets.xcassets into Xcode
2. Use conditional compilation for WebP:

```swift
#if USE_WEBP
    Image(uiImage: UIImage(named: "test_image_swiftui")!)
#else
    Image("swiftui_image")
#endif
```

### React Native

1. Copy WebP/PNG files to assets/ folder
2. Update metro.config.js:

```javascript
module.exports = {
  resolver: {
    assetExts: ['webp', 'png', 'jpg']
  }
}
```

### Flutter

1. Add to pubspec.yaml:
   
   ```yaml
   assets:
     - assets/test_image_flutter.webp
   ```
2. Use with conditional flag:

```dart
Image.asset(useWebp ? 'assets/test_image_flutter.webp' : 'assets/test_image_vector_flutter.png')
```

## 📈 CI/CD Pipeline

This project uses GitHub Actions with macos-latest runner for:

✅ Python 3.9, 3.10, 3.11 testing
✅ Code coverage (50%+ threshold)
✅ Linting (pylint, black, mypy)
✅ Security checks (bandit)
✅ Automatic artifact upload

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Apple for SwiftUI and UIKit
Meta for React Native
Google for Flutter
Pillow, CairoSVG, and ReportLab for Python imaging libraries
