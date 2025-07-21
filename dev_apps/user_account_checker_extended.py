#!/usr/bin/env python3
import pwd
import spwd
import os
import subprocess
from datetime import datetime

def get_users():
    return [user for user in pwd.getpwall() if int(user.pw_uid) >= 0]

def get_shadow_info():
    try:
        return {entry.sp_nam: entry for entry in spwd.getspall()}
    except PermissionError:
        print("❌ Run this script as root to access /etc/shadow.")
        return {}

def get_lastlog_info():
    try:
        output = subprocess.check_output("lastlog", text=True)
        return output
    except subprocess.CalledProcessError:
        return ""

def user_creation_time(username):
    path = f"/home/{username}"
    if os.path.exists(path):
        timestamp = os.path.getctime(path)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def analyze_users():
    shadow_data = get_shadow_info()
    lastlog_data = get_lastlog_info()
    all_users = get_users()

    print("\n=== SYSTEM USER ACCOUNT ANALYSIS ===\n")

    for user in all_users:
        name = user.pw_name
        uid = user.pw_uid
        shell = user.pw_shell
        home = user.pw_dir
        suspicious = False
        issues = []

        # UID 0 but not root
        if uid == 0 and name != "root":
            suspicious = True
            issues.append("UID 0 (root privileges)")

        # Password status
        passwd_info = shadow_data.get(name)
        if passwd_info:
            if passwd_info.sp_pwd == '' or passwd_info.sp_pwd in ('*', '!', '!!'):
                issues.append("No usable password")

        # Shell access
        if shell not in ('/usr/sbin/nologin', '/bin/false', ''):
            if uid >= 1000 or uid == 0:
                issues.append(f"Shell access ({shell})")

        # Check login history
        if name not in lastlog_data:
            issues.append("No login history")

        # Check account creation time
        created = user_creation_time(name)
        if created != "N/A":
            issues.append(f"Created on: {created}")

        if issues:
            print(f"🔍 User: {name}\nUID: {uid}\nHome: {home}")
            for i in issues:
                print(f"  - {i}")
            print("-" * 40)

if __name__ == "__main__":
    analyze_users()
