from enum import Enum
from typing import Callable, TypedDict, Optional, Any, List
from utils.misc import MiscUtils
from utils.secret import SecretUtils


class KarzaDocumentType(Enum):
    AADHAAR_BACK = "Aadhaar Back"
    AADHAAR_FRONT_TOP = "Aadhaar Front Top"
    AADHAAR_FRONT_BOTTOM = "Aadhaar Front Bottom"
    DRIVING_LICENSE_FRONT = "DL Front"
    VOTER_ID_FRONT = "Voterid Front"
    VOTER_ID_FRONT_NEW = "Voterid Front New"
    VOTER_ID_BACK = "Voterid Back"


class KarzaOcrResult(TypedDict):
    type: str
    details: dict


class KarzaOcrValueMapping(TypedDict):
    locations: List[list]
    fn: Callable
    value: Optional[Any]


def DEFAULT_KARZA_HEADERS() -> dict:
    return {
                "Content-Type": "application/json",
                "x-karza-key": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.KARZA_AUTHENTICATION_ID
                )
            }


KarzaInternalStatusCodeAuthentication = {
    "101" : "Valid Authentication",
    "102" : "Invalid ID number or combination of inputs",
    "103" : "No records found for the given ID or combination of inputs",
    "104" : "Max retries exceeded",
    "105" : "Missing Consent",
    "106" : "Multiple Records Exist",
    "107" : "Not Supported",
    "108" : "Internal Resource Unavailable",
    "109" : "Too many records Found",
}

KarzaInternalStatusCodeOCR = {
    "101" : "Successful OCR",
    "102" : "No KYC Document identified",
    "103" : "Image Format Not Supported OR Size Exceeds 6MB",
}

KarzaInternalStatusCodeLiveliness = {
    "102": "No face was detected",
    "103": "Image didn't comply with the validations",
    "104": "Image is of poor quality",
    "105":  "The pose of the face is extreme",
    "107": "Face size restriction is not met"
}

KarzaInternalStatusCodePhone = {
    "107": "OTP service is not available for services like MTNL and BSNL"
}