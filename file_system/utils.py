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


def get_shadow(username: str) -> str | None:
    """Look up a user's hashed password in shadow.txt."""
    try:
        with open("shadow.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == username:
                    return parts[1]
    except FileNotFoundError:
        print("shadow.txt not found.")
    return None


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


def validate_password(password: str) -> bool:
    """Check if password meets complexity requirements."""
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not any(c.isupper() for c in password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not any(c.islower() for c in password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not any(c.isdigit() for c in password):
        print("Password must contain at least one digit.")
        return False
    special_chars = "!@#$%^&*()"
    if not any(c in special_chars for c in password):
        print(
            f"Password should contain at least one special character: {special_chars}")
        return False
    return True


def write_shadow(username: str, hashed_pass: str) -> None:
    """Append a username and its hashed password to shadow.txt."""
    with open("shadow.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{hashed_pass}\n")
