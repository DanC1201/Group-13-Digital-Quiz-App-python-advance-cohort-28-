import tkinter as tk
import json
import os

SCORE_FILE = "user_scores.json" # File to store our user scores

def save_score(user_name, score, total): # Function to save scores
    # Create a dictionary entry with the user's name, score and total questions
    entry = {
        "user": user_name,
        "score": score,
        "total": total
    }
    # Check if the score file already exists
    if os.path.exists(SCORE_FILE):
    # If it already exists, load it
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
    else:
    # If it does not exist create an empty list
        data = []
    # Add the new score entry to the list
    data.append(entry)
    #  Write the updated score list back to the file
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f, indent=2)
class ScoreWindow:
    def __init__(self, master, score, total, user_answers,user_name): # Updated Constructor to accept user_name
        self.master = master
        self.master.title("Quiz App - Score")
        self.master.geometry("400x400")

        save_score(user_name, score, total) #Save the score
        # Display the final score at the top of the window
        tk.Label(self.master, text=f"Your Final Score: {score} out of {total}", font=("Arial", 18)).pack(pady=20)

        # Create a text widget to show detailed answer breakdown
        details = tk.Text(self.master, height=15, width=50)
        details.pack()

        # Insert header row for the answer breakdown
        details.insert(tk.END, "Q | Your Answer | Correct\n")

        # Loop through each question and show user's answer and correctness
        for i, (q, ans, correct) in enumerate(user_answers, 1):
            details.insert(tk.END, f"{i}. {q[:30]}... | {ans} | {'✔' if correct else '✘'}\n")
        details.config(state=tk.DISABLED)

        # Add an Exit button to close the application
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10)
