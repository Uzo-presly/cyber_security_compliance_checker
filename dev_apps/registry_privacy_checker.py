import winreg

def check_registry_value(path, name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except Exception as e:
        return f"Error: {e}"

def check_privacy_settings():
    print("🔐 Checking registry privacy keys...")
    checks = [
        ("SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry"),
        ("SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled"),
        ("SOFTWARE\Policies\Microsoft\Windows\CloudContent", "DisableConsumerFeatures")
    ]
    for path, key in checks:
        print(f"{key}: {check_registry_value(path, key)}")

if __name__ == "__main__":
    check_privacy_settings()
