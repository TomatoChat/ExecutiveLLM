from typing import Dict, List

from openai import OpenAI


def runPrompt(
    client: OpenAI,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Dict[str, str]],
) -> str:
    """
    Run a prompt through the OpenAI API.
    """
    response = client.chat.completions.create(
        model=model,
        max_tokens=maxTokens,
        temperature=temperature,
        messages=messages,
    )

    return response.choices[0].message.content
