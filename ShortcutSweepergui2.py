import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import win32com.client

# get path to user's desktop
desk = os.path.join(os.environ["USERPROFILE"], "Desktop")

# holds all broken .lnk paths + their targets
dead_lnks = []

# function to scan .lnk files
def scan_lnks():
    prg["mode"] = "indeterminate"
    prg.start()

    shell = win32com.client.Dispatch("WScript.Shell")

    for f in os.listdir(desk):
        f_path = os.path.join(desk, f)

        if f.lower().endswith(".lnk"):
            try:
                shrt = shell.CreateShortcut(f_path)
                tgt = shrt.Targetpath
                if not os.path.exists(tgt):
                    dead_lnks.append((f_path, tgt))
                    list_box.insert(tk.END, os.path.basename(f_path))
            except:
                pass

    prg.stop()
    prg["mode"] = "determinate"
    prg["value"] = 100

    if not dead_lnks:
        list_box.insert(tk.END, "No broken shortcuts detected.")
        cancel_btn["state"] = "normal"
    else:
        del_btn["state"] = "normal"
        cancel_btn["state"] = "normal"

# delete all broken shortcuts
def del_lnks():
    with open("dead_shortcuts_log.txt", "w") as log:
        for lnk, tgt in dead_lnks:
            log.write(f"[DEAD] {lnk} -> {tgt}\n")
        log.write("\n[DELETED SHORTCUTS]\n")

        for lnk, _ in dead_lnks:
            try:
                os.remove(lnk)
                log.write(f"{lnk} deleted\n")
            except:
                pass

    messagebox.showinfo("Done", "Deleted all dead shortcuts.")
    root.destroy()

# close app
def cancel():
    root.destroy()

# run scan in background so GUI doesn’t freeze
def start_scan():
    th = threading.Thread(target=scan_lnks)
    th.start()

# --- GUI setup ---

root = tk.Tk()
root.title("DeadShortcut Sweeper v2")
root.geometry("450x400")
root.resizable(False, False)

# top bar – scanner look
prg = ttk.Progressbar(root, mode="determinate", length=400)
prg.pack(pady=15)

# middle list of broken shortcuts
list_box = tk.Listbox(root, width=55, height=15)
list_box.pack(pady=5)

# bottom buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

del_btn = tk.Button(btn_frame, text="Delete All", width=15, state="disabled", command=del_lnks)
del_btn.pack(side=tk.LEFT, padx=10)

cancel_btn = tk.Button(btn_frame, text="Cancel", width=15, state="disabled", command=cancel)
cancel_btn.pack(side=tk.LEFT, padx=10)

# start scan on launch
start_scan()

root.mainloop()
