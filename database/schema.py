"""Database schema definitions for the Accounts Payable System."""

from __future__ import annotations

import sqlite3
from typing import Sequence

DB_FILENAME = "ap_system.db"


def get_schema_statements() -> Sequence[str]:
    """Return the SQL statements needed to create all schema objects."""
    return (
        """
        CREATE TABLE IF NOT EXISTS vendor_codes (
            vendor_code TEXT PRIMARY KEY,
            vendor_description TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id TEXT PRIMARY KEY,
            vendor_code TEXT NOT NULL,
            vendor_name TEXT,
            vendor_address TEXT,
            vendor_phone TEXT,
            vendor_email TEXT,
            FOREIGN KEY (vendor_code)
                REFERENCES vendor_codes (vendor_code)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vendor_invoices (
            invoice_id TEXT PRIMARY KEY,
            vendor_id TEXT NOT NULL,
            vendor_invoice_number TEXT,
            payment_amount REAL,
            vendor_payment_date TEXT,
            notes TEXT,
            FOREIGN KEY (vendor_id)
                REFERENCES vendors (vendor_id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        )
        """,
    )


def enable_foreign_keys(connection: sqlite3.Connection) -> None:
    """Enable SQLite foreign key enforcement for the given connection."""
    try:
        connection.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to enable foreign keys: {exc}") from exc


def create_tables(connection: sqlite3.Connection) -> None:
    """Create all tables if they do not already exist."""
    try:
        enable_foreign_keys(connection)
        for statement in get_schema_statements():
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as exc:
        connection.rollback()
        raise sqlite3.Error(f"Failed to create schema: {exc}") from exc


def initialize_schema(connection: sqlite3.Connection) -> None:
    """Public helper to initialize the database schema."""
    create_tables(connection)
