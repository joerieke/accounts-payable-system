"""Database initialization utilities for the Accounts Payable System."""

from __future__ import annotations

import os
from typing import Iterable, Sequence, Tuple

from database.schema import create_tables, enable_foreign_keys

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILENAME = BASE_DIR / "ap_system.db"


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection to the application database."""
    try:
        connection = sqlite3.connect(DB_FILENAME)
        enable_foreign_keys(connection)
        return connection
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to connect to database: {exc}") from exc

def initialize_database() -> None:
    """Create the database and tables if needed, then seed vendor codes."""
    db_exists = os.path.exists(DB_FILENAME)

    connection = get_connection()
    try:
        if not db_exists:
            create_tables(connection)
        seed_vendor_codes(connection)
        connection.commit()
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to initialize database: {exc}") from exc
    finally:
        connection.close()


def seed_vendor_codes(connection: sqlite3.Connection) -> None:
    """Insert default vendor codes if the vendor_codes table is empty."""
    default_codes: Sequence[Tuple[str, str]] = (
        ("LL", "Legal Services"),
        ("HW", "Hardware"),
        ("SW", "Software"),
        ("CL", "Consulting"),
        ("MK", "Marketing"),
        ("MT", "Municiple/Taxes"),
        ("SU", "Subscriptions"),
        ("RE", "Real Estate"),
        ("GE", "General"),
    )

    try:
        cursor = connection.execute("SELECT COUNT(*) FROM vendor_codes")
        row = cursor.fetchone()
        if row is None or row[0] == 0:
            connection.executemany(
                "INSERT INTO vendor_codes (vendor_code, vendor_description) VALUES (?, ?)",
                default_codes,
            )
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to seed vendor codes: {exc}") from exc
