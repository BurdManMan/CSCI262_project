Basic password cracking solution

=== Environment Setup Guide ===
Windows:

1. Create virtual environment by using the following command "python -m venv .venv".
2. Navigate to virtual environment using the following command ".venv\Scripts\activate".
3. Install required modules seen below using pip:

- "pip install pyotp"
- "pip install argon2-cffi"

Linux:
1. Create virtual environment by using the following command "python3 -m venv .venv".
2. Navigate to virtual environment using the following command "source .venv/bin/activate".
3. Install required modules seen below using pip:

- "pip install pyotp"
- "pip install argon2-cffi"


=== Running Instructions ===
Windows:
1. To run main program use command "python main.py"
2. To run authenticator demo use commmand "python demo_show_user_code.py"

Linux:
1. To run main program use command "python3 main.py"
2. To run authenticator demo use commmand "python3 demo_show_user_code.py"
