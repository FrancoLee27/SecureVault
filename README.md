# SecureVault Password Manager

**A-Level Computer Science Coursework Project**  
**Authors:** Franco Lee and David Sun

## Project Overview

SecureVault is a desktop password manager application built with Python. It provides secure storage for passwords using industry-standard encryption methods while maintaining a user-friendly interface suitable for everyday use.

### Key Features

- **Secure Master Password Authentication**: Uses PBKDF2 hashing with salt
- **Encrypted Password Storage**: Implements Fernet symmetric encryption
- **Intuitive GUI**: Built with Tkinter for cross-platform compatibility
- **Password Generator**: Creates strong, customizable passwords
- **Search Functionality**: Quickly find stored passwords
- **Full CRUD Operations**: Create, Read, Update, and Delete password entries

## Technical Stack

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (built-in)
- **Encryption**: cryptography library
- **Storage**: JSON file format
- **Clipboard**: pyperclip (optional)

## Installation & Setup

### Prerequisites

1. Python 3.8 or higher installed
2. pip (Python package manager)

### Installation Steps

1. Clone or download this repository
2. Navigate to the project directory in terminal/command prompt
3. Install required dependencies:

```bash
pip install cryptography
pip install pyperclip  # Optional, for clipboard functionality
```

### Running the Application

From the project root directory:

```bash
python main.py
```

Or on some systems:

```bash
python3 main.py
```

### Running Tests

To run the test suite:

```bash
python -m pytest tests/
```

Or for basic tests without pytest:

```bash
python tests/test_basic.py
```

## First Time Setup

1. When you first run the application, you'll be prompted to create a master password
2. Choose a strong password (minimum 8 characters)
3. **Important**: This password cannot be recovered if forgotten!
4. The application will create necessary data files automatically

## User Guide

### Adding a Password

1. Click "Add New" button
2. Fill in the website/service name
3. Enter username/email
4. Either enter a password manually or click "Generate" for a random one
5. Add any notes (optional)
6. Click "Save"

### Viewing/Editing Passwords

1. Browse the list or use the search bar
2. Double-click an entry to edit
3. Click "Copy Password" or "Copy Username" to copy to clipboard

### Security Features

- Passwords are never stored in plain text
- Master password is hashed using PBKDF2 with 100,000 iterations
- All stored passwords are encrypted using Fernet encryption
- Clipboard is automatically cleared after 30 seconds when copying passwords
- Application can be locked without closing

## Project Structure

```
SecureVault/
│
├── securevault/          # Main application package
│   ├── __init__.py      # Package initialization
│   ├── core/            # Core functionality
│   │   ├── __init__.py
│   │   ├── encryption.py    # Encryption and security functions
│   │   └── password_manager.py  # Core business logic
│   └── gui/             # GUI components
│       ├── __init__.py
│       ├── gui.py          # Main GUI implementation
│       └── gui_alternative.py  # macOS-specific GUI fixes
│
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_basic.py    # Basic functionality tests
│
├── docs/                # Documentation
│   ├── DEVELOPMENT_JOURNEY.md   # Development timeline and learning process
│   ├── TECHNICAL_DOCUMENTATION.md # Technical implementation details
│   ├── USER_GUIDE.md          # Comprehensive user instructions
│   └── PROJECT_SUMMARY.md     # Executive summary for presentations
│
├── main.py              # Application entry point
├── setup.py             # Package setup script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore file
│
├── master_password.json # Stores hashed master password (created on first run)
└── passwords.json      # Encrypted password storage (created on first run)
```

## Security Considerations

### What the Application Does Well

- Uses industry-standard encryption (Fernet/AES)
- Implements proper key derivation (PBKDF2)
- Never stores passwords in plain text
- Uses random salts to prevent rainbow table attacks

### Known Limitations

- Single-user application (no multi-user support)
- No cloud backup/sync functionality
- Basic password strength checking
- No two-factor authentication
- Vulnerable if master password is compromised

## Development Process

This project was developed as part of my A-Level Computer Science coursework. The development process included:

1. **Research Phase**: Learning about encryption, password security, and GUI development
2. **Design Phase**: Creating UI mockups and planning the application structure
3. **Implementation Phase**: Coding the application with iterative improvements
4. **Testing Phase**: Manual testing and bug fixes
5. **Documentation Phase**: Creating user and technical documentation

## Testing

The application has been tested for:

- Creating and verifying master passwords
- Adding, editing, and deleting password entries
- Password generation with different settings
- Search functionality
- Encryption and decryption accuracy
- Error handling for various edge cases

## Future Improvements

If I were to continue developing this project, I would add:

1. Password strength indicator
2. Automatic backups
3. Import/export functionality
4. Password expiry reminders
5. More advanced search filters
6. Browser integration
7. Mobile app version

## Acknowledgments

- Python cryptography library documentation
- Tkinter documentation and tutorials
- Stack Overflow community for problem-solving help
- My Computer Science teacher for guidance

## License

This is an educational project created for A-Level Computer Science coursework.

---

**Note**: This application is created for educational purposes as part of an A-Level Computer Science project. While it implements real security measures, it should not be used for storing highly sensitive information in a production environment. 