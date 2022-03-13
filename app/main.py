import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import wordle
from app.wordle.solver import Guess

from . import gpt3

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
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


@app.post("/gpt3/summarize")
async def openai_summarize(request_body: SummarizeInput):
    """Summarize a piece of text with OpenAI GPT-3."""
    logger.info(f"/gpt3/summarize request_body: {request_body}")
    return gpt3.summarize(request_body.text)


# ===
# WORDLE SOLVER
# ===


@app.get("/wordle/random")
async def wordle_random():
    """Randomize a 5-letter word."""
    word = wordle.solver.choose_random_word()
    return {"word": word}


class GuessInput(BaseModel):
    guesses: list[Guess]


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

    possible_wordles = wordle.solver.find_candidate_results(guesses)

    return {
        "possible_wordles": possible_wordles,
    }
