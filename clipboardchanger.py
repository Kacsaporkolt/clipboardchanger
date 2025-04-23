import pyperclip
import tkinter as tk
from tkinter import messagebox
import threading
import time
import re

def monitor_clipboard(field_data):
    global running
    last_clipboard_content = pyperclip.paste()

    while running:
        try:
            current_clipboard_content = pyperclip.paste()
            if current_clipboard_content != last_clipboard_content:
                modified_content = current_clipboard_content
                for field in field_data:
                    if not field["enabled"].get():
                        continue

                    original_text = field["input1"].get()
                    replacement_text = field["input2"].get()
                    match_whole = field["whole_word"].get()
                    case_sensitive = field["case_sensitive"].get()

                    if not original_text or not replacement_text:
                        continue

                    flags = 0 if case_sensitive else re.IGNORECASE
                    pattern_str = rf'\b{re.escape(original_text)}\b' if match_whole else re.escape(original_text)
                    pattern = re.compile(pattern_str, flags)
                    modified_content = pattern.sub(replacement_text, modified_content)

                if modified_content != current_clipboard_content:
                    pyperclip.copy(modified_content)
                last_clipboard_content = modified_content
            time.sleep(0.1)
        except Exception as e:
            messagebox.showerror("Clipboard Changer - Error", f"Error: {e}")
            break

def start_stop_monitoring():
    global running, thread
    if running:
        running = False
        start_button.config(text="Start", bg="green")
    else:
        for field in field_data:
            if field["enabled"].get():
                if not field["input1"].get() or not field["input2"].get():
                    messagebox.showwarning("Clipboard Changer - Warning", "All active fields must be filled in!")
                    return

        running = True
        thread = threading.Thread(target=monitor_clipboard, args=(field_data,), daemon=True)
        thread.start()
        start_button.config(text="Stop", bg="red")

def add_field():
    for field in field_data:
        if not field["input1"].get() or not field["input2"].get():
            messagebox.showwarning("Clipboard Changer - Warning", "Please fill all existing fields before adding more.")
            return

    frame = tk.Frame(field_container, bg="#1e3a8a")
    frame.pack(pady=5)

    entry_font = ("Arial", 14)

    input1 = tk.Entry(frame, width=30, font=entry_font)
    input1.pack(side=tk.LEFT, padx=5)

    input2 = tk.Entry(frame, width=30, font=entry_font)
    input2.pack(side=tk.LEFT, padx=5)

    whole_word = tk.BooleanVar()
    case_sensitive = tk.BooleanVar()
    enabled = tk.BooleanVar(value=True)

    tk.Checkbutton(frame, text="Whole word", variable=whole_word,
                   bg="#1e3a8a", fg="white", selectcolor="#0f172a", font=entry_font).pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(frame, text="Case sensitive", variable=case_sensitive,
                   bg="#1e3a8a", fg="white", selectcolor="#0f172a", font=entry_font).pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(frame, text="Use", variable=enabled,
                   onvalue=True, offvalue=False,
                   bg="#1e3a8a", fg="white", selectcolor="#0f172a", font=entry_font).pack(side=tk.LEFT, padx=5)

    field_data.append({
        "frame": frame,
        "input1": input1,
        "input2": input2,
        "whole_word": whole_word,
        "case_sensitive": case_sensitive,
        "enabled": enabled
    })

# GUI létrehozása
root = tk.Tk()
root.title("Clipboard Changer")
root.geometry('1500x750')
root.configure(bg="#1e3a8a")

main_frame = tk.Frame(root, bg="darkblue", bd=4, relief=tk.GROOVE)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=1400, height=700)

title_label = tk.Label(main_frame, text="Clipboard Changer v2.1.3 by SoftVari",
                       bg="#1e3a8a", fg="white", font=("Arial", 24, "bold"))
title_label.pack(pady=10)


field_data = []
running = False
thread = None

top_controls = tk.Frame(main_frame, bg="#1e3a8a")
top_controls.pack(pady=10)

tk.Button(top_controls, text="Add +", bg="green", fg="white", font=("Arial", 14), command=add_field).pack(side=tk.LEFT, padx=5)
start_button = tk.Button(top_controls, text="Start", fg="white", bg="green", font=("Arial", 14), command=start_stop_monitoring)
start_button.pack(side=tk.LEFT, padx=5)

field_container = tk.Frame(main_frame, bg="#1e3a8a")
field_container.pack(fill=tk.BOTH, expand=True)

add_field()
root.mainloop()