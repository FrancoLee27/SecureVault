"""
password_manager.py - Core business logic for the password manager
Handles password storage, retrieval, generation, and management
"""

import json
import os
import random
import string
from datetime import datetime
from .encryption import EncryptionManager


class PasswordEntry:
    """Represents a single password entry"""
    
    def __init__(self, website, username, password, notes="", created_date=None):
        self.website = website
        self.username = username
        self.password = password  # This will be encrypted when stored
        self.notes = notes
        self.created_date = created_date or datetime.now().isoformat()
        self.modified_date = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert the entry to a dictionary for JSON storage"""
        return {
            "website": self.website,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "created_date": self.created_date,
            "modified_date": self.modified_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a PasswordEntry from a dictionary"""
        return cls(
            website=data.get("website", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            notes=data.get("notes", ""),
            created_date=data.get("created_date")
        )


class PasswordManager:
    """Main class for managing passwords"""
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.passwords_file = "passwords.json"
        self.entries = []
        self.is_unlocked = False
        
    def is_master_password_set(self):
        """Check if master password has been set"""
        return self.encryption_manager.is_master_password_set()
    
    def set_master_password(self, password):
        """Set the master password for the first time"""
        # Basic password strength validation
        if len(password) < 8:
            raise ValueError("Master password must be at least 8 characters long")
        
        # Set the password
        if self.encryption_manager.set_master_password(password):
            self.is_unlocked = True
            # Create empty passwords file
            self.save_entries()
            return True
        return False
    
    def unlock(self, password):
        """Unlock the password manager with master password"""
        if self.encryption_manager.verify_master_password(password):
            self.is_unlocked = True
            self.load_entries()
            return True
        return False
    
    def lock(self):
        """Lock the password manager"""
        self.is_unlocked = False
        self.entries = []
        self.encryption_manager.fernet = None
    
    def generate_password(self, length=16, use_uppercase=True, use_lowercase=True, 
                         use_digits=True, use_symbols=True):
        """
        Generate a random password with specified parameters
        
        Args:
            length (int): Length of the password
            use_uppercase (bool): Include uppercase letters
            use_lowercase (bool): Include lowercase letters
            use_digits (bool): Include numbers
            use_symbols (bool): Include special symbols
            
        Returns:
            str: Generated password
        """
        # Build character set based on options
        chars = ""
        
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            # Using a limited set of symbols to avoid issues
            chars += "!@#$%^&*"
        
        # Make sure we have at least some characters to choose from
        if not chars:
            # Default to alphanumeric if nothing selected
            chars = string.ascii_letters + string.digits
        
        # Generate password
        # Initially I used random.choice but learned about more secure methods
        # For now, keeping it simple for A-Level project
        password = ''.join(random.choice(chars) for _ in range(length))
        
        return password
    
    def add_entry(self, website, username, password, notes=""):
        """Add a new password entry"""
        if not self.is_unlocked:
            raise Exception("Password manager is locked")
        
        # Check for duplicate entries
        for entry in self.entries:
            if entry.website.lower() == website.lower() and entry.username == username:
                raise ValueError("Entry already exists for this website and username")
        
        # Encrypt the password before storing
        encrypted_password = self.encryption_manager.encrypt_password(password)
        
        # Create new entry with encrypted password
        entry = PasswordEntry(website, username, encrypted_password, notes)
        self.entries.append(entry)
        
        # Save to file
        self.save_entries()
        
        return True
    
    def update_entry(self, index, website=None, username=None, password=None, notes=None):
        """Update an existing password entry"""
        if not self.is_unlocked:
            raise Exception("Password manager is locked")
        
        if index < 0 or index >= len(self.entries):
            raise IndexError("Invalid entry index")
        
        entry = self.entries[index]
        
        # Update fields if provided
        if website is not None:
            entry.website = website
        if username is not None:
            entry.username = username
        if password is not None:
            # Encrypt new password
            entry.password = self.encryption_manager.encrypt_password(password)
        if notes is not None:
            entry.notes = notes
        
        # Update modified date
        entry.modified_date = datetime.now().isoformat()
        
        # Save changes
        self.save_entries()
        
        return True
    
    def delete_entry(self, index):
        """Delete a password entry"""
        if not self.is_unlocked:
            raise Exception("Password manager is locked")
        
        if index < 0 or index >= len(self.entries):
            raise IndexError("Invalid entry index")
        
        # Remove the entry
        del self.entries[index]
        
        # Save changes
        self.save_entries()
        
        return True
    
    def get_entries(self, search_term=""):
        """
        Get all entries or search for specific ones
        
        Args:
            search_term (str): Optional search term to filter entries
            
        Returns:
            list: List of matching entries with decrypted passwords
        """
        if not self.is_unlocked:
            raise Exception("Password manager is locked")
        
        # If no search term, return all entries
        if not search_term:
            return self.get_all_entries_decrypted()
        
        # Search in website and username fields
        search_lower = search_term.lower()
        matching_entries = []
        
        for i, entry in enumerate(self.entries):
            if (search_lower in entry.website.lower() or 
                search_lower in entry.username.lower() or
                search_lower in entry.notes.lower()):
                # Create a copy with decrypted password
                decrypted_entry = PasswordEntry(
                    website=entry.website,
                    username=entry.username,
                    password=self.encryption_manager.decrypt_password(entry.password),
                    notes=entry.notes,
                    created_date=entry.created_date
                )
                matching_entries.append((i, decrypted_entry))
        
        return matching_entries
    
    def get_all_entries_decrypted(self):
        """Get all entries with passwords decrypted"""
        decrypted_entries = []
        
        for i, entry in enumerate(self.entries):
            # Create a copy with decrypted password
            decrypted_entry = PasswordEntry(
                website=entry.website,
                username=entry.username,
                password=self.encryption_manager.decrypt_password(entry.password),
                notes=entry.notes,
                created_date=entry.created_date
            )
            decrypted_entries.append((i, decrypted_entry))
        
        return decrypted_entries
    
    def save_entries(self):
        """Save all entries to JSON file"""
        try:
            # Convert entries to dictionaries
            data = {
                "entries": [entry.to_dict() for entry in self.entries],
                "last_modified": datetime.now().isoformat()
            }
            
            # Write to file with pretty formatting
            with open(self.passwords_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error saving entries: {e}")
            raise Exception("Failed to save password entries")
    
    def load_entries(self):
        """Load entries from JSON file"""
        try:
            # Check if file exists
            if not os.path.exists(self.passwords_file):
                # Create empty file
                self.entries = []
                self.save_entries()
                return
            
            # Load from file
            with open(self.passwords_file, 'r') as f:
                data = json.load(f)
            
            # Convert dictionaries back to PasswordEntry objects
            self.entries = []
            for entry_dict in data.get("entries", []):
                entry = PasswordEntry.from_dict(entry_dict)
                self.entries.append(entry)
                
        except json.JSONDecodeError:
            print("Error: Corrupted passwords file")
            # Start with empty list rather than crashing
            self.entries = []
        except Exception as e:
            print(f"Error loading entries: {e}")
            self.entries = []


# Test code for development
if __name__ == "__main__":
    # Test password manager functionality
    pm = PasswordManager()
    
    # Test password generation
    print("Testing password generation...")
    for i in range(3):
        pwd = pm.generate_password(12, True, True, True, False)
        print(f"Generated password {i+1}: {pwd}")
    
    print("\nPassword manager basic tests completed!") 