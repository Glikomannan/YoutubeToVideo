"""
Core configuration management system for YouTube to Video application.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import os
import json
import yaml
import toml
from typing import Dict, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


class ConfigFormat(Enum):
    """Supported configuration file formats."""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"


@dataclass
class UIConfig:
    """UI configuration settings."""
    theme: str = "dark"
    language: str = "en"
    font_family: str = "Segoe UI"
    font_size: int = 10
    window_width: int = 1200
    window_height: int = 800
    high_dpi_scaling: bool = True
    accessibility_mode: bool = False


@dataclass
class APIConfig:
    """API configuration settings."""
    openai_api_key: str = ""
    gemini_api_key: str = ""
    assemblyai_api_key: str = ""
    elevenlabs_api_key: str = ""
    segmind_api_key: str = ""


@dataclass
class VideoConfig:
    """Video generation configuration."""
    default_duration: float = 60.0
    default_resolution: tuple = (1080, 1920)
    default_fps: int = 30
    output_format: str = "mp4"
    quality: str = "high"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file_enabled: bool = True
    console_enabled: bool = True
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class ComplianceConfig:
    """GDPR/HIPAA compliance configuration."""
    data_encryption_enabled: bool = True
    audit_logging_enabled: bool = True
    user_consent_required: bool = True
    data_retention_days: int = 365
    anonymization_enabled: bool = False


@dataclass
class AppConfig:
    """Main application configuration."""
    ui: UIConfig = None
    api: APIConfig = None
    video: VideoConfig = None
    logging: LoggingConfig = None
    compliance: ComplianceConfig = None
    
    
    # Application metadata
    app_name: str = "YouTube to Video Generator"
    app_version: str = "2.0.0"
    author: str = "Mustafa Hüseyin Temel, M.D."
    
    # Runtime settings
    auto_save_enabled: bool = True
    plugin_directory: str = "plugins"
    temp_directory: str = "temp"
    
    def __post_init__(self):
        """Initialize nested configurations with defaults."""
        if self.ui is None:
            self.ui = UIConfig()
        if self.api is None:
            self.api = APIConfig()
        if self.video is None:
            self.video = VideoConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
        if self.compliance is None:
            self.compliance = ComplianceConfig()


class ConfigManager:
    """
    Configuration manager with hot-reloading and multi-format support.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    def __init__(self, config_dir: Union[str, Path] = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.config = AppConfig()
        self._watchers = []
        
    def load_config(self, format_type: ConfigFormat = ConfigFormat.YAML) -> AppConfig:
        """Load configuration from file."""
        config_file = self.config_dir / f"app.{format_type.value}"
        
        if not config_file.exists():
            self.save_config(format_type)
            return self.config
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if format_type == ConfigFormat.JSON:
                    data = json.load(f)
                elif format_type == ConfigFormat.YAML:
                    data = yaml.safe_load(f)
                elif format_type == ConfigFormat.TOML:
                    data = toml.load(f)
                
            # Update config with loaded data
            self._update_config_from_dict(data)
            
        except Exception as e:
            print(f"Error loading config: {e}")
            
        return self.config
    
    def save_config(self, format_type: ConfigFormat = ConfigFormat.YAML) -> None:
        """Save configuration to file."""
        config_file = self.config_dir / f"app.{format_type.value}"
        config_dict = asdict(self.config)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                if format_type == ConfigFormat.JSON:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
                elif format_type == ConfigFormat.YAML:
                    yaml.safe_dump(config_dict, f, default_flow_style=False, 
                                 allow_unicode=True, indent=2)
                elif format_type == ConfigFormat.TOML:
                    toml.dump(config_dict, f)
                    
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _update_config_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        if 'ui' in data:
            self.config.ui = UIConfig(**data['ui'])
        if 'api' in data:
            self.config.api = APIConfig(**data['api'])
        if 'video' in data:
            self.config.video = VideoConfig(**data['video'])
        if 'logging' in data:
            self.config.logging = LoggingConfig(**data['logging'])
        if 'compliance' in data:
            self.config.compliance = ComplianceConfig(**data['compliance'])
            
        # Update top-level fields
        for key, value in data.items():
            if hasattr(self.config, key) and key not in ['ui', 'api', 'video', 'logging', 'compliance']:
                setattr(self.config, key, value)
    
    def get_config(self) -> AppConfig:
        """Get current configuration."""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = AppConfig()


# Global configuration instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config() -> AppConfig:
    """Get current application configuration."""
    return get_config_manager().get_config()