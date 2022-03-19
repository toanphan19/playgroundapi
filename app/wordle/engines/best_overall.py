from app.wordle.models import CandidateWord, Guess
from . import common


class BestOverallEngine(common.SolverEngine):
    def get_candidate_result(self, limit) -> list[CandidateWord]:
        """If the number of candidates is quite few, return the candidate list.
        Otherwise return the words that give the most number of new letters."""
        NB_CANDIDATES_THRESHOLD = 12

        candidate_results = self.word_list
        for guess in self.guesses:
            candidate_results = common.filter_non_matches(candidate_results, guess)

        print(len(candidate_results))
        if len(candidate_results) < NB_CANDIDATES_THRESHOLD:
            return [
                CandidateWord(
                    word=word,
                    score=common.compute_score_by_matches_and_freq(word, self.guesses),
                )
                for word in candidate_results
            ]

        # 2nd case:
        candidate_results = self.word_list
        candidates_with_score = [
            CandidateWord(
                word=word,
                score=common.compute_score_by_matches_and_freq(word, self.guesses),
            )
            for word in candidate_results
        ]
        candidates_with_score.sort(key=lambda candidate: candidate.score, reverse=True)

        return candidates_with_score[:limit]
