from enum import Enum
from typing import Optional, List, Any
from utils.misc import MiscUtils
from utils.secret import SecretUtils

class BankAccountDetails:
    def __init__(
        self,
        account_holder_name: Optional[str] = None,
        account_category: Optional[str] = None,
        account_number: Optional[str] = None,
        bank_name: Optional[str] = None,
        bank_ifsc_code: Optional[str] = None,
        account_holder_address: Optional[str] = None,
        is_fraud: Optional[bool] = None,
        fraud_type: Optional[Any] = None,
    ) -> None:
        self.account_holder_name=account_holder_name
        self.account_category=account_category
        self.account_number=account_number
        self.bank_name=bank_name
        self.bank_ifsc_code=bank_ifsc_code
        self.account_holder_address=account_holder_address
        self.is_fraud=is_fraud
        self.fraud_type=fraud_type


    def to_dict(self):
        return {
            "account_holder_name":self.account_holder_name,
            "account_category":self.account_category,
            "account_number":self.account_number,
            "bank_name":self.bank_name,
            "bank_ifsc_code":self.bank_ifsc_code,
            "account_holder_address":self.account_holder_address,
            "is_fraud":self.is_fraud,
            "fraud_type":self.fraud_type,
        }

    @classmethod
    def from_finbox_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            account_holder_name=MiscUtils.get_nested_value_from_dict(d, ["identity","name"]),
            account_category=MiscUtils.get_nested_value_from_dict(d, ["identity", "account_category"]),
            account_number=MiscUtils.get_nested_value_from_dict(d, ["identity", "account_number"]),
            bank_name=MiscUtils.get_value_from_dict(d, "bank_name", none_accepted=True),
            bank_ifsc_code=MiscUtils.get_nested_value_from_dict(d, ["identity", "ifsc"]),
            account_holder_address=MiscUtils.get_nested_value_from_dict(d, ["identity", "address"]),
            is_fraud=MiscUtils.get_value_from_dict(d, "is_fraud", none_accepted=True),
            fraud_type=MiscUtils.get_value_from_dict(d, "fraud_type", none_accepted=True),
        )
    
    @classmethod
    def from_signzy_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            account_holder_name=MiscUtils.get_value_from_dict(d, "account_holder", none_accepted=True),
            account_category=MiscUtils.get_value_from_dict(d, "account_type", none_accepted=True), 
            account_number=MiscUtils.get_value_from_dict(d, "account_no", none_accepted=True), 
            bank_name=MiscUtils.get_value_from_dict(d, "bank_name", none_accepted=True),
            bank_ifsc_code=MiscUtils.get_value_from_dict(d,"ifsc_code", none_accepted=True),
            account_holder_address=MiscUtils.get_value_from_dict(d, "address", none_accepted=True),
        )