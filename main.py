"""Application entry point for the Accounts Payable System."""

from __future__ import annotations

from database.db_init import initialize_database, seed_vendor_codes, get_connection
from ui.login_ui import create_login_window

def main() -> None:
    """Initialize the database and launch the login UI."""
    try:
        initialize_database()
        with_db = True
    except Exception as exc:
        print("Application failed to start:", exc)
        with_db = False

    if with_db:
        try:
            seed_vendor_codes(get_connection())
        except Exception as exc:
            print("Application failed to seed vendor codes:", exc)
            return

        create_login_window()


if __name__ == "__main__":
    from database.db_init import get_connection

    main()
