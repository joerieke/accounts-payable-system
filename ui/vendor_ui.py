"""Tkinter vendor management UI for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.db_init import get_connection
from vendors.create_vendor import create_vendor
from vendors.edit_vendor import edit_vendor, get_vendor
from utils.verification_popup import verification_popup


def _fetch_vendor_codes() -> list[tuple[str, str]]:
    """Return a list of (vendor_code, vendor_description)."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT vendor_code, vendor_description FROM vendor_codes ORDER BY vendor_code"
        )
        return cursor.fetchall()
    finally:
        connection.close()


def open_vendor_ui() -> None:
    """Open the Vendor Management window."""
    root = tk.Tk()
    root.title("Vendor Management")
    root.geometry("450x400")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Vendor Management", font=("Arial", 14, "bold")).pack(pady=(0, 12))

    tk.Button(frame, text="New Vendor", width=25, command=lambda: create_vendor_form(root)).pack(pady=6)
    tk.Button(frame, text="Edit Vendor", width=25, command=lambda: edit_vendor_form(root)).pack(pady=6)
    tk.Button(frame, text="Return to Main Menu", width=25, command=root.destroy).pack(pady=(18, 0))

    root.mainloop()


def create_vendor_form(parent: tk.Tk) -> None:
    """Display the vendor creation form."""
    window = tk.Toplevel(parent)
    window.title("New Vendor")
    window.geometry("450x400")
    window.resizable(False, False)

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Vendor Type").grid(row=0, column=0, sticky="w", pady=6)

    codes = _fetch_vendor_codes()
    display_codes = [f"{code} - {desc}" for code, desc in codes]

    vendor_dropdown = ttk.Combobox(frame, values=display_codes, state="readonly")
    vendor_dropdown.grid(row=0, column=1, sticky="ew", pady=6)

    if display_codes:
        vendor_dropdown.current(0)
    
    tk.Label(frame, text="Vendor Name").grid(row=1, column=0, sticky="w", pady=6)
    name_entry = tk.Entry(frame, width=30)
    name_entry.grid(row=1, column=1, pady=6)

    tk.Label(frame, text="Vendor Address").grid(row=2, column=0, sticky="w", pady=6)
    address_entry = tk.Entry(frame, width=30)
    address_entry.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Vendor Phone").grid(row=3, column=0, sticky="w", pady=6)
    phone_entry = tk.Entry(frame, width=30)
    phone_entry.grid(row=3, column=1, pady=6)

    tk.Label(frame, text="Vendor Email").grid(row=4, column=0, sticky="w", pady=6)
    email_entry = tk.Entry(frame, width=30)
    email_entry.grid(row=4, column=1, pady=6)

    def on_save() -> None:
        try:
            if not vendor_dropdown.get():
                messagebox.showerror("Error", "Vendor type is required.")
                return

            vendor_code = vendor_dropdown.get().split(" - ", 1)[0]

            # Confirmation popup
            if not verification_popup("Confirm Vendor", "Save this vendor?"):
                return

            vendor_id = create_vendor(
                vendor_code=vendor_code,
                vendor_name=name_entry.get(),
                vendor_address=address_entry.get(),
                vendor_phone=phone_entry.get(),
                vendor_email=email_entry.get(),
            )

            if vendor_id:
                messagebox.showinfo("Success", f"Vendor created: {vendor_id}")
                window.destroy()

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frame, text="Save", width=12, command=on_save).grid(row=5, column=0, pady=16)
    tk.Button(frame, text="Cancel", width=12, command=window.destroy).grid(row=5, column=1, pady=16)

    name_entry.focus_set()


def edit_vendor_form(parent: tk.Tk) -> None:
    """Display the vendor editing form."""
    window = tk.Toplevel(parent)
    window.title("Edit Vendor")
    window.geometry("450x420")
    window.resizable(False, False)

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Vendor ID").grid(row=0, column=0, sticky="w", pady=6)
    vendor_id_entry = tk.Entry(frame, width=30)
    vendor_id_entry.grid(row=0, column=1, pady=6)

    tk.Label(frame, text="Vendor Code").grid(row=1, column=0, sticky="w", pady=6)
    vendor_code_var = tk.StringVar(value="")
    tk.Label(frame, textvariable=vendor_code_var).grid(row=1, column=1, sticky="w", pady=6)

    tk.Label(frame, text="Vendor Name").grid(row=2, column=0, sticky="w", pady=6)
    name_entry = tk.Entry(frame, width=30)
    name_entry.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Vendor Address").grid(row=3, column=0, sticky="w", pady=6)
    address_entry = tk.Entry(frame, width=30)
    address_entry.grid(row=3, column=1, pady=6)

    tk.Label(frame, text="Vendor Phone").grid(row=4, column=0, sticky="w", pady=6)
    phone_entry = tk.Entry(frame, width=30)
    phone_entry.grid(row=4, column=1, pady=6)

    tk.Label(frame, text="Vendor Email").grid(row=5, column=0, sticky="w", pady=6)
    email_entry = tk.Entry(frame, width=30)
    email_entry.grid(row=5, column=1, pady=6)

    def on_load() -> None:
        try:
            vendor_id = vendor_id_entry.get().strip()
            if not vendor_id:
                messagebox.showerror("Error", "Vendor ID is required.")
                return

            record = get_vendor(vendor_id)
            if not record:
                messagebox.showerror("Error", "Vendor not found.")
                return

            vendor_code_var.set(record["vendor_code"])
            name_entry.delete(0, tk.END)
            name_entry.insert(0, record["vendor_name"] or "")
            address_entry.delete(0, tk.END)
            address_entry.insert(0, record["vendor_address"] or "")
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, record["vendor_phone"] or "")
            email_entry.delete(0, tk.END)
            email_entry.insert(0, record["vendor_email"] or "")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_save() -> None:
        try:
            vendor_id = vendor_id_entry.get().strip()
            if not vendor_id:
                messagebox.showerror("Error", "Vendor ID is required.")
                return

            updated = edit_vendor(
                vendor_id=vendor_id,
                vendor_name=name_entry.get(),
                vendor_address=address_entry.get(),
                vendor_phone=phone_entry.get(),
                vendor_email=email_entry.get(),
            )
            if updated:
                messagebox.showinfo("Success", "Vendor updated.")
                window.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frame, text="Load", width=12, command=on_load).grid(row=0, column=2, padx=(8, 0))
    tk.Button(frame, text="Save", width=12, command=on_save).grid(row=6, column=0, pady=16)
    tk.Button(frame, text="Cancel", width=12, command=window.destroy).grid(row=6, column=1, pady=16)

    vendor_id_entry.focus_set()

def open_vendor_edit_ui(parent: tk.Tk) -> None:
    """
    Wrapper function used by main_menu_ui to open the vendor edit form.
    """
    edit_vendor_form(parent)
