
import os
import argparse
from datetime import datetime
import re

# ======================
# 📌 Define Compliance Patterns Per Framework
# ======================
framework_patterns = {
    "GDPR": [
        (r"personal data", "Mentions handling of personal data"),
        (r"consent", "User consent required"),
        (r"data breach", "Policy for data breach"),
        (r"right to be forgotten", "Right to data erasure")
    ],
    "HIPAA": [
        (r"protected health information", "PHI data handling"),
        (r"covered entity", "Covered entity responsibilities"),
        (r"security rule", "Security Rule compliance"),
        (r"privacy rule", "Privacy Rule compliance")
    ],
    "NDPR": [
        (r"Nigerian Data Protection Regulation", "NDPR compliance mention"),
        (r"data subject", "Refers to individual data subjects"),
        (r"third parties", "Disclosure to third parties"),
        (r"data controller", "Role of data controller defined")
    ]
}

# ======================
# 📁 Process and Analyze Target Text File
# ======================
def analyze_file(file_path, patterns):
    issues_found = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            for pattern, description in patterns:
                if re.search(pattern, content):
                    issues_found.append(f"✅ Found: {description} (Pattern: '{pattern}')")
                else:
                    issues_found.append(f"❌ Missing: {description}")
    except Exception as e:
        issues_found.append(f"⚠️ Error reading {file_path}: {e}")
    return issues_found

# ======================
# 🎯 Main CLI Script Execution
# ======================
def main():
    parser = argparse.ArgumentParser(description="Compliance Analyzer CLI Tool")
    parser.add_argument("--target", required=True, help="Path to file (e.g., sample_policy_hipaa.txt)")
    parser.add_argument("--framework", required=True, choices=framework_patterns.keys(), help="Compliance framework")

    args = parser.parse_args()

    patterns = framework_patterns[args.framework]
    print(f"🔍 Running compliance analysis for: {args.framework}")
    print(f"📄 Target File: {args.target}\n")

    results = analyze_file(args.target, patterns)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("results", exist_ok=True)
    report_path = f"results/report_{args.framework}_{timestamp}.txt"
    with open(report_path, "w") as report_file:
        report_file.write("\n".join(results))

    for line in results:
        print(line)

    print(f"\n📁 Report saved to: {report_path}")

if __name__ == "__main__":
    main()
