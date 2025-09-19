import tkinter as tk
import os
import json
from registration_login import RegistrationWindow
from quiz import QuizWindow
from score import ScoreWindow
from registration_login import LoginWindow


from add_question import AddQuestionWindow

SCORE_FILE = "user_scores.json"
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        tk.Label(frame, text="Welcome to the Quiz App!", font=("Arial", 18)).pack(pady=20)
        tk.Button(frame, text="Register & Start Quiz", command=self.show_registration, width=25).pack(pady=10)
        tk.Button(frame, text="Add a Question", command=self.show_add_question, width=25).pack(pady=10)
        tk.Button(frame, text="Login & Start Quiz", command=self.show_login, width=25).pack(pady=10)
        tk.Button(frame, text="View Score History", command=self.show_score_history, width=25).pack(pady=10) # Button to display score history

    def show_registration(self):
        self.clear_window()
        self.registration = RegistrationWindow(self.root, self.start_quiz)

    def show_add_question(self):
        win = tk.Toplevel(self.root)
        AddQuestionWindow(win, self.on_question_added)

    def on_question_added(self):
        # Optionally show a message or refresh
        pass

    def start_quiz(self, user_name):
        self.clear_window()
        self.quiz = QuizWindow(self.root, user_name, self.show_score)

    def show_score(self, score, total, user_answers):
        self.clear_window()
        self.score = ScoreWindow(self.root, score, total, user_answers, self.quiz.user_name)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        self.login = LoginWindow(self.root, self.start_quiz)

    def show_score_history(self):          # Method to display score history
        self.clear_window()
        frame = tk.Frame(self.root)        # Creates a new frame to hold the score history UI
        frame.pack(expand=True)
        tk.Label(frame, text="Score History", font=("Arial", 16)).pack(pady=10) # Title label

        if not os.path.exists(SCORE_FILE)or os.path.getsize(SCORE_FILE) == 0:  # If the score file doesn't exist, show a message and exit
            tk.Label(frame, text="No scores recorded yet.").pack()
            return

        with open(SCORE_FILE, "r") as f:    # Loads the scores from the JSON file
            scores = json.load(f)

        text = tk.Text(frame, height=15, width=50)   # Creates a text widget to display the score entries
        text.pack()
        text.insert(tk.END, "User | Score | Total\n")
        text.insert(tk.END, "-" * 30 + "\n")

        for entry in scores:                       # Loops through each score entry and displays it
            text.insert(tk.END, f"{entry['user']} | {entry['score']} | {entry['total']}\n")
        text.config(state=tk.DISABLED)

        tk.Button(frame, text="Back to Menu", command=self.show_main_menu).pack(pady=10) # Goes back to main menu



def main():
    root = tk.Tk()
    root.geometry("500x400")
    app = QuizApp(root)

    root.mainloop()
if __name__ == "__main__":
    main()
