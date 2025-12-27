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
    Run a prompt through the OpenAI Responses API.
    """

    requestParams = {
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
        requestParams["tools"] = [
            {
                "type": "web_search",
                "web_search": {},
            }
        ]

    response = client.responses.create(**requestParams)

    outputText = [
        part.text
        for msg in response.output
        if msg.type == "message"
        for part in msg.content
        if part.type == "output_text"
    ]

    return "".join(outputText)
