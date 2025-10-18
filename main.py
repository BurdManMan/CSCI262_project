"""Central module that manages control flow of file system helper functions"""
import argparse
from pathlib import Path
from file_system.account_initialiser import AccountInitialiser
from file_system.login_manager import LoginManager
from file_system.utils import hash_password


def ensure_files_exist():
    """Ensure salt.txt and shadow.txt exist; create empty if missing"""
    for filename in ("salt.txt", "shadow.txt"):
        path = Path(filename)
        if not path.exists():
            path.write_text("", encoding="utf-8")  # create an empty file
            print(f"Created missing file: {filename}")


def print_md5_test():
    """outputs hash for test string"""
    test_string = "This is a test"
    md5_hash = hash_password(test_string, "")
    print(f'MD5 ("{test_string}") = {md5_hash}')


def main():
    """Control flow manager for top level of file system"""
    # Print MD5 test
    print_md5_test()

    # Make sure required files exist
    ensure_files_exist()

    parser = argparse.ArgumentParser(description="Simple FileSystem")
    parser.add_argument(
        "-i",
        action="store_true",
        help="Initialize the file system"
    )
    args = parser.parse_args()

    # if command line argument is -i start the initialisation process
    if args.i:
        account_initialiser = AccountInitialiser()
        account_initialiser.run()

    # if there is no command line argument start login and file manipulation
    # process
    else:
        log_in_manager = LoginManager()
        log_in_manager.run()


if __name__ == "__main__":
    main()
