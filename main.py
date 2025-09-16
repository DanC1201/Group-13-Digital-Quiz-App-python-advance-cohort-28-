class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer


def run_quiz(questions):
    score = 0
    for q in questions:
        answer = input(q.prompt + "\nYour answer: ")
        if answer.lower() == q.answer.lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer is {q.answer}\n")

    print(f"🎯 Final Score: {score}/{len(questions)}")


questions = [
    Question("1) What is the capital of France? (A) Paris (B) London (C) Madrid", "A"),
    Question("2) Python is a programming language. (True/False)", "True"),
]

run_quiz(questions)
