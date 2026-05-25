"""Tkinter analytics dashboard UI for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from analytics.payment_analytics_engine import get_payment_summary
from database.db_init import get_connection


def _fetch_vendor_codes():
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT vendor_code, vendor_description
            FROM vendor_codes
            ORDER BY vendor_code
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()

def _fetch_vendor_names():
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT vendor_id, vendor_name
            FROM vendors
            ORDER BY vendor_name
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


def open_analytics_ui() -> None:
    """Open the analytics dashboard window."""
    root = tk.Tk()
    root.title("Analytics Dashboard")
    root.geometry("550x420")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Analytics Dashboard", font=("Arial", 14, "bold")).pack(pady=(0, 12))

    filters_frame = tk.Frame(frame)
    filters_frame.pack(fill="x")

    tk.Label(filters_frame, text="Year").grid(row=0, column=0, sticky="w", pady=4)
    year_entry = tk.Entry(filters_frame, width=10)
    year_entry.grid(row=0, column=1, pady=4, padx=(0, 10))

    tk.Label(filters_frame, text="Month").grid(row=0, column=2, sticky="w", pady=4)
    month_entry = tk.Entry(filters_frame, width=5)
    month_entry.grid(row=0, column=3, pady=4, padx=(0, 10))

    tk.Label(filters_frame, text="Day").grid(row=0, column=4, sticky="w", pady=4)
    day_entry = tk.Entry(filters_frame, width=5)
    day_entry.grid(row=0, column=5, pady=4)

    tk.Label(filters_frame, text="Vendor Type").grid(row=1, column=0, sticky="w", pady=4)
    vendor_code_var = tk.StringVar()
    vendor_code_dropdown = ttk.Combobox(
        filters_frame, textvariable=vendor_code_var, state="readonly", width=12
    )
    vendor_code_dropdown.grid(row=1, column=1, pady=4, padx=(0, 10))

    tk.Label(filters_frame, text="Vendor Name").grid(row=1, column=2, sticky="w", pady=4)
    vendor_name_var = tk.StringVar()
    vendor_name_dropdown = ttk.Combobox(
        filters_frame, textvariable=vendor_name_var, state="readonly", width=20
    )
    vendor_name_dropdown.grid(row=1, column=3, pady=4, padx=(0, 10), columnspan=2)

    vendor_codes = _fetch_vendor_codes()
    vendor_code_values = ["None"] + [f"{code} - {desc}" for code, desc in vendor_codes]
    vendor_code_dropdown["values"] = vendor_code_values
    vendor_code_dropdown.current(0)

    vendor_names = _fetch_vendor_names()
    vendor_name_values = ["None"] + [f"{vid} - {name}" for vid, name in vendor_names]
    vendor_name_dropdown["values"] = vendor_name_values
    vendor_name_dropdown.current(0)

    results_frame = tk.Frame(frame)
    results_frame.pack(fill="both", expand=True, pady=(12, 0))

    tree = ttk.Treeview(results_frame, columns=("count", "total"), show="headings", height=4)
    tree.heading("count", text="Payment Count")
    tree.heading("total", text="Total Payment Amount")
    tree.column("count", width=150, anchor="center")
    tree.column("total", width=200, anchor="center")
    tree.pack(fill="both", expand=True)

    def run_analysis() -> None:
        """Collect filters and run the analytics query."""
        
        filters = {}

        if year_entry.get().strip():
            filters["year"] = year_entry.get().strip()
        if month_entry.get().strip():
            filters["month"] = month_entry.get().strip()
        if day_entry.get().strip():
            filters["day"] = day_entry.get().strip()

        vendor_code_selection = vendor_code_dropdown.get().strip()
        if vendor_code_selection and vendor_code_selection != "None":
            filters["vendor_code"] = vendor_code_selection.split(" - ", 1)[0]

        vendor_name_selection = vendor_name_dropdown.get().strip()
        if vendor_name_selection and vendor_name_selection != "None":
            filters["vendor_id"] = vendor_name_selection.split(" - ", 1)[0]

        try:
            summary = get_payment_summary(filters)
            tree.delete(*tree.get_children())
            tree.insert(
                "",
                "end",
                values=(
                    summary.get("payment_count", 0),
                    f"{summary.get('total_payment', 0.0):.2f}",
                ),
            )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frame, text="Run Analysis", width=15, command=run_analysis).pack(pady=(10, 0))

    root.mainloop()
