import random
import json
import os
import csv

USER_QUESTIONS_FILE = "user_questions.json"
CSV_QUESTIONS_FILE = "csv_questions.csv"

def load_csv_questions():
    questions = []
    if os.path.exists(CSV_QUESTIONS_FILE):
        with open(CSV_QUESTIONS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                prompt = row['prompt'].strip()
                answer = row['answer'].strip()
                options = [opt.strip() for opt in row['options'].split(',')]
                questions.append(MultipleChoiceQuestion(prompt, options, answer))
    return questions


class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

    def is_correct(self, user_answer):
        raise NotImplementedError("Subclasses should implement this method.")

class MultipleChoiceQuestion(Question):
    def __init__(self, prompt, options, answer):
        super().__init__(prompt, answer)
        self.options = options

    def is_correct(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()

class TrueFalseQuestion(Question):
    def __init__(self, prompt, answer):
        super().__init__(prompt, answer)

    def is_correct(self, user_answer):
        return str(user_answer).strip().lower() == str(self.answer).strip().lower()

class FillInTheBlankQuestion(Question):
    def __init__(self, prompt, answer):
        super().__init__(prompt, answer)

    def is_correct(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()

# Example question list for testing
SAMPLE_QUESTIONS = [
    MultipleChoiceQuestion("What is the capital of France?", ["Paris", "London", "Berlin", "Rome"], "Paris"),
    MultipleChoiceQuestion("Which planet is known as the Red Planet?", ["Earth", "Mars", "Jupiter", "Venus"], "Mars"),
    MultipleChoiceQuestion("Who wrote 'Romeo and Juliet'?", ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"], "William Shakespeare"),
    MultipleChoiceQuestion("What is the largest mammal?", ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "Blue Whale"),
    MultipleChoiceQuestion("Which element has the chemical symbol 'O'?", ["Gold", "Oxygen", "Silver", "Iron"], "Oxygen"),
    MultipleChoiceQuestion("What is the hardest natural substance?", ["Gold", "Iron", "Diamond", "Quartz"], "Diamond"),
    MultipleChoiceQuestion("Which country is the Great Wall located in?", ["India", "China", "Japan", "Russia"], "China"),
    MultipleChoiceQuestion("How many continents are there?", ["5", "6", "7", "8"], "7"),
    MultipleChoiceQuestion("What is the boiling point of water?", ["100°C", "90°C", "80°C", "120°C"], "100°C"),
    MultipleChoiceQuestion("Who painted the Mona Lisa?", ["Vincent Van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"], "Leonardo da Vinci"),
    MultipleChoiceQuestion("Which gas do plants absorb from the atmosphere?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "Carbon Dioxide"),
    MultipleChoiceQuestion("What is the largest ocean?", ["Atlantic", "Indian", "Pacific", "Arctic"], "Pacific"),
    MultipleChoiceQuestion("Who discovered gravity?", ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"], "Isaac Newton"),
    MultipleChoiceQuestion("Which language has the most native speakers?", ["English", "Mandarin Chinese", "Spanish", "Hindi"], "Mandarin Chinese"),
    MultipleChoiceQuestion("What is the smallest prime number?", ["0", "1", "2", "3"], "2"),
    MultipleChoiceQuestion("Which country gifted the Statue of Liberty to the USA?", ["France", "England", "Germany", "Italy"], "France"),
    MultipleChoiceQuestion("What is the main ingredient in guacamole?", ["Tomato", "Avocado", "Onion", "Pepper"], "Avocado"),
    MultipleChoiceQuestion("Which instrument has keys, pedals, and strings?", ["Guitar", "Piano", "Drum", "Flute"], "Piano"),
    MultipleChoiceQuestion("What is the largest desert?", ["Sahara", "Gobi", "Kalahari", "Arctic"], "Sahara"),
    MultipleChoiceQuestion("Who is known as the father of computers?", ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"], "Charles Babbage"),
    MultipleChoiceQuestion("Which is the longest river in the world?", ["Amazon", "Nile", "Yangtze", "Mississippi"], "Nile"),
    MultipleChoiceQuestion("What is the main language spoken in Brazil?", ["Spanish", "Portuguese", "French", "English"], "Portuguese"),
    MultipleChoiceQuestion("Which vitamin is produced when a person is exposed to sunlight?", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "Vitamin D"),
    MultipleChoiceQuestion("What is the currency of Japan?", ["Yen", "Won", "Dollar", "Euro"], "Yen"),
    MultipleChoiceQuestion("Which animal is known as the King of the Jungle?", ["Tiger", "Lion", "Elephant", "Leopard"], "Lion"),
    MultipleChoiceQuestion("What is the chemical formula for water?", ["CO2", "H2O", "O2", "NaCl"], "H2O"),
    MultipleChoiceQuestion("Who invented the telephone?", ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "James Watt"], "Alexander Graham Bell"),
    MultipleChoiceQuestion("Which continent is Egypt in?", ["Asia", "Africa", "Europe", "Australia"], "Africa"),
    MultipleChoiceQuestion("What is the tallest mountain in the world?", ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"], "Mount Everest"),
    MultipleChoiceQuestion("Which organ pumps blood through the body?", ["Liver", "Heart", "Lungs", "Kidney"], "Heart"),
    MultipleChoiceQuestion("What is the freezing point of water?", ["0°C", "32°C", "100°C", "-10°C"], "0°C"),
]

def load_user_questions():
    if os.path.exists(USER_QUESTIONS_FILE):
        with open(USER_QUESTIONS_FILE, "r") as f:
            data = json.load(f)
        questions = []
        for q in data:
            if q.get("type") == "mc":
                questions.append(MultipleChoiceQuestion(q["prompt"], q["options"], q["answer"]))
            elif q.get("type") == "tf":
                questions.append(TrueFalseQuestion(q["prompt"], q["answer"]))
            elif q.get("type") == "fib":
                questions.append(FillInTheBlankQuestion(q["prompt"], q["answer"]))
        return questions
    return []

def get_random_questions(n=30):
    user_questions = load_user_questions()
    csv_questions = load_csv_questions()
    questions = SAMPLE_QUESTIONS + user_questions + csv_questions
    # Repeat sample questions if not enough
    while len(questions) < n:
        questions += SAMPLE_QUESTIONS
    random.shuffle(questions)

    return questions[:n]
