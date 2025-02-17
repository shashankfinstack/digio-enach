from enum import Enum
from utils.secret import SecretUtils


def DEFAULT_DIGIO_HEADERS() -> dict:
     return {
            "Authorization": SecretUtils.get_secret_value(SecretUtils.SECRETS.DIGIO_AUTHENTICATION_TOKEN)
        }


class AuthMode(Enum):
    ESIGN = "esign"
    API = "api"
    PHYSICAL = "physical"


# In case of API mandate, sub auth mode type
class AuthSubMode(Enum):
    NET_BANKING = "NET_BANKING"
    DEBIT = "DEBIT"
    AADHAAR = "AADHAAR"
    OTP = "OTP"


class ManagementCategory(Enum):
    C001 = "B2B Corporate"
    B001 = "Bill Payment Credit card"
    D001 = "Destination Bank Mandate"
    E001 = "Education fees"
    I001 = "Insurance Premium"
    I002 = "Insurance other payment"
    L099 = "Legacy One Crore and Above"
    L002 = "Loan amount security"
    L001 = "Loan installment payment"
    M001 = "Mutual Fund Payment"
    U099 = "Others"
    F001 = "Subscription Fees"
    T002 = "TReDS"
    T001 = "Tax Payment"
    U001 = "Utility Bill Payment Electricity"
    U003 = "Utility Bill payment Gas Supply Cos"
    U005 = "Utility Bill payment mobile telephone broadband"
    U006 = "Utility Bill payment water"
    S001 = "Small Value Mandate"



class Frequency(Enum):
    Adhoc = "Adhoc"
    IntraDay = "IntraDay"
    Daily = "Daily"
    Weekly = "Weekly"
    Monthly = "Monthly"
    BiMonthly = "BiMonthly"
    Quarterly = "Quarterly"
    Semiannually = "Semiannually"
    Yearly = "Yearly"

class MandateType(Enum):
    create = "create"

class Type(Enum):
    CREATE = "CREATE"


# class StateOfBank(Enum):
#     partial = "partial"
#     signed = "signed"
#     transfer_failed = "transfer_failed"
#     transfer_success = "transfer_success"
#     reject_spo_bank = "reject_spo_bank"
#     accepted_spo_bank = "accepted_spo_bank"
#     awaiting_ack = "awaiting_ack"
#     nack_received = "nack_received"
#     ack_received = "ack_received"
#     awaiting_res = "awaiting_res"
#     register_failed = "register_failed"
#     register_success = "register_success"
#     revoked = "revoked"

class StateOfBank(Enum):
    partial = "partial"
    SIGNED = "SIGNED"
    TRANSFER_FAILED = "TRANSFER_FAILED"
    TRANSFER_SUCCESS = "TRANSFER_SUCCESS"
    REJECT_SPO_BANK = "REJECT_SPO_BANK"
    ACCEPTED_SPO_BANK = "ACCEPTED_SPO_BANK"
    AWAITING_ACK = "AWAITING_ACK"
    NACK_RECEIVED = "NACK_RECEIVED"
    ACK_RECEIVED = "ACK_RECEIVED"
    AWAITING_RES = "AWAITING_RES"
    REGISTER_FAILED = "REGISTER_FAILED"
    REGISTER_SUCCESS = "REGISTER_SUCCESS"
    REVOKED = "REVOKED"

    
class CurrentStateOfMandate(Enum):
    PARTIAL = "partial"
    SIGNED = "signed"
    COMPLETE = "complete"
    EXPIRED = "expired"
    AUTH_SUCCESS = "auth_success"
    AUTH_FAILED = "auth_failed"
    CANCELLED = "cancelled"
    REVOKED = "revoked"

class StatusWithBank(Enum):
    CREATED = "CREATED"
    READY = "READY"
    DOWNLOADED = "DOWNLOADED"
    FAILED = "FAILED"
    AUTH_SUCCESS = "AUTH_SUCCESS"
    SUCCESSFUL = "SUCCESSFUL"
    PARTIAL = "PARTIAL"
    SIGN_PENDING = "SIGN_PENDING"
    SIGNED = "SIGNED"
    TRANSFER_FAILED = "TRANSFER_FAILED"
    TRANSFER_SUCCESS = "TRANSFER_SUCCESS"
    REJECT_SPO_BANK = "REJECT_SPO_BANK"
    ACCEPTED_SPO_BANK = "ACCEPTED_SPO_BANK"
    AWAITING_ACK = "AWAITING_ACK"
    NACK_RECEIVED = "NACK_RECEIVED"
    ACK_RECEIVED = "ACK_RECEIVED"
    AWAITING_RES = "AWAITING_RES"
    REGISTER_FAILED = "REGISTER_FAILED"
    REGISTER_SUCCESS = "REGISTER_SUCCESS"
    REVOKED = "REVOKED"


class TypeOfIdentifier(Enum):
    EMAIL = "EMAIL"
    MOBILE = "MOBILE"
    UNKNOWN = "UNKNOWN"

class AccountType(Enum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"
    OTHER = "OTHER"

class AmendmentReason(Enum):
    A001 = "On Customer Request"
    M036 = "Represent with CBS account number"



    

