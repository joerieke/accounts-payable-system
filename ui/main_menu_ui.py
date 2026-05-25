"""Tkinter main menu UI for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk

from ui.vendor_ui import open_vendor_ui, open_vendor_edit_ui
from ui.payment_invoice_ui import open_invoice_ui, open_invoice_edit_ui
from ui.payment_analytics_ui import open_analytics_ui
from ui.vendor_display_ui import open_vendor_display_ui
from ui.payment_invoice_display_ui import open_invoice_display_ui
from ui.payment_archive_ui import open_archive_ui

def open_main_menu() -> None:
    """Create and display the main menu window."""
    root = tk.Tk()
    root.title("Slava Tech Accounts Payable System")
    root.geometry("400x350")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True, fill="both")

    title = tk.Label(frame, text="Main Menu", font=("Arial", 14, "bold"))
    title.pack(pady=(0, 12))

    btn_config = {"width": 25, "pady": 6}

    tk.Button(frame, text="New/Edit Vendor", command=open_vendor_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="View Vendors", command=open_vendor_display_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="New/Edit Invoice", command=open_invoice_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="View Invoices", command=open_invoice_display_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="Archive Records", command=open_archive_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="Analytics Dashboard", command=open_analytics_ui, **btn_config).pack(pady=4)
    tk.Button(frame, text="Exit Application", command=root.destroy, **btn_config).pack(pady=8)

    root.mainloop()
