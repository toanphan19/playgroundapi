from audioop import reverse
import math
import random

from . import dictionary
from .models import CandidateWord, Guess


def choose_random_word():
    word = random.choice(dictionary.fives)
    return word


def find_candidate_results(guesses: list[Guess], limit=20) -> list[CandidateWord]:
    candidate_results = dictionary.fives
    for guess in guesses:
        candidate_results = _filter_candidate_results(candidate_results, guess)

    # Compute and order by score:
    candidates_with_score = [
        CandidateWord(word=word, score=_compute_score(word, guesses))
        for word in candidate_results
    ]
    candidates_with_score.sort(key=lambda candidate: candidate.score, reverse=True)

    return candidates_with_score[:limit]


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


def _compute_score(word: str, guesses: list[Guess]):
    """Score = number of new letters + their frequencies.

    Sorting by this score will give you an order based on:
    - the number of new characters
    - then on their frequencies
    """
    guessed_letters = _get_guessed_letters(guesses)
    letters = set(word)
    potential_new_letters = letters - guessed_letters

    score: float = len(potential_new_letters) + math.fsum(
        dictionary.letter_frequencies[l] / 100 for l in potential_new_letters
    )
    return score


def _get_guessed_letters(guesses: list[Guess]) -> set[str]:
    guessed_words = [guess.word for guess in guesses]
    guessed_letters = set("".join(guessed_words))
    return guessed_letters
