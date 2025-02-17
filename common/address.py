from __future__ import annotations
from typing import Optional
from utils.misc import MiscUtils
from helpers.common.misc import IndianStates

class ResidenceAddress:
    def __init__(
        self,
        house: Optional[str] = None,
        street: Optional[str] = None,
        post_office: Optional[str] = None,
        landmark: Optional[str] = None,
        city: Optional[str] = None,
        sub_district: Optional[str] = None,
        district: Optional[str] = None,
        pincode: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
    ) -> None:
        self.house = MiscUtils.check_unknown_empty_value(house)
        self.street = MiscUtils.check_unknown_empty_value(street)
        self.post_office = MiscUtils.check_unknown_empty_value(post_office)
        self.landmark = MiscUtils.check_unknown_empty_value(landmark)
        self.city = MiscUtils.check_unknown_empty_value(city)
        self.sub_district = MiscUtils.check_unknown_empty_value(sub_district)
        self.district = MiscUtils.check_unknown_empty_value(district)
        self.pincode = MiscUtils.check_unknown_empty_value(pincode)
        self.state = MiscUtils.check_unknown_empty_value(state)
        self.country = MiscUtils.check_unknown_empty_value(country)

    def to_dict(self):
        if self is None:
            return None
        return {
            "house": self.house,
            "street": self.street,
            "post_office": self.post_office,
            "landmark": self.landmark,
            "city": self.city,
            "sub_district": self.sub_district,
            "district": self.district,
            "pincode": self.pincode,
            "state": self.state,
            "country": self.country,
        }

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        return cls(
            house=MiscUtils.get_value_from_dict(
                d, "house", none_accepted=True),
            street=MiscUtils.get_value_from_dict(
                d, "street", none_accepted=True),
            post_office=MiscUtils.get_value_from_dict(
                d, "post_office", none_accepted=True),
            landmark=MiscUtils.get_value_from_dict(
                d, "landmark", none_accepted=True),
            city=MiscUtils.get_value_from_dict(
                d,"city",none_accepted=True
            ),
            sub_district=MiscUtils.get_value_from_dict(
                d, "sub_district", none_accepted=True),
            district=MiscUtils.get_value_from_dict(
                d, "district", none_accepted=True),
            pincode=MiscUtils.get_value_from_dict(
                d, "pincode", none_accepted=True),
            state=MiscUtils.get_value_from_dict(
                d, "state", none_accepted=True),
            country=MiscUtils.get_value_from_dict(
                d, "country", none_accepted=True),
        )

    @staticmethod
    def blank_if_null_string(s: str,comma: bool = True) -> str:
            if s is None or (isinstance(s,str) and s.strip()) == '':
                return ''
            return f"{s}{',' if comma is True else ''} "
    
    @staticmethod
    def format(address_line: str) -> str:
        while len(address_line) > 0 and (address_line[-1] == ',' or address_line[-1] == " "):
            address_line = address_line[:len(address_line)-1]
        return MiscUtils.check_unknown_empty_value(address_line)       
    
    def get_address_line1(self) -> str:
        address_line = f"{ResidenceAddress.blank_if_null_string(self.house)}{ResidenceAddress.blank_if_null_string(self.street)}"
        return ResidenceAddress.format(address_line)
    
    def get_address_line2(self) -> str:
        address_line = f"{ResidenceAddress.blank_if_null_string(self.post_office)}{ResidenceAddress.blank_if_null_string(self.landmark)}{ResidenceAddress.blank_if_null_string(self.sub_district)}"
        return ResidenceAddress.format(address_line)
    
    
class Address:
    def __init__(
        self,
        full_address: Optional[str] = None,
        address_line1: Optional[str] = None,
        address_line2: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        pincode: Optional[int] = None,
        type_of_address: Optional[str] = None,
        district: Optional[str] = None,
        **kwargs
    ) -> None:
        self.address_line1 = MiscUtils.check_unknown_empty_value(address_line1)
        self.address_line2 = MiscUtils.check_unknown_empty_value(address_line2)
        self.city = MiscUtils.title_case(MiscUtils.check_unknown_empty_value(city))
        self.type_of_address = type_of_address
        self.district = district
        self.state = None
        self.state_code = None
        indian_state = IndianStates.guess(state)
        if indian_state is not None:
            self.state = indian_state.value
            self.state_code = indian_state.name
        if country is None:
            self.country = "INDIA" if indian_state is not None else None
        else: 
            self.country = country.upper()
        self.pincode = MiscUtils.check_unknown_empty_value(pincode)
        self.full_address = MiscUtils.check_unknown_empty_value(self.get_full_address() if full_address is None else full_address)
    
    @classmethod
    def from_residence_address(cls,residence_address: ResidenceAddress) -> Address:
        return cls(
            address_line1=residence_address.get_address_line1(),
            address_line2=residence_address.get_address_line2(),
            city=MiscUtils.pick_non_null(residence_address.city,residence_address.district),
            state=residence_address.state,
            country=residence_address.country,
            pincode=residence_address.pincode,
        )
    
    def get_full_address(self) -> str:
        pin_code = ResidenceAddress.blank_if_null_string(self.pincode)
        address_line = f"{ResidenceAddress.blank_if_null_string(self.address_line1)}{ResidenceAddress.blank_if_null_string(self.address_line2)}{ResidenceAddress.blank_if_null_string(self.city)}{ResidenceAddress.blank_if_null_string(self.state)}{f'PO {pin_code}' if len(pin_code) > 0 else ''}{ResidenceAddress.blank_if_null_string(self.country)}"
        return ResidenceAddress.format(address_line)
    
    def to_dict(self) -> dict:
        return {
            "full_address": self.full_address,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "state_code": self.state_code,
            "country": self.country,
            "pincode": self.pincode,
        }