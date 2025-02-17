from enum import Enum
from typing import Optional
from utils.misc import MiscUtils

class PanType(Enum):
    INDIVIDUAL_PAN = "individualPan"
    BUSINESS_PAN = "businessPan"

class OcrKarzaDetail:
    def __init__(
        self,
        value: Optional[str] = None,
    ) -> None:
        self.value = value

    def to_dict(self, for_db: bool = False):
        return {
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            value = MiscUtils.get_value_from_dict(d, "value"),
        )