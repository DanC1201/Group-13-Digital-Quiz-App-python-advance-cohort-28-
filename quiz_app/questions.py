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

    # TF
    TrueFalseQuestion("The Earth is flat.", "False"),
    TrueFalseQuestion("The Sun is a star.", "True"),
    TrueFalseQuestion("The Earth revolves around the Sun.", "True"),
    TrueFalseQuestion("There are 26 letters in the English alphabet.", "True"),
    TrueFalseQuestion("The human body has four lungs.", "False"),
    TrueFalseQuestion("The Great Wall of China is located in India.", "False"),
    TrueFalseQuestion("Sharks are mammals.", "False"),
    TrueFalseQuestion("Lightning never strikes the same place twice.", "False"),
    TrueFalseQuestion("The Pacific Ocean is larger than the Atlantic Ocean.", "True"),
    TrueFalseQuestion("Bats are blind.", "False"),
    TrueFalseQuestion("The chemical symbol for gold is Au.", "True"),
    TrueFalseQuestion("Mount Everest is the tallest mountain in the world.", "True"),
    TrueFalseQuestion("An octopus has three hearts.", "True"),
    TrueFalseQuestion("Penguins can fly.", "False"),
    TrueFalseQuestion("The capital of Australia is Sydney.", "False"),  # It's Canberra
    TrueFalseQuestion("Water boils at 100 degrees Celsius.", "True"),
    TrueFalseQuestion("The Moon is a planet.", "False"),
    TrueFalseQuestion("Venus is the closest planet to the Sun.", "False"),  # Mercury is
    TrueFalseQuestion("Bananas grow on trees.", "False"),  # They grow on plants
    TrueFalseQuestion("The human skeleton is made up of more than 200 bones.", "True"),
    TrueFalseQuestion("Spiders have six legs.", "False"),  # They have eight
    TrueFalseQuestion("The Amazon is the longest river in the world.", "False"),  # Nile is
    TrueFalseQuestion("The human brain is inside the rib cage.", "False"),
    TrueFalseQuestion("The Statue of Liberty was a gift from France to the USA.", "True"),
    TrueFalseQuestion("Dolphins are fish.", "False"),  # They're mammals
    TrueFalseQuestion("The Sahara is the largest hot desert in the world.", "True"),
    TrueFalseQuestion("The Sun rises in the west and sets in the east.", "False"),
    TrueFalseQuestion("Sound travels faster in water than in air.", "True"),
    TrueFalseQuestion("A leap year has 366 days.", "True"),
    TrueFalseQuestion("The capital of Italy is Rome.", "True"),


    # FIB
    FillInTheBlankQuestion("______ is the largest ocean on Earth.", "Pacific"),
    FillInTheBlankQuestion("The process of converting water vapor into liquid is called ______.", "Condensation"),
    FillInTheBlankQuestion("The chemical symbol for water is ______.", "H2O"),
    FillInTheBlankQuestion("The largest ocean on Earth is the ______ Ocean.", "Pacific"),
    FillInTheBlankQuestion("The fastest land animal is the ______.", "Cheetah"),
    FillInTheBlankQuestion("The currency used in the United States is the ______.", "Dollar"),
    FillInTheBlankQuestion("The first man to walk on the Moon was ______ Armstrong.", "Neil"),
    FillInTheBlankQuestion("The Great Wall of ______ is visible from space.", "China"),
    FillInTheBlankQuestion("The process by which plants make food is called ______.", "Photosynthesis"),
    FillInTheBlankQuestion("The tallest mountain in the world is Mount ______.", "Everest"),
    FillInTheBlankQuestion("The freezing point of water is ______ degrees Celsius.", "0"),
    FillInTheBlankQuestion("The smallest prime number is ______.", "2"),
    FillInTheBlankQuestion("The currency of Japan is the ______.", "Yen"),
    FillInTheBlankQuestion("The longest river in the world is the ______.", "Nile"),
    FillInTheBlankQuestion("The study of stars and planets is called ______.", "Astronomy"),
    FillInTheBlankQuestion("The largest desert in the world is the ______ Desert.", "Sahara"),
    FillInTheBlankQuestion("The gas that humans need to survive is ______.", "Oxygen"),
    FillInTheBlankQuestion("The scientist who proposed the theory of relativity is ______.", "Einstein"),
    FillInTheBlankQuestion("The country famous for the Eiffel Tower is ______.", "France"),
    FillInTheBlankQuestion("The chemical symbol for water is ______.", "H2O"),
    FillInTheBlankQuestion("The fastest land animal is the ______.", "Cheetah"),
    FillInTheBlankQuestion("The first man to walk on the Moon was ______ Armstrong.", "Neil"),
    FillInTheBlankQuestion("The process by which plants make food is called ______.", "Photosynthesis"),
    FillInTheBlankQuestion("The tallest mountain in the world is Mount ______.", "Everest"),
    FillInTheBlankQuestion("The freezing point of water is ______ degrees Celsius.", "0"),
    FillInTheBlankQuestion("The smallest prime number is ______.", "2"),
    FillInTheBlankQuestion("The currency of Japan is the ______.", "Yen"),
    FillInTheBlankQuestion("The longest river in the world is the ______.", "Nile"),
    FillInTheBlankQuestion("The scientist who proposed the theory of relativity is ______.", "Einstein"),
    FillInTheBlankQuestion("The country famous for the Eiffel Tower is ______.", "France"),
    FillInTheBlankQuestion("The largest desert in the world is the ______ Desert.", "Sahara"),

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

def get_random_questions(n=1):
    user_questions = load_user_questions()
    csv_questions = load_csv_questions()
    questions = SAMPLE_QUESTIONS + user_questions + csv_questions
    # Repeat sample questions if not enough
    while len(questions) < n:
        questions += SAMPLE_QUESTIONS
    random.shuffle(questions)

    return questions[:n]
