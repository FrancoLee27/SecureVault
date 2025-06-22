"""
Core functionality for SecureVault password manager
"""

from .encryption import EncryptionManager
from .password_manager import PasswordManager, PasswordEntry

__all__ = [
    # Encryption class
    'EncryptionManager',
    
    # Password manager classes
    'PasswordManager',
    'PasswordEntry'
] 