#!/usr/bin/env python3
"""
YouTube to Video Generator - Enterprise Edition

A fully-featured, enterprise-grade video generation application
built with PyQt6 and Clean Architecture principles.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        'config', 'logs', 'temp', 'assets', 'plugins', 'data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    logger.info("Directory structure verified")


def check_dependencies():
    """Check if required dependencies are available."""
    required_modules = [
        ('PyQt6', 'PyQt6.QtWidgets'),
        ('yaml', 'yaml'),
        ('toml', 'toml'),
    ]
    
    missing_modules = []
    
    for module_name, import_name in required_modules:
        try:
            __import__(import_name)
            logger.info(f"✓ {module_name} available")
        except ImportError:
            missing_modules.append(module_name)
            logger.error(f"✗ {module_name} not available")
    
    if missing_modules:
        logger.error(f"Missing required modules: {', '.join(missing_modules)}")
        logger.error("Please install with: pip install -r requirements_new.txt")
        return False
    
    return True


def main():
    """Main application entry point."""
    logger.info("Starting YouTube to Video Generator - Enterprise Edition")
    logger.info("Created by Mustafa Hüseyin Temel, M.D.")
    
    # Ensure directory structure
    ensure_directories()
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting.")
        sys.exit(1)
    
    try:
        # Import and run the PyQt6 application
        from ui.main_window import Application
        
        app = Application(sys.argv)
        
        logger.info("Application initialized successfully")
        logger.info("Launching main window...")
        
        exit_code = app.run()
        
        logger.info(f"Application exited with code: {exit_code}")
        sys.exit(exit_code)
        
    except ImportError as e:
        logger.error(f"Failed to import application modules: {e}")
        logger.error("This might be due to missing PyQt6 installation")
        logger.error("Try: pip install PyQt6")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()