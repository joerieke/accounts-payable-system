"""Authentication logic for the Accounts Payable System."""

from __future__ import annotations
import os
import hashlib

VALID_USERNAME = "admin"
VALID_PASSWORD_HASH = hash_password("admin123")

def hash_password(password: str) -> str:
    """Return the SHA-256 hash of the provided plaintext password."""
    if password is None:
        raise ValueError("password is required")
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as exc:
        raise ValueError(f"Failed to hash password: {exc}") from exc


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
