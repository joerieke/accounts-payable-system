"""Tkinter invoice management UI for the Accounts Payable System."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from database.db_init import get_connection
from invoices.payment_create_invoice import create_invoice
from invoices.payment_edit_invoice import edit_invoice, get_invoice


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


def _fetch_vendors_by_code(vendor_code: str) -> list[tuple[str, str]]:
    """Return a list of (vendor_id, vendor_name) for a vendor_code."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT vendor_id, vendor_name
            FROM vendors
            WHERE vendor_code = ?
            ORDER BY vendor_name
            """,
            (vendor_code,),
        )
        return cursor.fetchall()
    finally:
        connection.close()


def open_invoice_ui() -> None:
    """Open the Invoice Management window."""
    root = tk.Tk()
    root.title("Invoice Management")
    root.geometry("500x420")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Invoice Management", font=("Arial", 14, "bold")).pack(pady=(0, 12))

    tk.Button(frame, text="Payment Entry", width=25, command=lambda: create_invoice_form(root)).pack(pady=6)
    tk.Button(frame, text="Edit Invoice", width=25, command=lambda: edit_invoice_form(root)).pack(pady=6)
    tk.Button(frame, text="Return to Main Menu", width=25, command=root.destroy).pack(pady=(18, 0))

    root.mainloop()


def create_invoice_form(parent: tk.Tk) -> None:
    """Display the invoice creation form."""
    window = tk.Toplevel(parent)
    window.title("Payment Entry")
    window.geometry("500x420")
    window.resizable(False, False)

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Vendor Type").grid(row=0, column=0, sticky="w", pady=6)
    vendor_code_var = tk.StringVar()
    vendor_code_dropdown = ttk.Combobox(
        frame,
        textvariable=vendor_code_var,
        state="readonly",
        width=28
    )
    vendor_code_dropdown.grid(row=0, column=1, pady=6)
        
    tk.Label(frame, text="Vendor Name").grid(row=1, column=0, sticky="w", pady=6)
    vendor_name_var = tk.StringVar()
    vendor_name_dropdown = ttk.Combobox(frame, textvariable=vendor_name_var, state="readonly", width=28)
    vendor_name_dropdown.grid(row=1, column=1, pady=6)

    tk.Label(frame, text="Vendor Invoice Number").grid(row=2, column=0, sticky="w", pady=6)
    invoice_number_entry = tk.Entry(frame, width=30)
    invoice_number_entry.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Payment Amount").grid(row=3, column=0, sticky="w", pady=6)
    payment_amount_entry = tk.Entry(frame, width=30)
    payment_amount_entry.grid(row=3, column=1, pady=6)

    tk.Label(frame, text="Payment Date").grid(row=4, column=0, sticky="w", pady=6)
    payment_date_entry = tk.Entry(frame, width=30, fg="grey")
    payment_date_entry.insert(0, "DD/MM/YYYY")
    payment_date_entry.grid(row=4, column=1, pady=6)

    def clear_date_placeholder(event):
        if payment_date_entry.get() == "DD/MM/YYYY":
            payment_date_entry.delete(0, tk.END)
            payment_date_entry.config(fg="black")

    def restore_date_placeholder(event):
        if payment_date_entry.get() == "":
            payment_date_entry.insert(0, "DD/MM/YYYY")
            payment_date_entry.config(fg="grey")


    payment_date_entry.bind("<FocusIn>", clear_date_placeholder)
    payment_date_entry.bind("<FocusOut>", restore_date_placeholder)

    tk.Label(frame, text="Notes").grid(row=5, column=0, sticky="w", pady=6)
    notes_entry = tk.Entry(frame, width=30)
    notes_entry.grid(row=5, column=1, pady=6)

    vendor_codes = _fetch_vendor_codes()
    vendor_code_values = [f"{code} - {desc}" for code, desc in vendor_codes]

    vendor_code_dropdown["values"] = vendor_code_values

    if vendor_code_values:
        vendor_code_dropdown.current(0)
        vendor_code_var.set(vendor_code_values[0])


    def refresh_vendor_names(*_args: object) -> None:
        selected = vendor_code_dropdown.get().split(" - ")[0] if vendor_code_dropdown.get() else ""
        vendors = _fetch_vendors_by_code(selected) if selected else []

        vendor_name_dropdown["values"] = [f"{vid} - {name}" for vid, name in vendors]

        if vendors:
            vendor_name_dropdown.current(0)
        else:
            vendor_name_var.set("")


    vendor_code_dropdown.bind("<<ComboboxSelected>>", refresh_vendor_names)

    refresh_vendor_names()

    def on_save() -> None:
        try:
            vendor_selection = vendor_name_dropdown.get()
            if not vendor_selection:
                messagebox.showerror("Error", "Vendor is required.")
                return

            vendor_id = vendor_selection.split(" - ", 1)[0]
            payment_amount_text = payment_amount_entry.get().strip()
            if not payment_amount_text:
                messagebox.showerror("Error", "Payment amount is required.")
                return

            try:
                payment_amount = float(payment_amount_text)
            except ValueError:
                messagebox.showerror("Error", "Payment amount must be a number.")
                return

            invoice_id = create_invoice(
                vendor_id=vendor_id,
                vendor_invoice_number=invoice_number_entry.get(),
                payment_amount=payment_amount,
                vendor_payment_date=payment_date_entry.get(),
                notes=notes_entry.get(),
            )
            if invoice_id:
                messagebox.showinfo("Success", f"Invoice created: {invoice_id}")
                window.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frame, text="Save", width=12, command=on_save).grid(row=6, column=0, pady=16)
    tk.Button(frame, text="Cancel", width=12, command=window.destroy).grid(row=6, column=1, pady=16)

    vendor_code_dropdown.focus_set()


def edit_invoice_form(parent: tk.Tk) -> None:
    """Display the invoice editing form."""
    window = tk.Toplevel(parent)
    window.title("Edit Invoice")
    window.geometry("500x420")
    window.resizable(False, False)

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Invoice ID").grid(row=0, column=0, sticky="w", pady=6)
    invoice_id_entry = tk.Entry(frame, width=30)
    invoice_id_entry.grid(row=0, column=1, pady=6)

    tk.Label(frame, text="Vendor Invoice Number").grid(row=1, column=0, sticky="w", pady=6)
    invoice_number_entry = tk.Entry(frame, width=30)
    invoice_number_entry.grid(row=1, column=1, pady=6)

    tk.Label(frame, text="Payment Amount").grid(row=2, column=0, sticky="w", pady=6)
    payment_amount_entry = tk.Entry(frame, width=30)
    payment_amount_entry.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Payment Date").grid(row=3, column=0, sticky="w", pady=6)
    payment_date_entry = tk.Entry(frame, width=30)
    payment_date_entry.grid(row=3, column=1, pady=6)

    tk.Label(frame, text="Notes").grid(row=4, column=0, sticky="w", pady=6)
    notes_entry = tk.Entry(frame, width=30)
    notes_entry.grid(row=4, column=1, pady=6)

    def on_load() -> None:
        try:
            invoice_id = invoice_id_entry.get().strip()
            if not invoice_id:
                messagebox.showerror("Error", "Invoice ID is required.")
                return

            record = get_invoice(invoice_id)
            if not record:
                messagebox.showerror("Error", "Invoice not found.")
                return

            invoice_number_entry.delete(0, tk.END)
            invoice_number_entry.insert(0, record["vendor_invoice_number"] or "")
            payment_amount_entry.delete(0, tk.END)
            payment_amount_entry.insert(0, str(record["payment_amount"] or ""))
            payment_date_entry.delete(0, tk.END)
            payment_date_entry.insert(0, record["vendor_payment_date"] or "")
            notes_entry.delete(0, tk.END)
            notes_entry.insert(0, record["notes"] or "")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_save() -> None:
        try:
            invoice_id = invoice_id_entry.get().strip()
            if not invoice_id:
                messagebox.showerror("Error", "Invoice ID is required.")
                return

            payment_amount_text = payment_amount_entry.get().strip()
            try:
                payment_amount = float(payment_amount_text) if payment_amount_text else 0.0
            except ValueError:
                messagebox.showerror("Error", "Payment amount must be a number.")
                return

            updated = edit_invoice(
                invoice_id=invoice_id,
                vendor_invoice_number=invoice_number_entry.get(),
                payment_amount=payment_amount,
                vendor_payment_date=payment_date_entry.get(),
                notes=notes_entry.get(),
            )
            if updated:
                messagebox.showinfo("Success", "Invoice updated.")
                window.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(frame, text="Load", width=12, command=on_load).grid(row=0, column=2, padx=(8, 0))
    tk.Button(frame, text="Save", width=12, command=on_save).grid(row=5, column=0, pady=16)
    tk.Button(frame, text="Cancel", width=12, command=window.destroy).grid(row=5, column=1, pady=16)

    invoice_id_entry.focus_set()

def open_invoice_edit_ui(parent: tk.Tk):
    """
    Wrapper used by main_menu_ui to open the invoice edit form.
    """
    edit_invoice_form(parent)
