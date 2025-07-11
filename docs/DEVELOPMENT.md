# Development Guide

## Architecture Overview

This application follows Clean Architecture principles with the following layers:

### Domain Layer (`core/`)
- **Purpose**: Contains business entities and rules
- **Files**: `domain.py` - Core entities, interfaces, and business logic
- **Dependencies**: None (most inner layer)

### Application Layer (`services/`)
- **Purpose**: Contains use cases and application services
- **Files**: `implementations.py` - Service implementations
- **Dependencies**: Core layer only

### Infrastructure Layer (`data/`, `config/`)
- **Purpose**: External concerns like databases, file systems, APIs
- **Files**: Configuration management, data persistence
- **Dependencies**: Core and Application layers

### Presentation Layer (`ui/`)
- **Purpose**: User interface components
- **Files**: PyQt6 windows, widgets, internationalization
- **Dependencies**: All other layers

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/Glikomannan/YoutubeToVideo.git
cd YoutubeToVideo

# Install dependencies
pip install -r requirements_new.txt

# Install development tools
pip install black flake8 mypy pytest pytest-cov pytest-asyncio

# Run tests to verify setup
python -m pytest tests/ -v
```

### 2. Running the Application

```bash
# Console demo (no GUI required)
python demo.py

# Full GUI application (requires display)
python main.py
```

### 3. Code Quality Standards

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .

# Run tests with coverage
python -m pytest tests/ -v --cov=. --cov-report=html
```

### 4. Configuration Management

The application supports multiple configuration formats:

```bash
# YAML (recommended)
config/app.yaml

# JSON
config/app.json

# TOML
config/app.toml
```

### 5. Adding New Features

#### Adding a New Service

1. Define interface in `core/domain.py`:
```python
class NewService(ABC):
    @abstractmethod
    def new_method(self, param: str) -> str:
        pass
```

2. Implement in `services/implementations.py`:
```python
class NewServiceImpl(NewService):
    def new_method(self, param: str) -> str:
        return f"Processed: {param}"
```

3. Add to service factory:
```python
@staticmethod
def create_new_service() -> NewService:
    return NewServiceImpl()
```

4. Write tests in `tests/test_services.py`

#### Adding UI Components

1. Create widget in `ui/` directory
2. Follow dark theme styling from `DarkTheme` class
3. Add internationalization strings to `ui/i18n.py`
4. Register translations for all supported languages

#### Adding Configuration Options

1. Add fields to appropriate config dataclass in `config/config_manager.py`
2. Update default values
3. Add validation if needed
4. Test configuration loading/saving

## Testing Strategy

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Service Tests**: Test async service operations
- **Configuration Tests**: Test config loading/saving

### Running Specific Tests

```bash
# All tests
python -m pytest tests/ -v

# Configuration tests only
python -m pytest tests/test_config.py -v

# Service tests only
python -m pytest tests/test_services.py -v

# With coverage
python -m pytest tests/ -v --cov=. --cov-report=html
```

### Test Coverage Goals

- **Target**: 95%+ coverage
- **Current**: 93%+ on new architecture modules
- **Exclusions**: UI components (requires display), demo scripts

## Compliance Guidelines

### GDPR Compliance

1. **Data Collection**: Only collect necessary data
2. **User Consent**: Implement consent management
3. **Data Access**: Provide data export functionality
4. **Data Deletion**: Implement right to be forgotten
5. **Audit Logging**: Log all data processing activities

### HIPAA Compliance

1. **Access Controls**: Implement role-based access
2. **Encryption**: Use AES-256 for sensitive data
3. **Audit Trails**: Comprehensive logging
4. **Data Integrity**: Validate and verify data
5. **Transmission Security**: Secure communication

### Implementation

```python
from services.implementations import ServiceFactory

# Get compliance service
compliance_service = ServiceFactory.create_compliance_service()

# Log user action
compliance_service.log_user_action("user-123", "data_access", {"type": "video"})

# Encrypt sensitive data
encrypted = compliance_service.encrypt_data("sensitive information")

# Anonymize personal data
anonymized = compliance_service.anonymize_data({"email": "user@example.com"})
```

## Performance Considerations

### Async Operations

All AI service calls are async to prevent UI blocking:

```python
# Correct async usage
result = await text_service.generate_script("topic", "en", 60.0)

# For non-async contexts
import asyncio
result = asyncio.run(text_service.generate_script("topic", "en", 60.0))
```

### Resource Management

- Temporary files are automatically cleaned up
- Services use dependency injection for loose coupling
- Configuration is loaded once and cached

### Scalability

- Service layer supports multiple implementations
- Plugin architecture allows extensions
- Configuration supports environment-specific settings

## Troubleshooting

### Common Issues

#### PyQt6 Import Errors
```bash
# Missing PyQt6
pip install PyQt6

# Missing display (headless environment)
# Use demo.py instead of main.py
python demo.py
```

#### Configuration Errors
```bash
# Invalid configuration file
# Delete and regenerate
rm config/app.yaml
python -c "from config.config_manager import get_config_manager; get_config_manager().save_config()"
```

#### Test Failures
```bash
# Missing test dependencies
pip install pytest pytest-cov pytest-asyncio

# Clear test cache
rm -rf .pytest_cache __pycache__
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Add docstrings to all public methods
- Maintain test coverage above 90%

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Run quality checks
5. Submit pull request

### Attribution

All contributions must maintain attribution to:
**Mustafa Hüseyin Temel, M.D.** as the original creator and architect.

---

**Created by: Mustafa Hüseyin Temel, M.D.**