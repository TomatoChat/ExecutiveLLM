from typing import Any, Dict, List, Optional

from anthropic import Anthropic
from anthropic.types import TextBlock

from ...models import ClaudeModelGrounding, Message


def runPrompt(
    client: Anthropic,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Message],
    enableGrounding: bool = False,
    countryCode: Optional[str] = None,
) -> str:
    """
    Run a prompt through the Anthropic API.

    Args:
        client: Anthropic client instance
        model: Model identifier
        maxTokens: Maximum tokens to generate
        temperature: Sampling temperature
        messages: Text-only messages (role + content)
        enableGrounding: Enable web search if supported by model
        countryCode: ISO 3166-1 alpha-2 country code for web search location

    Returns:
        Generated text response
    """

    textParts: List[str] = []
    requestParams: Dict[str, Any] = {
        "model": model,
        "max_tokens": maxTokens,
        "temperature": temperature,
        "messages": [msg.model_dump() for msg in messages],
    }

    if enableGrounding and any(
        model.startswith(member.value) for member in ClaudeModelGrounding
    ):
        webSearchTool = {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5,
        }

        if countryCode:
            webSearchTool["user_location"] = {
                "type": "approximate",
                "country": countryCode,
            }

        requestParams["tools"] = [webSearchTool]

    response = client.messages.create(**requestParams)

    for block in response.content:
        if isinstance(block, TextBlock):
            textParts.append(block.text)

    return "".join(textParts)
