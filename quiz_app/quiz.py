import tkinter as tk
from tkinter import messagebox
from questions import get_random_questions, MultipleChoiceQuestion, TrueFalseQuestion, FillInTheBlankQuestion

class QuizWindow:
    def __init__(self, master, user_name, on_finish):
        self.master = master
        self.user_name = user_name
        self.on_finish = on_finish
        self.questions = get_random_questions(30)
        self.current = 0
        self.score = 0
        self.timer = 60
        self.timer_id = None
        self.user_answers = []

        self.question_label = tk.Label(master, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)
        self.options_frame = tk.Frame(master)
        self.options_frame.pack()
        self.answer_entry = None
        self.next_button = tk.Button(master, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)
        self.timer_label = tk.Label(master, text="Time left: 60s", font=("Arial", 12))
        self.timer_label.pack()
        self.show_question()

    def show_question(self):
        if self.current >= len(self.questions):
            self.finish_quiz()
            return
        self.clear_options()
        q = self.questions[self.current]
        self.question_label.config(text=f"Q{self.current+1}: {q.prompt}")
        self.selected_option = tk.StringVar()
        if isinstance(q, MultipleChoiceQuestion):
            for opt in q.options:
                btn = tk.Radiobutton(self.options_frame, text=opt, variable=self.selected_option, value=opt)
                btn.pack(anchor='w')
        elif isinstance(q, TrueFalseQuestion):
            for opt in ["True", "False"]:
                btn = tk.Radiobutton(self.options_frame, text=opt, variable=self.selected_option, value=opt)
                btn.pack(anchor='w')
        elif isinstance(q, FillInTheBlankQuestion):
            self.answer_entry = tk.Entry(self.options_frame)
            self.answer_entry.pack()
        self.timer = 60
        self.update_timer()

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.answer_entry = None
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

    def get_user_answer(self):
        q = self.questions[self.current]
        if isinstance(q, (MultipleChoiceQuestion, TrueFalseQuestion)):
            return self.selected_option.get()
        elif isinstance(q, FillInTheBlankQuestion):
            return self.answer_entry.get() if self.answer_entry else ""
        return ""

    def next_question(self):
        user_answer = self.get_user_answer()
        q = self.questions[self.current]
        correct = q.is_correct(user_answer)
        if correct:
            self.score += 1
        self.user_answers.append((q.prompt, user_answer, correct))
        self.current += 1
        self.show_question()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.timer}s")
        if self.timer > 0:
            self.timer -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.next_question()

    def finish_quiz(self):
        self.clear_options()
        self.question_label.config(text="Quiz Finished!")
        self.timer_label.config(text="")
        self.next_button.pack_forget()
        self.on_finish(self.score, len(self.questions), self.user_answers)
