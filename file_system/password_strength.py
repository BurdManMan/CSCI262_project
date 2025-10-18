"""
PASSWORD POLICIES
1. A password must contain 8-31 characters.
2. A password must only contain printable characters.
3. A password should use a combination of alphabetic, numeric, and punctuation characters.
4. A password must contain at least one upper case and lower case letter.
5. A password cannot be re-used (check for username and password in salted and hashed 
    password file).
6. A password cannot be based on your username (e.g. abc123).
7. Passwords will not be accepted if they are found to be in a list of compromised passwords.
"""

import string

# List of compromised passwords (in production, this would come from a proper database or API)
COMPROMISED_PASSWORDS = {"Password123!", "12345678", "admin", "password"}


def is_printable(password: str) -> bool:
    """Check if all characters in the password are printable."""
    return all(char in string.printable for char in password)


def validate_password(username: str, new_password: str) -> tuple[bool, str]:
    """
    Validate a password against the system's security policies.

    Returns:
        (bool, str): (is_valid, message)
        - is_valid: True if password meets all criteria.
        - message: explanation of the result.
    """

    # 1. Length check
    if not (8 <= len(new_password) <= 31):
        return False, "Password must be between 8 and 31 characters."

    # 2. Printable characters only
    if not is_printable(new_password):
        return False, "Password must only contain printable characters."

    # 3. Must include alphabetic, numeric, and punctuation
    has_alpha = any(c.isalpha() for c in new_password)
    has_digit = any(c.isdigit() for c in new_password)
    has_punct = any(c in string.punctuation for c in new_password)
    if not (has_alpha and has_digit and has_punct):
        return False, "Password should combine letters with numbers and punctuation."

    # 4. Must include at least one uppercase and one lowercase letter
    has_upper = any(c.isupper() for c in new_password)
    has_lower = any(c.islower() for c in new_password)
    if not (has_upper and has_lower):
        return False, "Password must contain at least one uppercase and one lowercase letter."

    # 6. Cannot be based on username
    if username.lower() in new_password.lower():
        return False, "Password cannot contain your username."

    # 7. Cannot be a compromised password
    if new_password.lower() in COMPROMISED_PASSWORDS:
        return False, "Password is found on a list of compromised passwords."

    # All checks passed
    return True, "Password accepted!"
