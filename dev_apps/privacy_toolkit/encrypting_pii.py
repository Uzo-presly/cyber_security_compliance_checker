import argparse
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from getpass import getpass
from hashlib import sha256

KEY_FILE_ENCRYPTED = "encrypted_key.key"
SALT = b'secure_static_salt'  # You can randomize and save this if you want more security

def derive_key_from_password(password: str) -> bytes:
    """Derive a Fernet key from a password using PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=sha256(),
        length=32,
        salt=SALT,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_and_save_key(password: str):
    """Generate a Fernet key and encrypt it with a password."""
    key = Fernet.generate_key()
    fernet_key = Fernet(derive_key_from_password(password))
    encrypted_key = fernet_key.encrypt(key)
    with open(KEY_FILE_ENCRYPTED, 'wb') as f:
        f.write(encrypted_key)
    print("[+] Key generated and encrypted successfully.")
    return key

def load_decrypted_key(password: str):
    """Load and decrypt the Fernet key using a password."""
    with open(KEY_FILE_ENCRYPTED, 'rb') as f:
        encrypted_key = f.read()
    fernet_key = Fernet(derive_key_from_password(password))
    try:
        return fernet_key.decrypt(encrypted_key)
    except Exception:
        print("[!] Incorrect password. Cannot decrypt key.")
        return None

def encrypt_file_content(key, input_file="plaintext_data.txt", output_file="encrypted_data.txt"):
    with open(input_file, 'r') as f:
        plaintext = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(plaintext.encode())
    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print(f"[+] File '{input_file}' encrypted and saved as '{output_file}'")

def decrypt_file_content(key, input_file="encrypted_data.txt"):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    print("[+] Decrypted content:\n")
    print(decrypted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt PII file")
    parser.add_argument("--generate-key", action="store_true", help="Generate and encrypt a key with password")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt plaintext_data.txt")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt encrypted_data.txt")

    args = parser.parse_args()

    if args.generate_key:
        password = getpass("Set a shared password for encrypting the key: ")
        encrypt_and_save_key(password)

    elif args.encrypt:
        password = getpass("Enter the shared password to unlock the key: ")
        key = load_decrypted_key(password)
        if key:
            encrypt_file_content(key)

    elif args.decrypt:
        password = getpass("Enter the shared password to unlock the key: ")
        key = load_decrypted_key(password)
        if key:
            decrypt_file_content(key)
