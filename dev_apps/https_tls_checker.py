# https_tls_scanner_simple.py

import ssl
import socket

def scan_tls(hostname):
    print(f"\n🔍 Scanning TLS settings for: {hostname}")

    # Use default TLS settings
    context = ssl.create_default_context()

    # Connect to the host via HTTPS (port 443)
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Print secure connection info
                print("✅ Connected securely!")
                print(f"   🔒 TLS version: {ssock.version()}")
                print(f"   🔐 Cipher used: {ssock.cipher()}")
    except socket.gaierror:
        print("❌ Error: Hostname could not be resolved.")
    except socket.timeout:
        print("❌ Error: Connection timed out.")
    except ssl.SSLError as e:
        print(f"❌ SSL Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# === Main program ===
if __name__ == "__main__":
    print("🌐 Simple HTTPS/TLS Scanner")
    site = input("Enter a website (without 'https://'): ").strip()

    # Remove www. if user accidentally types https:// or www.
    site = site.replace("https://", "").replace("http://", "").replace("www.", "")

    if site:
        scan_tls(site)
    else:
        print("⚠️ You must enter a valid website name.")
