"""Tests for the main image generator."""

import os
import sys
from pathlib import Path

import pytest

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image

from src.image_generator.config import GenerationConfig
from src.image_generator.generator import ImageGenerator


class TestImageGenerator:
    """Test suite for ImageGenerator class."""

    def test_initialization_default_config(self):
        """Test generator initialization with default config."""
        generator = ImageGenerator()
        assert generator.config.image_size == 300
        assert generator.config.quality == 95
        assert generator.config.output_dir == "output"
        assert "webp" in generator.config.formats

    def test_initialization_custom_config(self):
        """Test generator initialization with custom config."""
        config = GenerationConfig(
            image_size=512,
            output_dir="custom_output",
            quality=85,
            formats=["webp", "png"],
        )
        generator = ImageGenerator(config)
        assert generator.config.image_size == 512
        assert generator.config.output_dir == "custom_output"
        assert generator.config.quality == 85
        assert generator.config.formats == ["webp", "png"]

    def test_frameworks_constant(self):
        """Test FRAMEWORKS constant contains expected frameworks."""
        assert "swiftui" in ImageGenerator.FRAMEWORKS
        assert "react" in ImageGenerator.FRAMEWORKS
        assert "flutter" in ImageGenerator.FRAMEWORKS
        assert ImageGenerator.FRAMEWORKS["swiftui"] == "#0055FF"
        assert ImageGenerator.FRAMEWORKS["react"] == "#61DAFB"
        assert ImageGenerator.FRAMEWORKS["flutter"] == "#45D1FD"

    def test_generate_webp_images(self, tmp_path):
        """Test WebP image generation."""
        config = GenerationConfig(output_dir=str(tmp_path))
        generator = ImageGenerator(config)
        results = generator._generate_webp_images()

        assert len(results) == 3
        for result in results:
            assert result["format"] == "webp"
            assert result["framework"] in ["swiftui", "react", "flutter"]
            assert os.path.exists(result["path"])
            assert result["size_kb"] > 0
            assert result["generation_time_ms"] >= 0

            # Verify image dimensions
            img = Image.open(result["path"])
            assert img.size[0] == config.image_size
            assert img.size[1] == config.image_size

    def test_generate_svg_images(self, tmp_path):
        """Test SVG image generation."""
        config = GenerationConfig(output_dir=str(tmp_path))
        generator = ImageGenerator(config)
        results = generator._generate_svg_images()

        assert len(results) == 3
        for result in results:
            assert result["format"] == "svg"
            assert os.path.exists(result["path"])
            assert result["size_kb"] > 0

            # Verify SVG file content
            with open(result["path"], "r") as f:
                content = f.read()
                assert "<svg" in content
                assert "xmlns" in content

    def test_generate_png_fallback(self, tmp_path):
        """Test PNG fallback generation."""
        config = GenerationConfig(output_dir=str(tmp_path))
        generator = ImageGenerator(config)
        results = generator._generate_png_fallback()

        assert len(results) == 3
        for result in results:
            assert result["format"] == "png"
            assert os.path.exists(result["path"])
            assert result["size_kb"] > 0

            # Verify image dimensions (2x size for Retina)
            img = Image.open(result["path"])
            assert img.size[0] == config.image_size * 2
            assert img.size[1] == config.image_size * 2

    def test_generate_all_formats(self, tmp_path):
        """Test complete generation of all formats."""
        config = GenerationConfig(
            output_dir=str(tmp_path), formats=["webp", "svg", "png"]
        )
        generator = ImageGenerator(config)
        result = generator.generate_all()

        assert "results" in result
        assert "metrics" in result
        assert result["metrics"]["files_generated"] > 0
        assert result["metrics"]["total_time_ms"] > 0

        # Verify all expected files exist
        for framework in ["swiftui", "react", "flutter"]:
            assert os.path.exists(
                os.path.join(str(tmp_path), f"test_image_{framework}.webp")
            )
            assert os.path.exists(
                os.path.join(str(tmp_path), f"test_image_vector_{framework}.svg")
            )
            assert os.path.exists(
                os.path.join(str(tmp_path), f"test_image_vector_{framework}.png")
            )

    def test_invalid_output_directory(self, tmp_path):
        """Test handling of nested directory creation."""
        nested_path = os.path.join(str(tmp_path), "deep", "nested", "directory", "path")
        config = GenerationConfig(output_dir=nested_path)
        generator = ImageGenerator(config)

        # Should create all nested directories automatically
        generator.file_utils.ensure_dir(config.output_dir)
        # Directory should be created
        assert os.path.exists(config.output_dir)

    @pytest.mark.parametrize("size", [100, 200, 300, 512])
    def test_different_image_sizes(self, tmp_path, size):
        """Test image generation with various sizes."""
        config = GenerationConfig(output_dir=str(tmp_path), image_size=size)
        generator = ImageGenerator(config)
        results = generator._generate_webp_images()

        for result in results:
            img = Image.open(result["path"])
            assert img.size[0] == size
            assert img.size[1] == size

    @pytest.mark.parametrize("quality", [75, 85, 95])
    def test_different_quality_settings(self, tmp_path, quality):
        """Test WebP generation with different quality settings."""
        config = GenerationConfig(output_dir=str(tmp_path), quality=quality)
        generator = ImageGenerator(config)
        results = generator._generate_webp_images()

        for result in results:
            assert result["size_kb"] > 0
