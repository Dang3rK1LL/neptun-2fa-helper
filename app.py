import os
import base64
import getpass
import time
import pyotp
import pyperclip
import questionary
from rich.console import Console
from rich.panel import Panel
from cryptography.fernet import Fernet, InvalidToken

# Constants
SECRET_FILE = 'neptun_secret.enc'
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_key(password: str) -> Fernet:
    password_bytes = password.encode('utf-8')
    padded_password = password_bytes.ljust(32, b'0')[:32]
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
            time_remaining = 30 - int(time.time()) % 30
            pyperclip.copy(code)

            console.print(Panel.fit(
                f"[bold green]🔑 Current 2FA Code: [white]{code}[/white][/bold green]\n\n"
                f"[cyan]⏳ Refreshes in: {time_remaining} seconds[/cyan]\n"
                f"[yellow]📋 Code copied to clipboard![/yellow]",
                title="[bold blue]Neptun 2FA Live Code Viewer[/bold blue]",
                border_style="bright_blue"))

            console.print("[dim]Press Ctrl+C to return to the main menu.[/dim]")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🔙 Returning to main menu...\n")
        time.sleep(1)

def enter_new_secret(key: Fernet):
    secret = questionary.text("Enter your new Neptun 2FA secret (Base32 format):").ask().strip()
    save_secret(secret, key)
    console.print("\n[bold green]✅ Secret updated and encrypted successfully![/bold green]\n")
    time.sleep(2)

def change_master_password(old_key: Fernet):
    try:
        secret = load_secret(old_key)
        new_password = questionary.password("Enter new master password:").ask()
        confirm_password = questionary.password("Confirm new master password:").ask()

        if new_password != confirm_password:
            console.print("\n[bold red]❌ Passwords do not match. Password change canceled.[/bold red]\n")
            time.sleep(2)
            return

        new_key = generate_key(new_password)
        save_secret(secret, new_key)
        console.print("\n[bold green]✅ Master password changed successfully![/bold green]\n")
        time.sleep(2)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error changing password: {e}[/bold red]\n")
        time.sleep(2)

def reset_data():
    confirm = questionary.confirm("⚠️ Are you sure you want to reset and delete all saved data?").ask()
    if confirm:
        delete_secret_file()
        console.print("\n[bold green]✅ Data reset successfully. Restart the app to set a new secret.[/bold green]\n")
        exit()
    else:
        console.print("\n[bold yellow]❌ Reset canceled.[/bold yellow]\n")
        time.sleep(2)

def main_menu(secret: str, key: Fernet):
    while True:
        clear_screen()
        console.print(Panel.fit("[bold blue]Welcome to the Neptun 2FA Helper![/bold blue]", border_style="cyan"))

        choice = questionary.select(
            "Select an option:",
            choices=[
                "🔑 Live 2FA code viewer (auto-refresh)",
                "✏️ Enter a new secret",
                "🛡️ Change master password",
                "🗑️ Reset all data",
                "🚪 Exit"
            ]
        ).ask()

        if choice.startswith("🔑"):
            live_generate_2fa(secret)
        elif choice.startswith("✏️"):
            enter_new_secret(key)
            secret = load_secret(key)
        elif choice.startswith("🛡️"):
            change_master_password(key)
            master_password = getpass.getpass("Re-enter your new master password to continue: ")
            key = generate_key(master_password)
            secret = load_secret(key)
        elif choice.startswith("🗑️"):
            reset_data()
        elif choice.startswith("🚪"):
            console.print("\n👋 [bold]Goodbye![/bold]\n")
            break
        else:
            console.print("\n[bold red]❌ Invalid option. Please try again.[/bold red]\n")
            time.sleep(2)

def setup_or_load_secret(key: Fernet) -> str:
    if not os.path.exists(SECRET_FILE):
        console.print("\n[bold yellow]First time setup![/bold yellow]")
        secret = questionary.text("Enter your Neptun 2FA secret (Base32 format):").ask().strip()
        save_secret(secret, key)
        console.print("\n[bold green]✅ Secret saved securely![/bold green]\n")
    secret = load_secret(key)
    return secret

def main():
    clear_screen()
    console.print(Panel.fit("[bold blue]Neptun 2FA Helper[/bold blue]", border_style="cyan"))

    master_password = getpass.getpass("Enter your master password: ")

    try:
        key = generate_key(master_password)
        secret = setup_or_load_secret(key)
        main_menu(secret, key)
    except InvalidToken:
        console.print("\n[bold red]❌ Error: Wrong master password or corrupted encrypted file.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
