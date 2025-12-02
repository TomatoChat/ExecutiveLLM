from enum import Enum


class GeminiModelGrounding(Enum):
    """
    Enum of Gemini models that support Google Search grounding.
    Source: https://ai.google.dev/gemini-api/docs/google-search
    """

    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
