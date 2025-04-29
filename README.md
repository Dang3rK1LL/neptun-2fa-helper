# Neptun 2FA Helper

A modern and secure command-line tool for generating and copying your Neptun University 2FA codes, without needing to reach for your phone every time.  
Designed with a beautiful interactive interface, automatic code refreshing, and secure encrypted secret storage.

---

## ✨ Features

- 🔐 Securely encrypts and stores your Neptun TOTP secret
- 🔑 Live 2FA code viewer with automatic refresh
- 📋 Automatically copies codes to clipboard
- 🛡️ Change master password without losing your 2FA secret
- 🗑️ Reset all data safely if needed
- 🎨 Beautiful interface with menus, colors, and large texts

---

## 🖥️ Technologies Used

- [Python](https://www.python.org/)
- [Rich](https://github.com/Textualize/rich) – for beautiful terminal formatting
- [Questionary](https://github.com/tmbo/questionary) – for interactive menus
- [Cryptography](https://cryptography.io/) – for secure encryption
- [PyOTP](https://pyauth.github.io/pyotp/) – for TOTP code generation
- [Pyperclip](https://pypi.org/project/pyperclip/) – for clipboard support

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/Dang3rK1LL/neptun-2fa-helper.git
cd neptun-2fa-helper
