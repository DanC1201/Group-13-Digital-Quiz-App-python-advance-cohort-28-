import tkinter as tk
from tkinter import messagebox
import json
import os

USER_DATA_FILE = "user_data.json"

def save_user_details(name, email, password): # Function to save a new user's registration details
    # Create a dictionary with the user's name, email, and password
    user = {"name": name, "email": email, "password": password}
    # Check if the user data file already exists
    if os.path.exists(USER_DATA_FILE):
        # If it exists, open and load the existing user data
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        # If it doesn't exist, create with an empty list
        data = []
        # Add the new user to the list of users
    data.append(user)

    # Write the updated user list back to the file with indentation for readability
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class RegistrationWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success

        # Set up the registration window
        master.title("Quiz App - Register")
        master.geometry("300x250")

        # Create and pack the Name label and entry field
        tk.Label(master, text="Name").pack(pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()
        # Create and pack the Email label and entry field
        tk.Label(master, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(master)
        self.email_entry.pack()
        # Create and pack the Password label and entry field (masked input)
        tk.Label(master, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()
        # Create and pack the Register button, which triggers the register method
        tk.Button(master, text="Register", command=self.register).pack(pady=20)

    def register(self):
        # Retrieve and clean input from the entry fields
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        # Validate that all fields are filled
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        # Save the user's details to the data file
        save_user_details(name, email, password)
        # Call the success callback with the user's name
        self.on_success(name)

    # Function to check if a user's login credentials are valid
def validate_user(email, password):
    # Check if the user data file exists if not return False (no users)
    if not os.path.exists(USER_DATA_FILE):
        return False
    # Load the list of registered users from the JSON file
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
    # Loop through each user and check for matching email and password
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user["name"] # Return the user's name if there is a match
    return False # if there is no match found, return false

class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master # Reference to the parent window
        self.on_success = on_success # Callback function to execute after successful login

        # Set window title and size
        master.title("Quiz App - Login")
        master.geometry("300x200")
        # Create and pack the email label and entry field
        tk.Label(master, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(master)
        self.email_entry.pack()
        # Create and pack the password label and entry field (masked input)
        tk.Label(master, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()
        # Create and pack the login button, which triggers the login method
        tk.Button(master, text="Login", command=self.login).pack(pady=20)

    def login(self): # Login method

        # Get and clean the input from the email and password fields
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate the credentials using the validate_user function
        name = validate_user(email, password)
        if name:
            # Prints user's name if login successful
            messagebox.showinfo("Success", f"Welcome back, {name}!")
            self.on_success(name)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

def launch_app():
    root = tk.Tk()

    def open_registration(name=None):
        root.destroy() # Close welcome window
        reg_root = tk.Tk() # Create new window for registration

        # Launch RegistrationWindow and show a success message upon completion
        RegistrationWindow(reg_root, lambda n: messagebox.showinfo("Registered", f"Welcome, {n}!"))

    # Function to open the login window
    def open_login(name=None):
        root.destroy()  # Close the welcome window
        login_root = tk.Tk()  # Create a new window for login

        # Launch LoginWindow and show a success message upon successful login
        LoginWindow(login_root, lambda n: messagebox.showinfo("Logged In", f"Welcome back, {n}!"))

    # Set up the welcome window UI
    root.title("Quiz App")
    root.geometry("300x150")

    # Display welcome message
    tk.Label(root, text="Welcome to Quiz App").pack(pady=10)

    # Buttons to navigate to registration or login
    tk.Button(root, text="Register", command=open_registration).pack(pady=5)
    tk.Button(root, text="Login", command=open_login).pack(pady=5)


