# demo_show_user_code_live.py
import pyotp
import time
import sys
from pathlib import Path


def get_mfa_secret_from_shadow(username: str, path: str = "shadow.txt"):
    p = Path(path)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(":", 2)
            if parts[0] == username:
                if len(parts) >= 3:
                    return parts[2]
                return None
    return None


if len(sys.argv) < 2:
    print("Usage: python demo_show_user_code_live.py <username>")
    sys.exit(1)

username = sys.argv[1]
secret = get_mfa_secret_from_shadow(username)
if not secret:
    print(f"No MFA secret found for user '{username}'")
    sys.exit(1)

totp = pyotp.TOTP(secret)

print(f"MFA secret for '{username}': {secret}")
print("Press Ctrl+C to exit.\n")

try:
    while True:
        code = totp.now()
        remaining = totp.interval - (int(time.time()) % totp.interval)
        print(
            f"Current 6-digit code: {code} | expires in {remaining:2} seconds", end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting.")
