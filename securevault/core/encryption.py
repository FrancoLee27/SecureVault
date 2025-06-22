"""
encryption.py - Handles all encryption and security functions
This module uses cryptography library for secure password storage

After researching, I learned about:
- PBKDF2: Password-Based Key Derivation Function 2 (for hashing master password)
- Fernet: Symmetric encryption (for encrypting stored passwords)
- Salt: Random data to prevent rainbow table attacks
"""

import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    """Manages encryption operations for the password manager"""
    
    def __init__(self):
        self.fernet = None
        self.master_password_file = "master_password.json"
        self.salt = None
        
    def generate_salt(self):
        """Generate a random salt for password hashing"""
        # Salt should be random and unique
        # I learned that 16 bytes is recommended for security
        return os.urandom(16)
    
    def derive_key_from_password(self, password, salt):
        """
        Derive an encryption key from the master password using PBKDF2
        
        Args:
            password (str): The master password
            salt (bytes): Random salt for key derivation
            
        Returns:
            bytes: The derived encryption key
        """
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        
        # Create PBKDF2 instance
        # Using 100,000 iterations as recommended for security
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits
            salt=salt,
            iterations=100000,  # High iteration count for security
        )
        
        # Derive the key
        key = kdf.derive(password_bytes)
        
        # Fernet needs the key to be base64 encoded
        return base64.urlsafe_b64encode(key)
    
    def set_master_password(self, password):
        """
        Set or update the master password
        
        Args:
            password (str): The new master password
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate new salt
            self.salt = self.generate_salt()
            
            # Derive key from password
            key = self.derive_key_from_password(password, self.salt)
            
            # Create Fernet instance with the key
            self.fernet = Fernet(key)
            
            # Store salt and a verification token
            # The verification token helps us check if the password is correct
            verification_token = self.fernet.encrypt(b"PASSWORD_CORRECT")
            
            # Save to file
            data = {
                "salt": base64.b64encode(self.salt).decode('utf-8'),
                "verification": verification_token.decode('utf-8')
            }
            
            with open(self.master_password_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
            
        except Exception as e:
            print(f"Error setting master password: {e}")
            return False
    
    def verify_master_password(self, password):
        """
        Verify if the provided password is correct
        
        Args:
            password (str): The password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        try:
            # Check if master password file exists
            if not os.path.exists(self.master_password_file):
                return False
            
            # Load stored data
            with open(self.master_password_file, 'r') as f:
                data = json.load(f)
            
            # Decode salt
            self.salt = base64.b64decode(data['salt'])
            
            # Derive key from provided password
            key = self.derive_key_from_password(password, self.salt)
            
            # Create Fernet instance
            self.fernet = Fernet(key)
            
            # Try to decrypt verification token
            try:
                decrypted = self.fernet.decrypt(data['verification'].encode())
                return decrypted == b"PASSWORD_CORRECT"
            except:
                # If decryption fails, password is wrong
                return False
                
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    
    def is_master_password_set(self):
        """Check if a master password has been set"""
        return os.path.exists(self.master_password_file)
    
    def encrypt_password(self, password):
        """
        Encrypt a password for storage
        
        Args:
            password (str): The password to encrypt
            
        Returns:
            str: The encrypted password as base64 string
        """
        if not self.fernet:
            raise Exception("No encryption key available. Please set master password first.")
        
        # Convert to bytes and encrypt
        password_bytes = password.encode('utf-8')
        encrypted = self.fernet.encrypt(password_bytes)
        
        # Return as string for JSON storage
        return encrypted.decode('utf-8')
    
    def decrypt_password(self, encrypted_password):
        """
        Decrypt a stored password
        
        Args:
            encrypted_password (str): The encrypted password as base64 string
            
        Returns:
            str: The decrypted password
        """
        if not self.fernet:
            raise Exception("No decryption key available. Please unlock with master password.")
        
        try:
            # Convert back to bytes and decrypt
            encrypted_bytes = encrypted_password.encode('utf-8')
            decrypted = self.fernet.decrypt(encrypted_bytes)
            
            # Return as string
            return decrypted.decode('utf-8')
            
        except Exception as e:
            print(f"Error decrypting password: {e}")
            # Return error message instead of crashing
            return "[Decryption Error]"


# Test the encryption manager (for development only)
if __name__ == "__main__":
    # Simple test to verify encryption works
    em = EncryptionManager()
    
    # Test setting master password
    print("Testing master password setup...")
    if em.set_master_password("test123"):
        print("✓ Master password set successfully")
    
    # Test verification
    print("\nTesting password verification...")
    if em.verify_master_password("test123"):
        print("✓ Correct password verified")
    
    if not em.verify_master_password("wrong"):
        print("✓ Wrong password rejected")
    
    # Test encryption/decryption
    print("\nTesting encryption/decryption...")
    test_password = "MySecretPassword123!"
    encrypted = em.encrypt_password(test_password)
    print(f"Encrypted: {encrypted[:20]}...")
    
    decrypted = em.decrypt_password(encrypted)
    print(f"Decrypted: {decrypted}")
    
    if decrypted == test_password:
        print("✓ Encryption/decryption working correctly") 