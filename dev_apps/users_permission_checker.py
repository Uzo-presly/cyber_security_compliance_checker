#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pwd
import subprocess
import os
import stat
import platform
from datetime import datetime

# ------------------------ User Info Functions ------------------------

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

def get_users():
    users = []
    for user in pwd.getpwall():
        if int(user.pw_uid) >= 1000 and 'nologin' not in user.pw_shell:
            users.append(user.pw_name)
    return users

def get_account_status(username):
    try:
        result = subprocess.check_output(['chage', '-l', username], text=True)
        return result
    except subprocess.CalledProcessError:
        return "Access Denied or Not Enough Privileges\n"

def display_users():
    output_box.delete('1.0', tk.END)
    users = get_users()
    output_box.insert(tk.END, f"Detected Users:\n{'-'*50}\n")
    for user in users:
        output_box.insert(tk.END, f"Username: {user}\n")
        output_box.insert(tk.END, f"UID: {pwd.getpwnam(user).pw_uid}\n")
        output_box.insert(tk.END, f"Created: {user_creation_time(user)}\n")
        if chage_toggle.get():
            status = get_account_status(user)
            output_box.insert(tk.END, f"Status:\n{status}\n")
        output_box.insert(tk.END, "-"*50 + "\n")

# ------------------------ Folder Permission Checker ------------------------

def check_access_control():
    output_box.insert(tk.END, "\nFolder Access Permissions:\n" + "-"*50 + "\n")
    if platform.system() == "Windows":
        targets = ["C:/Users/Public", os.path.expanduser("~")]
    else:
        targets = ["/home", os.path.expanduser("~")]

    for path in targets:
        try:
            mode = os.stat(path).st_mode
            perms = stat.filemode(mode)
            output_box.insert(tk.END, f"✅ {path} - Mode: {oct(mode)} ({perms})\n")
        except Exception as e:
            output_box.insert(tk.END, f"❌ {path} - Error: {e}\n")
    output_box.insert(tk.END, "-"*50 + "\n")

# ------------------------ GUI Setup ------------------------

root = tk.Tk()
root.title("User Account Checker (Extended GUI)")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

chage_toggle = tk.BooleanVar()
ttk.Checkbutton(frame, text="Include Account Status (Requires sudo)", variable=chage_toggle).grid(row=0, column=0, sticky=tk.W)

ttk.Button(frame, text="Scan Users", command=display_users).grid(row=1, column=0, pady=5, sticky=tk.W)
ttk.Button(frame, text="Check Folder Permissions", command=check_access_control).grid(row=2, column=0, pady=5, sticky=tk.W)

output_box = scrolledtext.ScrolledText(frame, width=100, height=30)
output_box.grid(row=3, column=0)

root.mainloop()
