"""
SecureVault - A secure password manager application
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "A secure password manager with encryption and GUI interface"

# Make key components easily accessible
from .core.password_manager import PasswordManager, PasswordEntry
from .core.encryption import EncryptionManager

__all__ = ['PasswordManager', 'PasswordEntry', 'EncryptionManager'] 