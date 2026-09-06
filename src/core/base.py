from pydantic import BaseModel, Field
from .answers import *

descfor_hexcolor = "preferred in Hex Color Code"

# ======================================================================== #
# IDENTITY SECTION                                                         #
# ======================================================================== #

# Name ------------------------------------------------------------------- #

class NameSection(BaseModel):
    full_name: str = Field(
        default="",
        description="Full Name",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER},
    )
    nicknames: list[str] = Field(  # Corrected type hint to list[str]
        default_factory=list,  # Use list factory instead of string
        description="Nickname(s)",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER},
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
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER},
    )
    job_satisfaction: int = Field(
        default=3,
        description="Job Satisfaction",
        json_schema_extra={
            "ui_component": AnswerType.LIKERT_SCALE,
            "min": 1,
            "max": 5,
        },
    )
    in_depth: str = Field(
        default="",
        description="In Depth Details",
        json_schema_extra={"ui_component": AnswerType.LONG_ANSWER},
    )


# Parent Class ----------------------------------------------------------- #

class CharacterGeneral(BaseModel):
    Names: NameSection = Field(default_factory=NameSection)
    Gender_and_Sex: GenderSexSection = Field(default_factory=GenderSexSection)
    Occupational: OccupationalSection = Field(default_factory=OccupationalSection)

# ======================================================================== #
# CHARACTERISTIC SECTION                                                       #
# ======================================================================== #

# General Body ----------------------------------------------------------- #

class AgeSubsec(BaseModel):
    value: float = Field(
        default=0,
        description="Age (In year old)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    BUTlooklike: float = Field(
        default=0,
        description="But look like age (In year old)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )

class GeneralBodySection(BaseModel):
    speciesORrace: str = Field(
        default="",
        description="Species or Race",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    Age: AgeSubsec = Field(
        default_factory=AgeSubsec
    )
    height: float = Field(
        default=0,
        description="Height (in meter)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    weight: float = Field(
        default=0,
        description="Weight (in kilogram)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )

# Appearance ------------------------------------------------------------- #

BodyShapeChoice = MULTIPLE_CHOICE(BODY_SHAPE).to_dict()
BodyTypeChoice = MULTIPLE_CHOICE(BODY_TYPE).to_dict()

class ApperanceSection(BaseModel):
    skin_tone: str = Field(
        default="",
        description=f"Skin Tone. {descfor_hexcolor}",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    skin_type: str = Field(
        default="",
        description="Skin Type. (WIP)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    body_shape: str = Field(
        default="",
        description="Body Shape. (WIP)",
        json_schema_extra=BodyShapeChoice
    )
    body_type: str = Field(
        default="",
        description="Body Type. (WIP)",
        json_schema_extra=BodyTypeChoice
    )
    posture: str = Field(
        default="",
        description="Posture. (WIP)",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    scarORmark: list[str] = Field(
        default_factory=list,
        description="Scars or Marks. (WIP)",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )

# Voice Class ------------------------------------------------------------ #

class VoiceSection(BaseModel):
    accent: str = Field(
        default="",
        description="Accent",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    pitch: str = Field(
        default="",
        description="Pitch",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )


# Head ------------------------------------------------------------------- #

FaceShapeChoice = MULTIPLE_CHOICE_CUSTOM(FACE_SHAPE).to_dict()
HairTypeChoice = MULTIPLE_CHOICE(HAIR_TYPE).to_dict()

class HeadSection(BaseModel):
    face_shape: str = Field(
        default="",
        description="Face Shape",
        json_schema_extra=FaceShapeChoice
    )
    hair_type: str = Field(
        default="",
        description="Hair Type",
        json_schema_extra=HairTypeChoice
    )
    hair_color: str = Field(
        default="",
        description=f"Hair Color. {descfor_hexcolor}",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    hair_style: str = Field(
        default="",
        description=f"Hair Style",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    eye_shape: str = Field(
        default="",
        description=f"Eye Shape",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )
    eye_color: str = Field(
        default="",
        description=f"Eye Color. {descfor_hexcolor}",
        json_schema_extra={"ui_component": AnswerType.SHORT_ANSWER}
    )


# Health ----------------------------------------------------------------- #

class HealthSection(BaseModel):
    health: int = Field(
        default=3,
        description="Healthiness. How strong the immnunity, or how often they get sick",
        json_schema_extra={"ui_component": AnswerType.LIKERT_SCALE}
    )
    hygiene: int = Field(
        default=3,
        description="Hygiene",
        json_schema_extra={"ui_component": AnswerType.LIKERT_SCALE}
    )
    allergies: list[str] = Field(
        default_factory=list,
        description="Allergies",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )
    weaknesses: list[str] = Field(
        default_factory=list,
        description="Weaknesses",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )

# Clothing --------------------------------------------------------------- #

class ClothingSection(BaseModel):
    outfit_usual: list[str] = Field(
        default_factory=list,
        description="Usual Fashion",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )
    outfit_favorite: list[str] = Field(
        default_factory=list,
        description="Favorite outfit",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )
    accessories: list[str] = Field(
        default_factory=list,
        description="Accessories",
        json_schema_extra={"ui_component": AnswerType.MULTIPLE_SHORT_ANSWER}
    )
    beauty: int = Field(
        default=3,
        description="Beauy. How much beauty they have",
        json_schema_extra={"ui_component": AnswerType.LIKERT_SCALE}
    )
    style: int = Field(
        default=3,
        description="Style",
        json_schema_extra={"ui_component": AnswerType.LIKERT_SCALE}
    )


# Parent Class ----------------------------------------------------------- #

class CharacterAppearance(BaseModel):
    refsheet_link: list[str] = Field(
        default_factory=list,
        description="Relative path to images",
        json_schema_extra={"ui_component": AnswerType.FILE_INPUT},
    )
    GeneralBody: GeneralBodySection = Field(
        default_factory=GeneralBodySection
    )
    Appearance: ApperanceSection = Field(
        default_factory=ApperanceSection
    )
    Voice: VoiceSection = Field(
        default_factory=VoiceSection
    )
    Head: HeadSection = Field(
        default_factory=HeadSection
    )
    Health: HealthSection = Field(
        default_factory=HealthSection
    )
    Clothings: ClothingSection = Field(
        default_factory=ClothingSection
    )


# ======================================================================== #
# MASTER CLASS                                                             #
# ======================================================================== #

class CharacterData(BaseModel):
    ID: str = Field(default="")
    VERSION: str = Field(default="")
    CHARACTER_GENERAL: CharacterGeneral = Field(
        default_factory=CharacterGeneral
    )
    CHARACTER_APPEARANCE: CharacterAppearance = Field(
        default_factory=CharacterAppearance
    )


