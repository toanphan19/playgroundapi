from app import wordle
from app.wordle.solver import Guess


def demo_find_candidate_results():
    # word = humor
    guesses = [
        Guess(word="lover", hints=list("NINNC")),
        Guess(word="tumor", hints=list("NCCCC")),
    ]
    candidate_results = wordle.solver.find_candidate_results(guesses)
    print(candidate_results, sep="\n")


if __name__ == "__main__":
    demo_find_candidate_results()
