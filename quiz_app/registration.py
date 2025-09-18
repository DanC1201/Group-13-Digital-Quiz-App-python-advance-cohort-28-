import tkinter as tk
from tkinter import messagebox
import json
import os

USER_DATA_FILE = "user_data.json"

def save_user_details(name, email, password):
    user = {"name": name, "email": email, "password": password}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(user)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class RegistrationWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        master.title("Quiz App - Register")
        master.geometry("300x250")

        tk.Label(master, text="Name").pack(pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        tk.Label(master, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(master)
        self.email_entry.pack()

        tk.Label(master, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Register", command=self.register).pack(pady=20)

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        save_user_details(name, email, password)
        self.on_success(name)
