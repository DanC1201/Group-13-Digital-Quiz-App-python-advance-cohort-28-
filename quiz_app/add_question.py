import customtkinter as ctk
import json
import os

USER_QUESTIONS_FILE = "user_questions.json"


class AddQuestionWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Add a Question")
        self.master.geometry("600x650")

        # Frame
        frame = ctk.CTkFrame(master, corner_radius=15)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        ctk.CTkLabel(frame, text="Add a New Question", font=("Arial", 20, "bold")).pack(pady=15)

        # Dropdown for question type
        self.q_type = ctk.StringVar(value="Multiple Choice")
        ctk.CTkLabel(frame, text="Select Question Type:", font=("Arial", 14)).pack(pady=(10, 5))
        self.type_menu = ctk.CTkOptionMenu(
            frame,
            values=["Multiple Choice", "True/False", "Fill in the Blank"],
            variable=self.q_type,
            command=self.update_fields
        )
        self.type_menu.pack(pady=10)

        # Prompt entry
        ctk.CTkLabel(frame, text="Question Prompt:", font=("Arial", 14)).pack(pady=(15, 5))
        self.prompt_entry = ctk.CTkEntry(frame, width=400)
        self.prompt_entry.pack(pady=5)

        # Options / Answer area
        self.options_frame = ctk.CTkFrame(frame)
        self.options_frame.pack(pady=10)

        self.update_fields("Multiple Choice")

        # Save button
        self.save_button = ctk.CTkButton(frame, text="Save Question", width=200, command=self.save_question)
        self.save_button.pack(pady=20)

        # Status label (feedback after save)
        self.status_label = ctk.CTkLabel(frame, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

    # ----------------------------
    # Field Updates
    # ----------------------------
    def update_fields(self, choice):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if choice == "Multiple Choice":
            self.option_entries = []
            for i in range(4):
                entry = ctk.CTkEntry(self.options_frame, width=300, placeholder_text=f"Option {i+1}")
                entry.pack(pady=3)
                self.option_entries.append(entry)

            self.answer_entry = ctk.CTkEntry(self.options_frame, width=300, placeholder_text="Correct Answer")
            self.answer_entry.pack(pady=(10, 5))

        elif choice == "True/False":
            ctk.CTkLabel(self.options_frame, text="Answer (True/False):", font=("Arial", 14)).pack(pady=5)
            self.answer_entry = ctk.CTkOptionMenu(self.options_frame, values=["True", "False"])
            self.answer_entry.pack(pady=5)

        elif choice == "Fill in the Blank":
            self.answer_entry = ctk.CTkEntry(self.options_frame, width=300, placeholder_text="Correct Answer")
            self.answer_entry.pack(pady=5)

    # ----------------------------
    # Save to JSON
    # ----------------------------
    def save_question(self):
        prompt = self.prompt_entry.get().strip()
        q_type = self.q_type.get()
        data = {}

        if not prompt:
            self.status_label.configure(text="⚠️ Please enter a question prompt!", text_color="red")
            return

        if q_type == "Multiple Choice":
            options = [e.get().strip() for e in self.option_entries if e.get().strip()]
            answer = self.answer_entry.get().strip()
            if not options or not answer:
                return
            data = {"type": "mc", "prompt": prompt, "options": options, "answer": answer}

        elif q_type == "True/False":
            answer = self.answer_entry.get().strip()
            data = {"type": "tf", "prompt": prompt, "answer": answer}

        elif q_type == "Fill in the Blank":
            answer = self.answer_entry.get().strip()
            if not answer:
                return
            data = {"type": "fib", "prompt": prompt, "answer": answer}

        # Save to file
        questions = []
        if os.path.exists(USER_QUESTIONS_FILE):
            with open(USER_QUESTIONS_FILE, "r") as f:
                try:
                    questions = json.load(f)
                except json.JSONDecodeError:
                    questions = []

        questions.append(data)

        with open(USER_QUESTIONS_FILE, "w") as f:
            json.dump(questions, f, indent=4)

        # Confirmation
        self.status_label.configure(text="✅ Question Saved!", text_color="green")

        self.prompt_entry.delete(0, "end")
        if q_type == "Multiple Choice":
            for entry in self.option_entries:
                entry.delete(0, "end")
        self.answer_entry.delete(0, "end")


# ----------------------------
# Test run
# ----------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    AddQuestionWindow(root)
    root.mainloop()
