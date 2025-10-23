"""authentication with MFA"""
import time
import pyotp
from file_system.file_system_manager import FileSystemManager
from file_system.utils import verify_password, get_shadow


# Lockout config
_LOCKS = {}
FAIL_THRESHOLD = 5
LOCK_DURATION_SECONDS = 10 * 60

class LoginManager:
    """Manages user authentication including optional MFA verification."""

    def run(self):
        """Control flow for login process."""

        # Step 1: Username
        username = input("Username: ").strip()
        if not username:
            print("No username provided. Aborting.")
            return

        # Step 2: Retrieve stored credentials
        shadow_entry = get_shadow(username)
        if shadow_entry is None:
            print(f"User '{username}' not found. Login failed.")
            return

        # Lcockout check before password prompt
        now = int(time.time())
        fail_count, lock_until = _LOCKS.get(username, (0, 0))
        if now < lock_until:
            remaining = lock_until - now
            mins, secs = divmod(remaining, 60)
            print(f"Account temporarily locked. Try again in {mins}m {secs}s.")
            return

        # Normalize shadow_entry into (stored_hash, mfa_secret_or_None)
        stored_hash = None
        mfa_secret = None

        # Accept several possible return shapes for backwards compatibility:
        # - (stored_hash, mfa_secret)
        # - (stored_hash,) or (stored_hash, "default")
        # - (stored_hash, "default", mfa_secret) (older inconsistent format)
        try:
            if isinstance(shadow_entry, (tuple, list)):
                if len(shadow_entry) == 2:
                    stored_hash, mfa_secret = shadow_entry
                elif len(shadow_entry) == 3:
                    # handle case like (hash, "default", mfa_secret)
                    stored_hash = shadow_entry[0]
                    # assume MFA secret is last element
                    mfa_secret = shadow_entry[2] if shadow_entry[2] else None
                elif len(shadow_entry) == 1:
                    stored_hash = shadow_entry[0]
                    mfa_secret = None
                else:
                    # fallback: try first element as hash and last as mfa
                    stored_hash = shadow_entry[0]
                    mfa_secret = shadow_entry[-1] if len(
                        shadow_entry) > 1 else None
            else:
                # If get_shadow returned a single string (hash), accept it
                stored_hash = shadow_entry
                mfa_secret = None
        except Exception:
            print("Malformed shadow entry. Login failed.")
            return

        if not stored_hash:
            print("No stored password hash found for that user. Login failed.")
            return

        # Step 4: Password verification
        password = input("Password: ").strip()
        if not password:
            print("No password entered. Login failed.")
            return

        print("Verifying password...")
        try:
            ok = verify_password(stored_hash, password)
        except Exception:
            print("Internal error during verification.")
            ok = False

        if not ok:
            # Increment fail count
            fail_count += 1
            if fail_count >= FAIL_THRESHOLD:
                lock_until = now + LOCK_DURATION_SECONDS
                _LOCKS[username] = (0, lock_until)
                print(f"Too many failed attempts. Account locked for {LOCK_DURATION_SECONDS // 60} minutes.")
            else:
                _LOCKS[username] = (fail_count, 0)
                remaining_tries = FAIL_THRESHOLD - fail_count
                print(f"Incorrect password. {remaining_tries} attempt(s) remaining before lockout.")
            return

        # --- Password success: clear any lock state ---
        if username in _LOCKS:
            del _LOCKS[username]
        print(f"Password authentication for user '{username}' complete.")

        # Step 5: MFA Verification (if configured)
        if mfa_secret:
            totp = pyotp.TOTP(mfa_secret)
            user_code = input("Enter your 6-digit MFA code: ").strip()
            if not user_code:
                print("No MFA code entered. Login failed.")
                return
            if not totp.verify(user_code):
                print("Invalid or expired MFA code. Login failed.")
                return
            print("MFA verification successful.")
        else:
            print("No MFA secret found — skipping MFA verification (demo user).")

        # Step 6: Hand control to file system
        print(f"Login successful. Welcome, {username}.")
        fs_manager = FileSystemManager(username)
        fs_manager.run()
