import os
import re
import openai  # Requires `openai` library. Install with: pip install openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store your key in a .env file as OPENAI_API_KEY


def analyze_with_llm(file_path):
    """Uses OpenAI GPT to detect potential privacy violations in the document."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    You are a cybersecurity assistant. Review the following document for any potential privacy or data protection violations 
    based on GDPR or HIPAA standards. Identify mentions of personal identifiable information (PII) such as full names, phone numbers,
    medical records, email addresses, or passwords and determine whether they are exposed inappropriately.

    Provide a list of flagged issues and categorize each under:
      - PII Exposure
      - Lack of Consent
      - Credential Leakage
      - Other

    Document:
    -----------
    {content}
    -----------
    """

    print("\n\n[INFO] Sending content to AI for analysis...\n")

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use gpt-3.5-turbo if gpt-4 is unavailable
        messages=[
            {"role": "system", "content": "You are a cybersecurity assistant helping with compliance auditing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    findings = response["choices"][0]["message"]["content"]
    return findings


if __name__ == "__main__":
    test_file = "finance_report.txt"  # Ensure this file exists in the same directory

    if not os.path.exists(test_file):
        print(f"[ERROR] File '{test_file}' not found. Please ensure it exists.")
        exit(1)

    results = analyze_with_llm(test_file)

    print("\n\n========== AI-Based Audit Results ==========")
    print(results)
