import argparse
import os
import re
from PyPDF2 import PdfReader

FRAMEWORK_DIR = os.path.join(os.path.dirname(__file__), "frameworks")

def extract_keywords_from_pdf(pdf_path):
    keywords = set()
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                for word in re.findall(r"\b\w{5,}\b", text.lower()):
                    keywords.add(word)
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
    return list(keywords)

def extract_keywords_from_txt(txt_path):
    keywords = set()
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                for word in re.findall(r"\b\w{5,}\b", line.lower()):
                    keywords.add(word)
    except Exception as e:
        print(f"❌ Error reading {txt_path}: {e}")
    return list(keywords)

def load_framework_rules(framework_name):
    framework_map = {
        "HIPAA": "hipaa-simplification-201303.pdf",
        "NDPR": "NDPR-Implementation-Framework.pdf",
        "NIST": "nist_full.txt",
        "GDPR": "gdpr_framework.txt"
    }

    file_name = framework_map.get(framework_name.upper())
    if not file_name:
        print(f"❌ Unsupported framework: {framework_name}")
        return {}

    path = os.path.join(FRAMEWORK_DIR, file_name)

    if file_name.endswith(".pdf"):
        keywords = extract_keywords_from_pdf(path)
    else:
        keywords = extract_keywords_from_txt(path)

    print(f"📚 Loaded {len(keywords)} keywords from {framework_name}")
    return {
        "RULES": keywords
    }

def scan_file_for_violations(file_path, rules):
    violations = []
    rule_keywords = rules.get("RULES", [])
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                for keyword in rule_keywords:
                    if keyword in line.lower():
                        violations.append(f"⚠️ Line {lineno}: '{keyword}' found in {file_path}")
    except Exception as e:
        print(f"❌ Failed to scan {file_path}: {e}")
    return violations

def main():
    parser = argparse.ArgumentParser(description="Run cybersecurity audit on company files.")
    parser.add_argument("--target", required=True, help="Target directory with company files")
    parser.add_argument("--framework", required=True, help="Regulatory framework (e.g., NDPR, HIPAA, NIST, GDPR)")
    args = parser.parse_args()

    print(f"🔍 Scanning files in '{args.target}' against '{args.framework.upper()}' rules...\n")

    rules = load_framework_rules(args.framework)

    if not rules:
        print("❌ No rules loaded. Aborting scan.")
        return

    for root, _, files in os.walk(args.target):
        for file in files:
            file_path = os.path.join(root, file)
            violations = scan_file_for_violations(file_path, rules)
            if violations:
                print(f"\n🚨 Violations in {file}:\n" + "\n".join(violations))
            else:
                print(f"✅ No violations in {file}")

if __name__ == "__main__":
    main()
