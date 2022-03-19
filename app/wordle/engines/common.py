import math

from app.wordle import dictionary
from app.wordle.models import CandidateWord, Guess


class SolverEngine:
    def __init__(self, word_list: list[str], guesses: list[Guess]):
        self.word_list = word_list
        self.guesses = guesses

    def get_candidate_result(self, limit) -> list[CandidateWord]:
        pass


def compute_score_by_matches_and_freq(word: str, guesses: list[Guess]):
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


def filter_non_matches(word_list: list[str], guess: Guess) -> list[str]:
    filtered = []
    for word in word_list:
        possible = _guess_align_with_word(guess, word)
        if possible:
            filtered.append(word)

    return filtered


def _guess_align_with_word(guess: Guess, word: str) -> bool:
    if len(guess.word) != len(word):
        raise ValueError(
            f"lenght of guess and candidate word do not match:"
            + f"guess={guess.word}, candidate_word={word}"
        )

    # 1st constraint: number of letters must match:
    letter_occurances: dict[str, int] = {}
    for i, letter in enumerate(guess.word):
        if guess.hints[i] in ("I", "C"):
            letter_occurances[letter] = 1 + (letter_occurances.get(letter) or 0)

    for letter, occurances in letter_occurances.items():
        if word.count(letter) != occurances:
            return False

    # 2nd constrant: letters position must match:
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
