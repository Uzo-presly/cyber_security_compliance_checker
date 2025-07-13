# run_code_check.py

import subprocess

def run_code_analysis():
    print("🧪 Running code analysis on target script...")

    try:
        result = subprocess.run(
            [
                "python",
                "cyber_security_proj_runner.py",
                "--target=example_company_papers",
                "--framework=NDPR",
                "--audit-code=example_company_papers/example_problem_code/vulnerable_script.py"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        print("✅ Analysis Output:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("❌ Error while analyzing code:")
        print(e.stderr)

if __name__ == "__main__":
    run_code_analysis()
