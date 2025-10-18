"""User creation"""
from file_system.utils import (
    account_exists,
    validate_password,
    generate_salt,
    hash_password,
    write_salt,
    write_shadow
)


class AccountInitialiser:
    """Manages the hash/salt/shadow based user/password creation system"""

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

            if not validate_password(input_password):
                print("Password does not meet requirements. Please try again.")
                continue

            confirmed_password = input("Confirm Password: ").strip()
            if input_password != confirmed_password:
                print("Passwords do not match. Please try again.")
                continue

            break

        # Generate salt
        salt = generate_salt()

        # Hash password + salt
        hashed_pass = hash_password(input_password, salt)

        # Update files
        write_salt(input_username, salt)
        write_shadow(input_username, hashed_pass)

        print(f"User {input_username} created successfully.")
