from app import wordle
from app.wordle.solver import Guess


def demo_find_candidate_results():
    # # word = humor
    # guesses = [
    #     Guess(word="lover", hints="NINNC"),
    #     Guess(word="tumor", hints="NCCCC"),
    # ]
    # candidate_results = wordle.solver.find_candidate_results(guesses)
    # print(candidate_results, sep="\n")

    # word = humor
    guesses = [
        Guess(word="lover", hints="IINNN"),
        Guess(word="gloam", hints="NCIIN"),
    ]
    candidate_results = wordle.solver.find_candidate_results(
        guesses,
        # engine="best_overall"
        engine="highest_matches",
    )
    for cr in candidate_results:
        print(cr)


if __name__ == "__main__":
    demo_find_candidate_results()
