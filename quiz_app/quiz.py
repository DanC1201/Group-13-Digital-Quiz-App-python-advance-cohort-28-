import customtkinter as ctk
from tkinter import messagebox
from questions import get_random_questions, MultipleChoiceQuestion, TrueFalseQuestion, FillInTheBlankQuestion
from score import ScoreWindow
import tkinter as tk


class QuizWindow:
    def __init__(self, master, user_name, on_finish):
        self.master = master
        self.user_name = user_name
        self.on_finish = on_finish

        self.master.title("Quiz App - Quiz")
        self.master.geometry("600x500")

        # Get questions
        self.questions = get_random_questions(10)  # Default 10

        if not self.questions:
            messagebox.showerror("Error", "No questions available.\nPlease add or import some questions.")
            self.master.destroy()
            return
        if len(self.questions) < 5:
            messagebox.showinfo("Notice", f"Only {len(self.questions)} questions available.")

        self.current_index = 0
        self.score = 0
        self.user_answers = []

        # Timer state
        self.time_left = 60
        self.timer_id = None

        # Layout
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Timer label
        self.timer_label = ctk.CTkLabel(
            self.frame,
            text="Time Left: 60s",
            font=("Arial", 14, "bold")
        )
        self.timer_label.pack(pady=(0, 10))

        # Question label
        self.question_label = ctk.CTkLabel(
            self.frame,
            text="",
            wraplength=500,
            font=("Arial", 16, "bold"),
            justify="center"
        )
        self.question_label.pack(pady=(10, 5))

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.frame, width=400)
        self.progress.pack(pady=10)
        self.progress.set(0)  # start empty

        # Options container
        self.options_frame = ctk.CTkFrame(self.frame)
        self.options_frame.pack(pady=15)

        # Selected option
        self.selected_option = ctk.StringVar(value="")

        # Buttons
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=25)

        # Quit button (left)
        self.quit_button = ctk.CTkButton(
            self.button_frame,
            text="Quit Quiz",
            command=self.quit_quiz,
            fg_color="red",
            hover_color="darkred",
            width=120,
        )
        self.quit_button.grid(row=0, column=0, padx=10)

        # Skip button (middle)
        self.skip_button = ctk.CTkButton(
            self.button_frame,
            text="Skip",
            command=self.skip_question,
            fg_color="orange",
            hover_color="darkorange",
            width=120,
        )
        self.skip_button.grid(row=0, column=1, padx=10)

        # Next button (right)
        self.next_button = ctk.CTkButton(
            self.button_frame, text="Next", command=self.next_question, width=120
        )
        self.next_button.grid(row=0, column=2, padx=10)

        # Show first question
        self.show_question()

    # ------------------------
    # Timer Methods
    # ------------------------
    def start_timer(self):
        """Start or restart the 60s timer for each question."""
        self.cancel_timer()
        self.time_left = 60
        self.update_timer()

    def update_timer(self):
        """Update the timer label each second."""
        self.timer_label.configure(text=f"Time Left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.skip_question()  # auto-skip if time runs out

    def cancel_timer(self):
        """Stop the timer if it's running."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    # ------------------------
    # Show Question
    # ------------------------
    def show_question(self):
        q = self.questions[self.current_index]
        self.question_label.configure(text=f"Q{self.current_index + 1}: {q.prompt}")

        # Clear old options safely
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Reset the StringVar to a new one each time
        self.selected_option = ctk.StringVar(value="")

        if isinstance(q, MultipleChoiceQuestion):
            for option in q.options:
                ctk.CTkRadioButton(
                    self.options_frame,
                    text=option,
                    variable=self.selected_option,
                    value=option,
                ).pack(anchor="w", pady=5)

        elif isinstance(q, TrueFalseQuestion):
            for option in ["True", "False"]:
                ctk.CTkRadioButton(
                    self.options_frame,
                    text=option,
                    variable=self.selected_option,
                    value=option,
                ).pack(anchor="w", pady=5)

        elif isinstance(q, FillInTheBlankQuestion):
            ctk.CTkEntry(
                self.options_frame,
                textvariable=self.selected_option,
                width=300
            ).pack(pady=10)

        # Update progress bar
        progress_value = (self.current_index + 1) / len(self.questions)
        self.progress.set(progress_value)

        # Start timer for this question
        self.start_timer()

    # ------------------------
    # Next Question
    # ------------------------
    def next_question(self):
        self.cancel_timer()  # stop timer
        q = self.questions[self.current_index]
        user_ans = self.selected_option.get().strip()

        # Auto-skip if nothing selected
        if not user_ans:
            self.record_answer(user_ans, correct=False)
        else:
            correct = q.is_correct(user_ans)
            if correct:
                self.score += 1
            self.record_answer(user_ans, correct)

        self.go_next()

    # ------------------------
    # Skip Question
    # ------------------------
    def skip_question(self):
        self.cancel_timer()  # stop timer
        self.record_answer("Skipped", correct=False)
        self.go_next()

    # ------------------------
    # Record Answer Helper
    # ------------------------
    def record_answer(self, user_ans, correct):
        q = self.questions[self.current_index]
        self.user_answers.append((q.prompt, user_ans, q.answer, correct))

    # ------------------------
    # Go to Next or Finish
    # ------------------------
    def go_next(self):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question()
        else:
            self.finish_quiz()

    # ------------------------
    # Finish Quiz
    # ------------------------
    def finish_quiz(self):
        self.cancel_timer()
        self.master.destroy()
        result_root = ctk.CTk()

        def back_to_main():
            from main import MainMenu
            root = ctk.CTk()
            MainMenu(root)
            root.mainloop()

        ScoreWindow(result_root, self.score, len(self.questions), self.user_answers, self.user_name)
        result_root.mainloop()
        self.on_finish(self.score, len(self.questions), self.user_answers)

    # ------------------------
    # Quit Quiz Early
    # ------------------------
    def quit_quiz(self):
        confirm = messagebox.askyesno("Quit", "Are you sure you want to quit the quiz?")
        if confirm:
            self.finish_quiz()
