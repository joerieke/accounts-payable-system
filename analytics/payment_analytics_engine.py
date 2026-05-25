"""Analytics and reporting logic for the Accounts Payable System."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Tuple

from database.db_init import get_connection


def _build_filters(filters: Dict[str, Any]) -> Tuple[str, List[Any], bool]:
    """Build SQL filter clauses and parameters based on provided filters."""
    clauses: List[str] = []
    params: List[Any] = []
    join_vendors = False

    if not filters:
        return "", params, join_vendors

    if filters.get("year") is not None:
        clauses.append("substr(vendor_invoices.vendor_payment_date, 7, 4) = ?")
        params.append(str(filters["year"]))

    if filters.get("month") is not None:
        clauses.append("substr(vendor_invoices.vendor_payment_date, 4, 2) = ?")
        params.append(f"{int(filters['month']):02d}")

    if filters.get("day") is not None:
        clauses.append("substr(vendor_invoices.vendor_payment_date, 1, 2) = ?")
        params.append(f"{int(filters['day']):02d}")

    if filters.get("vendor_id"):
        clauses.append("vendor_invoices.vendor_id = ?")
        params.append(filters["vendor_id"])

    if filters.get("vendor_code"):
        join_vendors = True
        clauses.append("vendors.vendor_code = ?")
        params.append(filters["vendor_code"])

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return where_sql, params, join_vendors


def get_payment_summary(filters: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return a payment summary based on optional filters."""
    where_sql, params, join_vendors = _build_filters(filters or {})

    join_sql = (
        "JOIN vendors ON vendor_invoices.vendor_id = vendors.vendor_id"
        if join_vendors
        else ""
    )

    query = f"""
        SELECT
            COUNT(vendor_invoices.invoice_id) AS payment_count,
            COALESCE(SUM(vendor_invoices.payment_amount), 0) AS total_payment
        FROM vendor_invoices
        {join_sql}
        {where_sql}
    """

    connection = get_connection()
    try:
        cursor = connection.execute(query, params)
        row = cursor.fetchone()
        return {
            "payment_count": row[0] if row else 0,
            "total_payment": row[1] if row else 0.0,
        }
    except sqlite3.Error as exc:
        raise sqlite3.Error(f"Failed to retrieve payment summary: {exc}") from exc
    finally:
        connection.close()
