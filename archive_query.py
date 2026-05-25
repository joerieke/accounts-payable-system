
"""
Archive Database Verification Script
Checks if archive database exists and prints archived invoices.
"""

import sqlite3
import os

ARCHIVE_DB = "archive_databases/archive_2026.db"


def verify_archive():

    # Check if archive database exists
    if not os.path.exists(ARCHIVE_DB):
        print("Archive database not found:", ARCHIVE_DB)
        return

    print("Archive database found:", ARCHIVE_DB)

    conn = sqlite3.connect(ARCHIVE_DB)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\nTables in archive database:")
    for table in tables:
        print("-", table[0])

    # Query archived invoices
    print("\nArchived invoice records:\n")

    cursor.execute("SELECT * FROM vendor_invoices")
    rows = cursor.fetchall()

    if not rows:
        print("No records found.")
    else:
        for row in rows:
            print(row)

    conn.close()


if __name__ == "__main__":
    verify_archive()
