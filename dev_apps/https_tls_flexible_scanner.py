import ssl
import socket
import argparse

# 🧠 Parse command-line arguments
parser = argparse.ArgumentParser(description="TLS Certificate Scanner")
parser.add_argument("--host", type=str, default="example.com", help="Target host (domain)")
parser.add_argument("--port", type=int, default=443, help="Port number (default: 443)")
args = parser.parse_args()

def scan_tls(host, port):
    print(f"🔍 Scanning TLS for {host}:{port}")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                print("✅ TLS Certificate Details:\n")
                for key, value in cert.items():
                    print(f"🔹 {key}: {value}")
    except Exception as e:
        print(f"❌ TLS Scan Failed: {e}")

if __name__ == "__main__":
    scan_tls(args.host, args.port)
