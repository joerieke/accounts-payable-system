
"""
Invoice Database Viewer UI
Displays invoice records with search capability.
"""

import tkinter as tk
from tkinter import ttk
import sqlite3


DB_NAME = "ap_system.db"


def fetch_invoices(search_term=None):
    """Retrieve invoice records from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if not search_term:
        cursor.execute("SELECT * FROM vendor_invoices")
    else:
        cursor.execute(
            """
            SELECT * FROM vendor_invoices
            WHERE invoice_id = ?
            OR vendor_invoice_number LIKE ?
            """,
            (search_term, f"%{search_term}%")
        )

    rows = cursor.fetchall()
    conn.close()
    return rows


def populate_tree(tree, rows):
    """Populate the Treeview with invoice records."""
    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", "end", values=row)


def open_invoice_display_ui():
    """Launch the invoice database viewer window."""

    window = tk.Toplevel()
    window.title("Invoice Database Viewer")
    window.geometry("950x450")

    # ---------------- Search Frame ----------------
    search_frame = tk.Frame(window, padx=10, pady=5)
    search_frame.pack(fill="x")

    tk.Label(search_frame, text="Search Invoice ID or Vendor Invoice #:").pack(side="left")

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)

    # ---------------- Table Frame ----------------
    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True)

    columns = (
        "invoice_id",
        "vendor_id",
        "vendor_invoice_number",
        "invoice_date",
        "invoice_amount",
        "invoice_description"
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    # ---------------- Button Frame ----------------
    button_frame = tk.Frame(window, pady=10)
    button_frame.pack()

    def search():
        term = search_entry.get().strip()
        rows = fetch_invoices(term)
        populate_tree(tree, rows)

    def clear():
        search_entry.delete(0, tk.END)
        populate_tree(tree, fetch_invoices())

    tk.Button(button_frame, text="Search", width=12, command=search).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear", width=12, command=clear).pack(side="left", padx=5)
    tk.Button(button_frame, text="Close", width=12, command=window.destroy).pack(side="left", padx=5)

    # Initial load
    populate_tree(tree, fetch_invoices())
