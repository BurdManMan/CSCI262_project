"""Hashing, validation, and file I/O"""
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from pathlib import Path
import random
import hashlib
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4, hash_len=32)

def account_exists(username: str) -> bool:
    """Check if the username already exists in the salt.txt file."""
    salt_file = Path("salt.txt")

    if not salt_file.exists():
        return False

    with salt_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: Username:Salt
            if line.split(":", 1)[0] == username:
                return True

    return False


def generate_salt(length: int = 8) -> str:
    """Generate a random numeric salt string of given length (default 8)."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def get_salt(username: str) -> str | None:
    """Retrieve a user's salt from salt.txt."""
    try:
        with open("salt.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == username:
                    return parts[1]
    except FileNotFoundError:
        print("salt.txt not found.")
    return None


def get_shadow(username: str) -> str | None:
    """
    Look up a user's hashed password in shadow.txt.
    Returns the hash if found, otherwise None.
    """
    try:
        with open("shadow.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == username:
                    return parts[1]
    except FileNotFoundError:
        print("shadow.txt not found.")
    return None


def hash_password(password: str, salt: str = None) -> str:
    """
    Hash a password using Argon2 and return the encoded string.
    Argon2 generates/embeds its own random salt inside the encoded hash. (So dont need to use salt.txt)
    """
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    return ph.hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify a plaintext password against an Argon2 encoded hash.
    Returns True if it matches, False otherwise.
    """
    if not stored_hash:
        return False
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    try:
        return ph.verify(stored_hash, password)
    except (argon2_exceptions.VerifyMismatchError, argon2_exceptions.InvalidHash):
        return False
    except Exception:
        return False
    
def validate_password(password: str) -> bool:
    """
    Check if password meets complexity requirements:
    - At least 8 characters
    - 1 uppercase letter
    - 1 lowercase letter
    - 1 digit
    - 1 special character (!@#$%^&*())
    """
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


def write_salt(username: str, salt: str) -> None:
    """Append a username and its salt to salt.txt."""
    with open("salt.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{salt}\n")


def write_shadow(username: str, hashed_pass: str) -> None:
    """Append a username and its hashed password to shadow.txt."""
    with open("shadow.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{hashed_pass}\n")
