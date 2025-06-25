"""
Humanlike-Automation Library
Human-like browser automation with stealth capabilities and anti-detection features
"""

__version__ = "1.0.0"
__author__ = "Bot Infrastructure Team"
__email__ = "contact@botinfrastructure.com"
__description__ = "Human-like browser automation with stealth capabilities and anti-detection features"

from .utility import Utility
from .browserhandler import BrowserHandler
from .webpagehandler import WebPageHandler
from .webpageanalyzer import WebpageAnalyzer
from .browsersessionmanager import BrowserSessionManager
from .config_manager import ConfigManager, config_manager
from .portable_browser import PortableBrowserManager

__all__ = [
    "Utility",
    "BrowserHandler", 
    "WebPageHandler",
    "WebpageAnalyzer",
    "BrowserSessionManager",
    "ConfigManager",
    "config_manager",
    "PortableBrowserManager",
]