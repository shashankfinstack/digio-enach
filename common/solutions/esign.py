from datetime import datetime
from typing import Optional, List
import json
from enum import Enum
from utils.misc import MiscUtils


class EsignPositions(Enum):
    TOP_LEFT = "TOP-LEFT"
    TOP_CENTER = "TOP-CENTER"
    TOP_RIGHT = "TOP-RIGHT"
    MIDDLE_LEFT = "MIDDLE-LEFT"
    MIDDLE_CENTER = "MIDDLE-CENTER"
    MIDDLE_RIGHT = "MIDDLE-RIGHT"
    BOTTOM_LEFT = "BOTTOM-LEFT"
    BOTTOM_CENTER = "BOTTOM-CENTER"
    BOTTOM_RIGHT = "BOTTOM-RIGHT"
    CUSTOMIZE = "CUSTOMIZE"


class EsignProviders(Enum):
    NSDL = "nsdl"
    EMUDHRA = "emudhra"


class EsignSignature:
    def __init__(
        self,
        page_nos: List[int],
        x_coordinates: List[float],
        y_coordinates: List[float],
        height: float = None,
        width: float = None,
        positions: List[EsignPositions] = None
    ) -> None:
        self.page_nos = page_nos
        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.height = 28 if height is None else height
        self.width = 170 if width is None else width
        self.positions = [
            EsignPositions.CUSTOMIZE] if positions is None else positions

    def to_dict(self, for_db: bool = False):
        return {
            "page_nos": self.page_nos,
            "x_coordinates": self.x_coordinates,
            "y_coordinates": self.y_coordinates,
            "height": self.height,
            "width": self.width,
            "positions": [position.value for position in self.positions],
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            page_nos=MiscUtils.get_value_from_dict(d, "page_nos"),
            x_coordinates=MiscUtils.get_value_from_dict(
                d, "x_coordinates"),
            y_coordinates=MiscUtils.get_value_from_dict(
                d, "y_coordinates"),
            height=MiscUtils.get_value_from_dict(d, "height"),
            width=MiscUtils.get_value_from_dict(d, "width"),
            positions=[MiscUtils.value_to_enum(
                position, EsignPositions) for position in MiscUtils.get_value_from_dict(d, "positions")],
        )


class EsignOptions:
    def __init__(
        self,
        name: str,
        callback_url: str,
        provider: EsignProviders = None,
        redirect_url: str = None,
        multi_pages: bool = None,
        page_number: int = None,
        signatures: List[EsignSignature] = None
    ) -> None:
        self.name = name
        self.callback_url = callback_url
        self.provider = EsignProviders.NSDL if provider is None else provider
        self.redirect_url = redirect_url
        self.multi_pages = multi_pages
        self.page_number = page_number
        self.signatures = [] if signatures is None else signatures

    def to_dict(self, for_db: bool = False):
        return {
            "name": self.name,
            "callback_url": self.callback_url,
            "provider": self.provider.value,
            "redirect_url": self.redirect_url,
            "multi_pages": self.multi_pages,
            "page_number": self.page_number,
            "signatures": [signature.to_dict(for_db) for signature in self.signatures],
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        multi_pages = MiscUtils.get_value_from_dict(
            d, "multi_pages", none_accepted=True)
        page_number = MiscUtils.get_value_from_dict(
            d, "page_number", none_accepted=True)
        return cls(
            name=MiscUtils.get_value_from_dict(d, "name"),
            callback_url=MiscUtils.get_value_from_dict(
                d, "callback_url"),
            provider=MiscUtils.value_to_enum(MiscUtils.get_value_from_dict(
                d, "provider", none_accepted=True), EsignProviders),
            redirect_url=MiscUtils.get_value_from_dict(
                d, "redirect_url", none_accepted=True),
            multi_pages=bool(
                multi_pages) if multi_pages is not None else multi_pages,
            page_number=int(
                page_number) if page_number is not None else page_number,
            signatures=[EsignSignature.from_dict(signature) for signature in MiscUtils.get_value_from_dict(
                d, "signatures", none_accepted=True, default=[])]
        )


class EsignCall:
    def __init__(
        self,
        _id: str,
        request: dict,
        document_url: str,
        esigning_url: str,
        signed_document_url: Optional[str] = None,
        callback: Optional[str] = None,
        _version: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self._id = _id
        self.request = request
        self.document_url = document_url
        self.esigning_url = esigning_url
        self.signed_document_url = signed_document_url
        self.callback = callback
        self._version = 1 if _version is None else _version
        self.created_at = datetime.utcnow() if created_at is None else created_at
        self.updated_at = datetime.utcnow() if updated_at is None else updated_at

    def to_dict(self, for_db: bool = False) -> dict:
        return {
            "_id": self._id,
            "request": self.request,
            "document_url": self.document_url,
            "esigning_url": self.esigning_url,
            "signed_document_url": self.signed_document_url,
            "callback": self.callback,
            "_version": self._version,
            "created_at": self.created_at.isoformat() if for_db is False and isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if for_db is False and isinstance(self.updated_at, datetime) else self.updated_at
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            _id=d.get("_id"),
            request=d.get("request"),
            document_url=d.get("document_url"),
            esigning_url=d.get("esigning_url"),
            signed_document_url=d.get("signed_document_url"),
            callback=d.get("callback"),
            _version=d.get("_version"),
            created_at=MiscUtils.typecast_string(MiscUtils.get_value_from_dict(
                d, "created_at", none_accepted=True), datetime, datetime.fromisoformat),
            updated_at=MiscUtils.typecast_string(MiscUtils.get_value_from_dict(
                d, "updated_at", none_accepted=True), datetime, datetime.fromisoformat),
        )

    def __str__(self) -> str:
        return f'''
EsignCall(
    {json.dumps(self.to_dict(),indent=2)}
)
'''
