"""Tkinter login UI for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from auth.login import authenticate_user
from ui.main_menu_ui import open_main_menu


def create_login_window() -> None:
    """Create and display the login window."""
    root = tk.Tk()
    root.title("Slava Tech Accounts Payable Login")
    root.geometry("350x200")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Username").grid(row=0, column=0, sticky="w", pady=(0, 6))
    username_entry = tk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, pady=(0, 6))

    tk.Label(frame, text="Password").grid(row=1, column=0, sticky="w", pady=(0, 12))
    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.grid(row=1, column=1, pady=(0, 12))

    def login_action() -> None:
        """Handle login button clicks."""
        username = username_entry.get().strip()
        password = password_entry.get()

        if authenticate_user(username, password):
            root.destroy()
            open_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_button = tk.Button(frame, text="Login", width=12, command=login_action)
    login_button.grid(row=2, column=0, columnspan=2, pady=(6, 0))

    username_entry.focus_set()
    root.mainloop()
