#!/usr/bin/env python3
"""
SecureVault Password Manager
Supercurricular Project
Main entry point for the application.
"""

import sys
import os
import platform
from tkinter import Tk, messagebox

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import appropriate GUI based on platform
    if platform.system() == "Darwin":  # macOS
        from securevault.gui.gui_alternative import MacOSPasswordManagerGUI as PasswordManagerGUI
    else:
        from securevault.gui import PasswordManagerGUI
    from securevault.core import PasswordManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure you run this from the project root directory.")
    sys.exit(1)


def main():
    """Main function to start the password manager application"""
    try:
        # Create the root window
        root = Tk()
        root.title("SecureVault Password Manager")
        
        # Set window size and center it
        window_width = 800
        window_height = 600
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate position to center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.resizable(False, False)
        
        # Create password manager instance
        password_manager = PasswordManager()
        
        # Create and start the GUI
        app = PasswordManagerGUI(root, password_manager)
        
        # Start the main event loop
        root.mainloop()
        
    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror("Critical Error", 
                           f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 