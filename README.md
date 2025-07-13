 Cybersecurity Compliance Checker (DIY Tools for End-Users)

This repository contains a set of simple, DIY-oriented tools to help individuals, small organizations, and developers improve their cybersecurity hygiene and regulatory compliance.

Each tool focuses on a specific area such as GDPR policy compliance, TLS/SSL validation, basic firewall check awareness, and system hardening hints.

    💡 "These tools reflect my passion to contribute as part of God's creation by making digital protection more accessible to everyday users." — Uzochi Presly

📁 Table of Contents

    Getting Started

    Tools & Scripts

        1. https_tls_flexible_scanner.py

        2. run_gdpr_ai_v2.py

        3. (More scripts…)

    Requirements

    How to Contribute

    License

🧰 Getting Started

    Clone the repository:

git clone https://github.com/your-username/cyber_security_compliance_checker.git
cd cyber_security_compliance_checker

Create and activate a virtual environment:

python3 -m venv myvenv
source myvenv/bin/activate

Install dependencies:

    pip install -r requirements.txt

🔧 Tools & Scripts
1. https_tls_flexible_scanner.py

✅ Purpose:
Check if a website or server uses secure TLS protocols and identify weak cipher suites.

✅ Usage:

python https_tls_flexible_scanner.py --host example.com --port 443

✅ Output:
Reports TLS version, certificate expiry, and any insecure protocols.
2. run_gdpr_ai_v2.py

✅ Purpose:
AI-powered checker that compares a company’s data policy with the full GDPR framework.

✅ Usage:

python run_gdpr_ai_v2.py \
  --policy path/to/policy.txt \
  --regulation path/to/gdpr_framework.txt \
  --save \
  --verbose

✅ Features:

    Loads .txt or .pdf files for both regulation and policy.

    Uses OpenAI’s API to highlight missing items and non-compliance.

    Saves the report to the results/ folder.

📝 Note: Requires OPENAI_API_KEY to be set in a .env file.
3. (More scripts…)

As new scripts are added, include them here with brief explanation and usage examples.
📦 Requirements

    Python 3.8+

    OpenAI Python SDK (openai)

    python-dotenv

    PyPDF2

You can install all dependencies via:

pip install -r requirements.txt

🤝 How to Contribute

    Open an issue for bugs, improvements, or regulatory framework suggestions.

    Fork and submit a pull request if you'd like to add a script.

    Community roadmap will be maintained in ROADMAP.md (coming soon).

This project is a modular Python-based toolkit that shall also help you scan and analyze codebases, system settings,
 and policies for compliance with various data protection frameworks:

- ✅ **GDPR**
- ✅ **HIPAA**
- ✅ **NDPR**
- ✅ **NIST**

Road Map:
Expected scripts that:
- 🔐 Perform firewall checks--	-	-Done
- 🔍 Run static code scans--	-	-Done
- 📊 Perform compliance analysis-	-On-going
- 🧠 Leverage AI (via OpenAI API) to reason about policies-	-On-going
- Check if a website or server uses secure TLS protocols and identify weak cipher suites.-	-Done
- Securely clean recycle bin /Trash-	-Done
