"""file operations"""

from file_system.access_control import can_read, can_write


class FileSystemManager:
    def __init__(self, username, clearance):
        self.username = username
        self.clearance = clearance
        self.files = {}  # filename -> (owner, clearance)
        self.load_files()

    def load_files(self):
        """Load file records from Files.store if it exists"""
        try:
            with open("Files.store", "r", encoding="utf-8") as f:
                for line in f:
                    fname, owner, fclear = line.strip().split(":")
                    self.files[fname] = (owner, int(fclear))
            print("Loaded files from Files.store.")
        except FileNotFoundError:
            print("No existing Files.store found. Starting fresh.")

    def save_files(self):
        """Save current file records to Files.store"""
        with open("Files.store", "w", encoding="utf-8") as f:
            for fname, (owner, fclear) in self.files.items():
                f.write(f"{fname}:{owner}:{fclear}\n")
        print("File system saved to Files.store.")

    def run(self):
        """Main menu loop for file system"""
        while True:
            choice = input(
                "Options: (C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave or (E)xit: "
            ).strip().upper()

            if choice == "C":
                fname = input("Filename: ").strip()
                if fname in self.files:
                    print(f"File '{fname}' already exists.")
                else:
                    self.files[fname] = (self.username, self.clearance)
                    print(
                        f"File '{fname}' created with classification {self.clearance}.")

            elif choice in ("A", "R", "W"):
                fname = input("Filename: ").strip()
                if fname not in self.files:
                    print(f"File '{fname}' does not exist")
                    continue
                owner, fclear = self.files[fname]

                if choice == "R":
                    if can_read(self.clearance, fclear):
                        print(f"Read from '{fname}' successful.")
                    else:
                        print("Access denied (no read up).")
                else:  # W or A
                    if can_write(self.clearance, fclear):
                        print(
                            f"{'Appended' if choice == 'A' else 'Wrote'} to '{fname}' successfully")
                    else:
                        print("Access denied (no write down).")

            elif choice == "L":
                if not self.files:
                    print("No files in system.")
                else:
                    for fname, (owner, fclear) in self.files.items():
                        print(f"{fname} (owner: {owner}, clearance: {fclear})")

            elif choice == "S":
                self.save_files()

            elif choice == "E":
                confirm = input(
                    "Shut down the FileSystem? (Y)es or (N)o").strip().upper()
                if confirm == "Y":
                    print("Exiting FileSystem.")
                    break

            else:
                print("Invalid option, try again.")
