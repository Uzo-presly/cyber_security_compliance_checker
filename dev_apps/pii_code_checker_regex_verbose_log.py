# pii_code_checker_regex_verbose_log.py

import os
import re
import argparse
from datetime import datetime

# Define PII patterns
patterns = {
    "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "NIN": r"\b[0-9]{11}\b",
    "Phone": r"\b(?:\+234|0)[789][01]\d{8}\b",
    "Names (Title)": r"\b(Mr|Mrs|Miss|Dr|Engr|Prof)\.?\s+[A-Z][a-z]+\b"
}

# Allowed file types
target_extensions = ('.html', '.js', '.txt')

# Create timestamped log file
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = f'pii_scan_log_{timestamp}.txt'

def write_log(message):
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(message + '\n')

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            findings = {}
            for label, pattern in patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    findings[label] = matches
            return findings
    except Exception as e:
        err = f"❌ Error reading {filepath}: {e}"
        print(err)
        write_log(err)
        return {}

def main(target_folder):
    print(f"\n🔍 Verbose scan started in folder: {target_folder}")
    write_log(f"🔐 PII Scan Log - {timestamp}")
    write_log(f"Scanning path: {target_folder}\n")

    for root, _, files in os.walk(target_folder):
        for file in files:
            if file.endswith(target_extensions):
                filepath = os.path.join(root, file)
                print(f"📄 Scanning file: {filepath}")
                write_log(f"\n📄 {filepath}")

                findings = scan_file(filepath)

                if findings:
                    print("🔴 PII Found:")
                    write_log("🔴 PII Found:")
                    for key, values in findings.items():
                        result_line = f"  - {key}: {list(set(values))[:5]}"
                        print(result_line)
                        write_log(result_line)
                    print("—" * 40)
                    write_log("—" * 40)
                else:
                    print("✅ No PII found in this file.\n")
                    write_log("✅ No PII found.")

    print(f"\n📁 Scan complete. Log saved to: {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔐 PII Regex Scanner (Verbose + Log)")
    parser.add_argument("--target", required=True, help="Target folder or domain to scan")
    args = parser.parse_args()
    main(args.target)
