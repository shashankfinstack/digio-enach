from __future__ import annotations
from datetime import date
from helpers.common import Address, Gender
from typing import Optional


class CompanyDetails:
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
        *args,
        **kwargs
    ):
        self.active_compliance = active_compliance
        self.authorized_capital = authorized_capital
        self.cin = cin
        self.cirp_status = cirp_status
        self.classification = classification
        self.efiling_status = efiling_status
        self.email = email
        self.incorporation_date = incorporation_date
        self.last_agm_date = last_agm_date
        self.last_filing_date = last_filing_date
        self.legal_name = legal_name
        self.lei = lei
        self.next_cin = next_cin
        self.paid_up_capital = paid_up_capital
        self.registered_address = registered_address
        self.status = status
        self.sum_of_charges = sum_of_charges

    def to_dict(self):
        return {
            "active_compliance": self.active_compliance,
            "authorized_capital": self.authorized_capital,
            "cin": self.cin,
            "cirp_status": self.cirp_status,
            "classification": self.classification,
            "efiling_status": self.efiling_status,
            "email": self.email,
            "incorporation_date": self.incorporation_date.isoformat() if isinstance(self.incorporation_date, date) else self.incorporation_date,
            "last_agm_date": self.last_agm_date.isoformat() if isinstance(self.last_agm_date, date) else self.last_agm_date,
            "last_filing_date": self.last_filing_date.isoformat() if isinstance(self.last_filing_date, date) else self.last_filing_date,
            "legal_name": self.legal_name,
            "lei": self.lei,
            "next_cin": self.next_cin,
            "paid_up_capital": self.paid_up_capital,
            "registered_address": self.registered_address.to_dict(),
            "status": self.status,
            "sum_of_charges": self.sum_of_charges,
        }


class PersonDetails:
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
        *args,
        **kwargs
    ):
        self.pan = pan
        self.din = din
        self.name = name
        self.designation = designation
        self.din_status = din_status
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.age = age
        self.date_of_appointment = date_of_appointment
        self.date_of_appointment_for_current_designation = date_of_appointment_for_current_designation
        self.date_of_cessation = date_of_cessation
        self.nationality = nationality
        self.dsc_status = dsc_status
        self.dsc_expiry_date = dsc_expiry_date
        self.father_name = father_name
        self.address = address

    def to_dict(self):
        return {
            "pan": self.pan,
            "din": self.din,
            "name": self.name,
            "designation": self.designation,
            "din_status": self.din_status,
            "gender": self.gender.value if isinstance(self.gender, Gender) else self.gender,
            "date_of_birth": self.date_of_birth.isoformat() if isinstance(self.date_of_birth, date) else self.date_of_birth,
            "age": self.age,
            "date_of_appointment": self.date_of_appointment.isoformat() if isinstance(self.date_of_appointment, date) else self.date_of_appointment,
            "date_of_appointment_for_current_designation": self.date_of_appointment_for_current_designation.isoformat() if isinstance(self.date_of_appointment_for_current_designation, date) else self.date_of_appointment_for_current_designation,
            "date_of_cessation": self.date_of_cessation.isoformat() if isinstance(self.date_of_cessation, date) else self.date_of_cessation,
            "nationality": self.nationality,
            "dsc_status": self.dsc_status,
            "dsc_expiry_date": self.dsc_expiry_date.isoformat() if isinstance(self.dsc_expiry_date, date) else self.dsc_expiry_date,
            "father_name": self.father_name,
            "address": self.address.to_dict(),
        }


class OpenCharge:
    def __init__(
        self,
        amount: float,
        date: date,
        holder_name: str,
        id: str,
        type: str,
        *args,
        **kwargs
    ) -> None:
        self.amount = amount
        self.date = date
        self.holder_name = holder_name
        self.id = id
        self.type = type

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.date.isoformat() if isinstance(self.date, date) else self.date,
            "holder_name": self.holder_name,
            "id": self.id,
            "type": self.type,
        }
