#!/usr/bin/env python3
"""
Demo script to showcase the YouTube to Video Generator capabilities.

This script demonstrates the enterprise-grade architecture and functionality
without requiring a GUI environment.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import asyncio
import sys
import os
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_manager import get_config_manager, ConfigFormat
from services.implementations import ServiceFactory
from core.domain import VideoRequest, VideoStatus
from ui.i18n import get_translation_manager, tr


async def demo_text_generation():
    """Demonstrate text generation service."""
    print("\n" + "="*60)
    print("🎯 TEXT GENERATION SERVICE DEMO")
    print("="*60)
    
    text_service = ServiceFactory.create_text_service()
    
    # Test different niches
    niches = ["Historical Facts", "Technology News", "Cooking Tips"]
    
    for niche in niches:
        print(f"\n📝 Generating script for: {niche}")
        result = await text_service.generate_script(niche, "English", 60.0)
        
        print(f"   Title: {result['title']}")
        print(f"   Description: {result['description'][:100]}...")
        print(f"   Script Length: {len(result['script'])} characters")
        print(f"   Valid: {text_service.validate_script(result['script'])}")


async def demo_audio_generation():
    """Demonstrate audio generation service."""
    print("\n" + "="*60)
    print("🎵 AUDIO GENERATION SERVICE DEMO")
    print("="*60)
    
    audio_service = ServiceFactory.create_audio_service()
    
    # Test voice generation
    text = "Welcome to the YouTube to Video Generator, created by Mustafa Hüseyin Temel, M.D."
    
    print(f"\n🗣️ Generating audio for text: {text[:50]}...")
    audio_path = await audio_service.generate_audio(text, "default", "English")
    print(f"   Audio saved to: {audio_path}")
    print(f"   File exists: {os.path.exists(audio_path)}")
    
    # Show available voices
    print(f"\n🎤 Available voices for English:")
    voices = audio_service.get_available_voices("English")
    for voice in voices:
        print(f"   - {voice}")
    
    # Cleanup
    if os.path.exists(audio_path):
        os.unlink(audio_path)


async def demo_image_generation():
    """Demonstrate image generation service."""
    print("\n" + "="*60)
    print("🎨 IMAGE GENERATION SERVICE DEMO")
    print("="*60)
    
    image_service = ServiceFactory.create_image_service()
    
    # Test image generation
    prompts = [
        "A beautiful sunset over mountains",
        "Futuristic cityscape with flying cars",
        "Ancient library with magical books"
    ]
    
    for prompt in prompts:
        print(f"\n🖼️ Generating image for: {prompt}")
        image_path = await image_service.generate_image(prompt)
        print(f"   Image saved to: {image_path}")
        print(f"   File exists: {os.path.exists(image_path)}")
        
        # Cleanup
        if os.path.exists(image_path):
            os.unlink(image_path)
    
    # Show available styles
    print(f"\n🎭 Available image styles:")
    styles = image_service.get_available_styles()
    for style in styles:
        print(f"   - {style}")


async def demo_video_generation():
    """Demonstrate complete video generation."""
    print("\n" + "="*60)
    print("🎬 VIDEO GENERATION SERVICE DEMO")
    print("="*60)
    
    video_service = ServiceFactory.create_video_service()
    
    # Create video request
    request = VideoRequest(
        id="demo-video-001",
        niche="Historical Facts",
        language="English",
        duration=60.0,
        resolution=(1080, 1920),
        status=VideoStatus.PENDING
    )
    
    print(f"\n📋 Video Request Details:")
    print(f"   ID: {request.id}")
    print(f"   Niche: {request.niche}")
    print(f"   Language: {request.language}")
    print(f"   Duration: {request.duration}s")
    print(f"   Resolution: {request.resolution}")
    print(f"   Valid: {video_service.validate_request(request)}")
    
    print(f"\n🎬 Generating complete video...")
    result = await video_service.generate_video(request)
    
    print(f"\n✅ Video Generation Complete!")
    print(f"   Result ID: {result.id}")
    print(f"   Title: {result.title}")
    print(f"   Description: {result.description[:100]}...")
    print(f"   Script Length: {len(result.script)} characters")
    print(f"   File Path: {result.file_path}")
    print(f"   File Size: {result.file_size} bytes")
    print(f"   Duration: {result.duration}s")
    
    # Show metadata
    print(f"\n📊 Generation Metadata:")
    for key, value in result.metadata.items():
        if isinstance(value, list):
            print(f"   {key}: {len(value)} items")
        else:
            print(f"   {key}: {value}")
    
    # Cleanup
    if os.path.exists(result.file_path):
        os.unlink(result.file_path)


def demo_configuration_system():
    """Demonstrate configuration management."""
    print("\n" + "="*60)
    print("⚙️ CONFIGURATION SYSTEM DEMO")
    print("="*60)
    
    config_manager = get_config_manager()
    
    # Show current configuration
    config = config_manager.get_config()
    print(f"\n📋 Current Configuration:")
    print(f"   App Name: {config.app_name}")
    print(f"   Version: {config.app_version}")
    print(f"   Author: {config.author}")
    print(f"   UI Theme: {config.ui.theme}")
    print(f"   UI Language: {config.ui.language}")
    print(f"   Window Size: {config.ui.window_width}x{config.ui.window_height}")
    print(f"   Auto Save: {config.auto_save_enabled}")
    
    # Test configuration formats
    formats = [ConfigFormat.YAML, ConfigFormat.JSON, ConfigFormat.TOML]
    
    for format_type in formats:
        print(f"\n💾 Testing {format_type.value.upper()} configuration...")
        try:
            config_manager.save_config(format_type)
            config_file = config_manager.config_dir / f"app.{format_type.value}"
            print(f"   ✅ Saved to: {config_file}")
            print(f"   📁 File exists: {config_file.exists()}")
            
            # Load and verify
            loaded_config = config_manager.load_config(format_type)
            print(f"   ✅ Loaded successfully")
            print(f"   🏷️ Author preserved: {loaded_config.author == config.author}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def demo_internationalization():
    """Demonstrate internationalization support."""
    print("\n" + "="*60)
    print("🌍 INTERNATIONALIZATION DEMO")
    print("="*60)
    
    translation_manager = get_translation_manager()
    
    # Show available languages
    languages = translation_manager.get_available_languages()
    print(f"\n🗣️ Available Languages:")
    for code, name in languages.items():
        print(f"   {code}: {name}")
    
    # Test translations
    test_keys = ["app_title", "generate_video", "settings", "created_by"]
    
    for lang_code, lang_name in languages.items():
        print(f"\n🌐 Testing {lang_name} ({lang_code}):")
        translation_manager.set_language(lang_code)
        
        for key in test_keys:
            translated = tr(key)
            print(f"   {key}: {translated}")


def demo_compliance_features():
    """Demonstrate compliance and security features."""
    print("\n" + "="*60)
    print("🔒 COMPLIANCE & SECURITY DEMO")
    print("="*60)
    
    compliance_service = ServiceFactory.create_compliance_service()
    
    # Test audit logging
    print(f"\n📝 Testing Audit Logging:")
    user_id = "demo-user-123"
    action = "generate_video"
    data = {"niche": "Historical Facts", "duration": 60.0}
    
    compliance_service.log_user_action(user_id, action, data)
    print(f"   ✅ Audit log entry created")
    print(f"   📁 Log file: {compliance_service.audit_log_path}")
    print(f"   📄 File exists: {os.path.exists(compliance_service.audit_log_path)}")
    
    # Test encryption
    print(f"\n🔐 Testing Data Encryption:")
    sensitive_data = "This is sensitive user information"
    encrypted = compliance_service.encrypt_data(sensitive_data)
    decrypted = compliance_service.decrypt_data(encrypted)
    
    print(f"   Original: {sensitive_data}")
    print(f"   Encrypted: {encrypted[:50]}...")
    print(f"   Decrypted: {decrypted}")
    print(f"   ✅ Encryption working: {sensitive_data == decrypted}")
    
    # Test anonymization
    print(f"\n🕶️ Testing Data Anonymization:")
    # Enable anonymization
    compliance_service.config.compliance.anonymization_enabled = True
    
    personal_data = {
        "email": "user@example.com",
        "name": "John Doe",
        "niche": "Historical Facts"
    }
    
    anonymized = compliance_service.anonymize_data(personal_data)
    print(f"   Original email: {personal_data['email']}")
    print(f"   Anonymized email: {anonymized['email']}")
    print(f"   Non-personal data preserved: {anonymized['niche'] == personal_data['niche']}")


def display_banner():
    """Display application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║    🎬 YouTube to Video Generator - Enterprise Edition                         ║
    ║                                                                               ║
    ║    Enterprise-grade video generation with AI-powered content creation        ║
    ║    Built with PyQt6, Clean Architecture, and comprehensive compliance        ║
    ║                                                                               ║
    ║    Created by: Mustafa Hüseyin Temel, M.D.                                   ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def main():
    """Main demo function."""
    display_banner()
    
    print("\n🚀 Starting comprehensive system demonstration...")
    print("This demo showcases all major features of the enterprise architecture")
    
    try:
        # Core system demos
        demo_configuration_system()
        demo_internationalization()
        demo_compliance_features()
        
        # AI service demos
        await demo_text_generation()
        await demo_audio_generation()
        await demo_image_generation()
        await demo_video_generation()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\n🎯 Key Features Demonstrated:")
        print("   ✅ Enterprise-grade architecture with Clean Architecture patterns")
        print("   ✅ Multi-format configuration system (YAML/JSON/TOML)")
        print("   ✅ Internationalization support (English, Spanish, French, German)")
        print("   ✅ GDPR/HIPAA compliance features (audit logging, encryption, anonymization)")
        print("   ✅ AI-powered content generation (text, audio, image, video)")
        print("   ✅ Type-safe service layer with dependency injection")
        print("   ✅ Comprehensive error handling and logging")
        
        print(f"\n🏆 Created by: Mustafa Hüseyin Temel, M.D.")
        print("   A professional, scalable, and maintainable enterprise solution")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)