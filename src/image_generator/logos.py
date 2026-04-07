import math

import svgwrite
from PIL import ImageDraw


class LogoDrawer:
    """Handles drawing framework-specific logos."""

    def draw_logo(
        self,
        draw: ImageDraw,
        size: int,
        color: str,
        framework: str,
        simplified: bool = False,
    ):
        """Draw framework-specific logo.

        Args:
            draw: PIL ImageDraw object
            size: Image size in pixels
            color: Logo color
            framework: Framework name (swiftui, react, flutter)
            simplified: Whether to use simplified version
        """
        center = size // 2

        if framework == "swiftui":
            self._draw_swiftui_logo(draw, size, color, center)
        elif framework == "react":
            self._draw_react_logo(draw, size, color, center, simplified)
        elif framework == "flutter":
            self._draw_flutter_logo(draw, size, color, center, simplified)
        else:
            # Default: draw a simple circle
            radius = size // 4
            draw.ellipse(
                [center - radius, center - radius, center + radius, center + radius],
                fill=color,
            )

    def _draw_swiftui_logo(self, draw: ImageDraw, size: int, color: str, center: int):
        """Draw SwiftUI-style logo."""
        radius = size // 3

        # Draw outer circle
        draw.ellipse(
            [center - radius, center - radius, center + radius, center + radius],
            outline=color,
            width=size // 40,
        )

        # Draw inner S curve
        points = [
            (center - radius // 2, center - radius // 2),
            (center + radius // 2, center - radius // 3),
            (center - radius // 2, center),
            (center + radius // 2, center + radius // 3),
            (center - radius // 2, center + radius // 2),
        ]
        draw.line(points, fill=color, width=size // 50)

    def _draw_react_logo(
        self, draw: ImageDraw, size: int, color: str, center: int, simplified: bool
    ):
        """Draw React-style logo."""
        orbit_radius = size // 3
        electron_radius = size // 12

        # Draw three ellipses (orbits)
        for angle in [0, 60, 120]:
            ellipse_width = orbit_radius * 2
            ellipse_height = (
                orbit_radius * 1.2 if not simplified else orbit_radius * 1.5
            )

            points = []
            for t in range(0, 360, 15):
                rad = math.radians(t)
                x = math.cos(rad) * ellipse_width / 2
                y = math.sin(rad) * ellipse_height / 2

                # Rotate
                rot_rad = math.radians(angle)
                rx = x * math.cos(rot_rad) - y * math.sin(rot_rad)
                ry = x * math.sin(rot_rad) + y * math.cos(rot_rad)

                points.append((center + rx, center + ry))

            if len(points) > 1:
                for i in range(len(points) - 1):
                    draw.line([points[i], points[i + 1]], fill=color, width=size // 100)

        # Draw center nucleus
        draw.ellipse(
            [
                center - electron_radius,
                center - electron_radius,
                center + electron_radius,
                center + electron_radius,
            ],
            fill=color,
        )

    def _draw_flutter_logo(
        self, draw: ImageDraw, size: int, color: str, center: int, simplified: bool
    ):
        """Draw Flutter-style logo."""
        bar_width = size // 4
        bar_height = size // 12

        # Draw main vertical bar
        draw.rectangle(
            [
                center - bar_width // 3,
                center - size // 3,
                center + bar_width // 3,
                center + size // 3,
            ],
            fill=color,
        )

        # Draw horizontal bars
        draw.rectangle(
            [
                center - bar_width // 2,
                center - bar_height,
                center + bar_width,
                center + bar_height,
            ],
            fill=color,
        )

        draw.rectangle(
            [
                center - bar_width // 2,
                center + bar_height,
                center + bar_width // 1.5,
                center + bar_height * 3,
            ],
            fill=color,
        )

        if not simplified:
            # Add decorative dots
            dot_radius = size // 20
            draw.ellipse(
                [
                    center + bar_width // 1.2,
                    center + size // 4,
                    center + bar_width // 1.2 + dot_radius * 2,
                    center + size // 4 + dot_radius * 2,
                ],
                fill=color,
            )

    def create_svg(self, svg_path: str, size: int, color: str, framework: str):
        """Create SVG version of logo.

        Args:
            svg_path: Output SVG file path
            size: Image size in pixels
            color: Logo color
            framework: Framework name
        """
        dwg = svgwrite.Drawing(svg_path, size=(size, size))
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=(size, size),
                fill="#F0F8FF",
                stroke=color,
                stroke_width=4,
            )
        )

        center = size // 2

        if framework == "swiftui":
            self._create_swiftui_svg(dwg, size, color, center)
        elif framework == "react":
            self._create_react_svg(dwg, size, color, center)
        elif framework == "flutter":
            self._create_flutter_svg(dwg, size, color, center)

        dwg.save()

    def _create_swiftui_svg(self, dwg, size: int, color: str, center: int):
        """Create SwiftUI SVG."""
        radius = size // 3

        # Outer circle
        dwg.add(
            dwg.circle(
                center=(center, center),
                r=radius,
                fill="none",
                stroke=color,
                stroke_width=8,
            )
        )

        # S-curve
        path = dwg.path(
            d=f"M {center - radius//2} {center - radius//2} "
            f"L {center + radius//2} {center - radius//3} "
            f"L {center - radius//2} {center} "
            f"L {center + radius//2} {center + radius//3} "
            f"L {center - radius//2} {center + radius//2}",
            stroke=color,
            stroke_width=6,
            fill="none",
        )
        dwg.add(path)

        # Text
        dwg.add(
            dwg.text(
                "SwiftUI",
                insert=(center - 35, center + radius + 20),
                fill=color,
                font_size=20,
                font_family="Helvetica",
            )
        )

    def _create_react_svg(self, dwg, size: int, color: str, center: int):
        """Create React SVG."""
        orbit_radius = size // 3
        electron_radius = size // 12

        for angle in [0, 60, 120]:
            g = dwg.g()
            ellipse = dwg.ellipse(
                center=(center, center),
                rx=orbit_radius,
                ry=orbit_radius * 0.7,
                fill="none",
                stroke=color,
                stroke_width=3,
            )
            g.add(ellipse)
            g.rotate(angle, center=(center, center))
            dwg.add(g)

        # Center nucleus
        dwg.add(dwg.circle(center=(center, center), r=electron_radius, fill=color))

    def _create_flutter_svg(self, dwg, size: int, color: str, center: int):
        """Create Flutter SVG."""
        bar_width = size // 4
        bar_height = size // 12

        # Vertical bar
        dwg.add(
            dwg.rect(
                insert=(center - bar_width // 3, center - size // 3),
                size=(bar_width // 1.5, size // 1.5),
                fill=color,
            )
        )

        # Horizontal bars
        dwg.add(
            dwg.rect(
                insert=(center - bar_width // 2, center - bar_height),
                size=(bar_width, bar_height * 2),
                fill=color,
            )
        )

        dwg.add(
            dwg.rect(
                insert=(center - bar_width // 2, center + bar_height),
                size=(bar_width // 1.2, bar_height * 2),
                fill=color,
            )
        )
