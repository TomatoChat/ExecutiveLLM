import os
from typing import List

from dotenv import load_dotenv
from google import genai

load_dotenv()


def getModelIds() -> List[str]:
    """
    Retrieve just the model IDs from the Gemini API.

    Returns:
        List of model ID strings
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    models = client.models.list()

    return [model.name for model in models if model.name is not None]
