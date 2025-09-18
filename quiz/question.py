class Question:
    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    def is_correct(self, user_answer):
        return self.answer == user_answer


class MultipleChoiceQuestion(Question):
    def __init__(self, text, choices, answer):
        super().__init__(text, answer)
        self.choices = choices

    def display(self):
        print(self.text)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")


class TrueFalseQuestion(Question):
    def __init__(self, text, answer: bool):
        super().__init__(text, answer)

    def display(self):
        print(f"{self.text} (True/False)")
