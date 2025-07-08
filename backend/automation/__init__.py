"""
AI LAM Automation Package
Intelligent form detection and filling for any website
"""

from .intelligent_automation import IntelligentFormAutomation
from .form_detection import FormFieldDetector, FieldType
from .data_parser import DataParser
from .automation_manager import AutomationManager
from .browser_automation import EnhancedBrowserAutomation

__all__ = [
    'IntelligentFormAutomation',
    'FormFieldDetector',
    'FieldType', 
    'DataParser',
    'AutomationManager',
    'EnhancedBrowserAutomation'
]
