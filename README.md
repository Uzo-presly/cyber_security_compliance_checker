 Cybersecurity Compliance Checker (DIY Tools for End-Users)

This repository contains a set of simple, DIY-oriented tools to help individuals, small organizations, and developers improve their cybersecurity hygiene and regulatory compliance.

Each tool focuses on a specific area such as GDPR policy compliance, TLS/SSL validation, basic firewall check awareness, and system hardening hints.

   
 💡 "These project reflects my passion to contribute as part of God's creation by making digital protection more accessible to everyday users." — Uzochi Presly

You are looking at largely, a Python-based toolkit primarily to help users scan and analyze codebases, system settings,
 and policies for compliance with various data protection frameworks:

- ✅ **GDPR**
- ✅ **HIPAA**
- ✅ **NDPR**
- ✅ **NIST**

📁 Table of Contents
	
	# Getting Started

	Tools & Scripts

        1. cyber_audit_files_for_regulators.py 

        2. user_account_checker_extended.py

        3. (More scripts…)

	Requirements

	How to Contribute

	License

🧰 Getting Started

    Clone the repository:

git clone https://github.com/uzo-presly/cyber_security_compliance_checker.git
cd cyber_security_compliance_checker

Create and activate a virtual environment:

python3 -m venv myvenv
source myvenv/bin/activate

Install dependencies:

    pip install -r requirements.txt

🔧 Tools & Scripts
Beside almost each python script, is a .txt file with a detailed explanation of its purpose and usage.


📦 Requirements

    Python 3.8+

    OpenAI Python SDK (openai)

    python-dotenv

    PyPDF2   etc.

You can install all dependencies via:

pip install -r requirements.txt



How to Install pywin32 on Your Windows PC
🔧 Step-by-Step:

    Open CMD (Command Prompt)
        Press Windows + R
        Type cmd
        Press Enter
        (Alternatively, you can right-click and select "Run as administrator" to be safe.)
    Check that Python and pip are installed

python --version
pip --version

If both work and return versions like Python 3.10.11, proceed.

If they don’t work, download Python from https://www.python.org/downloads/windows

✅ During install, make sure to check "Add Python to PATH"

To change directory on cmd on windows so as to execute a file, see the following example:
assuming we are here 

c:\Users>

and we want to get to a  path like

 \Users\mrs Water\Documents\python tools

manually go to the location, and press shift while you right-click on the folder of the intended python files to execute,

 like \Users\mrs Water\Documents\python tools

and copy the full path
then go back to cmd box and paste in the path in front of
 c:\Users>

for instance:

c:\Users>cd c:\Users\mrs Water\Documents\python tools

and presto! you should be there. Now go ahead to execute your python file

example python win_event_log_analyzer.py

However make sure you already have python installed on your windows pc
    Install pywin32

pip install pywin32

This will download and install the required modules from the Python Package Index (PyPI).

🔎 How to Confirm It Worked

After install, run:

python
>>> import win32evtlog
>>> import win32api
>>> exit()

If you see no errors, you're ready to run the scripts like:

python win_event_log_analyzer.py

🤝 How to Contribute

    Open an issue for bugs, improvements, or regulatory framework suggestions.

    Fork and submit a pull request if you'd like to add a script.

    Community roadmap will be maintained in ROADMAP.md (coming soon).

Road Map:

Expected scripts that:

- 🔐 Perform firewall checks--	-	-Done

- 🔍 Run static code scans--	-	-Done

- 📊 Perform compliance analysis-	-On-going

- 🧠 Leverage AI (via OpenAI API) to reason about policies-	-On-going

- Check if a website or server uses secure TLS protocols and identify weak cipher suites.-	-Done

- Securely clean recycle bin /Trash-	-Done
