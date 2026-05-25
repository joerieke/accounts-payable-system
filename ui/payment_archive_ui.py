
"""
Invoice Archive System UI
Archives invoices by month or year into yearly archive databases.
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


MAIN_DB = "ap_system.db"
ARCHIVE_FOLDER = "archive_databases"


def get_archive_db(year):
    """Return archive database path."""
    if not os.path.exists(ARCHIVE_FOLDER):
        os.makedirs(ARCHIVE_FOLDER)

    return os.path.join(ARCHIVE_FOLDER, f"archive_{year}.db")


def create_archive_table(conn):
    """Ensure vendor_invoices table exists in archive DB."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vendor_invoices (
            invoice_id TEXT,
            vendor_id TEXT,
            vendor_invoice_number TEXT,
            invoice_date TEXT,
            invoice_amount REAL,
            invoice_description TEXT
        )
        """
    )

    conn.commit()

def fetch_records(month, year):
    """Fetch records to archive."""
    conn = sqlite3.connect(MAIN_DB)
    cursor = conn.cursor()

    if month:
        cursor.execute(
            """
            SELECT * FROM vendor_invoices
            WHERE substr(vendor_payment_date,4,2)=?
            AND substr(vendor_payment_date,7,4)=?
            """,
            (month, year),
        )
    else:
        cursor.execute(
            """
            SELECT * FROM vendor_invoices
            WHERE substr(vendor_payment_date,7,4)=?
            """,
            (year,),
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_records(month, year):
    """Delete archived records from main DB."""
    conn = sqlite3.connect(MAIN_DB)
    cursor = conn.cursor()
    
    if month:
        cursor.execute(
            """
            DELETE FROM vendor_invoices
            WHERE substr(vendor_payment_date,4,2)=?
            AND substr(vendor_payment_date,7,4)=?
            """,
            (month, year),
        )
    else:
        cursor.execute(
            """
            DELETE FROM vendor_invoices
            WHERE substr(vendor_payment_date,7,4)=?
            """,
            (year,),
        )

    conn.commit()
    conn.close()


def archive_records(month, year):
    """Archive selected records."""
    rows = fetch_records(month, year)

    if not rows:
        messagebox.showinfo("Archive Result", "No records found for selected period.")
        return

    archive_db = get_archive_db(year)

    archive_conn = sqlite3.connect(archive_db)
    create_archive_table(archive_conn)

    cursor = archive_conn.cursor()

    cursor.executemany(
        """
        INSERT INTO vendor_invoices
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    archive_conn.commit()
    archive_conn.close()

    delete_records(month, year)

    messagebox.showinfo(
        "Archive Complete",
        f"{len(rows)} invoices archived to archive_{year}.db",
    )


def open_archive_ui():
    """Launch the archive interface."""

    window = tk.Toplevel()
    window.title("Invoice Archive System")
    window.geometry("350x300")

    frame = tk.Frame(window, padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Archive Invoices", font=("Arial", 14, "bold")).pack(pady=10)

    # Month
    tk.Label(frame, text="Month (MM)").pack()
    month_entry = tk.Entry(frame)
    month_entry.pack(pady=4)

    # Year
    tk.Label(frame, text="Year (YYYY)").pack()
    year_entry = tk.Entry(frame)
    year_entry.pack(pady=4)

    def run_archive():

        month = month_entry.get().strip()
        year = year_entry.get().strip()

        if month and not year:
            messagebox.showerror("Input Error", "Year is required when month is specified.")
            return

        if not year:
            messagebox.showerror("Input Error", "Year must be provided.")
            return

        confirm = messagebox.askyesno(
            "Confirm Archive",
            f"Archive records for {month+'/'+year if month else year}?"
        )

        if confirm:
            archive_records(month if month else None, year)

    tk.Button(frame, text="Run Archive", width=18, command=run_archive).pack(pady=12)

    tk.Button(frame, text="Close", width=18, command=window.destroy).pack()
