import tkinter as tk

class ScoreWindow:
    def __init__(self, master, score, total, user_answers):
        self.master = master
        self.master.title("Quiz App - Score")
        self.master.geometry("400x400")
        tk.Label(self.master, text=f"Your Final Score: {score} out of {total}", font=("Arial", 18)).pack(pady=20)
        details = tk.Text(self.master, height=15, width=50)
        details.pack()
        details.insert(tk.END, "Q | Your Answer | Correct\n")
        for i, (q, ans, correct) in enumerate(user_answers, 1):
            details.insert(tk.END, f"{i}. {q[:30]}... | {ans} | {'✔' if correct else '✘'}\n")
        details.config(state=tk.DISABLED)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10)
