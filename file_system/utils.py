"""Hashing, validation, and file I/O using Argon2."""

from pathlib import Path
from argon2 import PasswordHasher, exceptions as argon2_exceptions

# Create a single PasswordHasher instance to reuse
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4, hash_len=32)


def account_exists(username: str) -> bool:
    """Check if the username already exists in shadow.txt."""
    shadow_file = Path("shadow.txt")

    if not shadow_file.exists():
        return False

    with shadow_file.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            if line.split(":", 1)[0] == username:
                return True
    return False


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2 and return the encoded string.
    Argon2 generates and embeds its own random salt.
    """
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    return ph.hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a plaintext password against an Argon2 encoded hash."""
    if not stored_hash:
        return False
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    try:
        return ph.verify(stored_hash, password)
    except (argon2_exceptions.VerifyMismatchError, argon2_exceptions.InvalidHash):
        return False


def write_shadow(username, hashed_password, mfa_secret=None):
    """Write user credentials (username, hash, and optional MFA secret) to shadow.txt"""
    with open("shadow.txt", "a", encoding="utf-8") as file:
        if mfa_secret:
            file.write(f"{username}:{hashed_password}:{mfa_secret}\n")
        else:
            file.write(f"{username}:{hashed_password}\n")


def get_shadow(username: str):
    """
    Read shadow.txt and return (stored_hash, mfa_secret_or_None) for username,
    or None if not found.
    Expected file lines:
      username:hashed_password
      username:hashed_password:mfa_secret
    """
    try:
        with open("shadow.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split(
                    ":", 2)  # split into max 3 parts
                if parts[0] != username:
                    continue
                if len(parts) == 3:
                    return parts[1], parts[2]
                elif len(parts) == 2:
                    return parts[1], None
                else:
                    # malformed line
                    return None
    except FileNotFoundError:
        return None


def get_mfa_secret_from_shadow(username: str, path: str = "shadow.txt"):
    p = Path(path)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(":", 2)
            if parts[0] == username:
                if len(parts) >= 3:
                    return parts[2]
                return None
    return None
