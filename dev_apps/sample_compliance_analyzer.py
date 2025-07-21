# compliance_analyzer_cli.py

import argparse
import time
import json
import os
from datetime import datetime
from rich.console import Console
from rich.progress import track
from rich.live import Live
from rich.table import Table
from pathlib import Path
import schedule
import threading
import openai

# === CONFIG ===
openai.api_key = os.getenv("OPENAI_API_KEY")

console = Console()

# Simulated or AI-analyzed scan result data
SIMULATED_RESULTS = {
    "privacy_policy": [
        {"item": "Legal basis for data processing", "status": "✓"},
        {"item": "Data portability clause", "status": "✗"},
        {"item": "Retention policy", "status": "✗"},
    ],
    "web_config": [
        {"item": "HTTPS enforced", "status": "✓"},
        {"item": "CSP header", "status": "✗"},
        {"item": "CORS policy", "status": "✗"},
    ],
    "app_code": [
        {"item": "Password hashing with bcrypt", "status": "✓"},
        {"item": "Input validation (email)", "status": "✗"},
    ]
}


def ai_policy_analysis(policy_text):
    prompt = f"""
You are a cybersecurity compliance assistant. Analyze the following privacy policy text against GDPR Articles 12-22.
Return a list of strengths and gaps in the policy in bullet points.

Policy Text:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt + policy_text}]
    )
    return response.choices[0].message['content']


def simulate_scan():
    console.print("\n[bold cyan]Running Compliance Analyzer...[/bold cyan]\n")
    results = {}
    for section, checks in track(SIMULATED_RESULTS.items(), description="[green]Scanning modules..."):
        time.sleep(1)
        results[section] = checks
    return results


def display_results(results):
    console.rule("[bold green]COMPLIANCE SCAN RESULTS")
    for section, checks in results.items():
        console.print(f"\n[bold]{section.upper()}[/bold]")
        for check in checks:
            icon = "✅" if check["status"] == "✓" else "❌"
            console.print(f" {icon} {check['item']}")


def save_report(results, domain, framework):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"report_{domain}_{framework}_{timestamp}.json"
    report_path = Path("reports") / filename
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump({"framework": framework, "domain": domain, "results": results}, f, indent=2)
    console.print(f"\n[bold yellow]Report saved to:[/bold yellow] {report_path}")


def run_watch_mode(domain, framework, interval):
    def job():
        console.print(f"\n[bold blue]Running scheduled scan for {domain} ({framework})[/bold blue]")
        results = simulate_scan()
        display_results(results)
        save_report(results, domain, framework)

    schedule.every(interval).minutes.do(job)

    def scheduler_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=scheduler_loop).start()
    console.print("[green]Watch mode running. Press Ctrl+C to stop.[/green]")
    while True:
        time.sleep(60)


def run_dashboard():
    table = Table(title="Compliance Scan Progress")
    table.add_column("Section", justify="left")
    table.add_column("Check", justify="left")
    table.add_column("Status", justify="center")

    with Live(table, refresh_per_second=2):
        for section, checks in SIMULATED_RESULTS.items():
            for check in checks:
                time.sleep(0.5)
                status = "✅" if check["status"] == "✓" else "❌"
                table.add_row(section.title(), check["item"], status)


def main():
    parser = argparse.ArgumentParser(description="AI-Powered Compliance Analyzer")
    parser.add_argument("--target", required=True, help="Domain or system name to scan")
    parser.add_argument("--framework", default="GDPR", choices=["GDPR", "HIPAA", "NIST"], help="Compliance framework")
    parser.add_argument("--export", choices=["json"], help="Export format")
    parser.add_argument("--dashboard", action="store_true", help="Run in real-time dashboard mode")
    parser.add_argument("--watch", type=int, help="Re-scan every X minutes continuously")
    parser.add_argument("--policy", type=str, help="Optional path to privacy policy for AI analysis")
    args = parser.parse_args()

    if args.dashboard:
        run_dashboard()
    elif args.watch:
        run_watch_mode(args.target, args.framework, args.watch)
    else:
        results = simulate_scan()
        display_results(results)

        if args.export == "json":
            save_report(results, args.target, args.framework)

        if args.policy:
            with open(args.policy, "r") as f:
                policy_text = f.read()
            console.rule("[bold blue]AI Policy Analysis Report")
            analysis = ai_policy_analysis(policy_text)
            console.print(analysis)


if __name__ == "__main__":
    main()
