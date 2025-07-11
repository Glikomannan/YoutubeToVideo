"""
Main PyQt6 application window with ChatGPT-inspired dark theme.

Attribution: Created by Mustafa Hüseyin Temel, M.D.
"""

import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QTextEdit, QComboBox, QSpinBox,
    QSlider, QCheckBox, QProgressBar, QStatusBar, QMenuBar, QScrollArea,
    QGroupBox, QGridLayout, QFormLayout, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QTranslator, QLocale
from PyQt6.QtGui import (
    QAction, QFont, QIcon, QPalette, QColor, QPixmap, 
    QKeySequence, QShortcut
)

from config.config_manager import get_config_manager, AppConfig


class DarkTheme:
    """
    ChatGPT-inspired dark theme colors and styles.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    # Color palette inspired by ChatGPT dark theme
    BACKGROUND = "#202123"
    SURFACE = "#2d2d30"
    SURFACE_VARIANT = "#343541"
    PRIMARY = "#10a37f"
    PRIMARY_VARIANT = "#0891b2"
    SECONDARY = "#6366f1"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#c5c5d1"
    TEXT_DISABLED = "#6b7280"
    BORDER = "#4b5563"
    ERROR = "#ef4444"
    WARNING = "#f59e0b"
    SUCCESS = "#10b981"
    
    @classmethod
    def get_stylesheet(cls) -> str:
        """Get complete dark theme stylesheet."""
        return f"""
        QMainWindow {{
            background-color: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        QWidget {{
            background-color: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
            border: none;
        }}
        
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER};
            background-color: {cls.SURFACE};
            border-radius: 8px;
        }}
        
        QTabBar::tab {{
            background-color: {cls.SURFACE_VARIANT};
            color: {cls.TEXT_SECONDARY};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            min-width: 80px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:hover {{
            background-color: {cls.BORDER};
        }}
        
        QPushButton {{
            background-color: {cls.PRIMARY};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background-color: {cls.PRIMARY_VARIANT};
        }}
        
        QPushButton:pressed {{
            background-color: #0f766e;
        }}
        
        QPushButton:disabled {{
            background-color: {cls.BORDER};
            color: {cls.TEXT_DISABLED};
        }}
        
        QTextEdit, QPlainTextEdit {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        
        QComboBox {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 20px;
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.TEXT_SECONDARY};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 4px;
        }}
        
        QSpinBox, QDoubleSpinBox {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 6px;
            min-height: 20px;
        }}
        
        QSlider::groove:horizontal {{
            background-color: {cls.BORDER};
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {cls.PRIMARY};
            width: 18px;
            height: 18px;
            border-radius: 9px;
            margin-top: -6px;
            margin-bottom: -6px;
        }}
        
        QSlider::sub-page:horizontal {{
            background-color: {cls.PRIMARY};
            border-radius: 3px;
        }}
        
        QCheckBox {{
            color: {cls.TEXT_PRIMARY};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {cls.BORDER};
            border-radius: 3px;
            background-color: {cls.SURFACE};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {cls.PRIMARY};
            border-color: {cls.PRIMARY};
        }}
        
        QProgressBar {{
            background-color: {cls.SURFACE};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            text-align: center;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QProgressBar::chunk {{
            background-color: {cls.PRIMARY};
            border-radius: 5px;
        }}
        
        QStatusBar {{
            background-color: {cls.SURFACE_VARIANT};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER};
        }}
        
        QMenuBar {{
            background-color: {cls.SURFACE_VARIANT};
            color: {cls.TEXT_PRIMARY};
            border-bottom: 1px solid {cls.BORDER};
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
            background-color: transparent;
        }}
        
        QMenuBar::item:selected {{
            background-color: {cls.BORDER};
        }}
        
        QMenu {{
            background-color: {cls.SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
        }}
        
        QMenu::item {{
            padding: 6px 12px;
        }}
        
        QMenu::item:selected {{
            background-color: {cls.BORDER};
        }}
        
        QGroupBox {{
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            margin-top: 1ex;
            font-weight: 500;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        QScrollArea {{
            background-color: {cls.SURFACE};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
        }}
        
        QScrollBar:vertical {{
            background-color: {cls.SURFACE};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.TEXT_DISABLED};
        }}
        """


class VideoGenerationWidget(QWidget):
    """Main video generation interface widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = get_config_manager().get_config()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("YouTube to Video Generator")
        header.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {DarkTheme.TEXT_PRIMARY};
            padding: 16px 0;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Main content in tabs
        tab_widget = QTabWidget()
        
        # Generation tab
        generation_tab = self.create_generation_tab()
        tab_widget.addTab(generation_tab, "Generate Video")
        
        # Settings tab
        settings_tab = self.create_settings_tab()
        tab_widget.addTab(settings_tab, "Settings")
        
        # History tab
        history_tab = self.create_history_tab()
        tab_widget.addTab(history_tab, "History")
        
        layout.addWidget(tab_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Status area
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("Status messages will appear here...")
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
    
    def create_generation_tab(self) -> QWidget:
        """Create the video generation tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Input section
        input_group = QGroupBox("Video Parameters")
        input_layout = QFormLayout(input_group)
        
        self.niche_combo = QComboBox()
        self.niche_combo.addItems([
            "Historical Facts", "Cooking Tips", "Technology News",
            "Science Discoveries", "Travel Destinations", "Art History",
            "Music Theory", "Sports Facts", "Health Tips", "DIY Projects"
        ])
        input_layout.addRow("Niche:", self.niche_combo)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Spanish", "French", "German", "Italian"])
        input_layout.addRow("Language:", self.language_combo)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(30, 300)
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix(" seconds")
        input_layout.addRow("Duration:", self.duration_spin)
        
        layout.addWidget(input_group)
        
        # AI Model selection
        ai_group = QGroupBox("AI Model Configuration")
        ai_layout = QFormLayout(ai_group)
        
        self.text_model_combo = QComboBox()
        self.text_model_combo.addItems(["GPT-4", "GPT-3.5", "Gemini Pro", "Claude"])
        ai_layout.addRow("Text Model:", self.text_model_combo)
        
        self.image_model_combo = QComboBox()
        self.image_model_combo.addItems(["DALL-E 3", "Midjourney", "Stable Diffusion", "Flux"])
        ai_layout.addRow("Image Model:", self.image_model_combo)
        
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Neural Voice 1", "Neural Voice 2", "Edge TTS", "ElevenLabs"])
        ai_layout.addRow("Voice:", self.voice_combo)
        
        layout.addWidget(ai_group)
        
        # Video options
        video_group = QGroupBox("Video Options")
        video_layout = QFormLayout(video_group)
        
        self.subtitles_check = QCheckBox("Enable Subtitles")
        self.subtitles_check.setChecked(True)
        video_layout.addRow(self.subtitles_check)
        
        self.music_check = QCheckBox("Add Background Music")
        self.music_check.setChecked(True)
        video_layout.addRow(self.music_check)
        
        self.transitions_check = QCheckBox("Use Transitions")
        self.transitions_check.setChecked(True)
        video_layout.addRow(self.transitions_check)
        
        layout.addWidget(video_group)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Video")
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {DarkTheme.PRIMARY};
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {DarkTheme.PRIMARY_VARIANT};
            }}
        """)
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """Create the settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # API Keys section
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout(api_group)
        
        # Note: In a real implementation, these would be masked inputs
        api_layout.addRow("OpenAI API Key:", QTextEdit())
        api_layout.addRow("Gemini API Key:", QTextEdit())
        api_layout.addRow("AssemblyAI API Key:", QTextEdit())
        
        layout.addWidget(api_group)
        
        # UI Settings
        ui_group = QGroupBox("Interface Settings")
        ui_layout = QFormLayout(ui_group)
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light", "Auto"])
        ui_layout.addRow("Theme:", theme_combo)
        
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Spanish", "French", "German"])
        ui_layout.addRow("Interface Language:", lang_combo)
        
        layout.addWidget(ui_group)
        
        # Compliance settings
        compliance_group = QGroupBox("Privacy & Compliance")
        compliance_layout = QVBoxLayout(compliance_group)
        
        compliance_layout.addWidget(QCheckBox("Enable data encryption"))
        compliance_layout.addWidget(QCheckBox("Enable audit logging"))
        compliance_layout.addWidget(QCheckBox("Require user consent"))
        
        layout.addWidget(compliance_group)
        
        layout.addStretch()
        return widget
    
    def create_history_tab(self) -> QWidget:
        """Create the history tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        history_label = QLabel("Generated videos will appear here...")
        history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(history_label)
        
        return widget
    
    def generate_video(self):
        """Handle video generation request."""
        self.status_text.append("Video generation started...")
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.generate_btn.setEnabled(False)
        
        # In a real implementation, this would start the video generation process
        # For now, just simulate progress
        self.simulate_progress()
    
    def simulate_progress(self):
        """Simulate video generation progress."""
        self.timer = QTimer()
        self.progress_value = 0
        
        def update_progress():
            self.progress_value += 10
            self.progress_bar.setValue(self.progress_value)
            self.status_text.append(f"Progress: {self.progress_value}%")
            
            if self.progress_value >= 100:
                self.timer.stop()
                self.status_text.append("Video generation completed!")
                self.progress_bar.hide()
                self.generate_btn.setEnabled(True)
        
        self.timer.timeout.connect(update_progress)
        self.timer.start(500)


class MainWindow(QMainWindow):
    """
    Main application window with enterprise-grade architecture.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    def __init__(self):
        super().__init__()
        self.config = get_config_manager().get_config()
        self.translator = QTranslator()
        self.init_ui()
        self.setup_shortcuts()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{self.config.app_name} - {self.config.author}")
        self.setGeometry(100, 100, self.config.ui.window_width, self.config.ui.window_height)
        
        # Set up central widget
        central_widget = VideoGenerationWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage(f"Ready - {self.config.author}")
        self.setStatusBar(self.status_bar)
        
        # Apply theme
        self.setStyleSheet(DarkTheme.get_stylesheet())
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Project', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        settings_action = QAction('Settings', self)
        settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        tools_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Global shortcuts for accessibility
        QShortcut(QKeySequence("Ctrl+G"), self, self.centralWidget().generate_video)
        QShortcut(QKeySequence("F1"), self, self.show_about)
    
    def show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.about(self, "About", 
            f"{self.config.app_name} v{self.config.app_version}\n\n"
            f"Created by {self.config.author}\n\n"
            "An enterprise-grade video generation application\n"
            "built with PyQt6 and Clean Architecture principles.")
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Save configuration before closing
        get_config_manager().save_config()
        event.accept()


class Application(QApplication):
    """
    Main application class with enterprise features.
    
    Attribution: Created by Mustafa Hüseyin Temel, M.D.
    """
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application metadata
        config = get_config_manager().get_config()
        self.setApplicationName(config.app_name)
        self.setApplicationVersion(config.app_version)
        self.setOrganizationName(config.author)
        
        # Enable high DPI scaling
        if config.ui.high_dpi_scaling:
            self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
            self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        
        # Set up fonts
        font = QFont(config.ui.font_family, config.ui.font_size)
        self.setFont(font)
    
    def run(self):
        """Run the application."""
        # Load configuration
        config_manager = get_config_manager()
        config_manager.load_config()
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        return self.exec()