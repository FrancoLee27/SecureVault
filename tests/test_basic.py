"""
test_basic.py - Basic testing for SecureVault Password Manager

This file contains simple tests I created to verify the main functionality works.
I learned about unit testing late in the project, so these tests are quite basic.
In future projects, I would write tests as I develop (Test-Driven Development).
"""

import os
import sys

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from securevault.core.encryption import EncryptionManager
from securevault.core.password_manager import PasswordManager, PasswordEntry


def test_encryption_manager():
    """Test basic encryption functionality"""
    print("Testing Encryption Manager...")
    
    em = EncryptionManager()
    
    # Test 1: Setting master password
    print("  Test 1: Setting master password...", end="")
    result = em.set_master_password("TestPassword123!")
    assert result == True, "Failed to set master password"
    print(" PASSED")
    
    # Test 2: Verifying correct password
    print("  Test 2: Verifying correct password...", end="")
    result = em.verify_master_password("TestPassword123!")
    assert result == True, "Failed to verify correct password"
    print(" PASSED")
    
    # Test 3: Rejecting wrong password  
    print("  Test 3: Rejecting wrong password...", end="")
    result = em.verify_master_password("WrongPassword")
    assert result == False, "Accepted wrong password!"
    print(" PASSED")
    
    # Test 4: Encrypt and decrypt
    print("  Test 4: Encrypt/decrypt cycle...", end="")
    em.verify_master_password("TestPassword123!")  # Unlock first
    test_password = "MySecretPassword@2024"
    encrypted = em.encrypt_password(test_password)
    decrypted = em.decrypt_password(encrypted)
    assert decrypted == test_password, f"Decryption failed: {decrypted} != {test_password}"
    print(" PASSED")
    
    # Clean up test files
    if os.path.exists("master_password.json"):
        os.remove("master_password.json")
    
    print("✓ All encryption tests passed!\n")


def test_password_generator():
    """Test password generation"""
    print("Testing Password Generator...")
    
    pm = PasswordManager()
    
    # Test 1: Default generation
    print("  Test 1: Default password generation...", end="")
    pwd = pm.generate_password()
    assert len(pwd) == 16, f"Wrong default length: {len(pwd)}"
    assert any(c.isupper() for c in pwd), "No uppercase letters"
    assert any(c.islower() for c in pwd), "No lowercase letters"
    assert any(c.isdigit() for c in pwd), "No digits"
    print(" PASSED")
    
    # Test 2: Custom length
    print("  Test 2: Custom length (20 chars)...", end="")
    pwd = pm.generate_password(length=20)
    assert len(pwd) == 20, f"Wrong custom length: {len(pwd)}"
    print(" PASSED")
    
    # Test 3: Only letters
    print("  Test 3: Letters only...", end="")
    pwd = pm.generate_password(use_digits=False, use_symbols=False)
    assert not any(c.isdigit() for c in pwd), "Contains digits"
    assert all(c.isalpha() for c in pwd), "Contains non-letters"
    print(" PASSED")
    
    print("✓ All password generator tests passed!\n")


def test_password_entry():
    """Test password entry creation"""
    print("Testing Password Entry...")
    
    # Test 1: Create entry
    print("  Test 1: Creating entry...", end="")
    entry = PasswordEntry("google.com", "test@email.com", "password123", "My notes")
    assert entry.website == "google.com"
    assert entry.username == "test@email.com"
    assert entry.password == "password123"
    assert entry.notes == "My notes"
    print(" PASSED")
    
    # Test 2: Convert to dict
    print("  Test 2: Converting to dictionary...", end="")
    entry_dict = entry.to_dict()
    assert "website" in entry_dict
    assert "username" in entry_dict
    assert "password" in entry_dict
    assert "created_date" in entry_dict
    print(" PASSED")
    
    # Test 3: Create from dict
    print("  Test 3: Creating from dictionary...", end="")
    new_entry = PasswordEntry.from_dict(entry_dict)
    assert new_entry.website == entry.website
    assert new_entry.username == entry.username
    print(" PASSED")
    
    print("✓ All password entry tests passed!\n")


def test_password_manager_integration():
    """Test the full password manager workflow"""
    print("Testing Password Manager Integration...")
    
    pm = PasswordManager()
    
    # Test 1: Set master password
    print("  Test 1: Setting up master password...", end="")
    result = pm.set_master_password("MasterPass123!")
    assert result == True
    assert pm.is_unlocked == True
    print(" PASSED")
    
    # Test 2: Add entry
    print("  Test 2: Adding password entry...", end="")
    pm.add_entry("facebook.com", "user@test.com", "fbpassword123", "Test account")
    entries = pm.get_entries()
    assert len(entries) == 1
    print(" PASSED")
    
    # Test 3: Search functionality
    print("  Test 3: Searching entries...", end="")
    results = pm.get_entries("facebook")
    assert len(results) == 1
    assert results[0][1].website == "facebook.com"
    print(" PASSED")
    
    # Test 4: Update entry
    print("  Test 4: Updating entry...", end="")
    pm.update_entry(0, password="newpassword456")
    entries = pm.get_entries()
    assert entries[0][1].password == "newpassword456"
    print(" PASSED")
    
    # Test 5: Delete entry
    print("  Test 5: Deleting entry...", end="")
    pm.delete_entry(0)
    entries = pm.get_entries()
    assert len(entries) == 0
    print(" PASSED")
    
    # Test 6: Lock and unlock
    print("  Test 6: Lock and unlock...", end="")
    pm.lock()
    assert pm.is_unlocked == False
    result = pm.unlock("MasterPass123!")
    assert result == True
    assert pm.is_unlocked == True
    print(" PASSED")
    
    # Clean up test files
    for file in ["master_password.json", "passwords.json"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("✓ All integration tests passed!\n")


def run_all_tests():
    """Run all test suites"""
    print("=" * 50)
    print("Running SecureVault Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_encryption_manager()
        test_password_generator()
        test_password_entry()
        test_password_manager_integration()
        
        print("=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        return False
    
    return True


if __name__ == "__main__":
    # Run tests
    success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 