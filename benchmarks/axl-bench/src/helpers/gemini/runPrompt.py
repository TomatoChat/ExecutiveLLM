from typing import List

from google import genai
from google.genai import types

from ...models import Message
from ...models.GeminiModelGrounding import GeminiModelGrounding


def runPrompt(
    client: genai.Client,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Message],
    enableGrounding: bool = False,
) -> str:
    """
    Run a prompt through the Gemini API.

    Args:
        client: Gemini Client instance
        model: Model identifier
        maxTokens: Maximum tokens to generate
        temperature: Sampling temperature
        messages: List of message dictionaries
        enableGrounding: Enable Google Search grounding if supported by model

    Returns:
        Generated text response
    """
    if len(messages) == 1:
        contents = messages[0].content
    else:
        geminiMessages = []

        for msg in messages:
            role = "user" if msg.role == "user" else "model"
            geminiMessages.append(
                types.Content(role=role, parts=[types.Part(text=msg.content)])
            )
        contents = geminiMessages

    # Build config with grounding if enabled
    if enableGrounding and any(
        model.replace("models/", "").startswith(member.value)
        for member in GeminiModelGrounding
    ):
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=maxTokens,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
    else:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=maxTokens,
        )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    return response.text or ""
