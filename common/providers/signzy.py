from enum import Enum
from utils.misc import MiscUtils
from utils.secret import SecretUtils
from helpers.common import Address


class SignzyAccountType(Enum):
    SAVING = "SAVING"
    CURRENT = "CURRENT"
    CREDIT_CARD = "CREDIT_CARD"


def DEFAULT_SIGNZY_OKYC_HEADERS() -> dict:
    return {
                "Content-Type": "application/json",
                "Authorization": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_OKYC_AUTHENTICATION_ID
                )
            }

def DEFAULT_SIGNZY_ESIGN_HEADERS() -> dict:
    return {
                "Content-Type": "application/json",
                "Authorization": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_ESIGN_AUTHENTICATION_ID
                )
            }

def DEFAULT_SIGNZY_HEADERS() -> dict:
    return {
                "Content-Type": "application/json",
                "Authorization": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_AUTHENTICATION_ID
                )
            }


def parse_split_address(split_address: dict) -> Address:
    cities = MiscUtils.get_value_from_dict(split_address, "city", none_accepted=True)
    countries = MiscUtils.get_value_from_dict(
        split_address, "country", none_accepted=True
    )
    states = MiscUtils.get_value_from_dict(split_address, "state", none_accepted=True)
    return Address(
        pincode=MiscUtils.check_unknown_empty_value(
            MiscUtils.get_value_from_dict(split_address, "pincode")
        ),
        address_line1=MiscUtils.check_unknown_empty_value(
            MiscUtils.get_value_from_dict(split_address, "addressLine")
        ),
        city=cities[0] if isinstance(cities, list) and len(cities) > 0 else None,
        state=(
            states[0][0]
            if isinstance(states, list)
            and states
            and len(states) > 0
            and states[0]
            and len(states[0]) > 0
            else None
        ),
        country=(
            countries[2]
            if isinstance(countries, list) and len(countries) >= 3
            else None
        ),
    )
