import random

from . import dictionary
from .models import Guess


def choose_random_word():
    word = random.choice(dictionary.fives)
    return word


def find_candidate_results(guesses: list[Guess], limit=20) -> list[str]:
    candidate_results = dictionary.fives
    for guess in guesses:
        candidate_results = _filter_candidate_results(candidate_results, guess)

    return candidate_results[:limit]


def _filter_candidate_results(candidate_results: list[str], guess: Guess) -> list[str]:
    filtered = []
    for word in candidate_results:
        possible = _guess_align_with_word(guess, word)
        if possible:
            filtered.append(word)

    return filtered


def _guess_align_with_word(guess: Guess, word: str):
    if len(guess.word) != len(word):
        raise ValueError(
            f"lenght of guess and candidate word do not match:"
            + f"guess={guess.word}, candidate_word={word}"
        )

    hints = guess.hints.upper()
    for pos, hint in enumerate(hints):
        if hint == "N":
            if guess.word[pos] in word:
                return False
        if hint == "C":
            if word[pos] != guess.word[pos]:
                return False
        if hint == "I":
            if not (guess.word[pos] in word and guess.word[pos] != word[pos]):
                return False

    return True
