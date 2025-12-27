from enum import Enum


class OpenAiModel(Enum):
    """
    Enum of available OpenAI models.
    """

    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    O1 = "o1"
    O1_MINI = "o1-mini"
    O1_PREVIEW = "o1-preview"
    O3 = "o3"
    O4_MINI = "o4-mini"
    GPT_5 = "gpt-5"
