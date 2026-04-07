"""Image conversion utilities."""

import os
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image


class ImageConverter:
    """Handles image format conversions."""
    
    def svg_to_pdf(self, svg_path: str, pdf_path: str) -> bool:
        """Convert SVG to PDF.
        
        Args:
            svg_path: Path to SVG file
            pdf_path: Output PDF path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import cairosvg
            cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
            return True
        except Exception as e:
            print(f"Error converting SVG to PDF: {e}")
            return False
    
    def png_to_webp(self, png_path: str, webp_path: str, quality: int = 90) -> bool:
        """Convert PNG to WebP.
        
        Args:
            png_path: Path to PNG file
            webp_path: Output WebP path
            quality: WebP quality (1-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            img = Image.open(png_path)
            img.save(webp_path, 'WEBP', quality=quality)
            return True
        except Exception as e:
            print(f"Error converting PNG to WebP: {e}")
            return False
    
    def resize_image(self, src_path: str, dst_path: str, size: Tuple[int, int], 
                    maintain_aspect: bool = False) -> bool:
        """Resize an image.
        
        Args:
            src_path: Source image path
            dst_path: Destination image path
            size: Target size (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            img = Image.open(src_path)
            
            if maintain_aspect:
                img.thumbnail(size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Preserve original format
            format = img.format or 'PNG'
            img.save(dst_path, format=format)
            return True
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    def convert_format_batch(self, file_paths: List[str], target_format: str, 
                            quality: Optional[int] = None) -> List[Dict[str, Any]]:
        """Convert multiple images to target format.
        
        Args:
            file_paths: List of source file paths
            target_format: Target format (webp, png, jpg)
            quality: Quality setting for lossy formats
            
        Returns:
            List of conversion results
        """
        results = []
        
        for src_path in file_paths:
            base_name = os.path.splitext(src_path)[0]
            dst_path = f"{base_name}.{target_format.lower()}"
            
            try:
                img = Image.open(src_path)
                
                save_kwargs = {}
                if quality and target_format.lower() == 'webp':
                    save_kwargs['quality'] = quality
                
                img.save(dst_path, target_format.upper(), **save_kwargs)
                
                results.append({
                    "source": src_path,
                    "output_path": dst_path,
                    "success": True,
                    "size_kb": os.path.getsize(dst_path) / 1024
                })
            except Exception as e:
                results.append({
                    "source": src_path,
                    "output_path": dst_path,
                    "success": False,
                    "error": str(e)
                })
        
        return results
