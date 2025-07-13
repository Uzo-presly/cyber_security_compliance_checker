import os
import platform
import shutil
from pathlib import Path
import subprocess

# Define known suspicious extensions
SUSPICIOUS_EXTS = [".exe", ".sh", ".py", ".bat", ".js", ".vbs", ".zip"]

# Auto-detect trash path across OS
def get_trash_path():
    system = platform.system()
    if system == "Linux":
        return Path.home() / ".local/share/Trash/files"
    elif system == "Darwin":  # macOS
        return Path.home() / ".Trash"
    elif system == "Windows":
        return Path(os.environ.get("USERPROFILE", "")) / "Recycle.Bin"
    else:
        raise Exception("Unsupported OS")

# Determine if file/folder is suspicious
def is_suspicious(path: Path):
    if path.is_file() and path.suffix.lower() in SUSPICIOUS_EXTS:
        return True
    if path.is_dir() and any(path.suffix.lower() in SUSPICIOUS_EXTS for path in path.rglob("*")):
        return True
    return False

# Format file size in MB and KB
def format_size(size_bytes):
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    return f"{size_mb:.2f} MB ({size_kb:.1f} KB)"

# Scan and collect suspicious items (files & folders)
def scan_trash(trash_path):
    flagged = []
    for item in trash_path.iterdir():
        try:
            if is_suspicious(item):
                size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file()) if item.is_dir() else item.stat().st_size
                flagged.append((item, format_size(size), "Folder" if item.is_dir() else "File"))
        except Exception as e:
            print(f"⚠️ Error scanning {item}: {e}")
    return flagged

# Move or delete item securely
def handle_item(item: Path, action: str, log_lines: list, secure_delete_cmd="srm -vz"):
    if action == "m":
        vault = Path.home() / "VaultTrashBackup"
        vault.mkdir(parents=True, exist_ok=True)
        shutil.move(str(item), str(vault))
        log_lines.append(f"📦 Moved to vault: {item.name}")
    elif action == "d":
        if platform.system() == "Windows":
            os.remove(item) if item.is_file() else shutil.rmtree(item)
        else:
            try:
                if item.is_dir():
                    subprocess.run(["srm", "-rvz", str(item)], check=True)
                else:
                    subprocess.run(["srm", "-vz", str(item)], check=True)
                log_lines.append(f"🔥 Securely deleted: {item.name}")
            except subprocess.CalledProcessError as e:
                log_lines.append(f"⚠️ Error securely deleting {item.name}: {e}")


# Save log securely
def save_log(log_lines):
    log_dir = Path.home() / "VaultTrashBackup"
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "trash_cleanup_log.txt", "w") as log_file:
        for line in log_lines:
            log_file.write(line + "\n")
    print(f"\n📝 Log saved to: {log_dir / 'trash_cleanup_log.txt'}")

# -------------------------
# 🚀 Main Execution
# -------------------------
def main():
    trash_path = get_trash_path()
    print(f"🧹 Scanning Trash at: {trash_path}\n")

    suspicious = scan_trash(trash_path)
    if not suspicious:
        print("✅ No suspicious files or folders found.")
        return

    print("🚩 Suspicious Items Found:\n")
    for i, (f, size, typ) in enumerate(suspicious, start=1):
        print(f"   {i}. 📄 {f.name} | Type: {typ} | Size: {size}")

    choice = input("\n🔐 Move to vault (m) or 🔥 securely delete (d)? [m/d]: ").strip().lower()
    while choice not in ["m", "d"]:
        choice = input("Please enter 'm' or 'd': ").strip().lower()

    log_lines = []
    for f, _, _ in suspicious:
        handle_item(f, choice, log_lines)

    save_log(log_lines)

if __name__ == "__main__":
    main()

