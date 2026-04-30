from app.wordle import solvers
from app.wordle.models import Guess


def test_guess_align_with_word():
    word = "robot"
    guess = Guess(word="motor", hints="NCICI")
    guess2 = Guess(word="motor", hints="NCIII")
    assert solvers.engines.common._guess_align_with_word(guess, word) == True
    assert solvers.engines.common._guess_align_with_word(guess2, word) == False


def test_guess_align_with_word_double_letters():
    # "crook" vs target with one 'o': second 'o' gets N, meaning exactly 1 'o' in target
    guess = Guess(word="crook", hints="CICNN")
    assert solvers.engines.common._guess_align_with_word(guess, "chore") == True
    # target with two 'o's should be rejected (o=N means no extra o's beyond the C/I one)
    assert solvers.engines.common._guess_align_with_word(guess, "croon") == False
