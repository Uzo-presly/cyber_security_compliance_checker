import os
import winshell
import subprocess

# Set your suspicious file extensions here
SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.scr', '.vbs', '.ps1']

def is_suspicious(file_path):
    return any(file_path.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS)

def secure_delete(file_path):
    try:
        subprocess.run(['sdelete64.exe', '-accepteula', '-s', file_path], check=True)
        print(f"✅ Securely deleted: {file_path}")
    except Exception as e:
        print(f"❌ Failed to delete {file_path}: {e}")

def scan_recycle_bin():
    print("🔍 Scanning Recycle Bin...")
    for item in winshell.recycle_bin():
        file_path = item.filename()

        print(f"\n📁 Found: {file_path}")
        if is_suspicious(file_path):
            print("⚠️ SUSPICIOUS file detected!")
        else:
            choice = input("🗑️ Do you want to securely delete this file? (y/n): ").strip().lower()
            if choice == 'y':
                secure_delete(file_path)
            else:
                print(f"🛑 Kept: {file_path}")

if __name__ == "__main__":
    scan_recycle_bin()
