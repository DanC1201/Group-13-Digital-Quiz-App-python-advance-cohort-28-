import tkinter as tk
from registration import RegistrationWindow
from quiz import QuizWindow
from score import ScoreWindow


from add_question import AddQuestionWindow

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
        self.score = ScoreWindow(self.root, score, total, user_answers)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    root.geometry("500x400")
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
