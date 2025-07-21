import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def rebuild_exe():
    file_path = filedialog.askopenfilename(
        title="Choose your .py script to rebuild",
        filetypes=[("Python Files", "*.py")]
    )

    if not file_path:
        return

    confirm = messagebox.askyesno(
        "Confirm Build",
        f"Do you want to rebuild this into an .exe?\n\n{file_path}"
    )

    if confirm:
        try:
            subprocess.run(["pyinstaller", "--onefile", file_path], check=True)
            messagebox.showinfo("Success", f"✔️ Build complete!\nCheck the 'dist' folder for the .exe.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"❌ Build failed.\n\n{e}")
    else:
        messagebox.showinfo("Cancelled", "Build was cancelled.")

# GUI window
root = tk.Tk()
root.title("Python to EXE Rebuilder")
root.geometry("300x150")

label = tk.Label(root, text="Click the button to rebuild your .py to .exe")
label.pack(pady=10)

btn = tk.Button(root, text="Select Python File", command=rebuild_exe)
btn.pack(pady=10)

root.mainloop()
