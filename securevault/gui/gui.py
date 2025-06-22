"""
gui.py - Graphical User Interface for the password manager
Uses Tkinter for cross-platform compatibility

This was challenging to create - I had to learn about:
- Tkinter widgets and layout managers
- Event handling
- Dialog windows
- Input validation
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
import platform
import subprocess

# For copying to clipboard - will need to install with pip
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Warning: pyperclip not installed. Copy to clipboard will not work.")
    print("Install with: pip install pyperclip")


# Dark mode detection and color schemes
class ColorScheme:
    """Color schemes for light and dark modes"""
    
    @staticmethod
    def is_dark_mode():
        """Detect if system is in dark mode"""
        system = platform.system()
        
        if system == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0 and "Dark" in result.stdout
            except:
                return False
        elif system == "Windows":
            try:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
            except:
                return False
        else:  # Linux and others
            # Check for common dark theme indicators
            import os
            theme = os.environ.get('GTK_THEME', '').lower()
            return 'dark' in theme
    
    def __init__(self):
        self.is_dark = self.is_dark_mode()
        
        if self.is_dark:
            # Dark mode colors with better contrast
            self.bg = "#1e1e1e"
            self.fg = "#ffffff"
            self.entry_bg = "#2d2d2d"
            self.entry_fg = "#ffffff"
            self.button_bg = "#0d7377"
            self.button_fg = "#ffffff"
            self.button_hover = "#14a085"
            self.success_bg = "#27ae60"
            self.error_bg = "#e74c3c"
            self.info_bg = "#3498db"
            self.frame_bg = "#252525"
            self.label_fg = "#e0e0e0"
            self.tree_bg = "#2d2d2d"
            self.tree_fg = "#ffffff"
            self.tree_selected = "#0d7377"
            self.tree_selected_fg = "#ffffff"
            # Ensure entry fields have visible borders
            self.entry_border = "#404040"
        else:
            # Light mode colors with better contrast
            self.bg = "#f5f5f5"
            self.fg = "#212121"
            self.entry_bg = "#ffffff"
            self.entry_fg = "#212121"
            self.button_bg = "#1976D2"
            self.button_fg = "#212121"  # Changed from white to dark for better contrast
            self.button_hover = "#1565C0"
            self.success_bg = "#388E3C"
            self.error_bg = "#D32F2F"
            self.info_bg = "#1976D2"
            self.frame_bg = "#fafafa"
            self.label_fg = "#424242"
            self.tree_bg = "#ffffff"
            self.tree_fg = "#212121"
            self.tree_selected = "#1976D2"
            self.tree_selected_fg = "#ffffff"
            # Ensure entry fields have visible borders
            self.entry_border = "#cccccc"


# Global color scheme instance
colors = ColorScheme()


def style_entry(entry_widget):
    """Apply consistent styling to entry widgets with proper borders"""
    entry_widget.config(
        bg=colors.entry_bg,
        fg=colors.entry_fg,
        insertbackground=colors.entry_fg,
        relief="solid",
        borderwidth=1,
        highlightthickness=2,
        highlightbackground=colors.entry_border,
        highlightcolor=colors.button_bg
    )


def style_button(button_widget, button_type="default"):
    """Apply consistent styling to buttons with proper colors"""
    if button_type == "success":
        bg = colors.success_bg
    elif button_type == "error":
        bg = colors.error_bg
    elif button_type == "info":
        bg = colors.info_bg
    else:
        bg = colors.button_bg
    
    # Force button styling even on macOS
    import platform
    if platform.system() == "Darwin":
        # On macOS, we need to be more aggressive with styling
        button_widget.config(
            bg=bg,
            fg=colors.button_fg,
            activebackground=colors.button_hover,
            activeforeground=colors.button_fg,
            highlightbackground=bg,
            highlightcolor=bg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=10,
            pady=5
        )
    else:
        button_widget.config(
            bg=bg,
            fg=colors.button_fg,
            activebackground=colors.button_hover,
            activeforeground=colors.button_fg,
            relief="raised",
            borderwidth=2,
            highlightthickness=0
        )


class CustomButton(tk.Frame):
    """Custom button implementation that works better on macOS"""
    
    def __init__(self, parent, text="", command=None, button_type="default", width=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Determine colors based on button type
        if button_type == "success":
            self.bg_color = colors.success_bg
        elif button_type == "error":
            self.bg_color = colors.error_bg
        elif button_type == "info":
            self.bg_color = colors.info_bg
        else:
            self.bg_color = colors.button_bg
        
        self.fg_color = colors.button_fg
        self.hover_color = colors.button_hover
        self.command = command
        
        # Configure frame
        self.config(bg=self.bg_color, relief="raised", borderwidth=1)
        
        # Create label
        self.label = tk.Label(self, text=text, bg=self.bg_color, fg=self.fg_color,
                             padx=20 if not width else width//2, pady=5, cursor="hand2")
        self.label.pack(fill="both", expand=True)
        
        # Bind events
        self.bind_events()
    
    def bind_events(self):
        """Bind mouse events"""
        # Mouse enter
        self.bind("<Enter>", self.on_enter)
        self.label.bind("<Enter>", self.on_enter)
        
        # Mouse leave
        self.bind("<Leave>", self.on_leave)
        self.label.bind("<Leave>", self.on_leave)
        
        # Click
        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        
        # Key press (for accessibility)
        self.bind("<Return>", self.on_click)
        self.bind("<space>", self.on_click)
    
    def on_enter(self, event):
        """Handle mouse enter"""
        self.config(bg=self.hover_color, relief="solid", borderwidth=2)
        self.label.config(bg=self.hover_color)
    
    def on_leave(self, event):
        """Handle mouse leave"""
        self.config(bg=self.bg_color, relief="raised", borderwidth=1)
        self.label.config(bg=self.bg_color)
    
    def on_click(self, event):
        """Handle click"""
        if self.command:
            self.command()
    
    def config_command(self, command):
        """Update the command"""
        self.command = command
    
    def pack(self, **kwargs):
        """Override pack to handle width properly"""
        if "fill" not in kwargs:
            kwargs["fill"] = "x"
        super().pack(**kwargs)


def create_button(parent, text="", command=None, button_type="default", width=None, use_custom=None):
    """Create a button - uses custom implementation on macOS to avoid white rectangle issue"""
    if use_custom is None:
        use_custom = platform.system() == "Darwin"
    
    if use_custom:
        btn = CustomButton(parent, text=text, command=command, button_type=button_type, width=width)
        return btn
    else:
        btn = tk.Button(parent, text=text, command=command, width=width)
        style_button(btn, button_type)
        return btn


class LoginWindow:
    """Window for master password login or setup"""
    
    def __init__(self, parent, password_manager, on_success_callback=None):
        self.parent = parent
        self.password_manager = password_manager
        self.on_success_callback = on_success_callback
        self.window = tk.Toplevel(parent)
        self.window.title("SecureVault - Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Apply color scheme
        self.window.configure(bg=colors.bg)
        
        # Center the window
        self.center_window()
        
        # Hide parent window
        parent.withdraw()
        
        # Make window modal
        self.window.transient(parent)
        
        # Check if this is first time setup
        if not password_manager.is_master_password_set():
            self.setup_new_password()
        else:
            self.setup_login()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Ensure window is visible before grab
        self.window.update()
        self.window.deiconify()
        
        # Force window to front
        self.window.lift()
        self.window.attributes('-topmost', True)
        
        # Set up proper focus handling after window is visible
        self.window.after(10, self._setup_window_focus)
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_window_focus(self):
        """Set up window focus and grab after window is visible"""
        try:
            # Wait for window to be visible
            self.window.wait_visibility()
            
            # Remove topmost after window is visible
            self.window.attributes('-topmost', False)
            
            # Check platform before using grab_set
            import platform
            if platform.system() != "Darwin":  # Not macOS
                # Set grab for modal behavior (causes issues on macOS)
                self.window.grab_set()
            
            # Force focus to the window
            self.window.focus_force()
            
            # Focus the appropriate entry field
            if hasattr(self, 'password_entry'):
                self.password_entry.focus_set()
                # Ensure the entry widget can receive input
                self.password_entry.focus_force()
                # Bind click to ensure focus
                self.password_entry.bind('<Button-1>', lambda e: self.password_entry.focus_set())
        except Exception as e:
            print(f"Error setting up window focus: {e}")

    def setup_new_password(self):
        """Setup interface for creating new master password"""
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.window, text="Welcome to SecureVault",
                              font=("Arial", 16, "bold"),
                              bg=colors.bg, fg=colors.fg)
        title_label.pack(pady=20)
        
        # Instructions
        info_label = tk.Label(self.window, 
                             text="Create a master password to secure your data.\n"
                                  "This password cannot be recovered if forgotten!",
                             wraplength=350,
                             bg=colors.bg, fg=colors.label_fg)
        info_label.pack(pady=10)
        
        # Password frame
        pwd_frame = tk.Frame(self.window, bg=colors.bg)
        pwd_frame.pack(pady=10)
        
        tk.Label(pwd_frame, text="Master Password:", 
                bg=colors.bg, fg=colors.label_fg).grid(row=0, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(pwd_frame, show="*", width=25)
        style_entry(self.password_entry)
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(pwd_frame, text="Confirm Password:",
                bg=colors.bg, fg=colors.label_fg).grid(row=1, column=0, padx=5, pady=5)
        self.confirm_entry = tk.Entry(pwd_frame, show="*", width=25)
        style_entry(self.confirm_entry)
        self.confirm_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Show/Hide password checkbox
        self.show_pwd_var = tk.BooleanVar()
        show_pwd_check = tk.Checkbutton(self.window, text="Show Password",
                                       variable=self.show_pwd_var,
                                       command=self.toggle_password_visibility,
                                       bg=colors.bg, fg=colors.label_fg,
                                       activebackground=colors.bg,
                                       selectcolor=colors.entry_bg,
                                       activeforeground=colors.fg)
        show_pwd_check.pack()
        
        # Create button
        create_btn = create_button(self.window, text="Create Master Password",
                                  command=self.create_master_password,
                                  button_type="success", width=20)
        create_btn.pack(pady=20)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.create_master_password())
        
    def setup_login(self):
        """Setup interface for logging in"""
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.window, text="SecureVault Login",
                              font=("Arial", 16, "bold"),
                              bg=colors.bg, fg=colors.fg)
        title_label.pack(pady=30)
        
        # Password frame
        pwd_frame = tk.Frame(self.window, bg=colors.bg)
        pwd_frame.pack(pady=20)
        
        tk.Label(pwd_frame, text="Master Password:",
                bg=colors.bg, fg=colors.label_fg).pack(side=tk.LEFT, padx=5)
        self.password_entry = tk.Entry(pwd_frame, show="*", width=25)
        style_entry(self.password_entry)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Show/Hide password checkbox
        self.show_pwd_var = tk.BooleanVar()
        show_pwd_check = tk.Checkbutton(self.window, text="Show Password",
                                       variable=self.show_pwd_var,
                                       command=self.toggle_password_visibility,
                                       bg=colors.bg, fg=colors.label_fg,
                                       activebackground=colors.bg,
                                       selectcolor=colors.entry_bg,
                                       activeforeground=colors.fg)
        show_pwd_check.pack(pady=10)
        
        # Login button
        login_btn = create_button(self.window, text="Unlock",
                                 command=self.login,
                                 button_type="info", width=20)
        login_btn.pack(pady=10)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
        
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
        
        # Validation
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
            # Set the master password
            if self.password_manager.set_master_password(password):
                messagebox.showinfo("Success", "Master password created successfully!")
                self.window.destroy()
                self.parent.deiconify()  # Show main window
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
        
        # Try to unlock
        if self.password_manager.unlock(password):
            self.window.destroy()
            self.parent.deiconify()  # Show main window
            if self.on_success_callback:
                self.on_success_callback()  # Refresh entries
        else:
            messagebox.showerror("Error", "Incorrect password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def on_close(self):
        """Handle window close"""
        self.parent.quit()


class PasswordGeneratorDialog:
    """Dialog for generating passwords"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Password Generator")
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        
        # Apply color scheme
        self.dialog.configure(bg=colors.bg)
        
        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.length_var = tk.IntVar(value=16)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
        # Focus
        self.dialog.focus_force()
        
    def setup_ui(self):
        """Setup the generator UI"""
        # Title
        title_label = tk.Label(self.dialog, text="Password Generator",
                              font=("Arial", 14, "bold"),
                              bg=colors.bg, fg=colors.fg)
        title_label.pack(pady=10)
        
        # Length frame
        length_frame = tk.Frame(self.dialog, bg=colors.bg)
        length_frame.pack(pady=10)
        
        tk.Label(length_frame, text="Password Length:",
                bg=colors.bg, fg=colors.label_fg).pack(side=tk.LEFT, padx=5)
        length_spinbox = tk.Spinbox(length_frame, from_=8, to=32,
                                   textvariable=self.length_var, width=10)
        style_entry(length_spinbox)
        length_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Character options
        options_frame = tk.LabelFrame(self.dialog, text="Character Types", padx=20, pady=10,
                                     bg=colors.bg, fg=colors.label_fg)
        options_frame.pack(pady=10)
        
        tk.Checkbutton(options_frame, text="Uppercase (A-Z)",
                      variable=self.uppercase_var,
                      bg=colors.bg, fg=colors.label_fg,
                      activebackground=colors.bg,
                      selectcolor=colors.entry_bg,
                      activeforeground=colors.fg).pack(anchor=tk.W)
        tk.Checkbutton(options_frame, text="Lowercase (a-z)",
                      variable=self.lowercase_var,
                      bg=colors.bg, fg=colors.label_fg,
                      activebackground=colors.bg,
                      selectcolor=colors.entry_bg,
                      activeforeground=colors.fg).pack(anchor=tk.W)
        tk.Checkbutton(options_frame, text="Digits (0-9)",
                      variable=self.digits_var,
                      bg=colors.bg, fg=colors.label_fg,
                      activebackground=colors.bg,
                      selectcolor=colors.entry_bg,
                      activeforeground=colors.fg).pack(anchor=tk.W)
        tk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)",
                      variable=self.symbols_var,
                      bg=colors.bg, fg=colors.label_fg,
                      activebackground=colors.bg,
                      selectcolor=colors.entry_bg,
                      activeforeground=colors.fg).pack(anchor=tk.W)
        
        # Generated password display
        self.password_display = tk.Entry(self.dialog, width=40, font=("Courier", 12))
        style_entry(self.password_display)
        self.password_display.pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=colors.bg)
        button_frame.pack()
        
        generate_btn = create_button(button_frame, text="Generate",
                                    command=self.generate_password,
                                    button_type="success")
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        use_btn = create_button(button_frame, text="Use This Password",
                               command=self.use_password,
                               button_type="info")
        use_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = create_button(button_frame, text="Cancel",
                                  command=self.dialog.destroy,
                                  button_type="default")
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Generate initial password
        self.generate_password()
    
    def generate_password(self):
        """Generate a new password"""
        # Import here to avoid circular import
        from ..core.password_manager import PasswordManager
        pm = PasswordManager()
        
        password = pm.generate_password(
            length=self.length_var.get(),
            use_uppercase=self.uppercase_var.get(),
            use_lowercase=self.lowercase_var.get(),
            use_digits=self.digits_var.get(),
            use_symbols=self.symbols_var.get()
        )
        
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, password)
    
    def use_password(self):
        """Use the generated password"""
        self.result = self.password_display.get()
        self.dialog.destroy()


