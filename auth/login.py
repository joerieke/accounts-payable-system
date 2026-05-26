"""Authentication logic for the Accounts Payable System."""

from __future__ import annotations

import hashlib
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def hash_password(password: str) -> str:
    """Return the SHA-256 hash of the provided plaintext password."""
    if password is None:
        raise ValueError("password is required")

    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as exc:
        raise ValueError(f"Failed to hash password: {exc}") from exc


# Load credentials from environment variables
VALID_USERNAME = os.getenv("APP_USERNAME")
VALID_PASSWORD_HASH = os.getenv("APP_PASSWORD_HASH")


def authenticate_user(username: str, password: str) -> bool:
    """Validate username and password against stored credentials."""
    if not username or password is None:
        return False

    if username != VALID_USERNAME:
        return False

    try:
        return hash_password(password) == VALID_PASSWORD_HASH
    except ValueError:
        return False
