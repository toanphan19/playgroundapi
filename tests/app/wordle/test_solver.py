from app.wordle import solvers
from app.wordle.models import Guess


def test_guess_align_with_word():
    word = "robot"
    guess = Guess(word="motor", hints="NCICI")
    guess2 = Guess(word="motor", hints="NCIII")
    assert solvers.engines.common._guess_align_with_word(guess, word) == True
    assert solvers.engines.common._guess_align_with_word(guess2, word) == False
