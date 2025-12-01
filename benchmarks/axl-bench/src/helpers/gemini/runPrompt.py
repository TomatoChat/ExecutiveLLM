from typing import Dict, List

import google.generativeai as genai


def runPrompt(
    client: genai.GenerativeModel,
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Dict[str, str]],
) -> str:
    """
    Run a prompt through the Gemini API.
    """
    geminiMessages = []

    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        geminiMessages.append({"role": role, "parts": [msg["content"]]})

    fullModelName = model if model.startswith("models/") else f"models/{model}"
    modelInstance = genai.GenerativeModel(fullModelName)
    response = modelInstance.generate_content(
        contents=geminiMessages,
        generation_config=genai.GenerationConfig(
            max_output_tokens=maxTokens,
            temperature=temperature,
        ),
    )

    return response.text
