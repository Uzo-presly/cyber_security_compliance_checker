import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Path to your built .exe apps
APP_PATHS = {
    "User Account Checker": "dist/user_account_checker_extended.exe",
    "Network Info Tool": "dist/network_info_tool.exe",
    "Disk Usage Reporter": "dist/disk_usage_reporter.exe"
}

def launch_app(app_name):
    exe_path = APP_PATHS.get(app_name)
    if exe_path and os.path.exists(exe_path):
        try:
            subprocess.Popen(exe_path, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch {app_name}:\n{str(e)}")
    else:
        messagebox.showerror("Missing", f"{app_name} not found at expected location.")

root = tk.Tk()
root.title("My Dev Tool Launcher")

tk.Label(root, text="Select an App to Launch:", font=("Arial", 14)).pack(pady=10)

for app in APP_PATHS:
    tk.Button(root, text=app, command=lambda a=app: launch_app(a), width=30).pack(pady=5)

tk.Button(root, text="Exit", command=root.quit, width=30, fg="red").pack(pady=20)

root.mainloop()
