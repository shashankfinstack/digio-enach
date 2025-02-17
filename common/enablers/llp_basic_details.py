from datetime import date
from helpers.common import Address


class LlpDetails:
    def __init__(
        self,
        cirp_status: str,
        classification: str,
        efiling_status: str,
        email: str,
        incorporation_date: date,
        last_annual_returns_filed_date: date,
        last_financial_reporting_date: date,
        legal_name: str,
        lei: dict,
        llpin: str,
        registered_address: Address,
        sum_of_charges: int,
        total_obligation_of_contribution: int
    ) -> None:
        self.cirp_status = cirp_status
        self.classification = classification
        self.efiling_status = efiling_status
        self.email = email
        self.incorporation_date = incorporation_date
        self.last_annual_returns_filed_date = last_annual_returns_filed_date
        self.last_financial_reporting_date = last_financial_reporting_date
        self.legal_name = legal_name
        self.lei = lei
        self.llpin = llpin
        self.registered_address = registered_address
        self.sum_of_charges = sum_of_charges
        self.total_obligation_of_contribution = total_obligation_of_contribution

    def to_dict(self):
        return {
            "cirp_status": self.cirp_status,
            "classification": self.classification,
            "efiling_status": self.efiling_status,
            "email": self.email,
            "incorporation_date": self.incorporation_date.isoformat() if isinstance(self.incorporation_date, date) else self.incorporation_date,
            "last_annual_returns_filed_date": self.last_annual_returns_filed_date.isoformat() if isinstance(self.last_annual_returns_filed_date, date) else self.last_annual_returns_filed_date,
            "last_financial_reporting_date": self.last_financial_reporting_date.isoformat() if isinstance(self.last_financial_reporting_date, date) else self.last_financial_reporting_date,
            "legal_name": self.legal_name,
            "lei": self.lei,
            "llpin": self.llpin,
            "registered_address": self.registered_address.to_dict(),
            "sum_of_charges": self.sum_of_charges,
            "total_obligation_of_contribution": self.total_obligation_of_contribution,
        }
