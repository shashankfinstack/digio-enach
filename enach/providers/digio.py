from __future__ import annotations
from datetime import datetime
from enum import Enum
import re
from helpers.body_field_validation import BodyFieldValidation 
from helpers.common import CallMeta, CallInfo, ResponseData, DictConfig, DictWithConfig, response_data
from helpers.common.response_data import ResponseCallbackHelper, CallbackStatusEnum
from helpers.common.providers.digio import (
    AuthMode, Frequency, ManagementCategory, MandateType, StateOfBank, CurrentStateOfMandate, StatusWithBank, 
    TypeOfIdentifier, AccountType, AuthSubMode, Type
)
from utils.misc import MiscUtils

from helpers.common import(
    DEFAULT_DIGIO_HEADERS
)

from typing import Any, Dict, Optional, List, Union
from helpers.api_response_helpers import ApiResponseHelpers
from helpers.common import (
    CallContext,
    CallInfo,
    CallMeta,
    RequestContext,
    DictWithConfig,
    AppContexts,
    ResponseData,
    AppEnvironments,
    HttpMethods,
)
from utils.secret import SecretUtils


# These 3 classes are used in DigioEnachCreateMandateCall for Response
class MandateData:
    SCHEME_REF_NUMBER_PATTERN = re.compile(r"^[0-9A-Za-z]{0,20}$")         # Max 20 chars, alphanumeric
    # ORIGINAL_MANDATE_ID_PATTERN = re.compile(r"^.{20}$")                 # Exactly 20 characters

    def __init__(
        self,
        destination_bank_id: str,
        destination_bank_name: str,
        management_category: ManagementCategory,
        customer_account_number: str,
        customer_account_type: AccountType,
        customer_name: str,
        instrument_type: str,
        maximum_amount: float,
        frequency: Frequency,
        first_collection_date: datetime,
        customer_email: Optional[str] = None,
        customer_mobile: Optional[str] = None,
        customer_ref_number: Optional[str] = None,
        scheme_ref_number: Optional[str] = None,
        collection_amount: Optional[float] = None,
        is_recurring: bool = False,
        final_collection_date: Optional[datetime] = None
        # original_mandate_id: str = None
    ):
        if scheme_ref_number and not self.SCHEME_REF_NUMBER_PATTERN.fullmatch(scheme_ref_number):
            raise ValueError("scheme_ref_number must be alphanumeric and up to 20 characters.")
        
        # if not self.ORIGINAL_MANDATE_ID_PATTERN.fullmatch(original_mandate_id):
        #     raise ValueError("original_mandate_id must be exactly 20 characters.")
        
        self.destination_bank_id = destination_bank_id
        self.destination_bank_name = destination_bank_name
        self.management_category = management_category
        self.customer_account_number = customer_account_number
        self.customer_account_type = customer_account_type
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_mobile = customer_mobile
        self.instrument_type = instrument_type
        self.customer_ref_number = customer_ref_number
        self.scheme_ref_number = scheme_ref_number
        self.collection_amount = collection_amount
        self.maximum_amount = maximum_amount
        self.is_recurring = is_recurring
        self.frequency = frequency
        self.first_collection_date = first_collection_date
        self.final_collection_date = final_collection_date
        # self.original_mandate_id = original_mandate_id

    # Converts the object into a dictionary. This is useful for serializing the object, e.g., when preparing data to send to an API. (OBJECT TO DICT)
    def to_dict(self) -> Dict[str, Union[str, float, bool]]:
        return {
            "destination_bank_id": self.destination_bank_id,
            "destination_bank_name": self.destination_bank_name,
            "management_category": self.management_category.name,
            "customer_account_number": self.customer_account_number,
            "customer_account_type": self.customer_account_type.name,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_mobile": self.customer_mobile,
            "instrument_type": self.instrument_type,
            "customer_ref_number": self.customer_ref_number,
            "scheme_ref_number": self.scheme_ref_number,
            "collection_amount": self.collection_amount,
            "maximum_amount": self.maximum_amount,
            "is_recurring": self.is_recurring,
            "frequency": self.frequency.name,
            "first_collection_date": self.first_collection_date.isoformat(),
            "final_collection_date": self.final_collection_date.isoformat() if self.final_collection_date else None
        }
    
    # Creates an instance of the MandateData class from a dictionary. This is often used when parsing API responses or deserializing JSON data. (DICT TO OBJECT)
    # A class method that creates an instance of MandateData from a dictionary. It uses helper methods from a 
    # MiscUtils class to extract values, ensuring the necessary ones are present and converting them appropriately.
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MandateData:
        if data is None:
            return None
        
        value_management_category = MiscUtils.get_value_from_dict(data, "management_category", none_accepted=False)
        value_account_type = MiscUtils.get_value_from_dict(data, "customer_account_type", none_accepted=False)
        value_frequency = MiscUtils.get_value_from_dict(data, "frequency", none_accepted=False)
        value_first_collection_date = MiscUtils.get_value_from_dict(data, "first_collection_date", none_accepted=False)
        value_final_collection_date = MiscUtils.get_value_from_dict(data, "final_collection_date", none_accepted=True)

        return cls(
            destination_bank_id = MiscUtils.get_value_from_dict(
                data, "destination_bank_id", none_accepted=True),

            destination_bank_name = MiscUtils.get_value_from_dict(
                data, "destination_bank_name", none_accepted=True),
            
            management_category = MiscUtils.value_to_enum(
                value_management_category, ManagementCategory),

            customer_account_number = MiscUtils.get_value_from_dict(
                data, "customer_account_number", none_accepted=True),

            customer_account_type = MiscUtils.value_to_enum(
                value_account_type, AccountType),

            customer_name = MiscUtils.get_value_from_dict(
                data, "customer_name", none_accepted=False),

            customer_email = MiscUtils.get_value_from_dict(
                data, "customer_email", none_accepted=True),

            customer_mobile = MiscUtils.get_value_from_dict(
                data, "customer_mobile", none_accepted=True),

            instrument_type = MiscUtils.get_value_from_dict(
                data, "instrument_type", none_accepted=False),

            customer_ref_number = MiscUtils.get_value_from_dict(
                data, "customer_ref_number", none_accepted=True),

            scheme_ref_number = MiscUtils.get_value_from_dict(
                data, "scheme_ref_number", none_accepted=True),
            
            collection_amount = MiscUtils.get_value_from_dict(
                data, "collection_amount", none_accepted=True),

            maximum_amount = MiscUtils.get_value_from_dict(
                data, "maximum_amount", none_accepted=False),

            is_recurring = MiscUtils.get_value_from_dict(
                data, "is_recurring", none_accepted=False),

            frequency = MiscUtils.value_to_enum(
                value_frequency, Frequency),

            first_collection_date = datetime.fromisoformat(
                value_first_collection_date),
            
            final_collection_date=datetime.fromisoformat(
                value_final_collection_date) if value_final_collection_date else None,
        )

    

