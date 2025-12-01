import os
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def getModelIds() -> List[str]:
    """
    Retrieve just the model IDs from the Gemini API.

    Returns:
        List of model ID strings
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    models = genai.list_models()

    return [model.name for model in models]
