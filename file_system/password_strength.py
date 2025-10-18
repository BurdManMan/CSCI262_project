"""
PASSWORD POLICIES
1. A password must contain 8-31 characters.
2. A password must only contain printable characters.
3. A password should use a combination of alphabetic, numeric, and punctuation characters.
4. A password must contain at least one upper case and lower case letter.
5. A password cannot be re-used (check for username and password in salted and hashed password file)
6. A password cannot be based on your username (e.g. abc123)
7. Passwords will not be accepted if they are found to be in a list of compromised passwords.
"""

import string

# List of compromised passwords (normally we would be checking from a real database)
COMPROMISED_PASSWORDS = {"password123", "12345678", "admin", "password"}

def is_printable(password):
    # Check if all characters in password are printable.
    return all(char in string.printable for char in password)

def validate_password(username, new_password):
    # Validate new password against our 7 password policies.

    # 1. Length check
    if not (8 <= len(new_password) <= 31):
        return "Password must be between 8 and 31 characters."

    # 2. Printable characters only
    if not is_printable(new_password):
        return "Password must only contain printable characters."

    # 3. Must include alphabetic, numeric, or punctuation
    has_alpha = any(c.isalpha() for c in new_password)
    has_digit = any(c.isdigit() for c in new_password)
    # string.punctuation checks for !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    has_punct = any(c in string.punctuation for c in new_password)
    if not (has_alpha and has_digit and has_punct):
        return "Password should combine letters with numbers and punctuation."

    # 4. Must include at least one uppercase and one lowercase letter
    has_upper = any(c.isupper() for c in new_password)
    has_lower = any(c.islower() for c in new_password)
    if not (has_upper and has_lower):
        return "Password must contain at least one uppercase and one lowercase letter."

    # 5. Cannot be reused
    # for this, check old passwords from the hashed and salted password file.
    # write a program if mew password = old pass, then return "Old password can't be reused."

    # 6. Cannot be based on username
    if username.lower() in new_password.lower():
        return "Password cannot contain your username."

    # 7. Cannot be a compromised password
    if new_password.lower() in COMPROMISED_PASSWORDS:
        return "Password is found on a list of compromised passwords."

    # If all checks pass, password is valid
    return "Password accepted!"

username = input("Enter your username: ")
while True:
    new_password = input("Enter your new password: ")

    result = validate_password(username, new_password)

    # Store valid password, print result and break out of loop if password is accepted.
    if result == "Password accepted!":
        print(result)
        break