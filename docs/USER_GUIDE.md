# SecureVault User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [First Time Setup](#first-time-setup)
3. [Main Features](#main-features)
4. [Security Best Practices](#security-best-practices)
5. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Windows 10/11, macOS 10.14+, or Linux
- Python 3.8 or higher
- 50MB free disk space

### Installation

1. **Download the Application**
   - Download all files to a folder on your computer

2. **Install Dependencies**
   Open Terminal/Command Prompt in the application folder and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**
   ```bash
   python main.py
   ```

## First Time Setup

### Creating Your Master Password

When you first launch SecureVault, you'll need to create a master password:

1. **Welcome Screen**
   - You'll see "Welcome to SecureVault"
   - Read the warning about password recovery carefully

2. **Choose a Strong Master Password**
   - Minimum 8 characters
   - Use a mix of uppercase, lowercase, numbers, and symbols
   - Make it memorable but unique
   - **IMPORTANT**: This password cannot be recovered if forgotten!

3. **Confirm Your Password**
   - Type your password again to confirm
   - Click "Create Master Password"

### Example of a Good Master Password:
- `MyDog$Name!Is#Rex2020` ✓ (Personal, memorable, complex)
- `password123` ✗ (Too common and simple)

## Main Features

### 1. Adding a New Password Entry

**Steps:**
1. Click the "Add New" button
2. Fill in the required fields:
   - **Website/Service**: e.g., "Gmail", "Amazon", "Netflix"
   - **Username/Email**: Your login username or email
   - **Password**: Your password (or generate one)
   - **Notes** (Optional): Any additional information

3. Click "Save"

**Using the Password Generator:**
- Click "Generate" next to the password field
- Adjust settings:
  - Length (8-32 characters)
  - Character types to include
- Click "Generate" to create a new password
- Click "Use This Password" when satisfied

### 2. Viewing and Copying Passwords

**To View Entries:**
- All your saved passwords appear in the main list
- Shows Website, Username, and Notes (passwords are hidden)

**To Copy Credentials:**
1. Select an entry by clicking on it
2. Click "Copy Password" to copy the password
3. Click "Copy Username" to copy the username
4. Paste into your login form (Ctrl+V or Cmd+V)

**Security Note**: Passwords are automatically cleared from clipboard after 30 seconds

### 3. Editing Existing Entries

**Steps:**
1. Double-click the entry you want to edit
   OR select it and click "Edit"
2. Make your changes
3. Click "Save"

**What You Can Edit:**
- Website/Service name
- Username
- Password
- Notes

### 4. Deleting Entries

**Steps:**
1. Select the entry you want to delete
2. Click "Delete"
3. Confirm the deletion when prompted

**Warning**: Deleted entries cannot be recovered!

### 5. Searching for Entries

**How to Search:**
- Type in the search box at the top
- Results update automatically as you type
- Searches in: Website name, Username, and Notes

**Search Examples:**
- "gmail" - finds all Gmail entries
- "john" - finds entries with "john" in username
- "work" - finds entries with "work" in notes

### 6. Locking the Application

**To Lock:**
- Go to File → Lock
- OR close the application

**To Unlock:**
- Enter your master password
- Click "Unlock"

## Security Best Practices

### 1. Master Password Security
- Never share your master password
- Don't write it down where others can find it
- Change it periodically (every 6-12 months)
- Use a unique password not used elsewhere

### 2. General Password Tips
- Use different passwords for each account
- Update passwords regularly for sensitive accounts
- Use the password generator for maximum security
- Enable two-factor authentication where available (not in this app)

### 3. Data Backup
- Regularly backup your password files:
  - `passwords.json`
  - `master_password.json`
- Store backups in a secure location
- Test restore process periodically

### 4. Application Security
- Always lock the application when not in use
- Don't leave the application open on shared computers
- Keep your computer's operating system updated
- Use antivirus software

## Troubleshooting

### Common Issues and Solutions

**Problem: "Incorrect password" error**
- Solution: Ensure Caps Lock is off and try again
- Check that you're entering the master password, not a stored password

**Problem: Application won't start**
- Solution: 
  1. Check Python is installed: `python --version`
  2. Reinstall dependencies: `pip install -r requirements.txt`
  3. Check for error messages in terminal

**Problem: Can't copy to clipboard**
- Solution: Install pyperclip: `pip install pyperclip`
- Alternative: Manually type the password

**Problem: Lost master password**
- Unfortunately, there's no way to recover a lost master password
- You'll need to delete the data files and start over
- This is a security feature, not a bug

**Problem: Corrupted data file**
- If you have a backup, restore from it
- Otherwise, rename the corrupted file and restart
- The application will create new empty files

### Getting Help

If you encounter issues not covered here:

1. Check the TECHNICAL_DOCUMENTATION.md file
2. Review error messages carefully
3. Ask your Computer Science teacher
4. Check the development journey for similar issues

## Tips for Effective Use

1. **Organize with Notes**
   - Use notes to categorize: "Work", "Personal", "Banking"
   - Add security questions/answers in notes
   - Include account numbers or IDs

2. **Regular Maintenance**
   - Review and remove old/unused entries monthly
   - Update passwords for important accounts regularly
   - Check for duplicate entries

3. **Keyboard Shortcuts**
   - Enter: Confirm dialogs
   - Escape: Cancel dialogs
   - Double-click: Edit entries

4. **Password Generation Strategy**
   - Use maximum length for important accounts
   - Include all character types when possible
   - Generate new passwords when updating

## Security Warnings

⚠️ **Never**:
- Store your master password in the application
- Share your password database files
- Use SecureVault on untrusted computers
- Ignore security warnings from the application

✅ **Always**:
- Lock the application when done
- Verify website URLs before entering passwords
- Keep backups in secure locations
- Update the application when new versions are available

---

Remember: SecureVault is an educational project. While it implements real security measures, always follow your organization's security policies for sensitive information. 