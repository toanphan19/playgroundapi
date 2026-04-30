import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from pydantic import BaseModel

from app import wordle
from app.wordle.solvers import Guess

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://playground.toanphan.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
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
def hckernews_top(days: int):
    conn_str = os.environ["SUPABASE_SESSION_CONN_STR"]
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            stories = get_top_stories(cur, days)
            conn.commit()
            return {"stories": stories}


def get_top_stories(cur, nr_days: int, limit: int = 20):
    limit = min(50, limit)
    sql = """
            select 
                id,
                time,
                title,
                url,
                score,
                comments
            from hn_stories
            where time > now() - make_interval(days => %s)
            order by score desc
            limit %s;
            """
    cur.execute(sql, (nr_days, limit))
    rows = cur.fetchall()
    print(len(rows))

    return rows


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
