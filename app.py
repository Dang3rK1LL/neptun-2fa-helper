import os
import base64
import getpass
import time
import pyotp
import pyperclip
from cryptography.fernet import Fernet, InvalidToken

# Constants
SECRET_FILE = 'neptun_secret.enc'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_key(password: str) -> Fernet:
    password_bytes = password.encode('utf-8')
    padded_password = password_bytes.ljust(32, b'0')[:32]  # ensure exactly 32 bytes
    return Fernet(base64.urlsafe_b64encode(padded_password))

def save_secret(secret: str, key: Fernet):
    encrypted_secret = key.encrypt(secret.encode())
    with open(SECRET_FILE, 'wb') as f:
        f.write(encrypted_secret)

def load_secret(key: Fernet) -> str:
    with open(SECRET_FILE, 'rb') as f:
        encrypted_secret = f.read()
    return key.decrypt(encrypted_secret).decode()

def delete_secret_file():
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)

def live_generate_2fa(secret: str):
    try:
        totp = pyotp.TOTP(secret)
        while True:
            clear_screen()
            code = totp.now()
            time_remaining = 30 - int(time.time()) % 30  # TOTP changes every 30 seconds
            pyperclip.copy(code)

            print("\n=== Neptun 2FA Live Code Generator ===")
            print(f"\n🔑 Current 2FA code: {code}")
            print(f"⏳ Code refreshes in: {time_remaining} seconds")
            print("\n(Press Ctrl+C to return to the menu.)")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🔙 Returning to main menu...\n")
        time.sleep(1)

def enter_new_secret(key: Fernet):
    secret = input("\nEnter your new Neptun 2FA secret (Base32 format): ").strip()
    save_secret(secret, key)
    print("✅ Secret updated and encrypted successfully.\n")
    time.sleep(2)

def reset_data():
    confirm = input("\n⚠️ Are you sure you want to reset and delete all saved data? (yes/no): ").strip().lower()
    if confirm == "yes":
        delete_secret_file()
        print("✅ Data reset successfully. Restart the app to set a new secret.\n")
        exit()
    else:
        print("❌ Reset canceled.\n")
        time.sleep(2)

def main_menu(secret: str, key: Fernet):
    while True:
        clear_screen()
        print("\n=== Neptun 2FA Helper ===")
        print("1. Live 2FA code viewer (auto-refresh)")
        print("2. Enter a new secret")
        print("3. Reset all data")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            live_generate_2fa(secret)
        elif choice == "2":
            enter_new_secret(key)
            secret = load_secret(key)  # reload updated secret
        elif choice == "3":
            reset_data()
        elif choice == "4":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please try again.\n")
            time.sleep(2)

def setup_or_load_secret(key: Fernet) -> str:
    if not os.path.exists(SECRET_FILE):
        print("\nFirst time setup!")
        secret = input("Enter your Neptun 2FA secret (Base32 format): ").strip()
        save_secret(secret, key)
        print("✅ Secret saved securely!\n")
    secret = load_secret(key)
    return secret

def main():
    clear_screen()
    print("=== Welcome to Neptun 2FA Helper ===\n")
    master_password = getpass.getpass("Enter your master password: ")

    try:
        key = generate_key(master_password)
        secret = setup_or_load_secret(key)
        main_menu(secret, key)
    except (InvalidToken, Exception) as e:
        print("\n❌ Error: Unable to decrypt or generate code. Wrong password or corrupted file.")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()
