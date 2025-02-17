from enum import Enum
from typing import Optional, List
from utils.misc import MiscUtils
from utils.secret import SecretUtils


def DEFAULT_FINBOX_HEADERS() -> dict:
     return {
            "x-api-key": SecretUtils.get_secret_value(SecretUtils.SECRETS.FINBOX_API_KEY)
        }

class FinboxStatementProcessingStatus(Enum):
    COMPLETED = "completed"
    PROCESSING = "processing"
    FAILED = "failed"


class FinboxBankAccountDetails:
    def __init__(
        self,
        account_number: Optional[str],
        name: Optional[str],
        address: Optional[str],
        ifsc: Optional[str],
        account_category: Optional[str],
        *args,
        **kwargs
    ) -> None:
        self.account_number = account_number
        self.name = name
        self.address = address
        self.ifsc = ifsc
        self.account_category = account_category

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "address": self.address,
            "ifsc": self.ifsc,
            "account_category": self.account_category,
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            account_number=MiscUtils.get_value_from_dict(
                d, "account_number", none_accepted=True
            ),
            name=MiscUtils.get_value_from_dict(d, "name", none_accepted=True),
            address=MiscUtils.get_value_from_dict(d, "address", none_accepted=True),
            ifsc=MiscUtils.get_value_from_dict(d, "ifsc", none_accepted=True),
            account_category=MiscUtils.get_value_from_dict(
                d, "account_category", none_accepted=True
            ),
        )

class FraudType:
    def __init__(
        self,
        account_id: Optional[str] = None,
        fraud_category: Optional[str] = None,
        fraud_type: Optional[str] = None,
        statement_id: Optional[str] = None,
        transaction_hash: Optional[str] = None,
        * args,
        **kwargs
    ) -> None:
        self.account_id = account_id
        self.fraud_category = fraud_category
        self.fraud_type = fraud_type
        self.statement_id = statement_id
        self.transaction_hash = transaction_hash

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "fraud_category": self.fraud_category,
            "fraud_type": self.fraud_type,
            "statement_id": self.statement_id,
            "transaction_hash": self.transaction_hash,
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            account_id=MiscUtils.get_value_from_dict(d, "account_id", none_accepted=True),
            fraud_category=MiscUtils.get_value_from_dict(d, "fraud_category", none_accepted=True),
            fraud_type=MiscUtils.get_value_from_dict(d, "fraud_type", none_accepted=True),
            statement_id=MiscUtils.get_value_from_dict(d, "statement_id", none_accepted=True),
            transaction_hash=MiscUtils.get_value_from_dict(d, "transaction_hash", none_accepted=True)
        )

class Fraud:
    def __init__(
        self,
        fraud_type: Optional[List[FraudType]] = None,
        fraudulent_statements: Optional[List[str]] = None,
        * args,
        **kwargs
    ) -> None:
        self.fraud_type = fraud_type
        self.fraudulent_statements = fraudulent_statements

    def to_dict(self):
        return {
            "fraud_type": [item.to_dict() for item in self.fraud_type],
            "fraudulent_statements": self.fraudulent_statements,
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            fraud_type=[item.from_dict() for item in MiscUtils.get_value_from_dict(d, "fraud_type", none_accepted=True)],
            fraudulent_statements=MiscUtils.get_value_from_dict(d, "fraudulent_statements", none_accepted=True),
        )

