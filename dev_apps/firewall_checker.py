import platform
import subprocess
import shutil

def check_windows_firewall():
    print("🛡️ Checking Windows Firewall status...")
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("❌ 'netsh' command not found. Are you sure this is a Windows machine?")
    except subprocess.CalledProcessError as e:
        print("⚠️ Error occurred while running netsh:", e)


def check_linux_firewall():
    print("🛡️ Checking Linux Firewall (UFW) status...")

    if shutil.which("ufw") is None:
        print("❌ UFW (Uncomplicated Firewall) is not installed.")
        return

    try:
        # Try without sudo first
        result = subprocess.run(["ufw", "status"], capture_output=True, text=True)
        output = result.stdout.strip()

        if "inactive" in output.lower():
            print("❌ Firewall is OFF")
        elif "active" in output.lower():
            print("✅ Firewall is ON")
        else:
            print("🔁 Retrying with sudo...")

            # Try again with sudo
            result = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
            output = result.stdout.strip()

            if "inactive" in output.lower():
                print("❌ Firewall is OFF")
            elif "active" in output.lower():
                print("✅ Firewall is ON")
            else:
                print("❓ Unable to determine firewall status.")

    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

def main():
    os_type = platform.system()
    print(f"🖥️ Detected OS: {os_type}")

    if os_type == "Windows":
        check_windows_firewall()
    elif os_type == "Linux":
        check_linux_firewall()
    else:
        print("❌ Unsupported operating system.")

if __name__ == "__main__":
    main()
 


