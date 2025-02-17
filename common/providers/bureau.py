from enum import Enum
from typing import Callable, TypedDict, Optional, Any, List
from utils.misc import MiscUtils
from utils.secret import SecretUtils
import base64

class BureauDocumentType(Enum):
    aadhaar = "Aadhaar"

def DEFAULT_BUREAU_HEADERS() -> dict:
    credential_id = SecretUtils.get_secret_value(SecretUtils.SECRETS.BUREAU_CREDENTIAL_ID)
    credential_secret = SecretUtils.get_secret_value(SecretUtils.SECRETS.BUREAU_CREDENTIAL_SECRET)
    # Combine credential ID and secret with a colon separator
    credentials = f"{credential_id}:{credential_secret}"
    # Encode the combined credentials using base64
    base64_encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return {
                "Authorization": f"Basic {base64_encoded_credentials}"
        }