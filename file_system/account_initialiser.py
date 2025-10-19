"""User creation with MFA setup"""
import pyotp
from file_system.utils import (
    account_exists,
    hash_password,
    write_shadow
)
from file_system.password_strength import validate_password


class AccountInitialiser:
    """Manages user creation, password hashing, and MFA setup"""

    def run(self):
        """Maintain control flow for creating a new user"""

        # Ask for a valid username
        while True:
            input_username = input("Username: ").strip()
            if not account_exists(input_username):
                break
            print("Account already exists. Please choose a different username.")

        # Get a valid password
        while True:
            input_password = input("Password: ").strip()

            valid, message = validate_password(input_username, input_password)
            if not valid:
                print(message)
                continue

            confirmed_password = input("Confirm Password: ").strip()
            if input_password != confirmed_password:
                print("Passwords do not match. Please try again.")
                continue

            break

        # Hash password (Argon2 has built-in salt)
        hashed_pass = hash_password(input_password)

        # ---- MFA SETUP SECTION ----
        # Generate a random secret key for MFA
        mfa_secret = pyotp.random_base32()
        print("\nYour MFA setup key:", mfa_secret)
        print(
            "Add this setup key to an authenticator app like Google Authenticator or Authy.")
        print("This app will now generate 6-digit codes for your login.\n")

        # OPTIONAL: show the current code for testing
        totp = pyotp.TOTP(mfa_secret)
        print(f"Example current 6-digit code (for testing): {totp.now()}\n")

        # ---- STORE USER CREDENTIALS ----
        # Store username, hashed password, and MFA secret in shadow file
        write_shadow(input_username, hashed_pass, mfa_secret)

        print(f"User '{input_username}' created successfully.")
