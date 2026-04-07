"""Utility functions for file handling and metrics."""

import os
import glob
import shutil
import time
from typing import List, Dict, Optional
from datetime import datetime


class FileUtils:
    """File system utilities."""
    
    @staticmethod
    def ensure_dir(directory: str) -> None:
        """Ensure directory exists, create if it doesn't.
        
        Args:
            directory: Directory path to ensure
        """
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size in bytes.
        
        Args:
            filepath: Path to file
            
        Returns:
            File size in bytes, 0 if file doesn't exist
        """
        if os.path.exists(filepath):
            return os.path.getsize(filepath)
        return 0
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """List files in directory matching pattern.
        
        Args:
            directory: Directory to search
            pattern: File pattern (e.g., "*.webp")
            
        Returns:
            List of matching file paths
        """
        search_path = os.path.join(directory, pattern)
        return glob.glob(search_path)
    
    @staticmethod
    def delete_directory(directory: str) -> bool:
        """Delete directory and all contents.
        
        Args:
            directory: Directory path to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            return True
        except Exception as e:
            print(f"Error deleting directory {directory}: {e}")
            return False
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp as string.
        
        Returns:
            Formatted timestamp string
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """Copy a file.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"Error copying file {src} to {dst}: {e}")
            return False


class MetricsCollector:
    """Collects and stores performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self._timers: Dict[str, float] = {}
        self._metrics: Dict[str, float] = {}
    
    def start_timer(self, name: str) -> None:
        """Start a timer.
        
        Args:
            name: Timer name
        """
        self._timers[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """End a timer and record metric.
        
        Args:
            name: Timer name
            
        Returns:
            Elapsed time in milliseconds
        """
        if name in self._timers:
            elapsed = (time.time() - self._timers[name]) * 1000
            self._metrics[name] = elapsed
            del self._timers[name]
            return elapsed
        return 0.0
    
    def get_all_metrics(self) -> Dict[str, float]:
        """Get all recorded metrics.
        
        Returns:
            Dictionary of metric names and values
        """
        return self._metrics.copy()
    
    def reset(self) -> None:
        """Reset all metrics and timers."""
        self._timers.clear()
        self._metrics.clear()
    
    def get_average_time(self) -> float:
        """Calculate average time of all metrics.
        
        Returns:
            Average time in milliseconds
        """
        if not self._metrics:
            return 0.0
        return sum(self._metrics.values()) / len(self._metrics)
