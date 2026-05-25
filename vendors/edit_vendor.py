
"""Vendor editing logic for the Accounts Payable System."""

from __future__ import annotations

import sqlite3
from typing import Dict, Optional

from database.db_init import get_connection
from utils.verification_popup import verification_popup


def get_vendor(vendor_id: str) -> Optional[Dict[str, str]]:
    """Retrieve a vendor record by vendor_id."""
    if not vendor_id:
        raise ValueError("vendor_id is required")

    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT vendor_id, vendor_code, vendor_name, vendor_address, vendor_phone, vendor_email
            FROM vendors
            WHERE vendor_id = ?
            """,
            (vendor_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "vendor_id": row[0],
            "vendor_code": row[1],
            "vendor_name": row[2],
            "vendor_address": row[3],
            "vendor_phone": row[4],
            "vendor_email": row[5],
        }
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to retrieve vendor: {exc}") from exc
    finally:
        connection.close()


def edit_vendor(
    vendor_id: str,
    vendor_name: str,
    vendor_address: str,
    vendor_phone: str,
    vendor_email: str,
) -> bool:
    """Edit an existing vendor record after user confirmation."""
    if not vendor_id:
        raise ValueError("vendor_id is required")

    existing = get_vendor(vendor_id)
    if not existing:
        raise ValueError(f"Vendor not found: {vendor_id}")

    message = (
        "Please confirm the updated vendor details:\n\n"
        f"Vendor ID: {vendor_id}\n"
        f"Vendor Name: {vendor_name}\n"
        f"Vendor Address: {vendor_address}\n"
        f"Vendor Phone: {vendor_phone}\n"
        f"Vendor Email: {vendor_email}"
    )

    confirmed = verification_popup("Confirm Action", message)
    if not confirmed:
        return False

    connection = get_connection()
    try:
        connection.execute(
            """
            UPDATE vendors
            SET vendor_name = ?, vendor_address = ?, vendor_phone = ?, vendor_email = ?
            WHERE vendor_id = ?
            """,
            (vendor_name, vendor_address, vendor_phone, vendor_email, vendor_id),
        )
        connection.commit()
        return True
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to update vendor: {exc}") from exc
    finally:
        connection.close()

