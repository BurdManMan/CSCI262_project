"""File operations (simplified, no access control)"""


class FileSystemManager:
    def __init__(self, username):
        self.username = username
        self.files = {}  # filename -> owner
        self.load_files()

    def load_files(self):
        """Load file records from Files.store if it exists"""
        try:
            with open("Files.store", "r", encoding="utf-8") as f:
                for line in f:
                    fname, owner = line.strip().split(":")
                    self.files[fname] = owner
            print("Loaded files from Files.store.")
        except FileNotFoundError:
            print("No existing Files.store found. Starting fresh.")

    def save_files(self):
        """Save current file records to Files.store"""
        with open("Files.store", "w", encoding="utf-8") as f:
            for fname, owner in self.files.items():
                f.write(f"{fname}:{owner}\n")
        print("File system saved to Files.store.")

    def run(self):
        """Main menu loop for file system"""
        while True:
            choice = input(
                "\nOptions: (C)reate, (A)ppend, (R)ead, (W)rite, "
                "(L)ist, (S)ave or (E)xit: "
            ).strip().upper()

            if choice == "C":
                fname = input("Filename: ").strip()
                if fname in self.files:
                    print(f"File '{fname}' already exists.")
                else:
                    self.files[fname] = self.username
                    # Create an empty file on disk
                    with open(fname, "w", encoding="utf-8") as f:
                        f.write("")
                    print(f"File '{fname}' created successfully.")

            elif choice == "A":
                fname = input("Filename: ").strip()
                if fname not in self.files:
                    print(f"File '{fname}' does not exist.")
                    continue
                text = input("Enter text to append: ")
                with open(fname, "a", encoding="utf-8") as f:
                    f.write(text + "\n")
                print(f"Appended to '{fname}' successfully.")

            elif choice == "R":
                fname = input("Filename: ").strip()
                if fname not in self.files:
                    print(f"File '{fname}' does not exist.")
                    continue
                with open(fname, "r", encoding="utf-8") as f:
                    print("\n=== File Contents ===")
                    print(f.read())
                    print("=====================")

            elif choice == "W":
                fname = input("Filename: ").strip()
                if fname not in self.files:
                    print(f"File '{fname}' does not exist.")
                    continue
                text = input("Enter new file contents: ")
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(text + "\n")
                print(f"Wrote to '{fname}' successfully.")

            elif choice == "L":
                if not self.files:
                    print("No files in system.")
                else:
                    for fname, owner in self.files.items():
                        print(f"{fname} (owner: {owner})")

            elif choice == "S":
                self.save_files()

            elif choice == "E":
                confirm = input("Exit the FileSystem? (Y/N): ").strip().upper()
                if confirm == "Y":
                    print("Exiting FileSystem.")
                    break

            else:
                print("Invalid option, try again.")
