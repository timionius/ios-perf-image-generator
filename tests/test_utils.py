"""Tests for utility functions."""

import os
import tempfile
from pathlib import Path

import pytest

from src.image_generator.utils import FileUtils, MetricsCollector


class TestFileUtils:
    """Test suite for FileUtils class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.file_utils = FileUtils()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ensure_dir_creates_directory(self):
        """Test directory creation."""
        test_dir = os.path.join(self.temp_dir, "new_dir")
        assert not os.path.exists(test_dir)

        self.file_utils.ensure_dir(test_dir)
        assert os.path.exists(test_dir)
        assert os.path.isdir(test_dir)

    def test_ensure_dir_existing_directory(self):
        """Test ensure_dir with existing directory."""
        self.file_utils.ensure_dir(self.temp_dir)
        assert os.path.exists(self.temp_dir)

    def test_get_file_size(self):
        """Test getting file size."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("x" * 1024)  # 1KB

        size = self.file_utils.get_file_size(test_file)
        assert size == 1024

    def test_get_file_size_nonexistent(self):
        """Test getting size of non-existent file."""
        size = self.file_utils.get_file_size("nonexistent.txt")
        assert size == 0

    def test_list_files_by_pattern(self):
        """Test listing files by pattern."""
        # Create test files
        for i in range(3):
            Path(self.temp_dir, f"test_{i}.webp").touch()
        Path(self.temp_dir, "other.txt").touch()

        files = self.file_utils.list_files(self.temp_dir, "*.webp")
        assert len(files) == 3
        assert all(f.endswith(".webp") for f in files)

    def test_delete_directory(self):
        """Test directory deletion."""
        test_dir = os.path.join(self.temp_dir, "to_delete")
        os.makedirs(test_dir)
        Path(test_dir, "file.txt").touch()

        self.file_utils.delete_directory(test_dir)
        assert not os.path.exists(test_dir)

    def test_get_timestamp(self):
        """Test timestamp generation."""
        timestamp = self.file_utils.get_timestamp()
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0

    def test_copy_file(self):
        """Test file copying."""
        src = os.path.join(self.temp_dir, "source.txt")
        dst = os.path.join(self.temp_dir, "dest.txt")

        with open(src, "w") as f:
            f.write("test content")

        result = self.file_utils.copy_file(src, dst)
        assert result is True
        assert os.path.exists(dst)

    def test_copy_file_nonexistent(self):
        """Test copying non-existent file."""
        result = self.file_utils.copy_file("nonexistent.txt", "dest.txt")
        assert result is False


class TestMetricsCollector:
    """Test suite for MetricsCollector class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.metrics = MetricsCollector()

    def test_start_and_end_timer(self):
        """Test timer functionality."""
        self.metrics.start_timer("test_task")
        import time

        time.sleep(0.1)
        elapsed = self.metrics.end_timer("test_task")

        assert elapsed >= 100  # Should be at least 100ms
        assert elapsed < 200  # Should be less than 200ms

    def test_end_timer_nonexistent(self):
        """Test ending non-existent timer."""
        elapsed = self.metrics.end_timer("nonexistent")
        assert elapsed == 0

    def test_multiple_timers(self):
        """Test multiple concurrent timers."""
        self.metrics.start_timer("task1")
        self.metrics.start_timer("task2")
        import time

        time.sleep(0.05)

        elapsed1 = self.metrics.end_timer("task1")
        elapsed2 = self.metrics.end_timer("task2")

        assert elapsed1 > 0
        assert elapsed2 > 0

    def test_get_all_metrics(self):
        """Test retrieving all metrics."""
        self.metrics.start_timer("task1")
        self.metrics.end_timer("task1")

        all_metrics = self.metrics.get_all_metrics()
        assert "task1" in all_metrics
        assert all_metrics["task1"] > 0

    def test_reset_metrics(self):
        """Test resetting all metrics."""
        self.metrics.start_timer("task1")
        self.metrics.end_timer("task1")

        self.metrics.reset()
        assert len(self.metrics.get_all_metrics()) == 0

    def test_average_timer(self):
        """Test timer with average calculation."""
        for i in range(3):
            self.metrics.start_timer(f"task_{i}")
            self.metrics.end_timer(f"task_{i}")

        avg = self.metrics.get_average_time()
        assert avg > 0
