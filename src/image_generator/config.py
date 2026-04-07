"""Configuration module for image generation."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class GenerationConfig:
    """Configuration for image generation."""
    
    image_size: int = 300
    output_dir: str = "output"
    quality: int = 95
    formats: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = ["webp", "pdf", "svg", "png"]
        
        # Validate formats
        valid_formats = {"webp", "pdf", "svg", "png"}
        for fmt in self.formats:
            if fmt not in valid_formats:
                raise ValueError(f"Invalid format: {fmt}. Must be one of {valid_formats}")
        
        # Validate quality
        if not 1 <= self.quality <= 100:
            raise ValueError(f"Quality must be between 1 and 100, got {self.quality}")
        
        # Validate image size
        if not 1 <= self.image_size <= 4096:
            raise ValueError(f"Image size must be between 1 and 4096, got {self.image_size}")
