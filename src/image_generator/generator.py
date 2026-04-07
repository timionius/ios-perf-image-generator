"""Main image generator module."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PIL import Image, ImageDraw

from .config import GenerationConfig
from .converters import ImageConverter
from .logos import LogoDrawer
from .utils import FileUtils, MetricsCollector


class ImageGenerator:
    """Main class for generating performance test images."""

    FRAMEWORKS = {"swiftui": "#0055FF", "react": "#61DAFB", "flutter": "#45D1FD"}

    def __init__(self, config: Optional[GenerationConfig] = None):
        """Initialize the image generator.

        Args:
            config: Configuration for generation. If None, default config used.
        """
        self.config = config or GenerationConfig()
        self.logo_drawer = LogoDrawer()
        self.converter = ImageConverter()
        self.metrics = MetricsCollector()
        self.file_utils = FileUtils()

    def generate_all(self) -> Dict[str, Any]:
        """Generate all images for all frameworks.

        Returns:
            Dictionary with generation metrics and results.
        """
        self.metrics.start_timer("total")

        # Create output directory
        self.file_utils.ensure_dir(self.config.output_dir)

        results: Dict[str, Any] = {
            "webp": [],
            "svg": [],
            "pdf": [],
            "png": [],
            "asset_catalogs": [],
        }

        # Generate each format
        if "webp" in self.config.formats:
            results["webp"] = self._generate_webp_images()

        if "svg" in self.config.formats:
            results["svg"] = self._generate_svg_images()

        if "pdf" in self.config.formats:
            results["pdf"] = self._generate_pdf_images()

        if "png" in self.config.formats:
            results["png"] = self._generate_png_fallback()

        # Generate asset catalogs
        results["asset_catalogs"] = self._generate_asset_catalogs()

        total_time = self.metrics.end_timer("total")

        return {
            "results": results,
            "metrics": {
                "total_time_ms": total_time,
                "files_generated": sum(
                    len(v) for v in results.values() if isinstance(v, list)
                ),
                "output_dir": self.config.output_dir,
            },
        }

    def _generate_webp_images(self) -> List[Dict[str, Any]]:
        """Generate WebP images for all frameworks.

        Returns:
            List of generated file information.
        """
        generated = []

        for framework, color in self.FRAMEWORKS.items():
            self.metrics.start_timer(f"webp_{framework}")

            # Create image
            img = Image.new(
                "RGBA",
                (self.config.image_size, self.config.image_size),
                (255, 255, 255, 0),
            )
            draw = ImageDraw.Draw(img)

            # Draw background
            draw.rectangle(
                [0, 0, self.config.image_size, self.config.image_size],
                fill=(240, 248, 255, 255),
            )

            # Draw logo
            self.logo_drawer.draw_logo(draw, self.config.image_size, color, framework)

            # Draw border
            draw.rectangle(
                [2, 2, self.config.image_size - 2, self.config.image_size - 2],
                outline=color,
                width=4,
            )

            # Save as WebP
            filepath = os.path.join(
                self.config.output_dir, f"test_image_{framework}.webp"
            )
            img.save(filepath, "WEBP", quality=self.config.quality, method=6)

            generation_time = self.metrics.end_timer(f"webp_{framework}")
            file_size = os.path.getsize(filepath) / 1024

            generated.append(
                {
                    "framework": framework,
                    "format": "webp",
                    "path": filepath,
                    "size_kb": round(file_size, 2),
                    "generation_time_ms": round(generation_time, 2),
                }
            )

        return generated

    def _generate_svg_images(self) -> List[Dict[str, Any]]:
        """Generate SVG vector images for all frameworks.

        Returns:
            List of generated file information.
        """
        generated = []

        for framework, color in self.FRAMEWORKS.items():
            self.metrics.start_timer(f"svg_{framework}")

            svg_path = os.path.join(
                self.config.output_dir, f"test_image_vector_{framework}.svg"
            )
            self.logo_drawer.create_svg(
                svg_path, self.config.image_size, color, framework
            )

            generation_time = self.metrics.end_timer(f"svg_{framework}")
            file_size = os.path.getsize(svg_path) / 1024

            generated.append(
                {
                    "framework": framework,
                    "format": "svg",
                    "path": svg_path,
                    "size_kb": round(file_size, 2),
                    "generation_time_ms": round(generation_time, 2),
                }
            )

        return generated

    def _generate_pdf_images(self) -> List[Dict[str, Any]]:
        """Generate PDF vector images from SVGs.

        Returns:
            List of generated file information.
        """
        generated = []

        for framework in self.FRAMEWORKS.keys():
            self.metrics.start_timer(f"pdf_{framework}")

            svg_path = os.path.join(
                self.config.output_dir, f"test_image_vector_{framework}.svg"
            )
            pdf_path = os.path.join(
                self.config.output_dir, f"test_image_vector_{framework}.pdf"
            )

            if os.path.exists(svg_path):
                success = self.converter.svg_to_pdf(svg_path, pdf_path)
                if success:
                    generation_time = self.metrics.end_timer(f"pdf_{framework}")
                    file_size = os.path.getsize(pdf_path) / 1024

                    generated.append(
                        {
                            "framework": framework,
                            "format": "pdf",
                            "path": pdf_path,
                            "size_kb": round(file_size, 2),
                            "generation_time_ms": round(generation_time, 2),
                        }
                    )
            else:
                self.metrics.end_timer(f"pdf_{framework}")  # Still end timer

        return generated

    def _generate_png_fallback(self) -> List[Dict[str, Any]]:
        """Generate PNG fallback images for React Native.

        Returns:
            List of generated file information.
        """
        generated = []
        scaled_size = self.config.image_size * 2

        for framework, color in self.FRAMEWORKS.items():
            self.metrics.start_timer(f"png_{framework}")

            img = Image.new("RGBA", (scaled_size, scaled_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            draw.rectangle([0, 0, scaled_size, scaled_size], fill=(240, 248, 255, 255))

            # Simplified logo for PNG (using same drawer but scaled)
            self.logo_drawer.draw_logo(
                draw, scaled_size, color, framework, simplified=True
            )

            png_path = os.path.join(
                self.config.output_dir, f"test_image_vector_{framework}.png"
            )
            img.save(png_path, "PNG", optimize=True)

            generation_time = self.metrics.end_timer(f"png_{framework}")
            file_size = os.path.getsize(png_path) / 1024

            generated.append(
                {
                    "framework": framework,
                    "format": "png",
                    "path": png_path,
                    "size_kb": round(file_size, 2),
                    "generation_time_ms": round(generation_time, 2),
                }
            )

        return generated

    def _generate_asset_catalogs(self) -> List[str]:
        """Generate iOS asset catalog structure.

        Returns:
            List of created asset catalog paths.
        """
        catalogs = []
        assets_dir = os.path.join(self.config.output_dir, "Assets.xcassets")

        for framework in self.FRAMEWORKS.keys():
            imageset_dir = os.path.join(assets_dir, f"{framework}_image.imageset")
            os.makedirs(imageset_dir, exist_ok=True)

            # Copy PDF if exists
            pdf_source = os.path.join(
                self.config.output_dir, f"test_image_vector_{framework}.pdf"
            )
            pdf_dest = os.path.join(imageset_dir, f"{framework}_image.pdf")

            if os.path.exists(pdf_source):
                shutil.copy2(pdf_source, pdf_dest)

            # Create Contents.json
            contents = {
                "images": [
                    {"idiom": "universal", "filename": f"{framework}_image.pdf"}
                ],
                "info": {"author": "xcode", "version": 1},
                "properties": {"preserves-vector-representation": True},
            }

            contents_path = os.path.join(imageset_dir, "Contents.json")
            with open(contents_path, "w") as f:
                json.dump(contents, f, indent=2)

            catalogs.append(imageset_dir)

        return catalogs
