"""Invoice creation logic for the Accounts Payable System."""

from __future__ import annotations

import sqlite3

from database.db_init import get_connection
from utils.id_generator import generate_invoice_id
from utils.verification_popup import verification_popup


def _vendor_exists(connection: sqlite3.Connection, vendor_id: str) -> bool:
    """Return True if the vendor exists."""
    cursor = connection.execute(
        "SELECT 1 FROM vendors WHERE vendor_id = ? LIMIT 1",
        (vendor_id,),
    )
    return cursor.fetchone() is not None


def create_invoice(
    vendor_id: str,
    vendor_invoice_number: str,
    payment_amount: float,
    vendor_payment_date: str,
    notes: str,
) -> str | None:
    """Create an invoice record after validation and user confirmation."""
    if not vendor_id:
        raise ValueError("vendor_id is required")

    normalized_invoice_number = (
        vendor_invoice_number.strip() if vendor_invoice_number else ""
    )
    if not normalized_invoice_number:
        normalized_invoice_number = "N/A"

    try:
        payment_amount = float(payment_amount)
    except ValueError:
        raise ValueError("Payment amount must be a valid number.")
    if payment_amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")
    # Validate payment date format (DD/MM/YYYY)

    try:
        parts = vendor_payment_date.split("/")

        if len(parts) != 3:
            raise ValueError

        day, month, year = parts

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            raise ValueError

        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            raise ValueError

        day_int = int(day)
        month_int = int(month)

        if not (1 <= day_int <= 31):
            raise ValueError

        if not (1 <= month_int <= 12):
            raise ValueError

    except Exception:
        raise ValueError("Payment date must be in DD/MM/YYYY format.")

    invoice_id = generate_invoice_id()

    message = (
        "Please confirm the invoice details:\n\n"
        f"Invoice ID: {invoice_id}\n"
        f"Vendor ID: {vendor_id}\n"
        f"Vendor Invoice Number: {normalized_invoice_number}\n"
        f"Payment Amount: {payment_amount}\n"
        f"Payment Date: {vendor_payment_date}\n"
        f"Notes: {notes}"
    )

    confirmed = verification_popup("Confirm Action", message)
    if not confirmed:
        return None

    connection = get_connection()
    try:
        if not _vendor_exists(connection, vendor_id):
            raise ValueError(f"Vendor not found: {vendor_id}")

        connection.execute(
            """
            INSERT INTO vendor_invoices (
                invoice_id,
                vendor_id,
                vendor_invoice_number,
                payment_amount,
                vendor_payment_date,
                notes
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                invoice_id,
                vendor_id,
                normalized_invoice_number,
                payment_amount,
                vendor_payment_date,
                notes,
            ),
        )
        connection.commit()
        return invoice_id
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to create invoice: {exc}") from exc
    finally:
        connection.close()
