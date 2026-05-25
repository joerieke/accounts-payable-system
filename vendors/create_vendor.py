"""Vendor creation logic for the Accounts Payable System."""

from __future__ import annotations

import sqlite3

from database.db_init import get_connection
from utils.id_generator import generate_vendor_id
from utils.verification_popup import verification_popup


def create_vendor(
    vendor_code: str,
    vendor_name: str,
    vendor_address: str,
    vendor_phone: str,
    vendor_email: str,
) -> str | None:
    """Create a vendor record after validation and user confirmation."""
    if not vendor_name or not vendor_name.strip():
        raise ValueError("vendor_name is required")

    vendor_id = generate_vendor_id(vendor_code)

    message = (
        "Please confirm the vendor details:\n\n"
        f"Vendor ID: {vendor_id}\n"
        f"Vendor Code: {vendor_code}\n"
        f"Vendor Name: {vendor_name}\n"
        f"Vendor Address: {vendor_address}\n"
        f"Vendor Phone: {vendor_phone}\n"
        f"Vendor Email: {vendor_email}"
    )

    confirmed = verification_popup("Confirm Vendor Creation", message)
    if not confirmed:
        return None

    connection = get_connection()
    try:
        connection.execute(
            """
            INSERT INTO vendors (
                vendor_id,
                vendor_code,
                vendor_name,
                vendor_address,
                vendor_phone,
                vendor_email
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                vendor_id,
                vendor_code,
                vendor_name,
                vendor_address,
                vendor_phone,
                vendor_email,
            ),
        )
        connection.commit()
        return vendor_id
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to create vendor: {exc}") from exc
    finally:
        connection.close()
