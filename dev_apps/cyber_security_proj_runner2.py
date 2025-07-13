import json
import subprocess
from datetime import datetime
import os
from dotenv import load_dotenv

# ✅ Load .env variables
load_dotenv()

def run_module(script_name, label, enabled, output_lines, args=None, env_vars=None, verbose=False):
    if enabled:
        output_lines.append(f"✅ [RUNNING] {label}")
        try:
            command = ["python", script_name] + (args if args else [])
            if verbose:
                print(f"👉 Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=not verbose,
                text=True,
                env={**os.environ, **(env_vars or {})}
            )
            output_lines.append(result.stdout.strip() if not verbose else "")
        except Exception as e:
            output_lines.append(f"❌ Error running {label}: {e}")
    else:
        output_lines.append(f"❌ [SKIPPED] {label}")


def main():
    with open("config.json") as f:
        config = json.load(f)

    output_lines = ["\n🔐 Compliance Analyzer v2 Results\n"]

    # Use centralized common arguments
    common_args = [
        "--target", config["policy_compliance_target"],
        "--framework", config["policy_compliance_framework"],
        "--reasoning"
    ]

    env = {"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")}

    # Run tools one by one
    run_module("https_tls_scanner.py", "TLS / HTTPS Scanner", config.get("run_tls_scan"), output_lines, args=[
        "--host", config.get("tls_host", "example.com"),
        "--port", str(config.get("tls_port", 443))
    ])

    verbose = config.get("verbose", False)
    run_module("user_permissions_checker.py", "Access Control Checker", config.get("run_access_control"), output_lines, verbose=verbose)
    run_module("win_event_log_analyzer.py", "Windows Event Log Analyzer", config.get("run_event_log"), output_lines, verbose=verbose)
    run_module("check_windows_firewall.py", "Firewall Check", config.get("run_firewall_check"), output_lines, verbose=verbose)
    run_module("system_patch_checker.py", "Patch Checker", config.get("run_patch_check"), output_lines, verbose=verbose)
    run_module("registry_privacy_checker.py", "Registry Privacy Checker", config.get("run_registry_check"), output_lines, verbose=verbose)

    run_module("run_gdpr.py", "GDPR Compliance", config.get("run_gdpr_check"), output_lines, args=common_args, env_vars=env, verbose=verbose)
    run_module("run_hipaa.py", "HIPAA Compliance", config.get("run_hipaa_check"), output_lines, args=common_args, env_vars=env, verbose=verbose)
    run_module("run_ndpr.py", "NDPR Compliance", config.get("run_ndpr_check"), output_lines, args=common_args, env_vars=env, verbose=verbose)
    run_module("run_nist.py", "NIST Compliance", config.get("run_nist_check"), output_lines, args=common_args, env_vars=env)
    run_module("codes_checker.py", "Vulnerable Code Checker", config.get("run_vulnerable_code_check"), output_lines, args=common_args, env_vars=env, verbose=verbose)

    run_module("run_dashboard_dynamic.py", "Dashboard of Four Frameworks", config.get("run_for_cybersecurity_regulatory_policy"), output_lines, verbose=verbose)

    run_module("policy_compliance_checker.py", "OpenAI Policy Compliance Checker", config.get("check_compliance_with_openai"), output_lines, args=common_args, env_vars=env, verbose=verbose)

    report = "\n".join(output_lines)
    print(report)

    if config.get("save_output_to_file"):
        os.makedirs("results", exist_ok=True)
        filename = f"results/compliance_report_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(filename, "w") as f:
            f.write(report)
        print(f"📁 Output saved to: {filename}")

if __name__ == "__main__":
    main()
