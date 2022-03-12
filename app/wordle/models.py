from typing import Any

from pydantic import BaseModel


class Guess(BaseModel):
    word: str
    hints: str  # Correct/Incorrect spot, Not in word
    # example: word="robot", hints="ICNCI"

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__._normalize()

    def _normalize(self):
        self.word = self.word.lower()
        self.hints = self.hints.upper()

    def is_valid(self) -> bool:
        if len(self.word) != len(self.hints):
            return False

        for hint in self.hints:
            if hint.upper() not in "CIN":
                return False

        return True


class CandidateWord(BaseModel):
    word: str
    score: float
