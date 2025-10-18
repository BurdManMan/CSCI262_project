"""User creation"""
from file_system.utils import (
    account_exists,
    hash_password,
    write_shadow,
)
from file_system.password_strength import validate_password


class AccountInitialiser:
    """Manages the hash/shadow-based user/password creation system."""

    def run(self):
        """Maintain control flow for creating a new user."""

        # Ask for a valid username
        while True:
            input_username = input("Username: ").strip()
            if not account_exists(input_username):
                break
            print("Account already exists. Please choose a different username.")

        # Get a valid password
        while True:
            input_password = input("Password: ").strip()

            # Validate password strength
            valid, message = validate_password(input_username, input_password)
            if not valid:
                print(message)
                continue

            confirmed_password = input("Confirm Password: ").strip()
            if input_password != confirmed_password:
                print("Passwords do not match. Please try again.")
                continue

            break

        # Hash password (Argon includes built-in salting)
        hashed_pass = hash_password(input_password)

        # Update files
        write_shadow(input_username, hashed_pass)

        print(f"User '{input_username}' created successfully.")
