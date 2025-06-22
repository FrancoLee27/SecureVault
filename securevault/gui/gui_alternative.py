"""
Alternative GUI implementation with improved macOS compatibility
This version uses a different approach to modal windows to avoid input issues
"""

import tkinter as tk
from tkinter import messagebox
import platform

# Import the existing GUI module to reuse most components
from .gui import colors, PasswordGeneratorDialog, AddEditDialog, PasswordManagerGUI as BasePasswordManagerGUI, style_button, create_button


class MacOSLoginWindow:
    """Login window with macOS-specific fixes"""
    
    def __init__(self, parent, password_manager, on_success_callback=None):
        self.parent = parent
        self.password_manager = password_manager
        self.on_success_callback = on_success_callback
        
        # Create window but don't use Toplevel
        self.window = tk.Toplevel(parent)
        self.window.title("SecureVault - Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Apply color scheme
        self.window.configure(bg=colors.bg)
        
        # Hide parent
        parent.withdraw()
        
        # Center window
        self.center_window()
        
        # Setup UI first
        if not password_manager.is_master_password_set():
            self.setup_new_password()
        else:
            self.setup_login()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # macOS specific: Use update and lift without grab_set
        self.window.update()
        self.window.lift()
        
        # Focus without grab - this often works better on macOS
        if hasattr(self, 'password_entry'):
            self.window.after(50, lambda: self.password_entry.focus_force())
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = 400
        height = 300
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_new_password(self):
        """Setup interface for creating new master password"""
        # Main container frame
        container = tk.Frame(self.window, bg=colors.bg)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(container, text="Welcome to SecureVault",
                              font=("Arial", 16, "bold"),
                              bg=colors.bg, fg=colors.fg)
        title_label.pack(pady=(0, 10))
        
        # Instructions
        info_label = tk.Label(container, 
                             text="Create a master password to secure your data.\n"
                                  "This password cannot be recovered if forgotten!",
                             wraplength=350,
                             bg=colors.bg, fg=colors.label_fg)
        info_label.pack(pady=(0, 20))
        
        # Password fields in a frame
        fields_frame = tk.Frame(container, bg=colors.bg)
        fields_frame.pack(pady=(0, 10))
        
        # Master password
        tk.Label(fields_frame, text="Master Password:", 
                bg=colors.bg, fg=colors.label_fg).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.password_entry = tk.Entry(fields_frame, show="*", width=25,
                                     bg=colors.entry_bg, fg=colors.entry_fg,
                                     insertbackground=colors.entry_fg,
                                     relief="solid", borderwidth=1,
                                     highlightthickness=2,
                                     highlightbackground=colors.entry_border,
                                     highlightcolor=colors.button_bg)
        self.password_entry.grid(row=0, column=1, pady=5)
        
        # Confirm password
        tk.Label(fields_frame, text="Confirm Password:",
                bg=colors.bg, fg=colors.label_fg).grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        self.confirm_entry = tk.Entry(fields_frame, show="*", width=25,
                                    bg=colors.entry_bg, fg=colors.entry_fg,
                                    insertbackground=colors.entry_fg,
                                    relief="solid", borderwidth=1,
                                    highlightthickness=2,
                                    highlightbackground=colors.entry_border,
                                    highlightcolor=colors.button_bg)
        self.confirm_entry.grid(row=1, column=1, pady=5)
        
        # Show/Hide password
        self.show_pwd_var = tk.BooleanVar()
        show_check = tk.Checkbutton(container, text="Show Password",
                                   variable=self.show_pwd_var,
                                   command=self.toggle_password_visibility,
                                   bg=colors.bg, fg=colors.label_fg,
                                   activebackground=colors.bg,
                                   selectcolor=colors.entry_bg,
                                   activeforeground=colors.fg)
        show_check.pack(pady=(0, 20))
        
        # Create button
        create_btn = create_button(container, text="Create Master Password",
                                  command=self.create_master_password,
                                  button_type="success", width=20)
        create_btn.pack()
        
        # Bind Enter
        self.window.bind('<Return>', lambda e: self.create_master_password())
        
        # Focus first field
        self.password_entry.focus_set()
    
    def setup_login(self):
        """Setup interface for logging in"""
        # Main container
        container = tk.Frame(self.window, bg=colors.bg)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(container, text="SecureVault Login",
                              font=("Arial", 16, "bold"),
                              bg=colors.bg, fg=colors.fg)
        title_label.pack(pady=(0, 30))
        
        # Password field frame
        field_frame = tk.Frame(container, bg=colors.bg)
        field_frame.pack(pady=(0, 20))
        
        tk.Label(field_frame, text="Master Password:",
                bg=colors.bg, fg=colors.label_fg).pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = tk.Entry(field_frame, show="*", width=25,
                                     bg=colors.entry_bg, fg=colors.entry_fg,
                                     insertbackground=colors.entry_fg,
                                     relief="solid", borderwidth=1,
                                     highlightthickness=2,
                                     highlightbackground=colors.entry_border,
                                     highlightcolor=colors.button_bg)
        self.password_entry.pack(side=tk.LEFT)
        
        # Show/Hide password
        self.show_pwd_var = tk.BooleanVar()
        show_check = tk.Checkbutton(container, text="Show Password",
                                   variable=self.show_pwd_var,
                                   command=self.toggle_password_visibility,
                                   bg=colors.bg, fg=colors.label_fg,
                                   activebackground=colors.bg,
                                   selectcolor=colors.entry_bg,
                                   activeforeground=colors.fg)
        show_check.pack(pady=(0, 20))
        
        # Login button
        login_btn = create_button(container, text="Unlock",
                                 command=self.login,
                                 button_type="info", width=20)
        login_btn.pack()
        
        # Bind Enter
        self.window.bind('<Return>', lambda e: self.login())
        
        # Focus password field
        self.password_entry.focus_set()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_pwd_var.get():
            self.password_entry.config(show="")
            if hasattr(self, 'confirm_entry'):
                self.confirm_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            if hasattr(self, 'confirm_entry'):
                self.confirm_entry.config(show="*")
    
    def create_master_password(self):
        """Handle master password creation"""
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            return
        
        try:
            if self.password_manager.set_master_password(password):
                messagebox.showinfo("Success", "Master password created successfully!")
                self.window.destroy()
                self.parent.deiconify()
                if self.on_success_callback:
                    self.on_success_callback()  # Refresh entries
            else:
                messagebox.showerror("Error", "Failed to create master password")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def login(self):
        """Handle login attempt"""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter your password")
            return
        
        if self.password_manager.unlock(password):
            self.window.destroy()
            self.parent.deiconify()
            if self.on_success_callback:
                self.on_success_callback()  # Refresh entries
        else:
            messagebox.showerror("Error", "Incorrect password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def on_close(self):
        """Handle window close"""
        self.parent.quit()


class MacOSPasswordManagerGUI(BasePasswordManagerGUI):
    """Password manager GUI with macOS-specific login window"""
    
    def __init__(self, root, password_manager):
        # Store references
        self.root = root
        self.password_manager = password_manager
        
        # Setup styles
        self.setup_styles()
        
        # Setup main UI first (but hidden)
        self.setup_main_ui()
        
        # Use macOS-specific login window with callback
        if platform.system() == "Darwin":
            login_window = MacOSLoginWindow(root, password_manager, self.refresh_entries)
        else:
            # Use original for other platforms
            from .gui import LoginWindow
            login_window = LoginWindow(root, password_manager, self.refresh_entries)
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def lock_manager(self):
        """Lock the password manager"""
        self.password_manager.lock()
        self.root.withdraw()
        
        # Use appropriate login window with callback
        if platform.system() == "Darwin":
            MacOSLoginWindow(self.root, self.password_manager, self.refresh_entries)
        else:
            from .gui import LoginWindow
            LoginWindow(self.root, self.password_manager, self.refresh_entries) 