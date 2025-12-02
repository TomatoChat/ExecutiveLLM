from typing import Dict, List

from anthropic import Anthropic

from ...models.ClaudeModelGrounding import ClaudeModelGrounding


def runPrompt(
    client: Anthropic,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Dict[str, str]],
    enableGrounding: bool = False,
) -> str:
    """
    Run a prompt through the Anthropic API.

    Args:
        client: Anthropic client instance
        model: Model identifier
        maxTokens: Maximum tokens to generate
        temperature: Sampling temperature
        messages: List of message dictionaries
        enableGrounding: Enable web search if supported by model

    Returns:
        Generated text response
    """
    requestParams = {
        "model": model,
        "max_tokens": maxTokens,
        "temperature": temperature,
        "messages": messages,
    }

    if enableGrounding and any(
        model == member.value for member in ClaudeModelGrounding
    ):
        requestParams["tools"] = [
            {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}
        ]

    response = client.messages.create(**requestParams)

    textContent: List[str] = []

    for block in response.content:
        if hasattr(block, "text"):
            textContent.append(block.text)

    return "".join(textContent) if textContent else ""
