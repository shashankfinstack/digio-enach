from __future__ import annotations
from typing import Optional, List, Dict, Union, TypedDict
from datetime import date
from helpers.common import Address, Gender
from utils.misc import MiscUtils
from utils.secret import SecretUtils


DATE_FORMAT = "%Y-%m-%d"

def DEFAULT_PROBE42_HEADERS() -> dict:
    return {
        "x-api-key": SecretUtils.get_secret_value(SecretUtils.SECRETS.PROBE42_API_KEY),
        "x-api-version": SecretUtils.get_secret_value(
            SecretUtils.SECRETS.PROBE42_API_VERSION
        )
    }


class NameChange(TypedDict):
    name: str
    date: date


class ProbePersonAssociation:
    def __init__(
        self,
        event: Optional[str],
        designation_after_event: Optional[str],
        event_date: Optional[str],
        filing_date: Optional[str],
    ):
        self.event = event
        self.designation_after_event = designation_after_event
        self.event_date = MiscUtils.date_parser(event_date, DATE_FORMAT) if event_date is not None else None
        self.filing_date = MiscUtils.date_parser(filing_date, DATE_FORMAT) if filing_date is not None else None

    def to_dict(self):
        return {
            "event": self.event,
            "designation_after_event": self.designation_after_event,
            "event_date": self.event_date,
            "filing_date": self.filing_date,
        }


class ProbeCompanyDetails:
    def __init__(
        self,
        active_compliance: str,
        authorized_capital: int,
        cin: str,
        cirp_status: Optional[str],
        classification: str,
        efiling_status: str,
        email: str,
        incorporation_date: str,
        last_agm_date: str,
        last_filing_date: str,
        legal_name: str,
        lei: dict,
        next_cin: Optional[str],
        paid_up_capital: int,
        registered_address: dict,
        status: str,
        sum_of_charges: int,
    ):
        self.active_compliance = active_compliance
        self.authorized_capital = authorized_capital
        self.cin = cin
        self.cirp_status = cirp_status
        self.classification = classification
        self.efiling_status = efiling_status
        self.email = email
        self.incorporation_date = MiscUtils.date_parser(incorporation_date, DATE_FORMAT)
        self.last_agm_date = MiscUtils.date_parser(last_agm_date, DATE_FORMAT)
        self.last_filing_date = MiscUtils.date_parser(last_filing_date, DATE_FORMAT)
        self.legal_name = legal_name
        self.lei = lei
        self.next_cin = next_cin
        self.paid_up_capital = paid_up_capital
        self.registered_address = (
            Address(**registered_address)
            if isinstance(registered_address, dict)
            else registered_address
        )
        self.status = status
        self.sum_of_charges = sum_of_charges


class ProbePersonDetails:
    def __init__(
        self,
        pan: str,
        din: str,
        name: str,
        designation: str,
        din_status: str,
        gender: str,
        date_of_birth: str,
        age: int,
        date_of_appointment: str,
        date_of_appointment_for_current_designation: str,
        date_of_cessation: str,
        nationality: str,
        dsc_status: str,
        dsc_expiry_date: str,
        father_name: str,
        address: dict,
    ):
        self.pan = pan
        self.din = din
        self.name = name
        self.designation = designation
        self.din_status = din_status
        self.gender = gender
        if gender == "Male":
            self.gender = Gender.MALE
        elif gender == "Female":
            self.gender = Gender.FEMALE
        self.date_of_birth = MiscUtils.date_parser(date_of_birth, DATE_FORMAT)
        self.age = int(age)
        self.date_of_appointment = MiscUtils.date_parser(
            date_of_appointment, DATE_FORMAT
        )
        self.date_of_appointment_for_current_designation = MiscUtils.date_parser(
            date_of_appointment_for_current_designation, DATE_FORMAT
        )
        self.date_of_cessation = MiscUtils.date_parser(date_of_cessation, DATE_FORMAT)
        self.nationality = nationality
        self.dsc_status = dsc_status
        self.dsc_expiry_date = MiscUtils.date_parser(dsc_expiry_date, DATE_FORMAT)
        self.father_name = father_name
        self.address = Address(**address) if isinstance(address, dict) else address


class ProbeOpenCharge:
    def __init__(
        self, amount: float, date: str, holder_name: str, id: str, type: str
    ) -> None:
        self.amount = amount
        self.date = MiscUtils.date_parser(date, DATE_FORMAT)
        self.holder_name = holder_name
        self.id = id
        self.type = type


class ProbeLlpDetails:
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
    ) -> None:
        self.cirp_status = cirp_status
        self.classification = classification
        self.efiling_status = efiling_status
        self.email = email
        self.incorporation_date = MiscUtils.date_parser(incorporation_date, DATE_FORMAT)
        self.last_annual_returns_filed_date = MiscUtils.date_parser(
            last_annual_returns_filed_date, DATE_FORMAT
        )
        self.last_financial_reporting_date = MiscUtils.date_parser(
            last_financial_reporting_date, DATE_FORMAT
        )
        self.legal_name = legal_name
        self.lei = lei
        self.llpin = llpin
        self.registered_address = (
            Address(**registered_address)
            if isinstance(registered_address, dict)
            else registered_address
        )
        self.sum_of_charges = sum_of_charges
        self.total_obligation_of_contribution = total_obligation_of_contribution


