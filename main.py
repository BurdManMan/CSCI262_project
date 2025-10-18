"""Central module that manages control flow of file system helper functions"""
from pathlib import Path
from file_system.account_initialiser import AccountInitialiser
from file_system.login_manager import LoginManager


def ensure_files_exist():
    """Ensure salt.txt and shadow.txt exist; create empty if missing"""
    for filename in ("salt.txt", "shadow.txt"):
        path = Path(filename)
        if not path.exists():
            path.write_text("", encoding="utf-8")
            print(f"Created missing file: {filename}")


def display_menu():
    """Display the command line menu and get user choice"""
    print("\n=== Password Cracking Solution ===")
    print("1. Account creation")
    print("2. Log in and start file manipulation")
    print("3. Exit")

    while True:
        choice = input("Select an option (1-3): ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Control flow manager for top level of file system"""
    ensure_files_exist()

    while True:
        choice = display_menu()

        if choice == "1":
            account_initialiser = AccountInitialiser()
            account_initialiser.run()

        elif choice == "2":
            log_in_manager = LoginManager()
            log_in_manager.run()

        elif choice == "3":
            print("Exiting program. Goodbye!")
            break


if __name__ == "__main__":
    main()
