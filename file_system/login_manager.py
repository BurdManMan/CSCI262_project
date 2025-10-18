"""authentication"""
from file_system.file_system_manager import FileSystemManager
from file_system.utils import (
    get_salt,
    hash_password,
    get_shadow
)


class LoginManager():
    """Manages logging the user into the file system"""

    def run(self):
        """control flow manager"""
        # Username
        username = input("Username: ").strip()
        salt = get_salt(username)
        if salt is None:
            print(f"User {username} not found in salt.txt")
            return

        print(f"{username} found in salt.txt")
        print(f"salt retrieved: {salt}")

        # Password
        password = input("Password: ").strip()

        # Hash
        print("hashing...")
        computed_hash = hash_password(password, salt)
        print(f"hash value: {computed_hash}")

        # Compare with shadow.txt
        shadow_entry = get_shadow(username)
        if shadow_entry is None:
            print(f"No shadow entry for {username}. Login failed.")
            return

        stored_hash, clearance = shadow_entry
        if computed_hash != stored_hash:
            print("Authentication failed. Incorrect password.")
            return

        print(f"Authentication for user {username} complete.")
        print(f"The clearance for {username} is {clearance}.")

        # Move control to file system
        fs_manager = FileSystemManager(username, clearance)
        fs_manager.run()
