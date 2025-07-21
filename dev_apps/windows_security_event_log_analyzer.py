import platform
import subprocess

# Windows imports (only if running on Windows)
try:
    import win32evtlog
except ImportError:
    win32evtlog = None

def analyze_windows_security_logs(server='localhost'):
    print("🔍 Analyzing Windows Security Log...")
    if win32evtlog is None:
        print("❌ win32evtlog module not available. Are you running on Windows?")
        return
    try:
        hand = win32evtlog.OpenEventLog(server, 'Security')
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        print(f"🧾 Total Security Events: {total}")
    except Exception as e:
        print(f"⚠️ Error reading Windows logs: {e}")

def analyze_linux_security_logs():
    print("🔍 Analyzing Linux Security Log...")

    try:
        # Try using journalctl if available
        result = subprocess.run(['which', 'journalctl'], capture_output=True, text=True)
        if result.stdout.strip():
            # journalctl is available
            log_output = subprocess.run(
                ['journalctl', '-q', '-n', '20', '_SYSTEMD_UNIT=systemd-logind.service'],
                capture_output=True, text=True)
            print("📄 Recent security-related logins (last 20):")
            print(log_output.stdout.strip() or "🕳️ No recent login logs found.")
        else:
            # Fall back to /var/log/auth.log
            print("📂 Using /var/log/auth.log...")
            with open('/var/log/auth.log', 'r') as f:
                lines = f.readlines()[-20:]
                for line in lines:
                    print("📄", line.strip())
    except FileNotFoundError:
        print("❌ Could not find /var/log/auth.log or journalctl")
    except Exception as e:
        print(f"⚠️ Error reading Linux logs: {e}")

def detect_os_and_analyze_logs():
    os_name = platform.system()
    print(f"🖥️ Detected OS: {os_name}")
    if os_name == "Windows":
        analyze_windows_security_logs()
    elif os_name == "Linux":
        analyze_linux_security_logs()
    else:
        print("❌ Unsupported OS")

if __name__ == "__main__":
    detect_os_and_analyze_logs()
