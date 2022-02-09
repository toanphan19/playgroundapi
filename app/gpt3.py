import os
import json
import logging

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


def summarize(text: str) -> str:
    """Summarise a piece of text.

    Maximum text input: 6000 characters.
    """
    MAX_INPUT_CHARS = 6000
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(f"Input text exceed maximum of {MAX_INPUT_CHARS} characters")

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt="Summarize this for a second-grade student:\n\n" + text,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    if len(response["choices"]) == 0:
        raise Exception(
            f"No answer found from openai. Response: {json.dumps(response)}"
        )

    logger.info(response)
    response_text: str = response["choices"][0]["text"]
    response_text = response_text.strip()

    return response_text


if __name__ == "__main__":
    response = summarize(
        """Tokens can be thought of as pieces of words. Before the API processes the prompts, the input is broken down into tokens. These tokens are not cut up exactly where the words start or end - tokens can include trailing spaces and even sub-words.
    """
    )

    print(response)
