from datetime import date
from utils.misc import MiscUtils
from typing import Optional

class FilingStatus:
    def __init__(
        self,
        date: date,
        month: str,
        filing_year: str,
        gst_status: str,
        gst_type: str,
        method: str
    ):
        self.date = date
        self.month = month
        self.filing_year = filing_year
        self.gst_status = gst_status
        self.gst_type = gst_type
        self.method = method

    def to_dict(self):
        return {
            **self.__dict__,
            "date": MiscUtils.date_iso_string(self.date)
        }

class Charges:
    def __init__(self,
        assets_under_charge: Optional[str] = None,
        date_of_creation: Optional[date] = None,
        date_of_modification: Optional[date] = None,
        charge_amount: Optional[str] = None,
        status: Optional[str] = None
    ) -> None:
        self.assets_under_charge = assets_under_charge if assets_under_charge!="NA" else None
        self.date_of_creation = date_of_creation
        self.date_of_modification = date_of_modification
        self.charge_amount = charge_amount
        self.status = status

    def to_dict(self):
        return {
            **self.__dict__,
            "date_of_creation": MiscUtils.date_iso_string(self.date_of_creation),
            "date_of_modification": (MiscUtils.date_iso_string(self.date_of_modification)if self.date_of_modification else None)
        }
    
class Directors:
    def __init__(self,
    end_date: Optional[str] = None,
    din_or_pan: Optional[str] = None,
    begin_date: Optional[date] = None,
    name: Optional[str] = None
    ) -> None:
        self.end_date = end_date
        self.din_or_pan = din_or_pan
        self.begin_date = begin_date
        self.name = name

    def to_dict(self):
        return {
            **self.__dict__,
            "begin_date": MiscUtils.date_iso_string(self.begin_date)
        }
    

class CompanyMasterData:
    def __init__(
    self,
    company_category: Optional[str] = None,
    email_id: Optional[str] = None,
    class_of_company: Optional[str] = None,
    number_of_members_applicable: Optional[str] = None,
    address_where_books_maintained: Optional[str] = None,
    date_of_last_agm: Optional[date] = None,
    registered_address: Optional[str] = None,
    registration_number: Optional[str] = None,
    paid_up_capital_in_inr: Optional[str] = None,
    whether_listed_or_not: Optional[str] = None,
    suspended_at_stock_exchange: Optional[str] = None,
    cin: Optional[str] = None,
    company_subcategory: Optional[str] = None,
    authorised_capital_in_inr: Optional[str] = None,
    company_status_for_e_filing: Optional[str] = None,
    roc_code: Optional[str] = None,
    date_of_balance_sheet: Optional[date] = None,
    date_of_incorporation: Optional[date] = None,
    company_name: Optional[str] = None,
    active_compliance: Optional[str] = None,
    main_division_of_business_activity: Optional[str] = None,
    previous_fir_company_detail: Optional[str] = None,
    number_of_designated_partners: Optional[str] = None,
    total_obligation_of_contribution: Optional[str] = None,
    description_of_main_division: Optional[str] = None,
    number_of_partners: Optional[str] = None
    ) -> None:
        self.company_category = company_category
        self.email_id = email_id
        self.class_of_company = class_of_company
        self.number_of_members_applicable = number_of_members_applicable
        self.address_where_books_maintained = address_where_books_maintained
        self.date_of_last_agm = date_of_last_agm
        self.registered_address = registered_address
        self.registration_number = registration_number
        self.paid_up_capital_in_inr = paid_up_capital_in_inr
        self.whether_listed_or_not = whether_listed_or_not
        self.suspended_at_stock_exchange = suspended_at_stock_exchange
        self.cin = cin
        self.company_subcategory = company_subcategory
        self.authorised_capital_in_inr = authorised_capital_in_inr
        self.company_status_for_e_filing = company_status_for_e_filing
        self.roc_code = roc_code
        self.date_of_balance_sheet = date_of_balance_sheet
        self.date_of_incorporation = date_of_incorporation
        self.company_name = company_name
        self.active_compliance = active_compliance
        self.main_division_of_business_activity = main_division_of_business_activity
        self.previous_fir_company_detail = previous_fir_company_detail
        self.number_of_designated_partners = number_of_designated_partners
        self.total_obligation_of_contribution = total_obligation_of_contribution
        self.description_of_main_division = description_of_main_division
        self.number_of_partners = number_of_partners

    def to_dict(self):
        return {
            **self.__dict__,
            "date_of_last_agm": (MiscUtils.date_iso_string(self.date_of_last_agm) if MiscUtils.date_iso_string(self.date_of_last_agm) else None ),
            "date_of_balance_sheet":  (MiscUtils.date_iso_string(self.date_of_balance_sheet) if MiscUtils.date_iso_string(self.date_of_last_agm) else None),
            "date_of_incorporation": (MiscUtils.date_iso_string(self.date_of_incorporation)if MiscUtils.date_iso_string(self.date_of_last_agm) else None)
        }
