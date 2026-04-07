"""Tests for logo drawing functionality."""

import pytest
from PIL import Image, ImageDraw

from src.image_generator.logos import LogoDrawer


class TestLogoDrawer:
    """Test suite for LogoDrawer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.drawer = LogoDrawer()
        self.size = 300
        self.color = "#0055FF"

    def test_draw_swiftui_logo(self):
        """Test SwiftUI logo drawing."""
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Should not raise exception
        self.drawer.draw_logo(draw, self.size, self.color, "swiftui")

        # Verify image has content (non-zero pixels)
        assert img.getbbox() is not None

    def test_draw_react_logo(self):
        """Test React logo drawing."""
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        self.drawer.draw_logo(draw, self.size, self.color, "react")
        assert img.getbbox() is not None

    def test_draw_flutter_logo(self):
        """Test Flutter logo drawing."""
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        self.drawer.draw_logo(draw, self.size, self.color, "flutter")
        assert img.getbbox() is not None

    def test_draw_unknown_framework(self):
        """Test handling of unknown framework."""
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Should not raise exception for unknown framework
        self.drawer.draw_logo(draw, self.size, self.color, "unknown")

    def test_create_svg_swiftui(self, tmp_path):
        """Test SVG creation for SwiftUI."""
        svg_path = tmp_path / "test_swiftui.svg"
        self.drawer.create_svg(str(svg_path), self.size, self.color, "swiftui")

        assert svg_path.exists()
        content = svg_path.read_text()
        assert "<svg" in content
        assert "SwiftUI" in content

    def test_create_svg_react(self, tmp_path):
        """Test SVG creation for React."""
        svg_path = tmp_path / "test_react.svg"
        self.drawer.create_svg(str(svg_path), self.size, self.color, "react")

        assert svg_path.exists()
        content = svg_path.read_text()
        assert "<svg" in content

    def test_create_svg_flutter(self, tmp_path):
        """Test SVG creation for Flutter."""
        svg_path = tmp_path / "test_flutter.svg"
        self.drawer.create_svg(str(svg_path), self.size, self.color, "flutter")

        assert svg_path.exists()
        content = svg_path.read_text()
        assert "<svg" in content

    def test_svg_has_correct_dimensions(self, tmp_path):
        """Test SVG has correct dimensions."""
        svg_path = tmp_path / "test.svg"
        self.drawer.create_svg(str(svg_path), self.size, self.color, "swiftui")

        content = svg_path.read_text()
        assert f'width="{self.size}"' in content or f'width="{self.size}px"' in content
        assert (
            f'height="{self.size}"' in content or f'height="{self.size}px"' in content
        )

    def test_logo_drawer_simplified_mode(self):
        """Test simplified logo drawing for PNG fallback."""
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        self.drawer.draw_logo(draw, self.size, self.color, "swiftui", simplified=True)
        assert img.getbbox() is not None
