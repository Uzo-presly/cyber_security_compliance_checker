#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import pwd, spwd, os, subprocess
from datetime import datetime

def get_shadow_info():
    try:
        return {entry.sp_nam: entry for entry in spwd.getspall()}
    except PermissionError:
        return {}

def get_lastlog_info():
    try:
        return subprocess.check_output("lastlog", text=True)
    except:
        return ""

def user_creation_time(username):
    path = f"/home/{username}"
    if os.path.exists(path):
        return datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def detect_suspicious_users():
    shadow_data = get_shadow_info()
    lastlog = get_lastlog_info()
    users = pwd.getpwall()
    data = []

    for user in users:
        name = user.pw_name
        uid = user.pw_uid
        shell = user.pw_shell
        home = user.pw_dir
        issues = []

        if uid == 0 and name != "root":
            issues.append("UID 0 (root privileges)")

        if name in shadow_data:
            passwd = shadow_data[name].sp_pwd
            if passwd in ('', '*', '!', '!!'):
                issues.append("No password")

        if shell not in ('/usr/sbin/nologin', '/bin/false', ''):
            if uid >= 1000 or uid == 0:
                issues.append(f"Shell access: {shell}")

        if name not in lastlog:
            issues.append("No login history")

        created = user_creation_time(name)
        if created != "N/A":
            issues.append(f"Created on: {created}")

        if issues:
            data.append((name, uid, shell, home, "; ".join(issues)))

    return data

def create_gui():
    root = tk.Tk()
    root.title("Suspicious User Account Detector")

    tree = ttk.Treeview(root, columns=("Username", "UID", "Shell", "Home", "Issues"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

    suspicious = detect_suspicious_users()
    for item in suspicious:
        tree.insert("", "end", values=item)

    if not suspicious:
        messagebox.showinfo("Check Complete", "No suspicious users found.")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
