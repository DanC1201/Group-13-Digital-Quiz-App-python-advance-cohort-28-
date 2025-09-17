import pytest
import sys, os

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quiz.question import TrueFalseQuestion

def test_truefalse_correct_answer():
    q = TrueFalseQuestion(
        text="The Earth orbits the Sun.",
        answer=True
    )
    assert q.is_correct(True) is True
    assert q.is_correct(False) is False

def test_truefalse_incorrect_answer():
    q = TrueFalseQuestion(
        text="The Moon is bigger than the Earth.",
        answer=False
    )
    assert q.is_correct(False) is True
    assert q.is_correct(True) is False
