from typing import List

from openai import OpenAI

from ...models import Message
from ...models.OpenAiModelGrounding import OpenAiModelGrounding


def runPrompt(
    client: OpenAI,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Message],
    enableGrounding: bool = False,
) -> str:
    """
    Run a prompt through the OpenAI API.

    Args:
        client: OpenAI client instance
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
        "messages": [msg.to_dict() for msg in messages],
    }

    # Enable web search if supported by the model
    if enableGrounding and any(
        model.startswith(member.value) for member in OpenAiModelGrounding
    ):
        requestParams["tools"] = [{"type": "web_search"}]
        response = client.chat.completions.create(**requestParams)
    else:
        response = client.chat.completions.create(**requestParams)

    return response.choices[0].message.content or ""