class AddEditDialog:
    """Dialog for adding or editing password entries"""
    
    def __init__(self, parent, password_manager, entry=None, index=None):
        self.password_manager = password_manager
        self.entry = entry
        self.index = index
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Entry" if entry else "Add New Entry")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Apply color scheme
        self.dialog.configure(bg=colors.bg)
        
        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        # Populate fields if editing
        if entry:
            self.website_entry.insert(0, entry.website)
            self.username_entry.insert(0, entry.username)
            self.password_entry.insert(0, entry.password)
            self.notes_text.insert("1.0", entry.notes)
        
        # Focus
        self.dialog.focus_force()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        # Main frame with padding
        main_frame = tk.Frame(self.dialog, padx=20, pady=20, bg=colors.bg)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Website
        tk.Label(main_frame, text="Website/Service:",
                bg=colors.bg, fg=colors.label_fg).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.website_entry = tk.Entry(main_frame, width=40)
        style_entry(self.website_entry)
        self.website_entry.grid(row=0, column=1, columnspan=2, pady=5)
        
        # Username
        tk.Label(main_frame, text="Username/Email:",
                bg=colors.bg, fg=colors.label_fg).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = tk.Entry(main_frame, width=40)
        style_entry(self.username_entry)
        self.username_entry.grid(row=1, column=1, columnspan=2, pady=5)
        
        # Password
        tk.Label(main_frame, text="Password:",
                bg=colors.bg, fg=colors.label_fg).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = tk.Entry(main_frame, width=30, show="*")
        style_entry(self.password_entry)
        self.password_entry.grid(row=2, column=1, pady=5)
        
        # Generate button
        generate_btn = create_button(main_frame, text="Generate",
                                    command=self.generate_password,
                                    button_type="default")
        generate_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # Show password checkbox
        self.show_pwd_var = tk.BooleanVar()
        show_pwd_check = tk.Checkbutton(main_frame, text="Show Password",
                                       variable=self.show_pwd_var,
                                       command=self.toggle_password,
                                       bg=colors.bg, fg=colors.label_fg,
                                       activebackground=colors.bg,
                                       selectcolor=colors.entry_bg,
                                       activeforeground=colors.fg)
        show_pwd_check.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Notes
        tk.Label(main_frame, text="Notes:",
                bg=colors.bg, fg=colors.label_fg).grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(main_frame, width=40, height=5,
                                bg=colors.entry_bg, fg=colors.entry_fg,
                                insertbackground=colors.entry_fg,
                                relief="solid", borderwidth=1,
                                highlightthickness=2,
                                highlightbackground=colors.entry_border,
                                highlightcolor=colors.button_bg)
        self.notes_text.grid(row=4, column=1, columnspan=2, pady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=colors.bg)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        save_btn = create_button(button_frame, text="Save",
                                command=self.save_entry,
                                button_type="success", width=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = create_button(button_frame, text="Cancel",
                                  command=self.dialog.destroy,
                                  button_type="default", width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Focus on first field after a delay
        self.dialog.after(100, lambda: self.website_entry.focus_force())
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_pwd_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def generate_password(self):
        """Open password generator"""
        gen_dialog = PasswordGeneratorDialog(self.dialog)
        self.dialog.wait_window(gen_dialog.dialog)
        
        if gen_dialog.result:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, gen_dialog.result)
            self.show_pwd_var.set(True)
            self.toggle_password()
    
    def save_entry(self):
        """Save the entry"""
        # Get values
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Validation
        if not website:
            messagebox.showerror("Error", "Website/Service name is required")
            return
        
        if not username:
            messagebox.showerror("Error", "Username is required")
            return
        
        if not password:
            messagebox.showerror("Error", "Password is required")
            return
        
        try:
            if self.index is not None:
                # Update existing entry
                self.password_manager.update_entry(
                    self.index, website, username, password, notes
                )
                messagebox.showinfo("Success", "Entry updated successfully")
            else:
                # Add new entry
                self.password_manager.add_entry(website, username, password, notes)
                messagebox.showinfo("Success", "Entry added successfully")
            
            self.result = True
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")


class PasswordManagerGUI:
    """Main GUI window for the password manager"""
    
    def __init__(self, root, password_manager):
        self.root = root
        self.password_manager = password_manager
        
        # Setup styles
        self.setup_styles()
        
        # Setup main UI first (but hidden)
        self.setup_main_ui()
        
        # Create login window with callback to refresh entries after login
        login_window = LoginWindow(root, password_manager, self.refresh_entries)
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure window background
        self.root.configure(bg=colors.bg)
        
        # Configure Treeview colors based on theme
        style.configure("Treeview", 
                       background=colors.tree_bg,
                       foreground=colors.tree_fg,
                       fieldbackground=colors.tree_bg)
        style.configure("Treeview.Heading", 
                       background=colors.frame_bg,
                       foreground=colors.fg)
        style.map('Treeview', 
                 background=[('selected', colors.tree_selected)],
                 foreground=[('selected', colors.tree_selected_fg)])
    
    def setup_main_ui(self):
        """Setup the main window UI"""
        # Menu bar
        menubar = tk.Menu(self.root, bg=colors.frame_bg, fg=colors.fg,
                         activebackground=colors.button_hover,
                         activeforeground=colors.button_fg)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=colors.frame_bg, fg=colors.fg,
                           activebackground=colors.button_hover,
                           activeforeground=colors.button_fg)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Lock", command=self.lock_manager)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=colors.frame_bg, fg=colors.fg,
                           activebackground=colors.button_hover,
                           activeforeground=colors.button_fg)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=colors.bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg=colors.bg)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg=colors.bg, fg=colors.label_fg).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.refresh_entries())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        style_entry(search_entry)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=colors.bg)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_btn = create_button(button_frame, text="Add New",
                               command=self.add_entry,
                               button_type="success")
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = create_button(button_frame, text="Edit",
                                command=self.edit_entry,
                                button_type="info")
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = create_button(button_frame, text="Delete",
                                  command=self.delete_entry,
                                  button_type="error")
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        copy_pwd_btn = create_button(button_frame, text="Copy Password",
                                    command=self.copy_password,
                                    button_type="default")
        copy_pwd_btn.pack(side=tk.LEFT, padx=5)
        
        copy_user_btn = create_button(button_frame, text="Copy Username",
                                     command=self.copy_username,
                                     button_type="default")
        copy_user_btn.pack(side=tk.LEFT, padx=5)
        
        # Password list (Treeview)
        tree_frame = tk.Frame(main_frame, bg=colors.bg)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("Website", "Username", "Notes"),
                                show="tree headings", yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading("#0", text="ID")
        self.tree.heading("Website", text="Website/Service")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Notes", text="Notes")
        
        self.tree.column("#0", width=50)
        self.tree.column("Website", width=200)
        self.tree.column("Username", width=200)
        self.tree.column("Notes", width=300)
        
        # Double-click to edit
        self.tree.bind("<Double-Button-1>", lambda e: self.edit_entry())
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W,
                                  bg=colors.frame_bg, fg=colors.fg)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Don't refresh entries here - will be done after login
    
    def refresh_entries(self):
        """Refresh the password list"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Get entries
            search_term = self.search_var.get()
            entries = self.password_manager.get_entries(search_term)
            
            # Add to tree
            for i, (index, entry) in enumerate(entries):
                self.tree.insert("", "end", text=str(i+1),
                               values=(entry.website, entry.username, entry.notes))
            
            # Update status
            self.status_bar.config(text=f"Showing {len(entries)} entries")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load entries: {str(e)}")
    
    def add_entry(self):
        """Add a new password entry"""
        dialog = AddEditDialog(self.root, self.password_manager)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_entries()
    
    def edit_entry(self):
        """Edit selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        # Get the index
        item = self.tree.item(selection[0])
        index = int(item['text']) - 1
        
        # Get the actual entry
        entries = self.password_manager.get_entries(self.search_var.get())
        if index < len(entries):
            real_index, entry = entries[index]
            
            dialog = AddEditDialog(self.root, self.password_manager, entry, real_index)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.refresh_entries()
    
    def delete_entry(self):
        """Delete selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  "Are you sure you want to delete this entry?"):
            return
        
        # Get the index
        item = self.tree.item(selection[0])
        index = int(item['text']) - 1
        
        # Get the actual entry index
        entries = self.password_manager.get_entries(self.search_var.get())
        if index < len(entries):
            real_index, _ = entries[index]
            
            try:
                self.password_manager.delete_entry(real_index)
                self.refresh_entries()
                messagebox.showinfo("Success", "Entry deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def copy_password(self):
        """Copy password to clipboard"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry")
            return
        
        # Get the index
        item = self.tree.item(selection[0])
        index = int(item['text']) - 1
        
        # Get the entry
        entries = self.password_manager.get_entries(self.search_var.get())
        if index < len(entries):
            _, entry = entries[index]
            
            if CLIPBOARD_AVAILABLE:
                try:
                    pyperclip.copy(entry.password)
                    self.status_bar.config(text="Password copied to clipboard")
                    # Clear clipboard after 30 seconds for security
                    self.root.after(30000, lambda: pyperclip.copy(""))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy: {str(e)}")
            else:
                # Show password in a dialog if clipboard not available
                messagebox.showinfo("Password", f"Password: {entry.password}\n\nNote: Install pyperclip for clipboard support")
    
    def copy_username(self):
        """Copy username to clipboard"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry")
            return
        
        # Get the values directly from tree
        item = self.tree.item(selection[0])
        username = item['values'][1]  # Username is second value
        
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(username)
                self.status_bar.config(text="Username copied to clipboard")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy: {str(e)}")
        else:
            # Show username in a dialog if clipboard not available
            messagebox.showinfo("Username", f"Username: {username}\n\nNote: Install pyperclip for clipboard support")
    
    def lock_manager(self):
        """Lock the password manager"""
        self.password_manager.lock()
        self.root.withdraw()
        LoginWindow(self.root, self.password_manager, self.refresh_entries)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """SecureVault Password Manager
Version 1.0

Supercurricular Project

This application provides secure password storage
using encryption to protect your sensitive data.

© 2024 - Educational Project"""
        
        messagebox.showinfo("About SecureVault", about_text)
    
    def on_close(self):
        """Handle window close"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()


# For testing the GUI independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide initially
    
    # Create mock password manager for testing
    from ..core.password_manager import PasswordManager
    pm = PasswordManager()
    
    app = PasswordManagerGUI(root, pm)
    root.mainloop() 