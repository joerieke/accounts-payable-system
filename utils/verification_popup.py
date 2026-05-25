"""Reusable verification popup for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


def verification_popup(title: str, message: str) -> bool:
    """Display a confirmation dialog and return True if confirmed."""
    if title is None:
        title = "Confirm"
    if message is None:
        message = ""

    try:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(title, message)
        root.destroy()
        return bool(result)
    except Exception:
        return False
