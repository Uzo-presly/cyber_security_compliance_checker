import argparse
from datetime import datetime
import os
from dotenv import load_dotenv
import openai
import PyPDF2

# ✅ Load environment variables (must contain OPENAI_API_KEY)
load_dotenv(dotenv_path="/home/uzochi/protectedVault/mountpoint/cyber_security_compliance_checker/.env")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_file(path, verbose=False):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    if verbose:
        print(f"📄 Loading file: {path}")

    if path.lower().endswith('.pdf'):
        text = ""
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise RuntimeError(f"⚠️ Error reading PDF: {e}")
        return text

    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def compare_with_ai(gdpr_text, company_policy_text):
    prompt = f"""
You are a compliance assistant. Compare the following company policy against the GDPR regulation.
Highlight non-compliance, missing elements, and offer improvements.

GDPR Regulation:
{gdpr_text[:4000]}

Company Policy:
{company_policy_text[:4000]}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a cybersecurity compliance assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="🧠 AI-Powered GDPR Compliance Checker")
    parser.add_argument("--policy", required=True, help="Path to the company policy file")
    parser.add_argument("--regulation", default="gdpr_framework.txt", help="Path to the full GDPR regulation file")
    parser.add_argument("--save", action="store_true", help="Save output to file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.verbose:
        print("\n🛠️  AI GDPR Compliance Checker Running with verbose output...\n")

    try:
        gdpr_text = load_file(args.regulation, verbose=args.verbose)
        company_policy_text = load_file(args.policy, verbose=args.verbose)

        print("🔍 Analyzing policy compliance using AI...\n")
        result = compare_with_ai(gdpr_text, company_policy_text)

        print("\n📋 AI Feedback:\n")
        print(result)

        if args.save:
            os.makedirs("results", exist_ok=True)
            filename = f"results/gdpr_ai_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, "w") as f:
                f.write(result)
            print(f"\n✅ Report saved to: {filename}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
