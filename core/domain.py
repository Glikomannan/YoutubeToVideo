"""
Core application domain layer following Clean Architecture principles.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime


class VideoStatus(Enum):
    """Video generation status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoFormat(Enum):
    """Supported video formats."""
    MP4 = "mp4"
    AVI = "avi"
    MOV = "mov"
    MKV = "mkv"


@dataclass
class VideoRequest:
    """Domain model for video generation request."""
    id: str
    niche: str
    language: str
    duration: float
    resolution: tuple
    status: VideoStatus = VideoStatus.PENDING
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class VideoResult:
    """Domain model for video generation result."""
    id: str
    request_id: str
    file_path: str
    title: str
    description: str
    script: str
    duration: float
    file_size: int
    metadata: Dict[str, Any]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()


class VideoRepository(ABC):
    """Abstract repository for video data persistence."""
    
    @abstractmethod
    def save_request(self, request: VideoRequest) -> None:
        """Save video generation request."""
        pass
    
    @abstractmethod
    def get_request(self, request_id: str) -> Optional[VideoRequest]:
        """Get video request by ID."""
        pass
    
    @abstractmethod
    def update_request_status(self, request_id: str, status: VideoStatus, 
                             error_message: Optional[str] = None) -> None:
        """Update request status."""
        pass
    
    @abstractmethod
    def save_result(self, result: VideoResult) -> None:
        """Save video generation result."""
        pass
    
    @abstractmethod
    def get_result(self, result_id: str) -> Optional[VideoResult]:
        """Get video result by ID."""
        pass
    
    @abstractmethod
    def get_results_by_request(self, request_id: str) -> List[VideoResult]:
        """Get all results for a request."""
        pass


class VideoGenerationService(ABC):
    """Abstract service for video generation."""
    
    @abstractmethod
    async def generate_video(self, request: VideoRequest) -> VideoResult:
        """Generate video from request."""
        pass
    
    @abstractmethod
    def validate_request(self, request: VideoRequest) -> bool:
        """Validate video generation request."""
        pass


class AudioGenerationService(ABC):
    """Abstract service for audio generation."""
    
    @abstractmethod
    async def generate_audio(self, text: str, voice: str, language: str) -> str:
        """Generate audio from text."""
        pass
    
    @abstractmethod
    def get_available_voices(self, language: str) -> List[str]:
        """Get available voices for language."""
        pass


class ImageGenerationService(ABC):
    """Abstract service for image generation."""
    
    @abstractmethod
    async def generate_image(self, prompt: str, style: str = "realistic") -> str:
        """Generate image from prompt."""
        pass
    
    @abstractmethod
    def get_available_styles(self) -> List[str]:
        """Get available image styles."""
        pass


class TextGenerationService(ABC):
    """Abstract service for text generation."""
    
    @abstractmethod
    async def generate_script(self, niche: str, language: str, 
                             duration: float) -> Dict[str, str]:
        """Generate video script."""
        pass
    
    @abstractmethod
    def validate_script(self, script: str) -> bool:
        """Validate generated script."""
        pass


class ComplianceService(ABC):
    """Abstract service for compliance and audit logging."""
    
    @abstractmethod
    def log_user_action(self, user_id: str, action: str, 
                       data: Dict[str, Any]) -> None:
        """Log user action for audit trail."""
        pass
    
    @abstractmethod
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        pass
    
    @abstractmethod
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        pass
    
    @abstractmethod
    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize personal data."""
        pass


@dataclass
class User:
    """Domain model for application user."""
    id: str
    email: str
    name: str
    preferences: Dict[str, Any]
    consent_given: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()


class UserRepository(ABC):
    """Abstract repository for user data."""
    
    @abstractmethod
    def save_user(self, user: User) -> None:
        """Save user data."""
        pass
    
    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def update_user_preferences(self, user_id: str, 
                              preferences: Dict[str, Any]) -> None:
        """Update user preferences."""
        pass


class EventBus(ABC):
    """Abstract event bus for application events."""
    
    @abstractmethod
    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish an event."""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: str, handler: callable) -> None:
        """Subscribe to an event type."""
        pass
    
    @abstractmethod
    def unsubscribe(self, event_type: str, handler: callable) -> None:
        """Unsubscribe from an event type."""
        pass