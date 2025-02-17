from .llp_basic_details import LlpDetails
from helpers.common import ProbeLlpComprehensiveDetails

class LlpComprehensiveDetails(LlpDetails):
    def __init__(
        self,
        cirp_status: str,
        classification: str,
        efiling_status: str,
        email: str,
        incorporation_date: str,
        last_annual_returns_filed_date: str,
        last_financial_reporting_date: str,
        legal_name: str,
        lei: dict,
        llpin: str,
        registered_address: dict,
        sum_of_charges: int,
        total_obligation_of_contribution: int,
        total_contribution_received: float,
        business_address: dict,
        pan: str,
        website: str,
    ) -> None:
        super().__init__(
            cirp_status,
            classification,
            efiling_status,
            email,
            incorporation_date,
            last_annual_returns_filed_date,
            last_financial_reporting_date,
            legal_name,
            lei,
            llpin,
            registered_address,
            sum_of_charges,
            total_obligation_of_contribution,
        )
        self.total_contribution_received = total_contribution_received
        self.business_address = business_address
        self.pan = pan
        self.website = website

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "total_contribution_received": self.total_contribution_received,
            "business_address": self.business_address,
            "pan": self.pan,
            "website": self.website,
        }
    
    @classmethod
    def from_probe42(cls,vs: ProbeLlpComprehensiveDetails):
        return cls(
            cirp_status=vs.cirp_status,
            classification=vs.classification,
            efiling_status=vs.efiling_status,
            email=vs.email,
            incorporation_date=vs.incorporation_date,
            last_annual_returns_filed_date=vs.last_annual_returns_filed_date,
            last_financial_reporting_date=vs.last_financial_reporting_date,
            legal_name=vs.legal_name,
            lei=vs.lei,
            llpin=vs.llpin,
            registered_address=vs.registered_address,
            sum_of_charges=vs.sum_of_charges,
            total_obligation_of_contribution=vs.total_obligation_of_contribution,
            total_contribution_received=vs.total_contribution_received,
            business_address=vs.business_address,
            pan=vs.pan,
            website=vs.website,
        )
