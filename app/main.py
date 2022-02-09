from fastapi import FastAPI
from pydantic import BaseModel
import logging

from . import gpt3

app = FastAPI()

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
