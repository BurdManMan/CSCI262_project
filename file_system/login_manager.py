"""Authentication"""
from file_system.file_system_manager import FileSystemManager
from file_system.utils import get_salt, hash_password, get_shadow


class LoginManager:
    """Manages logging the user into the file system"""

    def run(self):
        """Control flow manager"""
        # Username
        username = input("Username: ").strip()
        salt = get_salt(username)
        if salt is None:
            print(f"User {username} not found in salt.txt")
            return

        print(f"{username} found in salt.txt")
        print(f"Salt retrieved: {salt}")

        # Password
        password = input("Password: ").strip()

        # Hash
        print("Hashing...")
        computed_hash = hash_password(password, salt)
        print(f"Hash value: {computed_hash}")

        # Compare with shadow.txt
        stored_hash = get_shadow(username)
        if stored_hash is None:
            print(f"No shadow entry for {username}. Login failed.")
            return

        if computed_hash != stored_hash:
            print("Authentication failed. Incorrect password.")
            return

        print(f"Authentication for user {username} complete.")

        # Move control to file system
        fs_manager = FileSystemManager(username)
        fs_manager.run()
