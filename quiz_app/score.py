import customtkinter as ctk
import json
import os

SCORE_FILE = "user_scores.json"  # File to store user scores


# ----------------------------
# Save Score
# ----------------------------
def save_score(user_name, score, total):
    """Save a single score entry for the user."""
    entry = {"user": user_name, "score": score, "total": total}

    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(SCORE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ----------------------------
# Score Window (after finishing a quiz)
# ----------------------------
class ScoreWindow:
    def __init__(self, master, score, total, user_answers, user_name):
        self.master = master
        self.master.title("Quiz App - Score")
        self.master.geometry("850x550")  # wider for question column

        save_score(user_name, score, total)  # Save score

        frame = ctk.CTkFrame(master, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Final score label
        ctk.CTkLabel(
            frame,
            text=f"Your Final Score: {score} / {total}",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        # Scrollable Frame for results
        scroll_frame = ctk.CTkScrollableFrame(frame, width=800, height=350)
        scroll_frame.pack(pady=10)

        # Table headers (added Question column)
        headers = ["Q#", "Question", "Your Answer", "Correct Answer", "Status"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=text,
                font=("Arial", 12, "bold"),
                wraplength=250,  # wrap long text in Question column
                anchor="w"
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Table rows
        for i, (q, user_ans, correct_ans, correct) in enumerate(user_answers, 1):
            ctk.CTkLabel(scroll_frame, text=str(i)).grid(row=i, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(scroll_frame, text=q, wraplength=250, anchor="w").grid(row=i, column=1, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(scroll_frame, text=user_ans).grid(row=i, column=2, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(scroll_frame, text=correct_ans).grid(row=i, column=3, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(
                scroll_frame,
                text="✔" if correct else "✘",
                text_color="green" if correct else "red"
            ).grid(row=i, column=4, padx=10, pady=2, sticky="w")

        # Exit button
        ctk.CTkButton(frame, text="Exit", command=self.master.destroy, fg_color="red").pack(pady=15)


# ----------------------------
# Score History Window
# ----------------------------
class ScoreHistoryWindow:
    def __init__(self, master, close_callback=None):
        self.master = master
        self.close_callback = close_callback
        self.master.title("Quiz App - Score History")
        self.master.geometry("600x550")

        frame = ctk.CTkFrame(master, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Score History",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        # Scrollable frame for history
        history_frame = ctk.CTkScrollableFrame(frame, width=540, height=350)
        history_frame.pack(pady=10, fill="both", expand=True)

        # Table headers
        headers = ["User", "Score", "Total", "Percent"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                history_frame,
                text=header,
                font=("Arial", 14, "bold"),
                anchor="center"
            ).grid(row=0, column=col, padx=10, pady=5, sticky="ew")

        # Load & sort data
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)

            # Sort by percentage (descending)
            data.sort(key=lambda x: x["score"] / x["total"], reverse=True)

            for i, entry in enumerate(data, start=1):
                percent = f"{(entry['score']/entry['total'])*100:.1f}%"
                values = [entry['user'], entry['score'], entry['total'], percent]

                for col, val in enumerate(values):
                    ctk.CTkLabel(
                        history_frame,
                        text=str(val),
                        anchor="center"
                    ).grid(row=i, column=col, padx=10, pady=5, sticky="ew")
        else:
            ctk.CTkLabel(history_frame, text="No scores recorded yet.").grid(row=1, column=0, columnspan=4, pady=20)

        # Close button
        ctk.CTkButton(frame, text="Close", command=self.close_window).pack(pady=15)

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.master.destroy()
        if self.close_callback:
            self.close_callback()
