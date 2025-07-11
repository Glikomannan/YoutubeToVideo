"""
Tests for service implementations.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import pytest
import asyncio
import tempfile
import os
from services.implementations import (
    ServiceFactory, VideoGenerationServiceImpl, MockTextGenerationService,
    MockAudioGenerationService, MockImageGenerationService, ComplianceServiceImpl
)
from core.domain import VideoRequest, VideoStatus


class TestMockTextGenerationService:
    """Test cases for mock text generation service."""
    
    @pytest.mark.asyncio
    async def test_generate_script_historical_facts(self, text_service):
        """Test script generation for historical facts niche."""
        result = await text_service.generate_script("Historical Facts", "English", 60.0)
        
        assert isinstance(result, dict)
        assert "title" in result
        assert "description" in result
        assert "script" in result
        assert "Historical Facts" in result["title"]
        assert len(result["script"]) > 100
    
    @pytest.mark.asyncio
    async def test_generate_script_custom_niche(self, text_service):
        """Test script generation for custom niche."""
        result = await text_service.generate_script("Custom Topic", "English", 30.0)
        
        assert isinstance(result, dict)
        assert "Custom Topic" in result["title"]
        assert result["script"]
    
    def test_validate_script_valid(self, text_service):
        """Test script validation with valid script."""
        valid_script = "This is a valid script that is long enough to pass validation. " * 5
        assert text_service.validate_script(valid_script) is True
    
    def test_validate_script_too_short(self, text_service):
        """Test script validation with too short script."""
        short_script = "Too short"
        assert text_service.validate_script(short_script) is False
    
    def test_validate_script_too_long(self, text_service):
        """Test script validation with too long script."""
        long_script = "Very long script. " * 200
        assert text_service.validate_script(long_script) is False


class TestMockAudioGenerationService:
    """Test cases for mock audio generation service."""
    
    @pytest.mark.asyncio
    async def test_generate_audio(self, audio_service):
        """Test audio generation from text."""
        text = "This is a test script for audio generation."
        audio_path = await audio_service.generate_audio(text, "default", "English")
        
        assert isinstance(audio_path, str)
        assert audio_path.endswith(".wav")
        assert os.path.exists(audio_path)
        
        # Cleanup
        os.unlink(audio_path)
    
    def test_get_available_voices_english(self, audio_service):
        """Test getting available voices for English."""
        voices = audio_service.get_available_voices("English")
        
        assert isinstance(voices, list)
        assert len(voices) > 0
        assert "en-US-AriaNeural" in voices
    
    def test_get_available_voices_unsupported(self, audio_service):
        """Test getting voices for unsupported language."""
        voices = audio_service.get_available_voices("Unsupported")
        
        assert voices == ["default"]


class TestMockImageGenerationService:
    """Test cases for mock image generation service."""
    
    @pytest.mark.asyncio
    async def test_generate_image(self, image_service):
        """Test image generation from prompt."""
        prompt = "A beautiful sunset over mountains"
        image_path = await image_service.generate_image(prompt)
        
        assert isinstance(image_path, str)
        assert image_path.endswith(".jpg")
        assert os.path.exists(image_path)
        
        # Cleanup
        os.unlink(image_path)
    
    @pytest.mark.asyncio
    async def test_generate_image_with_style(self, image_service):
        """Test image generation with specific style."""
        prompt = "A futuristic city"
        image_path = await image_service.generate_image(prompt, "artistic")
        
        assert isinstance(image_path, str)
        assert os.path.exists(image_path)
        
        # Cleanup
        os.unlink(image_path)
    
    def test_get_available_styles(self, image_service):
        """Test getting available image styles."""
        styles = image_service.get_available_styles()
        
        assert isinstance(styles, list)
        assert "realistic" in styles
        assert "artistic" in styles


class TestVideoGenerationService:
    """Test cases for video generation service."""
    
    def test_validate_request_valid(self, video_service):
        """Test video request validation with valid request."""
        request = VideoRequest(
            id="test-123",
            niche="Historical Facts",
            language="English",
            duration=60.0,
            resolution=(1080, 1920)
        )
        
        assert video_service.validate_request(request) is True
    
    def test_validate_request_missing_niche(self, video_service):
        """Test video request validation with missing niche."""
        request = VideoRequest(
            id="test-123",
            niche="",
            language="English",
            duration=60.0,
            resolution=(1080, 1920)
        )
        
        assert video_service.validate_request(request) is False
    
    def test_validate_request_invalid_duration(self, video_service):
        """Test video request validation with invalid duration."""
        request = VideoRequest(
            id="test-123",
            niche="Historical Facts",
            language="English",
            duration=20.0,  # Too short
            resolution=(1080, 1920)
        )
        
        assert video_service.validate_request(request) is False
    
    @pytest.mark.asyncio
    async def test_generate_video(self, video_service, sample_video_request):
        """Test complete video generation process."""
        result = await video_service.generate_video(sample_video_request)
        
        assert result.request_id == sample_video_request.id
        assert result.title
        assert result.description
        assert result.script
        assert result.duration == sample_video_request.duration
        assert os.path.exists(result.file_path)
        
        # Cleanup
        os.unlink(result.file_path)


class TestComplianceService:
    """Test cases for compliance service."""
    
    def test_log_user_action(self, compliance_service):
        """Test user action logging."""
        user_id = "test-user-123"
        action = "generate_video"
        data = {"niche": "Historical Facts", "duration": 60.0}
        
        # This should not raise an exception
        compliance_service.log_user_action(user_id, action, data)
        
        # Verify log file exists
        assert os.path.exists(compliance_service.audit_log_path)
    
    def test_encrypt_decrypt_data(self, compliance_service):
        """Test data encryption and decryption."""
        original_data = "sensitive information"
        
        encrypted = compliance_service.encrypt_data(original_data)
        assert encrypted != original_data
        
        decrypted = compliance_service.decrypt_data(encrypted)
        assert decrypted == original_data
    
    def test_anonymize_data(self, compliance_service):
        """Test data anonymization."""
        # Enable anonymization for this test
        compliance_service.config.compliance.anonymization_enabled = True
        
        data = {
            "email": "user@example.com",
            "name": "John Doe",
            "niche": "Historical Facts"
        }
        
        anonymized = compliance_service.anonymize_data(data)
        
        # Personal fields should be anonymized
        assert anonymized["email"] != data["email"]
        assert anonymized["name"] != data["name"]
        # Non-personal fields should remain
        assert anonymized["niche"] == data["niche"]


class TestServiceFactory:
    """Test cases for service factory."""
    
    def test_create_text_service(self):
        """Test text service creation."""
        service = ServiceFactory.create_text_service()
        assert isinstance(service, MockTextGenerationService)
    
    def test_create_audio_service(self):
        """Test audio service creation."""
        service = ServiceFactory.create_audio_service()
        assert isinstance(service, MockAudioGenerationService)
    
    def test_create_image_service(self):
        """Test image service creation."""
        service = ServiceFactory.create_image_service()
        assert isinstance(service, MockImageGenerationService)
    
    def test_create_video_service(self):
        """Test video service creation."""
        service = ServiceFactory.create_video_service()
        assert isinstance(service, VideoGenerationServiceImpl)
    
    def test_create_compliance_service(self):
        """Test compliance service creation."""
        service = ServiceFactory.create_compliance_service()
        assert isinstance(service, ComplianceServiceImpl)