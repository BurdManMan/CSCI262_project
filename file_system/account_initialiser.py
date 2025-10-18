"""user creation"""
from file_system.utils import (
    account_exists,
    validate_password,
    generate_salt,
    hash_password,
    write_salt,
    write_shadow
)


class AccountInitialiser():
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

        # Get a valid clearance level
        while True:
            input_clearance = input(
                "User clearance (0, 1, 2, or 3.): ").strip()
            if input_clearance in {"0", "1", "2", "3"}:
                clearance = int(input_clearance)
                break
            print("Invalid clearance level. Please enter 0, 1, 2, or 3.")

        # Generate salt
        salt = generate_salt()

        # Hash password + salt
        hashed_pass = hash_password(input_password, salt)

        # Update files
        write_salt(input_username, salt)  # placeholder
        write_shadow(input_username, hashed_pass, clearance)  # placholder

        print(
            f"User {input_username} created successfully with clearance {clearance}.")
