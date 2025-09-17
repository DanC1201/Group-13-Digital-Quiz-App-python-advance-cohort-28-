from abc import ABC, abstractmethod

class Question(ABC):
    """Base class for all quiz questions."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    @abstractmethod
    def is_correct(self, user_answer):
        """Check if the user's answer is correct."""
        pass


class MultipleChoiceQuestion(Question):
    """A question with multiple choice answers."""

    def __init__(self, text, choices, answer):
        super().__init__(text, answer)
        self.choices = choices  # list of possible answers

    def is_correct(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()
