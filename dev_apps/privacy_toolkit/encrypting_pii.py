# 1. Sample Python Encryption Script
# ----------------------------------
# This script demonstrates how to encrypt and decrypt sensitive data using Fernet symmetric encryption.
# Use this to encrypt files or sensitive strings like emails, phone numbers, etc.

from cryptography.fernet import Fernet

# Generate and store this key securely!
key = Fernet.generate_key()
cipher = Fernet(key)

# Sample data to encrypt
data = "user@example.com"
print("Original Data:", data)

# Encrypt the data
encrypted = cipher.encrypt(data.encode())
print("Encrypted:", encrypted)

# Decrypt the data
decrypted = cipher.decrypt(encrypted).decode()
print("Decrypted:", decrypted)

