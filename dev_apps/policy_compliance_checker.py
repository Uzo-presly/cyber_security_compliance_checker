# policy_compliance_checker.py

import os
import argparse
from datetime import datetime
import re
import openai
import subprocess
from dotenv import load_dotenv

# =========================
# 🔐 Load OpenAI API Key
# =========================
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# =========================
# 📌 Compliance Patterns
# =========================
framework_patterns = {
    "GDPR": [
        (r"personal data", "Mentions handling of personal data"),
        (r"consent", "User consent required"),
        (r"data breach", "Policy for data breach"),
        (r"right to be forgotten", "Right to data erasure"),
        {"id": "GDPR001", "desc": "Avoid storing personal data in plaintext", "pattern": r"store_data\s*\(.+?\)"}
    ],
    "HIPAA": [
        (r"protected health information", "PHI data handling"),
        (r"covered entity", "Covered entity responsibilities"),
        (r"security rule", "Security Rule compliance"),
        (r"privacy rule", "Privacy Rule compliance"),
        {"id": "HIPAA001", "desc": "Avoid logging medical data", "pattern": r"log\s*\(.+medical.+\)"}
    ],
    "NDPR": [
        (r"Nigerian Data Protection Regulation", "NDPR compliance mention"),
        (r"data subject", "Refers to individual data subjects"),
        (r"third parties", "Disclosure to third parties"),
        (r"data controller", "Role of data controller defined"),
        {"id": "NDPR001", "desc": "Avoid unsecured personal data", "pattern": r"save_unencrypted\s*\("}
    ],
    "NIST": [
        (r"eval\(", "Avoid use of eval() for security reasons"),
        (r"exec\(", "Avoid use of exec()"),
        {"id": "NIST001", "desc": "Avoid hardcoded passwords", "pattern": r"password\s*=\s*['\"]\w+['\"]"}
    ]
}

# =========================
# 📁 Analyze Target File
# =========================
def analyze_file(file_path, patterns):
    issues_found = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            for p in patterns:
                pattern, desc = (p["pattern"], p["desc"]) if isinstance(p, dict) else p
                if re.search(pattern, content):
                    issues_found.append(f"✅ Found: {desc} (Pattern: '{pattern}')")
                else:
                    issues_found.append(f"❌ Missing: {desc}")
    except Exception as e:
        issues_found.append(f"⚠️ Error reading file: {e}")
    return issues_found

# =========================
# 🧠 Ask GPT for Reasoning
# =========================
def ask_openai_for_reasoning(results, framework):
    print("🤖 Contacting OpenAI for deeper reasoning...")
    joined_findings = "\n".join(results)
    prompt = (
        f"As a compliance expert, analyze the following findings for the {framework} framework.\n\n"
        f"{joined_findings}\n\n"
        "Give your verdict on whether this code is compliant, and explain why."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity compliance auditor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error while querying OpenAI: {e}"

# =========================
# 💾 Save Report to File
# =========================
def save_report(results, framework):
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"results/{framework.lower()}_report_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"📋 Compliance Report for: {framework}\n")
        f.write(f"🕒 Generated on: {datetime.now()}\n\n")
        f.write("\n".join(results))
    return filename

# =========================
# 🎯 Main CLI Entry Point
# =========================
def main():
    parser = argparse.ArgumentParser(description="Compliance Analyzer with GPT")
    parser.add_argument("--target", required=True, help="Path to the policy or code file")
    parser.add_argument("--framework", required=True, choices=framework_patterns.keys(), help="Framework to check against")
    parser.add_argument("--reasoning", action="store_true", help="Include GPT-based reasoning")

    args = parser.parse_args()
    print(f"🔍 Scanning file: {args.target} against {args.framework}...")

    patterns = framework_patterns[args.framework]
    results = analyze_file(args.target, patterns)

    if args.reasoning:
        explanation = ask_openai_for_reasoning(results, args.framework)
        results.append("\n🧠 GPT-4 Explanation:\n" + explanation)

    report_file = save_report(results, args.framework)

    for line in results:
        print(line)
    print(f"\n📁 Saved to: {report_file}")

if __name__ == "__main__":
    main()
