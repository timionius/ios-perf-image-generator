"""Tests for image converter functionality."""

import os
import sys
from pathlib import Path

import pytest

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image

from src.image_generator.converters import ImageConverter


class TestImageConverter:
    """Test suite for ImageConverter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = ImageConverter()

    def test_svg_to_pdf(self, tmp_path):
        """Test SVG to PDF conversion."""
        # Skip if cairosvg is not available
        if not self.converter.cairosvg_available:
            pytest.skip("cairosvg not installed, skipping PDF test")

        # Create a simple SVG
        svg_path = tmp_path / "test.svg"
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
            <rect width="100" height="100" fill="blue"/>
        </svg>"""
        svg_path.write_text(svg_content)

        pdf_path = tmp_path / "test.pdf"
        result = self.converter.svg_to_pdf(str(svg_path), str(pdf_path))

        assert result is True
        assert pdf_path.exists()
        assert os.path.getsize(pdf_path) > 0

    def test_svg_to_pdf_nonexistent_svg(self, tmp_path):
        """Test conversion with non-existent SVG file."""
        pdf_path = tmp_path / "test.pdf"
        result = self.converter.svg_to_pdf("nonexistent.svg", str(pdf_path))

        assert result is False
        assert not pdf_path.exists()

    def test_png_to_webp(self, tmp_path):
        """Test PNG to WebP conversion."""
        # Create a test PNG
        png_path = tmp_path / "test.png"
        img = Image.new("RGB", (100, 100), color="red")
        img.save(png_path)

        webp_path = tmp_path / "test.webp"
        result = self.converter.png_to_webp(str(png_path), str(webp_path), quality=90)

        assert result is True
        assert webp_path.exists()
        assert os.path.getsize(webp_path) > 0

    def test_png_to_webp_nonexistent_png(self, tmp_path):
        """Test PNG to WebP with non-existent source."""
        webp_path = tmp_path / "test.webp"
        result = self.converter.png_to_webp("nonexistent.png", str(webp_path))

        assert result is False
        assert not webp_path.exists()

    def test_resize_image(self, tmp_path):
        """Test image resizing functionality."""
        # Create test image
        src_path = tmp_path / "source.png"
        img = Image.new("RGB", (200, 200), color="green")
        img.save(src_path)

        dst_path = tmp_path / "resized.png"
        result = self.converter.resize_image(str(src_path), str(dst_path), (100, 100))

        assert result is True
        assert dst_path.exists()

        # Verify dimensions
        resized = Image.open(dst_path)
        assert resized.size[0] == 100
        assert resized.size[1] == 100

    def test_resize_image_maintain_aspect(self, tmp_path):
        """Test image resizing maintaining aspect ratio."""
        src_path = tmp_path / "source.png"
        img = Image.new("RGB", (200, 100), color="blue")
        img.save(src_path)

        dst_path = tmp_path / "resized.png"
        result = self.converter.resize_image(
            str(src_path), str(dst_path), (100, 100), maintain_aspect=True
        )

        assert result is True
        resized = Image.open(dst_path)
        # Should maintain aspect ratio (2:1), so 100x50
        assert resized.size[0] == 100
        assert resized.size[1] == 50

    def test_convert_format_batch(self, tmp_path):
        """Test batch format conversion."""
        # Create multiple test images
        images = []
        for i in range(3):
            png_path = tmp_path / f"test_{i}.png"
            img = Image.new("RGB", (100, 100), color="red")
            img.save(png_path)
            images.append(str(png_path))

        results = self.converter.convert_format_batch(images, "webp", quality=85)

        assert len(results) == 3
        for result in results:
            assert result["success"] is True
            assert os.path.exists(result["output_path"])
            assert result["output_path"].endswith(".webp")
