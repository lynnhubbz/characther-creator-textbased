from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
from pydantic import BaseModel, Field
from .answers import *


# ======================================================================== #
# ANSWERTYPE CONFIG                                                        #
# ======================================================================== #

class AnswerType(str, Enum):
    SHORT_ANSWER = "ShortAnswer"
    LONG_ANSWER = "LongAnswer"
    LIKERT_SCALE = "LikertScale"
    YES_NO = "YesNo"
    MULTIPLE_CHOICE = "MultipleChoice"


class MULTIPLE_CHOICE:

    def __init__(self, literal_type: Any):
        self.widget = AnswerType.MULTIPLE_CHOICE
        self.choices: Tuple[str, ...] = self._extract_choices(literal_type)

    def _extract_choices(self, type_hint: Any) -> Tuple[str, ...]:
        extracted = []
        for arg in get_args(type_hint):
            if get_origin(arg) is Literal:
                extracted.extend(get_args(arg))
            elif isinstance(arg, str):
                extracted.append(arg)
        return tuple(extracted)

    def to_dict(self) -> Dict[str, Any]:
        return {"widget": self.widget.value, "choices": list(self.choices)}

# ======================================================================== #
# IDENTITY SECTION                                                         #
# ======================================================================== #

# Name ------------------------------------------------------------------- #

class NameSection(BaseModel):
    full_name: str = Field(
        default="",
        description="Full Name",
        json_schema_extra={"widget": AnswerType.SHORT_ANSWER},
    )
    nicknames: list[str] = Field(  # Corrected type hint to list[str]
        default_factory=list,  # Use list factory instead of string
        description="Nickname(s)",
        json_schema_extra={"widget": AnswerType.SHORT_ANSWER},
    )

# Gender And Sex --------------------------------------------------------- #

GenderChoice = MULTIPLE_CHOICE(GENDER).to_dict()
SexualityChoice = MULTIPLE_CHOICE(SEXUALITY).to_dict()

class GenderSexSection(BaseModel):
    gender: GENDER = Field(
        default=None,
        description="Gender",
        json_schema_extra=GenderChoice,
    )
    sexuality: Optional[SEXUALITY] = Field(
        default=None,
        description="Sexuality",
        json_schema_extra=SexualityChoice,
    )

# Occupation ------------------------------------------------------------- #

class OccupationalSection(BaseModel):
    occupation: str = Field(
        default="",
        description="Occupation",
        json_schema_extra={"widget": AnswerType.SHORT_ANSWER},
    )
    job_satisfaction: int = Field(
        default=3,
        description="Job Satisfaction",
        json_schema_extra={
            "widget": AnswerType.LIKERT_SCALE,
            "min": 1,
            "max": 5,
        },
    )
    in_depth: str = Field(
        default="",
        description="In Depth Details",
        json_schema_extra={"widget": AnswerType.LONG_ANSWER},
    )


# Parent Class ----------------------------------------------------------- #

class CharacterIdentity(BaseModel):
    names: NameSection = Field(default_factory=NameSection)
    gender_and_sex: GenderSexSection = Field(default_factory=GenderSexSection)
    occupational: OccupationalSection = Field(default_factory=OccupationalSection)

# ======================================================================== #
# MASTER CLASS                                                             #
# ======================================================================== #

class CharacterData(BaseModel):
    id: str = Field(default="")
    character_identity: CharacterIdentity = Field(
        default_factory=CharacterIdentity
    )


