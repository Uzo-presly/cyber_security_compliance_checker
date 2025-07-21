import subprocess
import platform
import sys

def check_installed_updates():
    system_type = platform.system()

    if system_type == "Windows":
        print("Listing installed updates on Windows...")
        try:
            result = subprocess.run(["wmic", "qfe", "list", "brief", "/format:table"],
                                    capture_output=True, text=True)
            print(result.stdout)
        except FileNotFoundError:
            print("'wmic' command not found. Make sure it's available on your Windows system.")
    
    elif system_type == "Linux":
        print("Listing installed packages on Linux...")
        try:
            # Try dpkg log for installed packages
            result = subprocess.run(["grep", "install", "/var/log/dpkg.log"],
                                    capture_output=True, text=True)
            print(result.stdout or "No recent installs found in dpkg log.")
        except FileNotFoundError:
            print("'/var/log/dpkg.log' not found. Try using 'apt list --installed' instead.")
        except Exception as e:
            print(f"Error checking Linux updates: {e}")
    
    else:
        print(f"Unsupported OS: {system_type}")
        sys.exit(1)

if __name__ == "__main__":
    check_installed_updates()
