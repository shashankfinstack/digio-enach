from __future__ import annotations
from typing import Optional, List, TypedDict
from enum import Enum
from utils.misc import MiscUtils
from datetime import date
from helpers.common import Address, Gender, ProbePersonComprehensiveDetails,ProbeCompanyComprehensiveDetails,ProbeDirectorNetwork
from .company_basic_details import CompanyDetails,PersonDetails

class FINANCE_COMPANY_MCA_DATA_POINTS(Enum):
    OVERVIEW = "Overview"
    DIRECTOR_DETAILS = "Founder or Directors Details"
    DIRECTOR_SHAREHOLDINGS = "Directors Shareholdings"
    PNL = "Profit & Loss"
    BSL = "Balance Sheet (Liabilities)"
    BSA = "Balance Sheet (Assets)"
    KEY_INSIGHTS = "Key Insights"

class CompanyComprehensiveDetails(CompanyDetails):
    def __init__(
        self,
        active_compliance: str,
        authorized_capital: int,
        cin: str,
        cirp_status: Optional[str],
        classification: str,
        efiling_status: str,
        email: str,
        incorporation_date: date,
        last_agm_date: date,
        last_filing_date: date,
        legal_name: str,
        lei: dict,
        next_cin: Optional[str],
        paid_up_capital: int,
        registered_address: Address,
        status: str,
        sum_of_charges: int,
        business_address: dict,
        pan: str,
        website: str
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
        self.business_address = business_address
        self.pan = pan
        self.website = website

    def to_dict(self):
        return {
            **super().to_dict(),
            "business_address": self.business_address.to_dict(),
            "pan": self.pan,
            "website": self.website
        }

    @classmethod
    def from_probe42(cls,vs: ProbeCompanyComprehensiveDetails):
        return cls(
            active_compliance = vs.active_compliance,
            authorized_capital = vs.authorized_capital,
            cin = vs.cin,
            cirp_status = vs.cirp_status,
            classification = vs.classification,
            efiling_status = vs.efiling_status,
            email = vs.email,
            incorporation_date = vs.incorporation_date,
            last_agm_date = vs.last_agm_date,
            last_filing_date = vs.last_filing_date,
            legal_name = vs.legal_name,
            lei = vs.lei,
            next_cin = vs.next_cin,
            paid_up_capital = vs.paid_up_capital,
            registered_address = vs.registered_address,
            status = vs.status,
            sum_of_charges = vs.sum_of_charges,
            business_address = vs.business_address,
            pan = vs.pan,
            website = vs.website,
        )

class PersonAssociation:
    def __init__(
        self,
        event: Optional[str] = None,
        designation_after_event: Optional[str] = None,
        event_date: Optional[str] = None,
        filing_date: Optional[str] = None,
    ):
        self.event = event
        self.designation_after_event = designation_after_event
        self.event_date = event_date 
        self.filing_date = filing_date 

    def to_dict(self):
        return {
            "event": self.event,
            "designation_after_event": self.designation_after_event,
            "event_date": MiscUtils.date_iso_string(self.event_date) if self.event_date is not None else None,
            "filing_date": MiscUtils.date_iso_string(self.filing_date)if self.filing_date is not None else None,
        }

class PersonComprehensiveDetails(PersonDetails):
    def __init__(
        self,
        pan: str,
        din: str,
        name: str,
        designation: str,
        din_status: str,
        gender: Gender,
        date_of_birth: date,
        age: int,
        date_of_appointment: date,
        date_of_appointment_for_current_designation: date,
        date_of_cessation: date,
        nationality: str,
        dsc_status: str,
        dsc_expiry_date: date,
        father_name: str,
        address: Address,
        association_history: Optional[List[dict]] = None
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
        self.association_history = [] if association_history is None else [PersonAssociation(
            association) for association in association_history]

    def to_dict(self):
        return {
            **super().to_dict(),
            "association_history": [association.to_dict() for association in self.association_history]
        }

    @classmethod
    def from_probe42(cls, vs: ProbePersonComprehensiveDetails):
       return cls(
            pan = vs.pan,
            din = vs.din,
            name = vs.name,
            designation = vs.designation,
            din_status = vs.din_status,
            gender = vs.gender,
            date_of_birth = vs.date_of_birth,
            age = vs.age,
            date_of_appointment = vs.date_of_appointment,
            date_of_appointment_for_current_designation = vs.date_of_appointment_for_current_designation,
            date_of_cessation = vs.date_of_cessation,
            nationality = vs.nationality,
            dsc_status = vs.dsc_status,
            dsc_expiry_date = vs.dsc_expiry_date,
            father_name = vs.father_name,
            address = vs.address,
            association_history = vs.association_history,
       ) 

class DirectorNetwork:
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
            self.incorporation_date = incorporation_date
            self.paid_up_capital = paid_up_capital
            self.sum_of_charges = sum_of_charges
            self.city = city
            self.active_compliance = active_compliance
            self.cirp_status = cirp_status
            self.designation = designation
            self.date_of_appointment = date_of_appointment
            self.date_of_appointment_for_current_designation = date_of_appointment_for_current_designation
            self.date_of_cessation = date_of_cessation

        def to_dict(self):
            return {
                "cin": self.cin,
                "legal_name": self.legal_name,
                "company_status": self.company_status,
                "incorporation_date": MiscUtils.date_iso_string(self.incorporation_date),
                "paid_up_capital": self.paid_up_capital,
                "sum_of_charges": self.sum_of_charges,
                "city": self.city,
                "active_compliance": self.active_compliance,
                "cirp_status": self.cirp_status,
                "designation": self.designation,
                "date_of_appointment": MiscUtils.date_iso_string(self.date_of_appointment),
                "date_of_appointment_for_current_designation": MiscUtils.date_iso_string(self.date_of_appointment_for_current_designation),
                "date_of_cessation": MiscUtils.date_iso_string(self.date_of_cessation),
            }
        
        @classmethod
        def from_probe42(cls,vs: ProbeDirectorNetwork.CompanyNetwork):
            return cls(
                cin=vs.cin,
                legal_name=vs.legal_name,
                company_status=vs.company_status,
                incorporation_date=vs.incorporation_date,
                paid_up_capital=vs.paid_up_capital,
                sum_of_charges=vs.sum_of_charges,
                city=vs.city,
                active_compliance=vs.active_compliance,
                cirp_status=vs.cirp_status,
                designation=vs.designation,
                date_of_appointment=vs.date_of_appointment,
                date_of_appointment_for_current_designation=vs.date_of_appointment_for_current_designation,
                date_of_cessation=vs.date_of_cessation,
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
            self.incorporation_date = incorporation_date
            self.total_obligation_of_contribution = total_obligation_of_contribution
            self.sum_of_charges = sum_of_charges
            self.city = city
            self.cirp_status = cirp_status
            self.designation = designation
            self.date_of_appointment = date_of_appointment
            self.date_of_appointment_for_current_designation = date_of_appointment_for_current_designation
            self.date_of_cessation = date_of_cessation

        def to_dict(self):
            return {
                "llpin": self.llpin,
                "legal_name": self.legal_name,
                "status": self.status,
                "incorporation_date": MiscUtils.date_iso_string(self.incorporation_date),
                "total_obligation_of_contribution": self.total_obligation_of_contribution,
                "sum_of_charges": self.sum_of_charges,
                "city": self.city,
                "cirp_status": self.cirp_status,
                "designation": self.designation,
                "date_of_appointment": MiscUtils.date_iso_string(self.date_of_appointment),
                "date_of_appointment_for_current_designation": MiscUtils.date_iso_string(self.date_of_appointment_for_current_designation),
                "date_of_cessation": MiscUtils.date_iso_string(self.date_of_cessation),
            }
        
        @classmethod
        def from_probe42(cls,vs:ProbeDirectorNetwork.LlpNetwork):
            return cls(
                llpin = vs.llpin,
                legal_name = vs.legal_name,
                status = vs.status,
                incorporation_date = vs.incorporation_date,
                total_obligation_of_contribution = vs.total_obligation_of_contribution,
                sum_of_charges = vs.sum_of_charges,
                city = vs.city,
                cirp_status = vs.cirp_status,
                designation = vs.designation,
                date_of_appointment = vs.date_of_appointment,
                date_of_appointment_for_current_designation = vs.date_of_appointment_for_current_designation,
                date_of_cessation = vs.date_of_cessation,
            )
        
    class Network(TypedDict):
        companies: List[DirectorNetwork.CompanyNetwork]
        llps: List[DirectorNetwork.LlpNetwork]

    def __init__(
        self,
        name: str,
        pan: str,
        din: str,
        network: DirectorNetwork.Network,
    ) -> None:
        self.name = name
        self.pan = pan
        self.din = din
        self.network = network

    def to_dict(self):
        return {
            "name": self.name,
            "pan": self.pan,
            "din": self.din,
            "network": {
                "companies": [company.to_dict() for company in self.network["companies"]],
                "llps": [llp.to_dict() for llp in self.network["llps"]]
            }
        }

    @classmethod
    def from_probe42(cls,vs: ProbeDirectorNetwork):
        return cls(
            name = vs.name,
            pan = vs.pan,
            din = vs.din,
            network = DirectorNetwork.Network(
                companies=[DirectorNetwork.CompanyNetwork.from_probe42(company) for company in vs.network["companies"]],
                llps=[DirectorNetwork.LlpNetwork.from_probe42(llp) for llp in vs.network["llps"]]
            )
        )