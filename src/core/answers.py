# ======================================================================== #
# ANSWERTYPE CONFIG                                                        #
# ======================================================================== #

from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin

class AnswerType(str, Enum):
    SHORT_ANSWER = "ShortAnswer"
    LONG_ANSWER = "LongAnswer"
    LIKERT_SCALE = "LikertScale"
    YES_NO = "YesNo"
    MULTIPLE_CHOICE = "MultipleChoice"
    MULTIPLE_CHOICE_CUSTOM = "MultipleChoiceCustom"
    FILE_INPUT = "FileInput"
    MULTIPLE_SHORT_ANSWER = "MultipleShortAnswer"


class MULTIPLE_CHOICE:

    def __init__(self, literal_type: Any):
        self.ui_component = AnswerType.MULTIPLE_CHOICE
        self.options: Tuple[str, ...] = self._extract_choices(literal_type)

    def _extract_choices(self, type_hint: Any) -> Tuple[str, ...]:
        extracted = []
        for arg in get_args(type_hint):
            if get_origin(arg) is Literal:
                extracted.extend(get_args(arg))
            elif isinstance(arg, str):
                extracted.append(arg)
        return tuple(extracted)

    def to_dict(self) -> Dict[str, Any]:
        return {"ui_component": self.ui_component.value, "options": list(self.options)}

class MULTIPLE_CHOICE_CUSTOM:
    """Metadata generator for selectbox with a fallback text input for custom values."""

    def __init__(self, literal_type: Any):
        self.ui_component = AnswerType.MULTIPLE_CHOICE_CUSTOM
        self.options: Tuple[str, ...] = self._extract_choices(literal_type)

    def _extract_choices(self, type_hint: Any) -> Tuple[str, ...]:
        extracted = []
        for arg in get_args(type_hint):
            if get_origin(arg) is Literal:
                extracted.extend(get_args(arg))
            elif isinstance(arg, str):
                extracted.append(arg)
        return tuple(extracted)

    def to_dict(self) -> Dict[str, Any]:
        return {"ui_component": self.ui_component.value, "options": list(self.options)}

# ======================================================================== #
# AVAILABLE ANSWERS                                                        #
# ======================================================================== #

from typing import Literal, Optional

GENDER = Optional[Literal[
    "Male", "Female"
]]
SEXUALITY = Optional[Literal[
    "Heterosexual", "Homosexual", "Bisexual", "Asexual", "Other"
]]
BODY_SHAPE = Optional[Literal[
    "lorem"
]]
BODY_TYPE = Optional[Literal[
    "Ectomorph", "Mesomorph", "Endomorph"
]]

FACE_SHAPE = Optional[Literal[
    ""
]]

HAIR_TYPE = Optional[Literal[
    "(1a) Straight and Fine",
    "(1b) Less Straight",
    "(1c) Bone Straight"
    
    "(2a) Soft Waves",
    "(2b) Wavy",
    "(2c) Deep Waves",

    "(3a) Soft Curls",
    "(3b) Curly",
    "(3c) Ultra Curly",

    "(4a) Coiled",
    "(4b) Zig-zag",
    "(4c) Tighly Coiled"
]]