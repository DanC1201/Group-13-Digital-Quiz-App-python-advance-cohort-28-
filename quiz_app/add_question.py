import tkinter as tk
from tkinter import messagebox
from questions import MultipleChoiceQuestion, TrueFalseQuestion, FillInTheBlankQuestion
import json
import os

USER_QUESTIONS_FILE = "user_questions.json"

class AddQuestionWindow:
    def __init__(self, master, on_add):
        self.master = master
        self.on_add = on_add
        master.title("Add New Question")
        master.geometry("400x400")

        tk.Label(master, text="Question Type:").pack(pady=5)
        self.qtype_var = tk.StringVar(value="Multiple Choice")
        types = ["Multiple Choice", "True/False", "Fill in the Blank"]
        for t in types:
            tk.Radiobutton(master, text=t, variable=self.qtype_var, value=t, command=self.update_type).pack(anchor='w')

        tk.Label(master, text="Prompt:").pack(pady=5)
        self.prompt_entry = tk.Entry(master, width=50)
        self.prompt_entry.pack()

        self.options_label = tk.Label(master, text="Options (comma separated):")
        self.options_entry = tk.Entry(master, width=50)
        self.options_label.pack(pady=5)
        self.options_entry.pack()

        tk.Label(master, text="Answer:").pack(pady=5)
        self.answer_entry = tk.Entry(master, width=50)
        self.answer_entry.pack()

        tk.Button(master, text="Add Question", command=self.add_question).pack(pady=20)
        self.update_type()

    def update_type(self):
        if self.qtype_var.get() == "Multiple Choice":
            self.options_label.pack(pady=5)
            self.options_entry.pack()
        else:
            self.options_label.pack_forget()
            self.options_entry.pack_forget()

    def add_question(self):
        qtype = self.qtype_var.get()
        prompt = self.prompt_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if not prompt or not answer:
            messagebox.showerror("Error", "Prompt and answer are required!")
            return
        if qtype == "Multiple Choice":
            options = [o.strip() for o in self.options_entry.get().split(",") if o.strip()]
            if len(options) < 2:
                messagebox.showerror("Error", "At least two options required for multiple choice.")
                return
            q = {"type": "mc", "prompt": prompt, "options": options, "answer": answer}
        elif qtype == "True/False":
            q = {"type": "tf", "prompt": prompt, "answer": answer}
        else:
            q = {"type": "fib", "prompt": prompt, "answer": answer}
        self.save_user_question(q)
        self.on_add()
        messagebox.showinfo("Success", "Question added!")
        self.master.destroy()

    def save_user_question(self, q):
        if os.path.exists(USER_QUESTIONS_FILE):
            with open(USER_QUESTIONS_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(q)
        with open(USER_QUESTIONS_FILE, "w") as f:
            json.dump(data, f, indent=2)
