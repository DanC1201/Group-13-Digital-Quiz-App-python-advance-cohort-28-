import customtkinter as ctk
from tkinter import messagebox
import json
import os

USER_DATA_FILE = "user_data.json"


# ------------------------
# Save User Details
# ------------------------
def save_user_details(name, email, password):
    user = {"name": name, "email": email, "password": password}

    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(user)

    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ------------------------
# Validate Login
# ------------------------
def validate_user(email, password):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return False

    for user in users:
        if user["email"] == email and user["password"] == password:
            return user["name"]

    return False


# ------------------------
# Registration Window
# ------------------------
class RegistrationWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.master.title("Quiz App - Register")
        self.master.geometry("400x450")

        # Title
        ctk.CTkLabel(self.master, text="Register", font=("Arial", 22, "bold")).pack(pady=20)

        # Name
        ctk.CTkLabel(self.master, text="Name").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.master, width=250)
        self.name_entry.pack(pady=5)

        # Email
        ctk.CTkLabel(self.master, text="Email").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.master, width=250)
        self.email_entry.pack(pady=5)

        # Password
        ctk.CTkLabel(self.master, text="Password").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.master, show="*", width=250)
        self.password_entry.pack(pady=5)

        # Register Button
        ctk.CTkButton(self.master, text="Register", command=self.register, width=200).pack(pady=20)

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        save_user_details(name, email, password)
        messagebox.showinfo("Success", f"Welcome, {name}!")
        self.master.destroy()
        self.on_success(name)


# ------------------------
# Login Window
# ------------------------
class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.master.title("Quiz App - Login")
        self.master.geometry("400x300")  # ⬅️ Increased size

        # Title
        ctk.CTkLabel(self.master, text="Login", font=("Arial", 22, "bold")).pack(pady=20)

        # Email
        ctk.CTkLabel(self.master, text="Email").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.master, width=250)
        self.email_entry.pack(pady=5)

        # Password
        ctk.CTkLabel(self.master, text="Password").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.master, show="*", width=250)
        self.password_entry.pack(pady=5)

        # Login Button
        ctk.CTkButton(self.master, text="Login", command=self.login, width=200).pack(pady=20)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        name = validate_user(email, password)
        if name:
            messagebox.showinfo("Success", f"Welcome back, {name}!")
            self.master.destroy()
            self.on_success(name)
        else:
            messagebox.showerror("Error", "Invalid email or password.")
