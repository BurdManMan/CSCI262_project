"""hashing, validation, file I/O"""
from pathlib import Path
import random
import hashlib


def account_exists(username: str) -> bool:
    """checks if the username already exists in the salt.txt file"""
    salt_file = Path("salt.txt")

    # If the file doesn't exist yet, the account definitely doesn't exist
    if not salt_file.exists():
        return False

    # Read the file line by line and check for the username
    with salt_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Each line is expected to be: Username:Salt
            if line.split(":", 1)[0] == username:
                return True

    return False


def generate_salt(length: int = 8) -> str:
    """Generate a random salt string of specified length (default 8 digits)."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def get_salt(username: str) -> str | None:
    """
    Look up a user's salt in salt.txt.
    Returns the salt string if found, otherwise None.
    """
    try:
        with open("salt.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == username:
                    return parts[1]
    except FileNotFoundError:
        print("salt.txt not found.")
    return None


def get_shadow(username: str) -> tuple[str, int] | None:
    """
    Look up a user's (hashed password, clearance) in shadow.txt.
    Returns a tuple (hash, clearance) if found, otherwise None.
    """
    try:
        with open("shadow.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 3 and parts[0] == username:
                    stored_hash, clearance = parts[1], int(parts[2])
                    return stored_hash, clearance
    except FileNotFoundError:
        print("shadow.txt not found.")
    return None


def hash_password(password: str, salt: str) -> str:
    """
    Hash a password with its salt using MD5.
    Returns the hexadecimal digest.
    """
    combined = password + salt
    md5_hash = hashlib.md5(combined.encode("utf-8"))
    return md5_hash.hexdigest()


def validate_password(password: str) -> bool:
    """
    Returns True if the password meets the requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - Opyyptional: at least 1 special character
    """

    # Check length
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False

    # Check for uppercase
    if not any(c.isupper for c in password):
        print("Password must contain at least one uppercase letter.")
        return False

    # Check for lowercase
    if not any(c.islower() for c in password):
        print("Password must contain at least one lowercase letter.")
        return False

    # Check for digit
    if not any(c.isdigit() for c in password):
        print("Password must contain at least one digit.")
        return False

    # Check for special character
    special_chars = "!@#$%^&*()"
    if not any(c in special_chars for c in password):
        print(
            f"Password should contain at least one special character: {special_chars}")
        return False

    return True


def write_salt(username: str, salt: str) -> None:
    """
    Append a username and its salt to salt.txt.
    Format: Username:Salt
    """
    with open("salt.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{salt}\n")


def write_shadow(username: str, hashed_pass: str, clearance: int) -> None:
    """
    Append a username, hash, and clearance level to shadow.txt.
    Format: Username:PassSaltHash:SecurityClearance
    """
    with open("shadow.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{hashed_pass}:{clearance}\n")
