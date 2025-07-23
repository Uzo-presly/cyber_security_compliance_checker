# encrypting_pii.py

import argparse
from cryptography.fernet import Fernet
from getpass import getpass

def generate_key(outfile='pii_access.key'):
    """Generate a new Fernet key and save it to a file."""
    key = Fernet.generate_key()
    with open(outfile, 'wb') as keyfile:
        keyfile.write(key)
    print(f"[+] Key generated and saved to '{outfile}'.")

def load_key(keyfile='pii_access.key'):
    """Load a key from file, or prompt user to paste it."""
    try:
        with open(keyfile, 'rb') as kf:
            return kf.read()
    except FileNotFoundError:
        print(f"[!] '{keyfile}' not found.")
        key_input = getpass("[?] Paste your decryption key: ").encode()
        return key_input

def encrypt_data(data, key, outfile):
    """Encrypt data using Fernet key and save to file."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    with open(outfile, 'wb') as f:
        f.write(encrypted)
    print(f"[+] Data encrypted and saved to '{outfile}'.")

def decrypt_data(key, infile):
    """Decrypt data using Fernet key and print to screen."""
    fernet = Fernet(key)
    with open(infile, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        print(f"\n[+] Decrypted content:\n{decrypted.decode()}")
    except Exception as e:
        print(f"[!] Decryption failed: {e}")

def encrypt_file(key, infile, outfile):
    """Encrypt content of an entire file (plaintext)."""
    with open(infile, 'r') as f:
        data = f.read()
    encrypt_data(data, key, outfile)

parser = argparse.ArgumentParser(description="PII Encryption Tool")

parser.add_argument('--generate-key', action='store_true', help="Generate and save encryption key.")
parser.add_argument('--encrypt', type=str, help="PII string to encrypt.")
parser.add_argument('--encrypt-file', type=str, help="Plaintext file to encrypt.")
parser.add_argument('--outfile', type=str, default='encrypted_data.txt', help="Output file to save encrypted data.")
parser.add_argument('--decrypt-from', type=str, help="File containing encrypted data to decrypt.")
parser.add_argument('--keyfile', type=str, default='pii_access.key', help="Optional key file.")

args = parser.parse_args()
key = None

if args.generate_key:
    generate_key(outfile=args.keyfile)

elif args.encrypt:
    key = load_key(args.keyfile)
    encrypt_data(args.encrypt, key, args.outfile)

elif args.encrypt_file:
    key = load_key(args.keyfile)
    encrypt_file(key, args.encrypt_file, args.outfile)

elif args.decrypt_from:
    key = load_key(args.keyfile)
    decrypt_data(key, args.decrypt_from)

else:
    print("[!] No action provided. Use --help to see options.")
