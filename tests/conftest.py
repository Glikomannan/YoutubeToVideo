"""
Test configuration and fixtures for the application.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import pytest
import asyncio
import tempfile
import os
from typing import Generator
from unittest.mock import Mock

from config.config_manager import ConfigManager, AppConfig
from core.domain import VideoRequest, VideoStatus
from services.implementations import ServiceFactory


@pytest.fixture
def temp_config_dir() -> Generator[str, None, None]:
    """Create a temporary directory for configuration files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def config_manager(temp_config_dir: str) -> ConfigManager:
    """Create a configuration manager with temporary directory."""
    return ConfigManager(temp_config_dir)


@pytest.fixture
def app_config() -> AppConfig:
    """Create a test application configuration."""
    config = AppConfig()
    config.app_name = "Test YouTube Video Generator"
    config.app_version = "2.0.0-test"
    config.author = "Mustafa Hüseyin Temel, M.D."
    return config


@pytest.fixture
def sample_video_request() -> VideoRequest:
    """Create a sample video request for testing."""
    return VideoRequest(
        id="test-request-123",
        niche="Historical Facts",
        language="English",
        duration=60.0,
        resolution=(1080, 1920),
        status=VideoStatus.PENDING
    )


@pytest.fixture
def text_service():
    """Create a mock text generation service."""
    return ServiceFactory.create_text_service()


@pytest.fixture
def audio_service():
    """Create a mock audio generation service."""
    return ServiceFactory.create_audio_service()


@pytest.fixture
def image_service():
    """Create a mock image generation service."""
    return ServiceFactory.create_image_service()


@pytest.fixture
def video_service(text_service, audio_service, image_service):
    """Create a video generation service with mocked dependencies."""
    return ServiceFactory.create_video_service()


@pytest.fixture
def compliance_service():
    """Create a compliance service for testing."""
    return ServiceFactory.create_compliance_service()


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Test utilities
class TestUtils:
    """
    Utility functions for testing.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    @staticmethod
    def create_temp_file(content: str = "test content", 
                        suffix: str = ".txt") -> str:
        """Create a temporary file with content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, 
                                       delete=False) as f:
            f.write(content)
            return f.name
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """Clean up a temporary file."""
        try:
            os.unlink(file_path)
        except FileNotFoundError:
            pass