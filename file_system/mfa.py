import pyotp

# GENERATE SETUP KEY FOR MFA
# store this setup key along with user details for MFA verification.
setup_key = pyotp.random_base32()
print("Your MFA setup key:", setup_key)
print("Add this setup code to an authenticator app like Google Authenicator, Authy, Microsoft..")




# VERIFY 6 DIGIT CODE FOR MFA
totp = pyotp.TOTP(setup_key)
user_code = input("Enter your 6-digit code: ")

if totp.verify(user_code):
    print("MFA passed")
else:
    print("Invalid or expired code")