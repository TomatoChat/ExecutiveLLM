from typing import Any, Dict, List

from openai import OpenAI

from ...models import Message, OpenAiModelGrounding


def runPrompt(
    client: OpenAI,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Message],
    enableGrounding: bool = False,
) -> str:
    """
    Run a prompt through the OpenAI Responses API.

    Args:
        client: OpenAI Client instance
        model: Model identifier
        maxTokens: Maximum tokens to generate
        temperature: Sampling temperature
        messages: List of messages with role and content
        enableGrounding: Enable web search grounding if supported by model

    Returns:
        Generated text response
    """

    requestParams: Dict[str, Any] = {
        "model": model,
        "max_output_tokens": maxTokens,
        "temperature": temperature,
        "input": [
            {
                "role": msg.role,
                "content": [{"type": "input_text", "text": msg.content}],
            }
            for msg in messages
        ],
    }

    if enableGrounding and any(
        model.startswith(member.value) for member in OpenAiModelGrounding
    ):
        requestParams["tools"] = [{"type": "web_search"}]

    response = client.responses.create(**requestParams)
    outputText = [
        part.text
        for msg in response.output
        if msg.type == "message"
        for part in msg.content
        if part.type == "output_text"
    ]

    return "".join(outputText)
