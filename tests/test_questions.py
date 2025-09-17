import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quiz.question import MultipleChoiceQuestion



def test_multiple_choice_correct_answer():
    q = MultipleChoiceQuestion(
        text="What is the capital of France?",
        choices=["Paris", "London", "Berlin", "Rome"],
        answer="Paris"
    )
    assert q.is_correct("Paris") is True

def test_multiple_choice_incorrect_answer():
    q = MultipleChoiceQuestion(
        text="What is 2 + 2?",
        choices=["3", "4", "5"],
        answer="4"
    )
    assert q.is_correct("5") is False
    
def test_multiple_choice_incorrect_answer():
    q = MultipleChoiceQuestion(
        text="What is the capital of Nigeria?",
        choices=["Lagos", "Abuja", "Kano", "Ibadan"],
        answer="Abuja"
    )
    assert q.is_correct("Lagos") is False
    assert q.is_correct("Abuja") is True