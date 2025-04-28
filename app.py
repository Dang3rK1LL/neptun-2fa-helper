import os
import getpass
import pyotp
import pyperclip
from cryptography.fernet import Fernet

# Constants
SECRET_FILE = 'neptun_secret.enc'

def generate_key(password: str) -> bytes:
    # Password to key: pad/cut to 32 bytes
    password_bytes = password.encode('utf-8')
    return Fernet(base64.urlsafe_b64encode(password_bytes.ljust(32, b'0')[:32]))

def save_secret(secret: str, key: Fernet):
    encrypted_secret = key.encrypt(secret.encode())
    with open(SECRET_FILE, 'wb') as f:
        f.write(encrypted_secret)

def load_secret(key: Fernet) -> str:
    with open(SECRET_FILE, 'rb') as f:
        encrypted_secret = f.read()
    return key.decrypt(encrypted_secret).decode()

def main():
    print("=== Neptun 2FA Code Generator ===\n")

    # Ask for master password
    master_password = getpass.getpass("Enter master password: ")

    try:
        key = generate_key(master_password)

        # Check if secret file exists
        if not os.path.exists(SECRET_FILE):
            print("\nFirst time setup!")
            secret = input("Enter your Neptun 2FA secret (from QR code setup): ").strip()
            save_secret(secret, key)
            print("Secret saved securely!\n")
        else:
            secret = load_secret(key)

        # Generate and display TOTP code
        totp = pyotp.TOTP(secret)
        code = totp.now()
        print(f"Your current Neptun 2FA code is: {code}")

        # Copy to clipboard
        pyperclip.copy(code)
        print("(Code copied to clipboard!)")

    except Exception as e:
        print("\nError: Unable to decrypt or generate code. Wrong password or corrupted file.")
        print(f"Details: {e}")

if __name__ == "__main__":
    import base64
    main()
