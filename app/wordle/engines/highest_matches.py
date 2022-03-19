from app.wordle.models import CandidateWord, Guess
from . import common


class HighestMatchesEngine(common.SolverEngine):
    def get_candidate_result(self, limit) -> list[CandidateWord]:
        candidate_results = self.word_list
        for guess in self.guesses:
            candidate_results = common.filter_non_matches(candidate_results, guess)

        # Compute and order by score:
        candidates_with_score = [
            CandidateWord(
                word=word,
                score=common.compute_score_by_matches_and_freq(word, self.guesses),
            )
            for word in candidate_results
        ]
        candidates_with_score.sort(key=lambda candidate: candidate.score, reverse=True)

        return candidates_with_score[:limit]
