from utils.misc import MiscUtils
from utils.secret import SecretUtils


class UlipHelper:
    @classmethod
    def get_default_ulip_headers(cls):
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SecretUtils.get_secret_value(SecretUtils.SECRETS.ULIP_AUTH_TOKEN)}",
        }
        return default_headers


DEFAULT_ULIP_LOGIN_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
