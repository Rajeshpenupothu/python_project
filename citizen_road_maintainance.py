import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

USERS_FILE, REPORTS_FILE = 'users.json', 'reports.json'

# Initialize JSON files
for file in [USERS_FILE, REPORTS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

# Load and save functions
def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Global variable to store current user
current_user = None

# Main application window
root = tk.Tk()
root.title("User Report Management System")
root.geometry("800x600")
root.configure(bg="#f9f9f9")

# Frame management
def clear_frames():
    for frame in frames:
        frame.pack_forget()

def show_frame(frame):
    clear_frames()
    frame.pack(fill="both", expand=True)

# Handle report submissjgion
def handle_submit_report():
    report = {k: v.get().strip() for k, v in entries.items()}
    if any(not value for value in report.values()):
        messagebox.showerror("Error", "All fields are required.")
        return
    reports = load_json(REPORTS_FILE)
    reports.append(report)
    save_json(REPORTS_FILE, reports)
    for entry in entries.values():
        entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Report submitted successfully!")
    show_frame(dashboard_frame)

# Switch frames
def switch_to_login():
    show_frame(login_frame)

def switch_to_registration():
    show_frame(registration_frame)

def submit_login():
    global current_user
    username = login_username.get()
    password = login_password.get()
    users = load_json(USERS_FILE)
    current_user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if current_user:
        messagebox.showinfo("Success", "Login successful!")
        show_frame(submit_report_frame)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def submit_registration():
    username = reg_username.get()
    password = reg_password.get()
    if password != reg_confirm_password.get():
        messagebox.showerror("Error", "Passwords do not match.")
        return
    users = load_json(USERS_FILE)
    if any(u['username'] == username for u in users):
        messagebox.showerror("Error", "Username already exists.")
        return
    users.append({'username': username, 'password': password})
    save_json(USERS_FILE, users)
    messagebox.showinfo("Success", "Registration successful!")
    switch_to_login()

# Frames setup
login_frame, registration_frame, submit_report_frame, dashboard_frame = [ttk.Frame(root, padding=20) for _ in range(4)]
frames = [login_frame, registration_frame, submit_report_frame, dashboard_frame]

# Login frame widgets
ttk.Label(login_frame, text="Username").grid(row=0, column=0, pady=10)
login_username = ttk.Entry(login_frame)
login_username.grid(row=0, column=1, pady=10)

ttk.Label(login_frame, text="Password").grid(row=1, column=0, pady=10)
login_password = ttk.Entry(login_frame, show='*')
login_password.grid(row=1, column=1, pady=10)

ttk.Button(login_frame, text="Login", command=submit_login).grid(row=2, columnspan=2, pady=10)
ttk.Button(login_frame, text="Register", command=switch_to_registration).grid(row=3, columnspan=2, pady=10)

# Registration frame widgets
ttk.Label(registration_frame, text="Username").grid(row=0, column=0, pady=10)
reg_username = ttk.Entry(registration_frame)
reg_username.grid(row=0, column=1, pady=10)

ttk.Label(registration_frame, text="Password").grid(row=1, column=0, pady=10)
reg_password = ttk.Entry(registration_frame, show='*')
reg_password.grid(row=1, column=1, pady=10)

ttk.Label(registration_frame, text="Confirm Password").grid(row=2, column=0, pady=10)
reg_confirm_password = ttk.Entry(registration_frame, show='*')
reg_confirm_password.grid(row=2, column=1, pady=10)

ttk.Button(registration_frame, text="Register", command=submit_registration).grid(row=3, columnspan=2, pady=10)

# Submit report frame widgets
entries = {}
for i, label in enumerate(["Issue", "Pin Code", "City", "Area", "Street", "Location"]):
    ttk.Label(submit_report_frame, text=label).grid(row=i, column=0, pady=10)
    entries[label] = ttk.Entry(submit_report_frame)
    entries[label].grid(row=i, column=1, pady=10)

ttk.Button(submit_report_frame, text="Submit", command=handle_submit_report).grid(row=len(entries), columnspan=2, pady=10)

# Start application
switch_to_login()
root.mainloop()
