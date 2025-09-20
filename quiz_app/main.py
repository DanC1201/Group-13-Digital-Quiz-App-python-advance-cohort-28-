import customtkinter as ctk
from tkinter import messagebox
from quiz import QuizWindow
from registration_login import RegistrationWindow, LoginWindow
from add_question import AddQuestionWindow
from score import ScoreHistoryWindow


# ----------------------------
# Main Menu
# ----------------------------
class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("600x400")

        # Title
        title_label = ctk.CTkLabel(master, text="Welcome to the Quiz App!", font=("Arial", 22, "bold"))
        title_label.pack(pady=25)

        # Buttons
        ctk.CTkButton(master, text="Register & Start Quiz", command=self.open_registration, width=200).pack(pady=10)
        ctk.CTkButton(master, text="Login & Start Quiz", command=self.open_login, width=200).pack(pady=10)
        ctk.CTkButton(master, text="Add a Question", command=self.open_add_question, width=200).pack(pady=10)
        ctk.CTkButton(master, text="View Score History", command=self.open_score_history, width=200).pack(pady=10)

        # Exit button
        ctk.CTkButton(master, text="Exit", command=self.master.quit, fg_color="red", hover_color="darkred", width=200).pack(pady=20)

    # ------------------------
    # Button Actions
    # ------------------------
    def open_registration(self):
        self.master.withdraw()  # hide main menu
        reg_root = ctk.CTkToplevel(self.master)
        RegistrationWindow(reg_root, self.start_quiz)

    def open_login(self):
        self.master.withdraw()  # hide main menu
        login_root = ctk.CTkToplevel(self.master)
        LoginWindow(login_root, self.start_quiz)

    def open_add_question(self):
        self.master.withdraw()  # hide main menu
        add_q_root = ctk.CTkToplevel(self.master)

        def on_close():
            add_q_root.destroy()
            self.master.deiconify()  # show menu again

        add_q_root.protocol("WM_DELETE_WINDOW", on_close)
        self.add_question_window = AddQuestionWindow(add_q_root)

    def open_score_history(self):
        self.master.withdraw()
        score_root = ctk.CTkToplevel(self.master)

        def on_close():
            score_root.destroy()
            self.master.deiconify()
        score_root.protocol("WM_DELETE_WINDOW", on_close)
        ScoreHistoryWindow(score_root, on_close)


    def start_quiz(self, user_name):
        # at this point, login/registration windows are destroyed
        # now destroy main menu completely and start quiz
        self.master.destroy()
        quiz_root = ctk.CTk()
        QuizWindow(quiz_root, user_name, self.show_results)
        quiz_root.mainloop()

    def show_results(self, score, total, answers):
        messagebox.showinfo("Quiz Finished", f"You scored {score}/{total}")


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")   # "light" or "dark"
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    MainMenu(root)
    root.mainloop()
