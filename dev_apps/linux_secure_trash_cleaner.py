import os
import time
import shutil
from pathlib import Path
import subprocess

TRASH_PATH = Path.home() / ".local/share/Trash/files"
SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.scr', '.vbs', '.sh']

def is_suspicious(file_path):
    return any(file_path.name.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS)

def shred_file(file_path):
    try:
        subprocess.run(['shred', '--remove', '--zero', '--verbose', file_path], check=True)
        print(f"✅ Shredded: {file_path}")
    except Exception as e:
        print(f"❌ Failed to shred {file_path}: {e}")

def process_trash():
    if not TRASH_PATH.exists():
        print("🚫 Trash folder does not exist.")
        return

    files = list(TRASH_PATH.iterdir())
    if not files:
        print("🧼 Trash is already empty.")
        return

    for file in files:
        if is_suspicious(file):
            print(f"⚠️ SUSPICIOUS FILE FOUND: {file.name}")
        else:
            print(f"📄 Non-suspicious file: {file.name}")
            choice = input("Do you want to securely delete it? (y/n): ").strip().lower()
            if choice == 'y':
                shred_file(str(file))
            else:
                print(f"🛑 Skipped: {file.name}")

if __name__ == "__main__":
    process_trash()
