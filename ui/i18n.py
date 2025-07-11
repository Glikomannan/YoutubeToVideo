"""
Internationalization (i18n) support for the application.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import os
from pathlib import Path
from typing import Dict, Any


class TranslationManager:
    """
    Manage application translations and internationalization.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    def __init__(self, locale_dir: str = "assets/locales"):
        self.locale_dir = Path(locale_dir)
        self.locale_dir.mkdir(parents=True, exist_ok=True)
        self.current_language = "en"
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all available translations."""
        # English (default)
        self.translations["en"] = {
            "app_title": "YouTube to Video Generator",
            "generate_video": "Generate Video",
            "settings": "Settings",
            "history": "History",
            "niche": "Niche",
            "language": "Language",
            "duration": "Duration",
            "text_model": "Text Model",
            "image_model": "Image Model",
            "voice": "Voice",
            "enable_subtitles": "Enable Subtitles",
            "add_background_music": "Add Background Music",
            "use_transitions": "Use Transitions",
            "video_parameters": "Video Parameters",
            "ai_model_configuration": "AI Model Configuration",
            "video_options": "Video Options",
            "api_configuration": "API Configuration",
            "interface_settings": "Interface Settings",
            "privacy_compliance": "Privacy & Compliance",
            "enable_data_encryption": "Enable data encryption",
            "enable_audit_logging": "Enable audit logging",
            "require_user_consent": "Require user consent",
            "theme": "Theme",
            "interface_language": "Interface Language",
            "video_generation_started": "Video generation started...",
            "progress": "Progress",
            "video_generation_completed": "Video generation completed!",
            "status_messages": "Status messages will appear here...",
            "created_by": "Created by Mustafa Hüseyin Temel, M.D.",
            "about": "About",
            "file": "File",
            "tools": "Tools",
            "help": "Help",
            "new_project": "New Project",
            "open_project": "Open Project",
            "save_project": "Save Project",
            "exit": "Exit",
            "ready": "Ready"
        }
        
        # Spanish
        self.translations["es"] = {
            "app_title": "Generador de YouTube a Video",
            "generate_video": "Generar Video",
            "settings": "Configuración",
            "history": "Historial",
            "niche": "Nicho",
            "language": "Idioma",
            "duration": "Duración",
            "text_model": "Modelo de Texto",
            "image_model": "Modelo de Imagen",
            "voice": "Voz",
            "enable_subtitles": "Habilitar Subtítulos",
            "add_background_music": "Agregar Música de Fondo",
            "use_transitions": "Usar Transiciones",
            "video_parameters": "Parámetros de Video",
            "ai_model_configuration": "Configuración de Modelo IA",
            "video_options": "Opciones de Video",
            "api_configuration": "Configuración de API",
            "interface_settings": "Configuración de Interfaz",
            "privacy_compliance": "Privacidad y Cumplimiento",
            "enable_data_encryption": "Habilitar encriptación de datos",
            "enable_audit_logging": "Habilitar registro de auditoría",
            "require_user_consent": "Requerir consentimiento del usuario",
            "theme": "Tema",
            "interface_language": "Idioma de Interfaz",
            "video_generation_started": "Generación de video iniciada...",
            "progress": "Progreso",
            "video_generation_completed": "¡Generación de video completada!",
            "status_messages": "Los mensajes de estado aparecerán aquí...",
            "created_by": "Creado por Mustafa Hüseyin Temel, M.D.",
            "about": "Acerca de",
            "file": "Archivo",
            "tools": "Herramientas",
            "help": "Ayuda",
            "new_project": "Nuevo Proyecto",
            "open_project": "Abrir Proyecto",
            "save_project": "Guardar Proyecto",
            "exit": "Salir",
            "ready": "Listo"
        }
        
        # French
        self.translations["fr"] = {
            "app_title": "Générateur YouTube vers Vidéo",
            "generate_video": "Générer Vidéo",
            "settings": "Paramètres",
            "history": "Historique",
            "niche": "Niche",
            "language": "Langue",
            "duration": "Durée",
            "text_model": "Modèle de Texte",
            "image_model": "Modèle d'Image",
            "voice": "Voix",
            "enable_subtitles": "Activer les Sous-titres",
            "add_background_music": "Ajouter Musique de Fond",
            "use_transitions": "Utiliser Transitions",
            "video_parameters": "Paramètres Vidéo",
            "ai_model_configuration": "Configuration Modèle IA",
            "video_options": "Options Vidéo",
            "api_configuration": "Configuration API",
            "interface_settings": "Paramètres Interface",
            "privacy_compliance": "Confidentialité et Conformité",
            "enable_data_encryption": "Activer chiffrement des données",
            "enable_audit_logging": "Activer journalisation d'audit",
            "require_user_consent": "Exiger consentement utilisateur",
            "theme": "Thème",
            "interface_language": "Langue de l'Interface",
            "video_generation_started": "Génération vidéo démarrée...",
            "progress": "Progrès",
            "video_generation_completed": "Génération vidéo terminée!",
            "status_messages": "Les messages d'état apparaîtront ici...",
            "created_by": "Créé par Mustafa Hüseyin Temel, M.D.",
            "about": "À propos",
            "file": "Fichier",
            "tools": "Outils",
            "help": "Aide",
            "new_project": "Nouveau Projet",
            "open_project": "Ouvrir Projet",
            "save_project": "Sauvegarder Projet",
            "exit": "Quitter",
            "ready": "Prêt"
        }
        
        # German
        self.translations["de"] = {
            "app_title": "YouTube zu Video Generator",
            "generate_video": "Video Generieren",
            "settings": "Einstellungen",
            "history": "Verlauf",
            "niche": "Nische",
            "language": "Sprache",
            "duration": "Dauer",
            "text_model": "Text-Modell",
            "image_model": "Bild-Modell",
            "voice": "Stimme",
            "enable_subtitles": "Untertitel Aktivieren",
            "add_background_music": "Hintergrundmusik Hinzufügen",
            "use_transitions": "Übergänge Verwenden",
            "video_parameters": "Video-Parameter",
            "ai_model_configuration": "KI-Modell Konfiguration",
            "video_options": "Video-Optionen",
            "api_configuration": "API-Konfiguration",
            "interface_settings": "Interface-Einstellungen",
            "privacy_compliance": "Datenschutz & Compliance",
            "enable_data_encryption": "Datenverschlüsselung aktivieren",
            "enable_audit_logging": "Audit-Protokollierung aktivieren",
            "require_user_consent": "Benutzereinwilligung erforderlich",
            "theme": "Thema",
            "interface_language": "Interface-Sprache",
            "video_generation_started": "Video-Generierung gestartet...",
            "progress": "Fortschritt",
            "video_generation_completed": "Video-Generierung abgeschlossen!",
            "status_messages": "Statusmeldungen erscheinen hier...",
            "created_by": "Erstellt von Mustafa Hüseyin Temel, M.D.",
            "about": "Über",
            "file": "Datei",
            "tools": "Werkzeuge",
            "help": "Hilfe",
            "new_project": "Neues Projekt",
            "open_project": "Projekt Öffnen",
            "save_project": "Projekt Speichern",
            "exit": "Beenden",
            "ready": "Bereit"
        }
    
    def set_language(self, language_code: str):
        """Set the current language."""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for a key."""
        if self.current_language in self.translations:
            translation = self.translations[self.current_language].get(key)
            if translation:
                return translation
        
        # Fallback to English
        if "en" in self.translations:
            translation = self.translations["en"].get(key)
            if translation:
                return translation
        
        # Final fallback
        return default or key
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their display names."""
        return {
            "en": "English",
            "es": "Español", 
            "fr": "Français",
            "de": "Deutsch"
        }
    
    def is_rtl_language(self, language_code: str = None) -> bool:
        """Check if language uses right-to-left text direction."""
        lang = language_code or self.current_language
        rtl_languages = ["ar", "he", "fa", "ur"]
        return lang in rtl_languages


# Global translation manager instance
_translation_manager = None


def get_translation_manager() -> TranslationManager:
    """Get global translation manager instance."""
    global _translation_manager
    if _translation_manager is None:
        _translation_manager = TranslationManager()
    return _translation_manager


def tr(key: str, default: str = None) -> str:
    """Get translated text (convenience function)."""
    return get_translation_manager().get_text(key, default)