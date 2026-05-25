
"""ID generation utilities for the Accounts Payable System."""

from __future__ import annotations

import sqlite3

from database.db_init import get_connection


def _next_sequence_from_id(last_id: str | None, prefix_len: int) -> int:
    """Return the next integer sequence given the last ID value."""
    if not last_id or len(last_id) <= prefix_len:
        return 1
    try:
        return int(last_id[prefix_len:]) + 1
    except ValueError:
        return 1


def generate_vendor_id(vendor_code: str) -> str:
    """Generate the next vendor ID for the given vendor_code."""
    if not vendor_code:
        raise ValueError("vendor_code is required")

    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT vendor_id
            FROM vendors
            WHERE vendor_code = ?
            ORDER BY vendor_id DESC
            LIMIT 1
            """,
            (vendor_code,),
        )
        row = cursor.fetchone()
        last_id = row[0] if row else None
        next_seq = _next_sequence_from_id(last_id, len(vendor_code))
        return f"{vendor_code}{next_seq:03d}"
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to generate vendor ID: {exc}") from exc
    finally:
        connection.close()


def generate_invoice_id() -> str:
    """Generate the next invoice ID for the system."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT invoice_id
            FROM vendor_invoices
            ORDER BY invoice_id DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        last_id = row[0] if row else None
        next_seq = _next_sequence_from_id(last_id, 2)
        return f"ST{next_seq:05d}"
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to generate invoice ID: {exc}") from exc
    finally:
        connection.close()
