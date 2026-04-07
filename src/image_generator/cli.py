"""Command-line interface for the image generator."""

import argparse
import sys

from .config import GenerationConfig
from .generator import ImageGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate iOS performance test images")
    parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=300,
        help="Image size in pixels (default: 300)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="Output directory (default: output)",
    )
    parser.add_argument(
        "--quality", "-q", type=int, default=95, help="WebP quality 1-100 (default: 95)"
    )
    parser.add_argument(
        "--formats",
        "-f",
        nargs="+",
        choices=["webp", "pdf", "svg", "png"],
        default=["webp", "pdf", "svg", "png"],
        help="Formats to generate (default: all)",
    )

    args = parser.parse_args()

    try:
        config = GenerationConfig(
            image_size=args.size,
            output_dir=args.output,
            quality=args.quality,
            formats=args.formats,
        )

        generator = ImageGenerator(config)
        results = generator.generate_all()

        print(f"\n✅ Generation complete!")
        print(f"📁 Output directory: {results['metrics']['output_dir']}")
        print(f"📊 Files generated: {results['metrics']['files_generated']}")
        print(f"⏱️  Total time: {results['metrics']['total_time_ms']:.2f}ms")

        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
