import random
from typing import Literal

from . import dictionary
from .models import CandidateWord, Guess
from . import engines


ENGINES = Literal["best_overall", "highest_matches"]


def choose_random_word():
    word = random.choice(dictionary.fives)
    return word


def find_candidate_results(
    guesses: list[Guess], engine: ENGINES = "best_overall", limit=20
) -> list[CandidateWord]:

    if engine == "best_overall":
        solver_engine: engines.SolverEngine = engines.BestOverallEngine(
            word_list=dictionary.fives, guesses=guesses
        )
    elif engine == "highest_matches":
        solver_engine = engines.HighestMatchesEngine(
            word_list=dictionary.fives, guesses=guesses
        )
    else:
        raise ValueError(f"Unknown solver: {engine}")

    candidate_results = solver_engine.get_candidate_result(limit)

    return candidate_results