class BankDetails:
    def __init__(
        self,
        shared_with_bank: str,
        bank_name: str,
        state: StateOfBank
    ):
        self.shared_with_bank = shared_with_bank
        self.bank_name = bank_name
        self.state = state

    def to_dict(self) -> Dict[str, Union[str, StateOfBank]]:
        return {
            "shared_with_bank": self.shared_with_bank,
            "bank_name": self.bank_name,
            "state": self.state.value
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BankDetails":
        return cls(
            shared_with_bank = MiscUtils.get_value_from_dict(
                data, "shared_with_bank", none_accepted=False),
            bank_name = MiscUtils.get_value_from_dict(
                data, "bank_name", none_accepted=False),
            state = MiscUtils.value_to_enum(
                MiscUtils.get_value_from_dict(data, "state", none_accepted=False), StateOfBank)            
        )

class ServiceProviderDetails:
    def __init__(
        self,
        service_provider_name: str,
        service_provider_utility_code: str,
    ):
        self.service_provider_name = service_provider_name
        self.service_provider_utility_code = service_provider_utility_code

    def to_dict(self) -> Dict[str, Union[str]]:
        return {
            "service_provider_name": self.service_provider_name,
            "service_provider_utility_code": self.service_provider_utility_code
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ServiceProviderDetails":
        return cls(
            service_provider_name = MiscUtils.get_value_from_dict(
                data, "service_provider_name", none_accepted=False),
            service_provider_utility_code = MiscUtils.get_value_from_dict(
                data, "service_provider_utility_code", none_accepted=False)            
        )

# 1. Create Mandate Request 
class DigioEnachCreateMandateCall:
    class Request:
        def __init__(
            self,
            corporate_config_id: str,
            mandate_type: MandateType,
            customer_identifier: str,
            auth_mode: AuthMode,
            mandate_data: MandateData = None,
            notify_customer: Optional[bool] = True,
            expire_in_days: Optional[int] = 10
        ):
            self.corporate_config_id = corporate_config_id
            self.mandate_type = mandate_type
            self.customer_identifier = customer_identifier
            self.auth_mode = auth_mode
            self.mandate_data = mandate_data
            self.notify_customer = notify_customer
            self.expire_in_days = max(1, min(90, expire_in_days)) if expire_in_days else 10

        def to_dict(self) -> Dict[str, Union[str, None, List[Dict[str, Any]]]]:
            # print(self.__dict__)
            # breakpoint()
            return {
                "customer_identifier": self.customer_identifier,
                "auth_mode": self.auth_mode,                 # No need to check for None since it's required
                "mandate_type": self.mandate_type,           # Same as above
                "corporate_config_id": self.corporate_config_id,
                "mandate_data": self.mandate_data,
                "notify_customer": self.notify_customer,
                "expire_in_days": self.expire_in_days
            }
        
    class Response:
        def __init__(
                self,
                id: str,
                mandate_id: str,
                state: CurrentStateOfMandate,
                type: Type,
                bank_details: BankDetails,
                created_at: datetime,
                mode: AuthMode,
                service_provider_details: ServiceProviderDetails
        ) -> None:
            self.id = id
            self.mandate_id = mandate_id
            self.state = state
            self.type = type
            self.bank_details = bank_details
            self.created_at = created_at
            self.mode = mode
            self.service_provider_details = service_provider_details

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> DigioEnachCreateMandateCall.Response:
            return cls(
                id = data.get("id"),
                mandate_id = data.get("mandate_id"),
                state = CurrentStateOfMandate(data.get("state")),
                type = Type(data.get("type")),
                bank_details = BankDetails.from_dict(data.get("bank_details")),
                created_at = datetime.fromisoformat(data.get("created_at")),
                mode = AuthMode(data.get("mode")),
                service_provider_details = ServiceProviderDetails.from_dict(data.get("service_provider_details"))
            )
            

    def __init__(
        self,
        request: Request,
        response: Optional[Response],
        raw_response: Optional[dict] = None,
        context: Optional[CallContext] = None,
        meta: Optional[CallMeta] = None,
        info: Optional[CallInfo] = None,
        helpers: Optional[ApiResponseHelpers] = None,
    ) -> None:
        self.request = request
        self.response = response
        self.raw_response = raw_response
        self.helpers = helpers
        self.context = (
            CallContext(
                base_url_var_name = SecretUtils.SECRETS.DIGIO_TEMPLATE_BASE_URL,
                request_contexts={
                    AppContexts.live: RequestContext(
                        path="/v3/client/mandate/create_form",
                        method=HttpMethods.POST,
                        headers=DEFAULT_DIGIO_HEADERS(),
                        json=request.to_dict()
                    ),
                    AppContexts.mock: RequestContext(
                        path="/v3/client/mandate/create_form",
                        method=HttpMethods.POST,
                    ),
                },
            )
            if context is None
            else context
        )
        self.meta = (
            CallMeta(
                error_message="Digio Enach creation failed",
                success_message="Digio Enach created successfully",
            )
            if meta is None
            else meta
        )
        self.info = info

    def response_data(self,body_field_validations: List[BodyFieldValidation] = [], document_url=None) -> ResponseData:
        return ResponseData(
            request = DictWithConfig(
                d=self.request,
            ),
            features = DictWithConfig(
                d=self.response
            ),
            helpers= self.helpers,
            vendor= "DIGIO",
            callback=ResponseCallbackHelper(
                id=self.response.id,
                status=CallbackStatusEnum.REQUESTED,
                is_polling=False,
            ) if self.response is not None else None
        )



# 2. Get Mandate Details by its unique mandate ID i.e. ENA ID
class AckReport:
    def __init__(
        self,
        id: str,
        umrn: str,
        message_id: str,
        original_message_id: str,
        enach_id: str,
        accepted: bool,
        generated_at: datetime,
        file_name: str,
        created_at: datetime,
        updated_at: datetime,
        reject_code: Optional[str] = None,
        reject_reason: Optional[str] = None
    ):
        self.id = id
        self.umrn = umrn
        self.message_id = message_id
        self.original_message_id = original_message_id
        self.enach_id = enach_id
        self.accepted = accepted
        self.generated_at = generated_at
        self.file_name = file_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.reject_code = reject_code
        self.reject_reason = reject_reason

    def to_dict(self) -> Dict[str, Union[str, bool, datetime, None]]:
        return {
            "id": self.id,
            "umrn": self.umrn,
            "message_id": self.message_id,
            "original_message_id": self.original_message_id,
            "enach_id": self.enach_id,
            "accepted": self.accepted,
            "generated_at": self.generated_at.isoformat(),
            "file_name": self.file_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "reject_code": self.reject_code,
            "reject_reason": self.reject_reason,
        }

class ResReport:
    def __init__(
            self,
            id: str,
            umrn: str,
            message_id: str,
            original_message_id: str,
            enach_id: str,
            accepted: bool,
            generated_at: datetime,
            file_name: str,
            reject_code: str,
            reject_reason: str,
            dest_bank_name: str,
            dest_bank_id: str,
            created_at: datetime,
            updated_at: datetime
    ):
        self.id = id 
        self.umrn = umrn
        self.message_id = message_id
        self.original_message_id = original_message_id
        self.enach_id = enach_id
        self.accepted = accepted
        self.generated_at = generated_at
        self.file_name = file_name
        self.reject_code = reject_code
        self.reject_reason = reject_reason
        self.dest_bank_name = dest_bank_name
        self.dest_bank_id = dest_bank_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Union[str, bool, datetime, None]]:
        return {
            "id": self.id,
            "umrn": self.umrn,
            "message_id": self.message_id,
            "original_message_id": self.original_message_id,
            "enach_id": self.enach_id,
            "accepted": self.accepted,
            "generated_at": self.generated_at.isoformat(),
            "file_name": self.file_name,
            "reject_code": self.reject_code,
            "reject_reason": self.reject_reason,
            "dest_bank_name": self.dest_bank_name,
            "dest_bank_id": self.dest_bank_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
  

class GetBankDetails:
    def __init__(
        self,
        shared_with_bank: str,
        bank_name: str,
        state: StatusWithBank,
        shared_at: datetime,
        authenticated_at: datetime,
        ack_report: List[AckReport],
        res_report: List[ResReport]
    ):
        self.shared_with_bank = shared_with_bank
        self.bank_name = bank_name
        self.state = state
        self.shared_at = shared_at
        self.authenticated_at = authenticated_at
        self.ack_report = ack_report
        self.res_report = res_report

    def to_dict(self) -> Dict[str, Union[str, datetime, List[Dict[str, Union[str, bool, datetime]]]]]:
        return {
            "shared_with_bank": self.shared_with_bank,
            "bank_name": self.bank_name,
            "state": self.state.value,
            "shared_at": self.shared_at.isoformat(),
            "authenticated_at": self.authenticated_at.isoformat(),
            "ack_report": [report.to_dict() for report in self.ack_report],
            "res_report": [report.to_dict() for report in self.res_report]
        }


class MandateDetails:
    def __init__(
        self,
        file_name: str,
        customer_identifier: str,
        customer_name: str,
        customer_ref_number: str,
        auth_type: AuthMode,
        authentication_time: datetime,
        is_recurring: bool,
        first_collection_date: datetime,
        maximum_amount: float,
        customer_account_number: str,
        customer_account_type: AccountType,
        destination_bank_id: str,
        destination_bank_name: str,
        sponsor_bank_name: str,
        scheme_ref_number: Optional[str] = None,
        customer_mobile: Optional[str] = None,
        customer_email: Optional[str] = None,
        frequency: Optional[Frequency] = None,
        final_collection_date: Optional[datetime] = None,
        collection_amount: Optional[float] = None,
        npci_txn_id: Optional[str] = None
    ):
        self.file_name = file_name
        self.customer_identifier = customer_identifier
        self.customer_name = customer_name
        self.customer_ref_number = customer_ref_number
        self.auth_type = auth_type
        self.authentication_time = authentication_time
        self.is_recurring = is_recurring
        self.first_collection_date = first_collection_date
        self.maximum_amount = maximum_amount
        self.customer_account_number = customer_account_number
        self.customer_account_type = customer_account_type
        self.destination_bank_id = destination_bank_id
        self.destination_bank_name = destination_bank_name
        self.sponsor_bank_name = sponsor_bank_name
        self.scheme_ref_number = scheme_ref_number
        self.customer_mobile = customer_mobile
        self.customer_email = customer_email
        self.frequency = frequency
        self.final_collection_date = final_collection_date
        self.collection_amount = collection_amount
        self.npci_txn_id = npci_txn_id

    def to_dict(self) -> Dict[str, Union[str, bool, float, datetime, None]]:
        return {
            "file_name": self.file_name,
            "customer_identifier": self.customer_identifier,
            "customer_name": self.customer_name,
            "customer_ref_number": self.customer_ref_number,
            "auth_type": self.auth_type.value,
            "authentication_time": self.authentication_time.isoformat(),
            "is_recurring": self.is_recurring,
            "first_collection_date": self.first_collection_date.isoformat(),
            "maximum_amount": self.maximum_amount,
            "customer_account_number": self.customer_account_number,
            "customer_account_type": self.customer_account_type.value,
            "destination_bank_id": self.destination_bank_id,
            "destination_bank_name": self.destination_bank_name,
            "sponsor_bank_name": self.sponsor_bank_name,
            "scheme_ref_number": self.scheme_ref_number,
            "customer_mobile": self.customer_mobile,
            "customer_email": self.customer_email,
            "frequency": self.frequency.value if self.frequency else None,
            "final_collection_date": self.final_collection_date.isoformat() if self.final_collection_date else None,
            "collection_amount": self.collection_amount,
            "npci_txn_id": self.npci_txn_id,
        }


class DigioEnachGetMandateDetails:
    class Request:
        def __init__(
                self,
                mandate_id: str   
        ) -> None:
            self.mandate_id = mandate_id
        
        def to_dict(self) -> Dict[str,str]:
            return {
                "mandate_id": self.mandate_id
            }
        
    class Response:
        def __init__(
                self,
                id: str,
                mandate_id: str,
                state: CurrentStateOfMandate,
                type: MandateType,
                bank_details: BankDetails,
                mandate_details: MandateDetails,
                umrn: str,
                created_at: datetime,
                updated_at: datetime,
                mode: AuthMode,
                service_provider_details: ServiceProviderDetails
        ) -> None:
            self.id = id 
            self.mandate_id = mandate_id
            self.state = state
            self.type = type
            self.bank_details = bank_details
            self.mandate_details = mandate_details
            self.umrn = umrn
            self.created_at = created_at
            self.updated_at = updated_at
            self.mode = mode 
            self.service_provider_details = service_provider_details


        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> DigioEnachGetMandateDetails.Response:
            return cls(
                id = data.get("id"),
                mandate_id = data.get("mandate_id"),
                state = CurrentStateOfMandate(data.get("state")),
                type = Type(data.get("type")),
                bank_details = BankDetails.from_dict(data.get("bank_details")),
                created_at = datetime.fromisoformat(data.get("created_at")),
                mode = AuthMode(data.get("mode")),
                service_provider_details = ServiceProviderDetails.from_dict(data.get("service_provider_details"))
            )
        
    def __init__(
        self,
        request: Request,
        response: Optional[Response],
        raw_response: Optional[dict] = None,
        context: Optional[CallContext] = None,
        meta: Optional[CallMeta] = None,
        info: Optional[CallInfo] = None,
        helpers: Optional[ApiResponseHelpers] = None,
    ) -> None:
        self.request = request
        self.response = response
        self.raw_response = raw_response
        self.helpers = helpers
        self.context = (
            CallContext(
                base_url_var_name = SecretUtils.SECRETS.DIGIO_TEMPLATE_BASE_URL,
                request_contexts={
                    AppContexts.live: RequestContext(
                        path=f"/v3/client/mandate/{request.mandate_id}",
                        method=HttpMethods.GET,
                        headers=DEFAULT_DIGIO_HEADERS(),
                        json=request.to_dict()
                    ),
                    AppContexts.mock: RequestContext(
                        path=f"/v3/client/mandate/{request.mandate_id}",
                        method=HttpMethods.GET,
                    ),
                },
            )
            if context is None
            else context
        )
        self.meta = (
            CallMeta(
                error_message="Failed to retrieve mandate details",
                success_message="Mandate details retrieved successfully",
            )
            if meta is None
            else meta
        )
        self.info = info

    def response_data(self,body_field_validations: List[BodyFieldValidation] = [], document_url=None) -> ResponseData:
        return ResponseData(
            request = DictWithConfig(
                d=self.request,
            ),
            features = DictWithConfig(
                d=self.response
            ),
            helpers= self.helpers,
            vendor= "DIGIO",
            callback=ResponseCallbackHelper(
                id=self.response.id,
                status=CallbackStatusEnum.REQUESTED,
                is_polling=False,
            ) if self.response is not None else None
        )




# 3. Get Mandate Details (by CRN)
class SubUser:
    def __init__(
        self,
        id: str,
        identifier_value: str,
        identifier: TypeOfIdentifier,
        email_id: str,
        mobile: str
    ):
        self.id = id 
        self.identifier_value = identifier_value
        self.identifier = identifier
        self.email_id = email_id
        self.mobile = mobile

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {
            "id": self.id,
            "identifier_value": self.identifier_value,
            "identifier": self.identifier.value if isinstance(self.identifier, TypeOfIdentifier) else str(self.identifier),
            "email_id": self.email_id,
            "mobile": self.mobile
        }

class DigioEnachGetMandateDetailsByCRN:
    class Request:
        def __init__(
                self,
                crn: str   
        ) -> None:
            self.crn = crn
        
        def to_dict(self) -> Dict[str,str]:
            return {
                "crn": self.crn
            }
        
    class Response:
        def __init__(
                self,
                id: str,
                mandate_id: str,
                state: CurrentStateOfMandate,
                type: MandateType,
                bank_details: BankDetails,
                mandate_details: MandateDetails,
                sub_user: SubUser,
                umrn: str,
                created_at: datetime,
                updated_at: datetime,
                auth_mode: AuthMode,
                auth_sub_mode: AuthSubMode,
                service_provider_details: ServiceProviderDetails,
                npci_auth_failed_error: str,
                npci_auth_reject_reason: str 

        ) -> None:
            self.id = id 
            self.mandate_id = mandate_id
            self.state = state
            self.type = type
            self.bank_details = bank_details
            self.mandate_details = mandate_details
            self.sub_user = sub_user
            self.umrn = umrn
            self.created_at = created_at
            self.updated_at = updated_at
            self.auth_mode = auth_mode
            self.auth_sub_mode = auth_sub_mode
            self.service_provider_details = service_provider_details
            self.npci_auth_failed_error = npci_auth_failed_error
            self.npci_auth_reject_reason = npci_auth_reject_reason



# 4. Cancel Mandate Request (implement both -> UMRN based & DIGIO Mandate ID based)
class DigioEnachCancelExistingMandate:
    class Request:
        def __init__(
                self,
                umrn: str,
                dest_ifsc: str
        ) -> None:
            self.umrn = umrn
            self.dest_ifsc = dest_ifsc

        def to_dict(self) -> Dict[str,str]:
            return {
                "umrn": self.umrn,
                "dest_ifsc": self.dest_ifsc
            }
        
    class Response:
        def __init__(
                self,
                id: str,
                mandate_id: str,
                state: CurrentStateOfMandate,
                type: MandateType,
                bank_details: BankDetails,
                mandate_details: MandateDetails,
                sub_user: SubUser,
                umrn: str,
                created_at: datetime,
                updated_at: datetime,
                auth_mode: AuthMode,
                service_provider_details: ServiceProviderDetails,
                npci_auth_failed_error: str,
                npci_auth_reject_reason: str 

        ) -> None:
            self.id = id 
            self.mandate_id = mandate_id
            self.state = state
            self.type = type
            self.bank_details = bank_details
            self.mandate_details = mandate_details
            self.sub_user = sub_user
            self.umrn = umrn
            self.created_at = created_at
            self.updated_at = updated_at
            self.auth_mode = auth_mode
            self.service_provider_details = service_provider_details
            self.npci_auth_failed_error = npci_auth_failed_error
            self.npci_auth_reject_reason = npci_auth_reject_reason
            