"""Authentication"""
from file_system.file_system_manager import FileSystemManager
from file_system.utils import get_shadow, verify_password
import time

# in-memory lock map: { username: (fail_count:int, lock_until_epoch:int) }
_LOCKS = {}
FAIL_THRESHOLD = 5 # Number of password try before lock out
LOCK_DURATION_SECONDS = 10 * 60 # Lock Time


class LoginManager:
    """Manages logging the user into the file system"""

    def run(self):
        """Control flow manager"""
        # Username
        username = input("Username: ").strip()
        
        # Pull stored hash from shadow.txt
        stored_hash = get_shadow(username)
        if stored_hash is None:
            print(f"User {username} not found (no shadow entry).")
            return

          # --- Lock check ---
        now = int(time.time())
        fail_count, lock_until = _LOCKS.get(username, (0, 0))
        if now < lock_until:
            # remaining seconds
            remaining = lock_until - now
            mins = remaining // 60
            secs = remaining % 60
            print(f"Authentication failed. Account temporarily locked. Try again in {mins}m {secs}s.")
            return

        # Password
        password = input("Password: ").strip()

       # Verify with Argon2 
        print("Verifying...")
        try:
                ok = verify_password(stored_hash, password)
        except Exception as e:
                # verify_password or argon2 could raise — treat as failure but log
                print("Internal error during verification.")
                
                ok = False

        if not ok:
                # increment fail count
            fail_count = fail_count + 1
            if fail_count >= FAIL_THRESHOLD:
                    lock_until = now + LOCK_DURATION_SECONDS
                    _LOCKS[username] = (0, lock_until)
                    minutes = LOCK_DURATION_SECONDS // 60
                    print(f"Authentication failed. Too many attempts — account locked for {minutes} minutes.")
            else:
                    _LOCKS[username] = (fail_count, 0)
                    remaining_tries = FAIL_THRESHOLD - fail_count
                    print(f"Authentication failed. Incorrect password. {remaining_tries} attempt(s) remaining before lockout.")
            return
        
        # --- Success path: clear any lock state ---
        if username in _LOCKS:
            del _LOCKS[username]
        print(f"Authentication for user {username} complete.")

        # Move control to file system
        fs_manager = FileSystemManager(username)
        fs_manager.run()
