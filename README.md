 Cybersecurity Compliance Checker (DIY Tools for End-Users)

This repository contains a set of simple, DIY-oriented tools to help individuals, small organizations, and developers improve their cybersecurity hygiene and regulatory compliance.

Each tool focuses on a specific area such as GDPR policy compliance, TLS/SSL validation, basic firewall check awareness, and system hardening hints.

   
	💡 This project reflects my passion to contribute as part of God's creation by making digital protection more accessible to everyday users.

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

For Windows OS Users: If they don’t work, download Python from https://www.python.org/downloads/windows

✅ During install, make sure to check "Add Python to PATH"

To change directory via cmd on a windows-OS PC, so as to execute a script; see the following example:
assuming we are here: 

	c:\Users>

and we want to get to a  path like:

	\Users\mrs Water\Documents\python tools

.., just manually go to that location on your PC, and press SHIFT while you Right-click on the folder containing the intended python scripts to be run,

 a copied path could look like this example:

	\Users\mrs Water\Documents\python tools

.., just go ahead and copy the full path by clicking the 'copy path' on the pop-up box, 

then go back to CMD-page and paste in front pf the prompt using the change directory command (cd):

	c:\Users>

for instance:

	c:\Users>cd c:\Users\mrs Water\Documents\python tools

and presto! you should be ready to run your scripts via CMD. Now go ahead to execute your python scripts

example:

	python users_permission_checker.py

for windows-os users

and 

	python3 users_permission_checker.py

for linux-based users 

However windows-os users should make sure they already have python installed on their windows PCs

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
