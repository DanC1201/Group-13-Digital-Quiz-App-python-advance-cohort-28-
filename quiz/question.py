# quiz/question.py

class Question:
    def __init__(self, text: str):
        """
        Base class for all question types.
        :param text: The question text
        """
        self.text = text

    def is_correct(self, answer):
        """
        Check if the provided answer is correct.
        Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method")


class MultipleChoiceQuestion(Question):
    def __init__(self, text: str, choices: list[str], answer: str):
        """
        A multiple-choice question.
        :param text: The question text
        :param choices: List of possible answers
        :param answer: The correct answer (must be in choices)
        """
        super().__init__(text)
        self.choices = choices
        self.answer = answer

    def is_correct(self, response: str) -> bool:
        """Return True if the response matches the correct answer."""
        return response == self.answer


class TrueFalseQuestion(Question):
    def __init__(self, text: str, answer: bool):
        """
        A true/false question.
        :param text: The question text
        :param answer: The correct answer (True or False)
        """
        super().__init__(text)
        self.answer = answer

    def is_correct(self, response: bool) -> bool:
        """Return True if the response matches the correct boolean answer."""
        return response is self.answer
