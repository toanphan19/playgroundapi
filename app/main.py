import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import wordle
from app import hnews
from app.wordle.solvers import Guess

app = FastAPI()

origins = [
    "https://playground.toanphan.dev",
    "https://toanphan.com",
]

if os.getenv("MYENV") == "local":
    origins += [
        "http://127.0.0.1:1111",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return "Hello World! This is a small playground, feel free to walk around!"


class SummarizeInput(BaseModel):
    text: str


# ===
# Others
# ===
@app.get("/hckernews/top")
def hckernews_top(days: int, limit: int = 10):
    conn_str = os.environ["SUPABASE_SESSION_CONN_STR"]
    stories = hnews.get_top_stories(conn_str, days, limit)
    return {"stories": stories}


# ===
# WORDLE SOLVER
# ===


@app.get("/wordle/random")
async def wordle_random():
    """Randomize a 5-letter word."""
    word = wordle.solvers.choose_random_word()
    return {"word": word}


class GuessInput(BaseModel):
    guesses: list[Guess]
    engine: str | None = None


@app.post("/wordle/solver")
async def wordle_solver(request_body: GuessInput):
    """Guess the word based on existing guesses."""
    guesses = request_body.guesses

    # Check valid
    for guess in guesses:
        if not guess.is_valid():
            raise HTTPException(
                status_code=400, detail="Invalid guess (incorrect guess word or hints)"
            )

    possible_wordles = wordle.solvers.find_candidate_results(guesses)

    return {
        "possible_wordles": possible_wordles,
    }
