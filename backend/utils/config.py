"""
Configuration management for AI LAM

Centralized configuration system inspired by Suna's patterns.
"""

import os
from typing import Optional
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnvMode(Enum):
    """Environment modes."""
    LOCAL = "local"
    STAGING = "staging"  
    PRODUCTION = "production"

class Config:
    """Application configuration."""
    
    def __init__(self):
        # Environment
        self.ENV_MODE = EnvMode(os.getenv('ENV_MODE', 'local'))
        
        # Database
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        
        # LLM API Keys
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        
        # Default models
        self.DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-2.0-flash-exp')
        self.MODEL_TO_USE = os.getenv('MODEL_TO_USE', self.DEFAULT_MODEL)
        
        # Security
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
        self.JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
        
        # Server settings
        self.PORT = int(os.getenv('PORT', '8000'))
        self.HOST = os.getenv('HOST', '0.0.0.0')
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # CORS settings
        self.ALLOWED_ORIGINS = self._parse_list(os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000'))
        
        # Monitoring
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Features
        self.ENABLE_AUTOMATION = os.getenv('ENABLE_AUTOMATION', 'true').lower() == 'true'
        self.ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true'
        
    def _parse_list(self, value: str) -> list:
        """Parse comma-separated string into list."""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENV_MODE == EnvMode.PRODUCTION
    
    @property
    def is_local(self) -> bool:
        """Check if running in local mode."""
        return self.ENV_MODE == EnvMode.LOCAL
    
    def validate(self) -> list:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Required settings
        if not self.SUPABASE_URL:
            errors.append("SUPABASE_URL is required")
        if not self.SUPABASE_KEY:
            errors.append("SUPABASE_KEY is required")
        
        # At least one LLM API key should be configured
        llm_keys = [self.OPENAI_API_KEY, self.ANTHROPIC_API_KEY, self.GOOGLE_API_KEY]
        if not any(llm_keys):
            errors.append("At least one LLM API key must be configured")
        
        return errors

# Global configuration instance
_config = None

def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config

def validate_config() -> None:
    """Validate configuration and raise exception if invalid."""
    config = get_config()
    errors = config.validate()
    
    if errors:
        error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        raise ValueError(error_msg) 