from typing import Dict, List

from anthropic import Anthropic


def runPrompt(
    client: Anthropic,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Dict[str, str]],
) -> str:
    """
    Run a prompt through the Anthropic API.
    """
    response = client.messages.create(
        model=model,
        max_tokens=maxTokens,
        temperature=temperature,
        messages=messages,
    )

    return response.content[0].text
