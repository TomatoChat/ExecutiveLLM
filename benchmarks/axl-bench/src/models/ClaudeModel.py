from enum import Enum

from dotenv import load_dotenv

from ..helpers.anthropic import getModelIds

load_dotenv()


class ClaudeModel(Enum):
    """
    Enum of available Claude models.
    This is dynamically populated from the Anthropic API at import time.
    """

    def __init__(self, modelId: str):
        self._value_ = modelId

    @classmethod
    def _missing_(cls, value):
        """Allow creation of new members dynamically."""
        return None


# Dynamically populate the enum with available models
def _populateClaudeModel():
    """Populate ClaudeModel enum with available models from Anthropic API."""
    modelIds = getModelIds()

    for modelId in modelIds:
        enumName = modelId.upper().replace("-", "_").replace(".", "_")

        if not hasattr(ClaudeModel, enumName):
            extendEnum(ClaudeModel, enumName, modelId)


def extendEnum(enumClass, name, value):
    """Extend an enum with a new member."""
    newMember = object.__new__(enumClass)
    newMember._name_ = name
    newMember._value_ = value

    setattr(enumClass, name, newMember)
    enumClass._member_names_.append(name)
    enumClass._member_map_[name] = newMember
    enumClass._value2member_map_[value] = newMember


_populateClaudeModel()
