"""
Tests for configuration management system.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import pytest
import os
import yaml
import json
import toml
from config.config_manager import ConfigManager, ConfigFormat, AppConfig, UIConfig


class TestConfigManager:
    """Test cases for configuration manager."""
    
    def test_config_manager_initialization(self, temp_config_dir):
        """Test configuration manager initialization."""
        manager = ConfigManager(temp_config_dir)
        assert manager.config_dir.exists()
        assert isinstance(manager.config, AppConfig)
    
    def test_save_and_load_yaml_config(self, config_manager):
        """Test saving and loading YAML configuration."""
        # Modify configuration
        config_manager.config.app_name = "Test App"
        config_manager.config.ui.theme = "light"
        
        # Save configuration
        config_manager.save_config(ConfigFormat.YAML)
        
        # Verify file exists
        config_file = config_manager.config_dir / "app.yaml"
        assert config_file.exists()
        
        # Load configuration in new manager
        new_manager = ConfigManager(config_manager.config_dir)
        loaded_config = new_manager.load_config(ConfigFormat.YAML)
        
        assert loaded_config.app_name == "Test App"
        assert loaded_config.ui.theme == "light"
    
    def test_save_and_load_json_config(self, config_manager):
        """Test saving and loading JSON configuration."""
        config_manager.config.app_version = "3.0.0"
        config_manager.config.ui.font_size = 14
        
        config_manager.save_config(ConfigFormat.JSON)
        
        config_file = config_manager.config_dir / "app.json"
        assert config_file.exists()
        
        new_manager = ConfigManager(config_manager.config_dir)
        loaded_config = new_manager.load_config(ConfigFormat.JSON)
        
        assert loaded_config.app_version == "3.0.0"
        assert loaded_config.ui.font_size == 14
    
    def test_save_and_load_toml_config(self, config_manager):
        """Test saving and loading TOML configuration."""
        config_manager.config.author = "Test Author"
        config_manager.config.ui.window_width = 1600
        
        config_manager.save_config(ConfigFormat.TOML)
        
        config_file = config_manager.config_dir / "app.toml"
        assert config_file.exists()
        
        new_manager = ConfigManager(config_manager.config_dir)
        loaded_config = new_manager.load_config(ConfigFormat.TOML)
        
        assert loaded_config.author == "Test Author"
        assert loaded_config.ui.window_width == 1600
    
    def test_update_config(self, config_manager):
        """Test updating configuration values."""
        original_name = config_manager.config.app_name
        
        config_manager.update_config(app_name="Updated Name")
        
        assert config_manager.config.app_name == "Updated Name"
        assert config_manager.config.app_name != original_name
    
    def test_reset_to_defaults(self, config_manager):
        """Test resetting configuration to defaults."""
        # Modify configuration
        config_manager.config.app_name = "Modified Name"
        config_manager.config.ui.theme = "custom"
        
        # Reset to defaults
        config_manager.reset_to_defaults()
        
        # Verify defaults are restored
        default_config = AppConfig()
        assert config_manager.config.app_name == default_config.app_name
        assert config_manager.config.ui.theme == default_config.ui.theme
    
    def test_load_nonexistent_config_creates_default(self, config_manager):
        """Test that loading non-existent config creates default file."""
        config_file = config_manager.config_dir / "app.yaml"
        assert not config_file.exists()
        
        loaded_config = config_manager.load_config(ConfigFormat.YAML)
        
        # File should be created with defaults
        assert config_file.exists()
        assert loaded_config.author == "Mustafa Hüseyin Temel, M.D."
    
    def test_config_with_invalid_data(self, config_manager):
        """Test handling of invalid configuration data."""
        config_file = config_manager.config_dir / "app.yaml"
        
        # Write invalid YAML
        with open(config_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        # Should handle gracefully and return current config
        loaded_config = config_manager.load_config(ConfigFormat.YAML)
        assert isinstance(loaded_config, AppConfig)


class TestAppConfig:
    """Test cases for application configuration dataclasses."""
    
    def test_app_config_defaults(self):
        """Test default values in application configuration."""
        config = AppConfig()
        
        assert config.app_name == "YouTube to Video Generator"
        assert config.app_version == "2.0.0"
        assert config.author == "Mustafa Hüseyin Temel, M.D."
        assert config.auto_save_enabled is True
    
    def test_ui_config_defaults(self):
        """Test default values in UI configuration."""
        ui_config = UIConfig()
        
        assert ui_config.theme == "dark"
        assert ui_config.language == "en"
        assert ui_config.font_family == "Segoe UI"
        assert ui_config.font_size == 10
        assert ui_config.window_width == 1200
        assert ui_config.window_height == 800
        assert ui_config.high_dpi_scaling is True
        assert ui_config.accessibility_mode is False
    
    def test_config_serialization(self):
        """Test configuration serialization to dictionary."""
        from dataclasses import asdict
        
        config = AppConfig()
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert 'ui' in config_dict
        assert 'api' in config_dict
        assert 'video' in config_dict
        assert 'logging' in config_dict
        assert 'compliance' in config_dict
        
        # Check nested structure
        assert 'theme' in config_dict['ui']
        assert 'data_encryption_enabled' in config_dict['compliance']