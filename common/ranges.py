
from typing import Any, Optional, TypedDict
from utils.misc import MiscUtils


class DateTimeRange:
    def __init__(
        self,
        start: Optional[str],
        end: Optional[str],
        DATE_FORMAT: Optional[str] = None
    ) -> None:
        self.start = MiscUtils.date_parser(start,DATE_FORMAT)
        self.end = MiscUtils.date_parser(end,DATE_FORMAT)

    def to_dict(self, for_db: bool = False):
        return {
            "start": MiscUtils.date_iso_string(self.start),
            "end": MiscUtils.date_iso_string(self.end)
        }
    
class GenericRange(TypedDict):
    min: Any
    max: Any

