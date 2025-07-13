import os
import platform
import stat

def check_access_control():
    print("📁 Checking file/folder access permissions...")

    if platform.system() == "Windows":
        targets = ["C:/Users/Public", os.path.expanduser("~")]
    else:  # Linux/macOS
        targets = ["/home", os.path.expanduser("~")]

    for path in targets:
        try:
            mode = os.stat(path).st_mode
            perms = stat.filemode(mode)
            print(f"✅ {path} - Mode: {oct(mode)} ({perms})")
        except Exception as e:
            print(f"❌ {path} - Error: {e}")

if __name__ == "__main__":
    check_access_control()
