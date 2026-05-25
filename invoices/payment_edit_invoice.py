
"""Invoice editing logic for the Accounts Payable System."""

from __future__ import annotations

import sqlite3
from typing import Dict, Optional

from database.db_init import get_connection
from utils.verification_popup import verification_popup


def get_invoice(invoice_id: str) -> Optional[Dict[str, str]]:
    """Retrieve an invoice record by invoice_id."""
    if not invoice_id:
        raise ValueError("invoice_id is required")

    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT invoice_id, vendor_id, vendor_invoice_number, payment_amount,
                   vendor_payment_date, notes
            FROM vendor_invoices
            WHERE invoice_id = ?
            """,
            (invoice_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "invoice_id": row[0],
            "vendor_id": row[1],
            "vendor_invoice_number": row[2],
            "payment_amount": row[3],
            "vendor_payment_date": row[4],
            "notes": row[5],
        }
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to retrieve invoice: {exc}") from exc
    finally:
        connection.close()


def edit_invoice(
    invoice_id: str,
    vendor_invoice_number: str,
    payment_amount: float,
    vendor_payment_date: str,
    notes: str,
) -> bool:
    """Edit an existing invoice record after user confirmation."""
    if not invoice_id:
        raise ValueError("invoice_id is required")

    existing = get_invoice(invoice_id)
    if not existing:
        raise ValueError(f"Invoice not found: {invoice_id}")

    normalized_invoice_number = (
        vendor_invoice_number.strip() if vendor_invoice_number else ""
    )
    if not normalized_invoice_number:
        normalized_invoice_number = "N/A"

    message = (
        "Please confirm the updated invoice details:\n\n"
        f"Invoice ID: {invoice_id}\n"
        f"Vendor Invoice Number: {normalized_invoice_number}\n"
        f"Payment Amount: {payment_amount}\n"
        f"Payment Date: {vendor_payment_date}\n"
        f"Notes: {notes}"
    )

    confirmed = verification_popup("Confirm Action", message)
    if not confirmed:
        return False

    connection = get_connection()
    try:
        connection.execute(
            """
            UPDATE vendor_invoices
            SET vendor_invoice_number = ?, payment_amount = ?, vendor_payment_date = ?, notes = ?
            WHERE invoice_id = ?
            """,
            (
                normalized_invoice_number,
                payment_amount,
                vendor_payment_date,
                notes,
                invoice_id,
            ),
        )
        connection.commit()
        return True
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to update invoice: {exc}") from exc
    finally:
        connection.close()

