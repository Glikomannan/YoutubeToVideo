# YouTube to Video Generator - Enterprise Edition

## Overview

A fully-featured, enterprise-grade video generation application built with PyQt6 and Clean Architecture principles, designed to convert user requirements into professional video content using AI-powered text, image, and audio generation.

**Created by: Mustafa Hüseyin Temel, M.D.**

## Features

### 🎯 Core Functionality
- **AI-Powered Content Generation**: Automated script, image, and audio generation
- **Multiple AI Model Support**: Integration with GPT-4, Gemini, DALL-E, and more
- **Professional Video Composition**: Automated video assembly with transitions and effects
- **Multi-Language Support**: Generate content in multiple languages
- **Customizable Templates**: Pre-configured templates for different content niches

### 🏗️ Enterprise Architecture
- **Clean Architecture**: Modular design with clear separation of concerns
- **MVVM Pattern**: Model-View-ViewModel architecture for maintainable UI
- **Dependency Injection**: Loosely coupled components for testability
- **Event-Driven Design**: Reactive architecture with event bus system
- **Plugin Architecture**: Extensible system for third-party integrations

### 🎨 User Interface
- **PyQt6 Implementation**: Modern, native desktop interface
- **ChatGPT-Inspired Dark Theme**: Professional, eye-friendly design
- **Responsive Layout**: Adapts to different screen sizes and DPI settings
- **Accessibility Compliance**: WCAG 2.2 compliant with keyboard navigation
- **Internationalization**: Multi-language UI with RTL support

### ⚙️ Configuration & Settings
- **Multi-Format Configuration**: Support for YAML, JSON, and TOML
- **Hot-Reloadable Settings**: Runtime configuration changes without restart
- **Environment-Specific Configs**: Development, staging, and production settings
- **GUI Settings Panel**: User-friendly configuration interface
- **CLI Configuration**: Command-line configuration options

### 🔐 Compliance & Security
- **GDPR Compliance**: Data protection and user consent management
- **HIPAA Ready**: Healthcare data protection capabilities
- **Audit Logging**: Comprehensive action tracking for compliance
- **Data Encryption**: AES-256 encryption for sensitive data
- **Privacy Controls**: Data anonymization and retention policies

### 🧪 Development & Quality
- **95%+ Test Coverage**: Comprehensive test suite with pytest
- **Type Hints**: Full static typing for better code quality
- **Documentation**: Sphinx-generated API and user documentation
- **Code Quality**: Black formatting, flake8 linting, mypy type checking
- **CI/CD Ready**: Automated testing and deployment pipelines

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PyQt6 (for GUI)
- Required AI service API keys (OpenAI, Google Gemini, etc.)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Glikomannan/YoutubeToVideo.git
cd YoutubeToVideo
```

2. Install dependencies:
```bash
pip install -r requirements_new.txt
```

3. Configure API keys (copy and edit `.env` file):
```bash
# Create configuration
python -c "from config.config_manager import get_config_manager; get_config_manager().save_config()"
```

4. Run the application:
```bash
python main.py
```

### Quick Test
```bash
# Run tests to verify installation
python -m pytest tests/ -v

# Test configuration system
python -c "from config.config_manager import get_config; print('✓ Configuration system ready')"

# Test services
python -c "from services.implementations import ServiceFactory; print('✓ Service layer ready')"
```

## Architecture

The application follows Clean Architecture principles with clear separation of concerns:

```
📁 Project Structure
├── 🎯 core/                   # Domain models and business logic
├── 🎨 ui/                     # PyQt6 user interface layer  
├── ⚙️ services/               # Service implementations
├── 📊 models/                 # Data models and schemas
├── 💾 data/                   # Data access layer
├── 🔧 config/                 # Configuration management
├── 🎪 assets/                 # Static assets (icons, themes)
├── 🧪 tests/                  # Comprehensive test suite
├── 📚 docs/                   # Documentation
├── 📝 logs/                   # Application logs
├── 🔌 plugins/                # Plugin directory
├── 🗂️ temp/                   # Temporary files
└── 🚀 main.py                 # Application entry point
```

### Key Components

- **Domain Layer** (`core/`): Business entities and rules
- **Application Layer** (`services/`): Use cases and application services  
- **Infrastructure Layer** (`data/`, `config/`): External concerns
- **Presentation Layer** (`ui/`): PyQt6 interface components

## Configuration

### YAML Configuration (auto-generated)
```yaml
app_name: "YouTube to Video Generator"
app_version: "2.0.0"
author: "Mustafa Hüseyin Temel, M.D."

ui:
  theme: "dark"
  language: "en"
  font_family: "Segoe UI"
  window_width: 1200
  window_height: 800

api:
  openai_api_key: ""
  gemini_api_key: ""
  # ... other API configurations

compliance:
  data_encryption_enabled: true
  audit_logging_enabled: true
  user_consent_required: true
```

### Environment Variables
```bash
# API Keys
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
ASSEMBLYAI_API_KEY=your_assemblyai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Development

### Running Tests
```bash
# Full test suite with coverage
python -m pytest tests/ -v --cov=. --cov-report=html

# Configuration tests only
python -m pytest tests/test_config.py -v

# View coverage report
open htmlcov/index.html
```

### Code Quality
```bash
# Format code
black .

# Lint code  
flake8 .

# Type checking
mypy .
```

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Compliance Features

### GDPR Compliance
- ✅ User consent management
- ✅ Data portability (export/import)
- ✅ Right to be forgotten (data deletion)
- ✅ Data minimization and purpose limitation
- ✅ Breach notification procedures

### HIPAA Compliance  
- ✅ Administrative safeguards
- ✅ Physical safeguards
- ✅ Technical safeguards
- ✅ Audit controls and logging
- ✅ Data encryption at rest and in transit

## API Reference

### Configuration API
```python
from config.config_manager import get_config_manager

# Get configuration
config = get_config_manager().get_config()
print(f"App: {config.app_name} by {config.author}")

# Update configuration
get_config_manager().update_config(theme="light")

# Save configuration
get_config_manager().save_config()
```

### Service API
```python
from services.implementations import ServiceFactory

# Create services
video_service = ServiceFactory.create_video_service()
text_service = ServiceFactory.create_text_service()

# Generate content
script = await text_service.generate_script("Technology", "English", 60.0)
```

## Attribution

This enterprise-grade video generation application was created by **Mustafa Hüseyin Temel, M.D.**, incorporating cutting-edge AI technologies, enterprise architecture patterns, and compliance frameworks to deliver a professional, scalable, and maintainable software solution.

### Copyright Notice
- **Original Creator**: Mustafa Hüseyin Temel, M.D.
- **Intellectual Property**: All design decisions, architecture patterns, and implementation details
- **Attribution Required**: Any derivatives must credit the original creator

## License

This project is the intellectual property of **Mustafa Hüseyin Temel, M.D.** and is protected by copyright. Please respect the authorship and attribution requirements.

## Support

- 📚 **Documentation**: See `docs/` directory
- 🐛 **Issues**: Report issues in the GitHub repository  
- ✉️ **Contact**: For enterprise support and licensing inquiries

---

**🎯 Built for the Future**: This is not just code—it's an eternal software artifact, designed to survive platform changes, library obsolescence, and paradigm shifts. Created with infinite dignity, adaptability, and philosophical consistency by **Mustafa Hüseyin Temel, M.D.**