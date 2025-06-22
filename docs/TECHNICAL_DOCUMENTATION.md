# Technical Documentation - SecureVault Password Manager

## System Architecture Overview

### High-Level Design

```
┌─────────────────┐
│    main.py      │ ← Entry Point
└────────┬────────┘
         │
┌────────▼────────┐
│     gui.py      │ ← User Interface Layer
└────────┬────────┘
         │
┌────────▼────────┐
│password_manager │ ← Business Logic Layer  
│      .py        │
└────────┬────────┘
         │
┌────────▼────────┐
│ encryption.py   │ ← Security Layer
└─────────────────┘
         │
┌────────▼────────┐
│   JSON Files    │ ← Data Storage Layer
└─────────────────┘
```

## Module Descriptions

### 1. main.py (Entry Point)
- **Purpose**: Application startup and initialization
- **Key Functions**:
  - Sets up the main Tkinter window
  - Initializes the PasswordManager instance
  - Handles application-level errors
  - Centers the window on screen

### 2. encryption.py (Security Layer)
- **Purpose**: Handles all cryptographic operations
- **Key Components**:
  
  **EncryptionManager Class**:
  - `generate_salt()`: Creates random 16-byte salt
  - `derive_key_from_password()`: Uses PBKDF2 to create encryption key
  - `set_master_password()`: Stores hashed master password
  - `verify_master_password()`: Checks if entered password is correct
  - `encrypt_password()`: Encrypts passwords for storage
  - `decrypt_password()`: Decrypts passwords for display

### 3. password_manager.py (Business Logic)
- **Purpose**: Core application logic and data management
- **Key Components**:
  
  **PasswordEntry Class**:
  - Represents a single password record
  - Contains: website, username, password, notes, timestamps
  
  **PasswordManager Class**:
  - `add_entry()`: Creates new password entries
  - `update_entry()`: Modifies existing entries
  - `delete_entry()`: Removes entries
  - `get_entries()`: Retrieves and searches entries
  - `generate_password()`: Creates random passwords
  - `save_entries()` / `load_entries()`: File I/O operations

### 4. gui.py (User Interface)
- **Purpose**: All user interface components
- **Key Components**:
  
  **LoginWindow Class**:
  - Master password entry/creation
  - First-time setup detection
  
  **PasswordManagerGUI Class**:
  - Main application window
  - Password list display (TreeView)
  - Search functionality
  - Menu system
  
  **AddEditDialog Class**:
  - Form for adding/editing entries
  - Input validation
  
  **PasswordGeneratorDialog Class**:
  - Customizable password generation
  - Character type selection

## Security Implementation

### 1. Master Password Security

**PBKDF2 Implementation**:
```python
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256-bit key
    salt=salt,
    iterations=100000,  # High iteration count
)
```

**Why PBKDF2?**
- Resistant to brute force attacks
- 100,000 iterations significantly slow down password guessing
- SHA-256 is cryptographically secure
- Salt prevents rainbow table attacks

### 2. Password Encryption

**Fernet Encryption**:
- Symmetric encryption (same key for encrypt/decrypt)
- Based on AES 128-bit encryption
- Includes built-in authentication
- Generates different ciphertext each time (using IV)

**Encryption Flow**:
1. User enters master password
2. PBKDF2 derives encryption key from password + salt
3. Fernet uses this key to encrypt/decrypt all stored passwords
4. Encrypted passwords stored as base64 strings in JSON

### 3. Data Storage Security

**What's Stored**:
```json
// master_password.json
{
    "salt": "base64_encoded_salt",
    "verification": "encrypted_test_string"
}

// passwords.json
{
    "entries": [
        {
            "website": "example.com",
            "username": "user@email.com", 
            "password": "encrypted_base64_string",
            "notes": "plain text notes",
            "created_date": "2024-01-01T10:00:00"
        }
    ]
}
```

**Security Measures**:
- Master password never stored (only verification token)
- All passwords encrypted before storage
- Salt stored separately from password data
- No sensitive data in plain text

## Design Decisions

### 1. Why JSON over Database?
- **Simplicity**: No additional dependencies
- **Portability**: Single file, easy to backup
- **Readability**: Can inspect file structure
- **Sufficient**: For single-user application

### 2. Why Tkinter over Web Interface?
- **Built-in**: No additional installation required
- **Cross-platform**: Works on Windows, Mac, Linux
- **Secure**: No network exposure
- **Learning curve**: Simpler than web development

### 3. Why Fernet over AES directly?
- **Simplicity**: High-level API
- **Safety**: Harder to misuse
- **Complete**: Includes authentication
- **Well-tested**: Part of cryptography library

## Error Handling Strategy

### 1. File Operations
```python
try:
    with open(self.passwords_file, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    # Create new file
except json.JSONDecodeError:
    # Handle corrupted file
except Exception as e:
    # Generic error handling
```

### 2. Encryption Errors
- Invalid key: Return user-friendly error
- Corrupted data: Mark as "[Decryption Error]"
- Missing master password: Prompt user to unlock

### 3. User Input Validation
- Empty fields: Show specific error message
- Duplicate entries: Prevent with validation
- Invalid password length: Enforce minimum

## Performance Considerations

### 1. Encryption Performance
- PBKDF2 iterations (100,000) intentionally slow
- Trade-off: Security vs login speed
- Password encryption/decryption is fast (< 1ms)

### 2. Search Performance
- Linear search through entries
- Acceptable for personal use (< 1000 entries)
- Case-insensitive search on multiple fields

### 3. GUI Responsiveness
- File operations could freeze UI
- Future improvement: Threading for long operations
- Current solution: Fast enough for typical use

## Testing Approach

### 1. Manual Testing Performed
- **Encryption**: Verified passwords decrypt correctly
- **Edge Cases**: Empty inputs, special characters
- **File Handling**: Missing files, corrupted data
- **GUI**: All buttons and features tested

### 2. Security Testing
- Verified passwords not visible in JSON
- Tested with various password lengths
- Confirmed clipboard clearing works
- Checked master password minimum length

### 3. User Acceptance Testing
- Family members tested usability
- Identified confusing UI elements
- Improved based on feedback

## Known Limitations

### 1. Security Limitations
- No protection against keyloggers
- Vulnerable if system is compromised
- No secure password sharing
- Single factor authentication only

### 2. Feature Limitations
- No password strength meter
- No automatic backups
- No import/export functionality
- English interface only

### 3. Technical Limitations
- Single-threaded (UI can freeze)
- No database transactions
- Limited to local storage
- No concurrent user support

## Future Enhancement Possibilities

### 1. Security Enhancements
- Two-factor authentication
- Secure password sharing
- Password strength analysis
- Encrypted backups

### 2. Feature Additions
- Browser integration
- Mobile companion app
- Cloud synchronization
- Password generation policies

### 3. Technical Improvements
- SQLite database backend
- Asynchronous operations
- Plugin architecture
- Automated testing suite

## Conclusion

This password manager successfully demonstrates understanding of:
- Cryptographic principles
- GUI application development  
- Object-oriented programming
- Error handling and validation
- Security best practices

While not production-ready for enterprise use, it provides a solid foundation for learning about secure application development and could serve as a personal password management tool. 