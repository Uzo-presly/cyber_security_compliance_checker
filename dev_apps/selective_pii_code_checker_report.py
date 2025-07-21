import os
import re
import argparse
import sys

# Define regex patterns for PII
PII_PATTERNS = {
    "Email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "Phone Number": r'\b(?:\+234|0)[789][01]\d{8}\b',
    "NIN": r'\b\d{11}\b',
    "BVN": r'\b\d{11}\b',
    "IP Address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
}

MAX_FILE_SIZE_MB = 5
SKIP_EXTENSIONS = ['.bundle.js', '.png', '.jpg', '.jpeg', '.svg', '.ico']

# File filters
def should_skip(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if any(file_path.endswith(skip) for skip in SKIP_EXTENSIONS):
        return True
    if os.path.getsize(file_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
        return True
    return False

def scan_file(file_path, verbose=False):
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pii_type, pattern in PII_PATTERNS.items():
                found = re.findall(pattern, content)
                if found:
                    matches.append((pii_type, len(found), file_path))
                    if verbose:
                        print(f"🔎 Found {pii_type} in {file_path}: {len(found)} match(es)")
    except Exception as e:
        if verbose:
            print(f"⚠️ Error reading file: {file_path} -> {e}")
    return matches

def main(target_dir, verbose=False):
    all_matches = []
    scanned_count = 0
    skipped_count = 0

    print(f"\n🔍 Verbose scan started in folder: {target_dir}\n")

    try:
        for root, _, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)

                if should_skip(filepath):
                    skipped_count += 1
                    if verbose:
                        print(f"⏩ Skipping file: {filepath}")
                    continue

                if verbose:
                    print(f"📄 Scanning file: {filepath}")

                scanned_count += 1
                findings = scan_file(filepath, verbose)
                all_matches.extend(findings)

    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user.\n")

    print(f"\n📊 Summary:")
    print(f"✅ Files scanned: {scanned_count}")
    print(f"🚫 Files skipped: {skipped_count}")
    print(f"🔐 PII Findings: {len(all_matches)}\n")

    for pii_type, count, path in all_matches:
        print(f"🔎 {pii_type} ({count} match(es)) in → {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PII Scanner with Regex and Verbose Logging")
    parser.add_argument("--target", required=True, help="Target directory to scan")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    main(args.target, args.verbose)