class ProbeCompanyComprehensiveDetails(ProbeCompanyDetails):
    def __init__(
        self,
        active_compliance: str,
        authorized_capital: int,
        cin: str,
        cirp_status: Optional[str],
        classification: str,
        efiling_status: str,
        email: str,
        incorporation_date: str,
        last_agm_date: str,
        last_filing_date: str,
        legal_name: str,
        lei: dict,
        next_cin: Optional[str],
        paid_up_capital: int,
        registered_address: dict,
        status: str,
        sum_of_charges: int,
        business_address: dict,
        pan: str,
        website: str,
    ):
        super().__init__(
            active_compliance=active_compliance,
            authorized_capital=authorized_capital,
            cin=cin,
            cirp_status=cirp_status,
            classification=classification,
            efiling_status=efiling_status,
            email=email,
            incorporation_date=incorporation_date,
            last_agm_date=last_agm_date,
            last_filing_date=last_filing_date,
            legal_name=legal_name,
            lei=lei,
            next_cin=next_cin,
            paid_up_capital=paid_up_capital,
            registered_address=registered_address,
            status=status,
            sum_of_charges=sum_of_charges,
        )
        self.business_address = (
            Address(**business_address)
            if isinstance(business_address, dict)
            else business_address
        )
        self.pan = pan
        self.website = website


class ProbeLlpComprehensiveDetails(ProbeLlpDetails):
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
        self.business_address = (
            Address(**business_address)
            if isinstance(business_address, dict)
            else business_address
        )
        self.pan = pan
        self.website = website


class ProbePersonComprehensiveDetails(ProbePersonDetails):
    def __init__(
        self,
        pan: str,
        din: str,
        name: str,
        designation: str,
        din_status: str,
        gender: str,
        date_of_birth: str,
        age: int,
        date_of_appointment: str,
        date_of_appointment_for_current_designation: str,
        date_of_cessation: str,
        nationality: str,
        dsc_status: str,
        dsc_expiry_date: str,
        father_name: str,
        address: dict,
        association_history: Optional[List[dict]] = None,
    ):
        super().__init__(
            pan=pan,
            din=din,
            name=name,
            designation=designation,
            din_status=din_status,
            gender=gender,
            date_of_birth=date_of_birth,
            age=age,
            date_of_appointment=date_of_appointment,
            date_of_appointment_for_current_designation=date_of_appointment_for_current_designation,
            date_of_cessation=date_of_cessation,
            nationality=nationality,
            dsc_status=dsc_status,
            dsc_expiry_date=dsc_expiry_date,
            father_name=father_name,
            address=address,
        )
        association_history = [] if association_history is None else association_history
        self.association_history = []
        for association in association_history:
            self.association_history.append(
                ProbePersonAssociation(**association).to_dict()
            ) 


class ProbeDirectorNetwork:
    class CompanyNetwork:
        def __init__(
            self,
            cin: str,
            legal_name: str,
            company_status: str,
            incorporation_date: str,
            paid_up_capital: str,
            sum_of_charges: str,
            city: str,
            active_compliance: str,
            cirp_status: str,
            designation: str,
            date_of_appointment: str,
            date_of_appointment_for_current_designation: str,
            date_of_cessation: str,
        ) -> None:
            self.cin = cin
            self.legal_name = legal_name
            self.company_status = company_status
            self.incorporation_date = MiscUtils.date_parser(
                incorporation_date, DATE_FORMAT
            )
            self.paid_up_capital = paid_up_capital
            self.sum_of_charges = sum_of_charges
            self.city = city
            self.active_compliance = active_compliance
            self.cirp_status = cirp_status
            self.designation = designation
            self.date_of_appointment = MiscUtils.date_parser(
                date_of_appointment, DATE_FORMAT
            )
            self.date_of_appointment_for_current_designation = MiscUtils.date_parser(
                date_of_appointment_for_current_designation, DATE_FORMAT
            )
            self.date_of_cessation = MiscUtils.date_parser(
                date_of_cessation, DATE_FORMAT
            )

    class LlpNetwork:
        def __init__(
            self,
            llpin: str,
            legal_name: str,
            status: str,
            incorporation_date: str,
            total_obligation_of_contribution: str,
            sum_of_charges: str,
            city: str,
            cirp_status: str,
            designation: str,
            date_of_appointment: str,
            date_of_appointment_for_current_designation: str,
            date_of_cessation: str,
        ) -> None:
            self.llpin = llpin
            self.legal_name = legal_name
            self.status = status
            self.incorporation_date = MiscUtils.date_parser(
                incorporation_date, DATE_FORMAT
            )
            self.total_obligation_of_contribution = total_obligation_of_contribution
            self.sum_of_charges = sum_of_charges
            self.city = city
            self.cirp_status = cirp_status
            self.designation = designation
            self.date_of_appointment = MiscUtils.date_parser(
                date_of_appointment, DATE_FORMAT
            )
            self.date_of_appointment_for_current_designation = MiscUtils.date_parser(
                date_of_appointment_for_current_designation, DATE_FORMAT
            )
            self.date_of_cessation = MiscUtils.date_parser(
                date_of_cessation, DATE_FORMAT
            )

    class Network(TypedDict):
        companies: List[ProbeDirectorNetwork.CompanyNetwork]
        llps: List[ProbeDirectorNetwork.LlpNetwork]

    def __init__(
        self,
        name: str,
        pan: str,
        din: str,
        network: Dict[str, List[Union[CompanyNetwork, LlpNetwork]]],
    ) -> None:
        self.name = name
        self.pan = pan
        self.din = din
        self.network = {
            "companies": [
                ProbeDirectorNetwork.CompanyNetwork(**company)
                for company in network["companies"]
            ],
            "llps": [ProbeDirectorNetwork.LlpNetwork(**llp) for llp in network["llps"]],
        }
