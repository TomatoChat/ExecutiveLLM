from enum import Enum

from dotenv import load_dotenv

from ..helpers.openai import getModelIds

load_dotenv()


class OpenAiModel(Enum):
    """
    Enum of available OpenAI models.
    This is dynamically populated from the OpenAI API at import time.
    """

    def __init__(self, modelId: str):
        self._value_ = modelId

    @classmethod
    def _missing_(cls, value):
        """Allow creation of new members dynamically."""
        return None


# Dynamically populate the enum with available models
def _populateOpenAiModel():
    """Populate OpenAiModel enum with available models from OpenAI API."""
    modelIds = getModelIds()

    for modelId in modelIds:
        enumName = modelId.upper().replace("-", "_").replace(".", "_")

        if not hasattr(OpenAiModel, enumName):
            extendEnum(OpenAiModel, enumName, modelId)


def extendEnum(enumClass, name, value):
    """Extend an enum with a new member."""
    newMember = object.__new__(enumClass)
    newMember._name_ = name
    newMember._value_ = value

    setattr(enumClass, name, newMember)
    enumClass._member_names_.append(name)
    enumClass._member_map_[name] = newMember
    enumClass._value2member_map_[value] = newMember


_populateOpenAiModel()
