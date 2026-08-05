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