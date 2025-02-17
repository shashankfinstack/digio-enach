from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from helpers.common import CallMeta, CallInfo, ResponseData, EsignOptions, DictConfig, DictWithConfig, response_data
from helpers.common.providers.digio import (
    AuthMode, Frequency, MandateType, CurrentStateOfMandate, StatusWithBank, 
    TypeOfIdentifier, AccountType, AuthSubMode
)
from helpers.enach.providers.digio import AuthMode, BankDetails, DigioEnachCreateMandateCall, DigioEnachGetMandateDetails, MandateData, MandateDetails, ServiceProviderDetails
from helpers.api_response_helpers import ApiResponseHelpers
from helpers.body_field_validation import BodyFieldValidation 
from utils.misc import MiscUtils


class EnachProviders(Enum):
    DIGIO = "DIGIO"

class EnachCreateMandateCall:
    class Request:
        def __init__(
            self,
            customer_identifier: str,                            # Email or Mobile number
            auth_mode: AuthMode,                      
            mandate_type: MandateType,                       # made default value of mandate type as create
            corporate_config_id: str,
            mandate_data: MandateData = None,              # Data related to the mandate (e.g., maximum amount, first collection date, etc.)
            notify_customer: Optional[bool] = True,
            **kwargs
        ) -> None:
            self.customer_identifier = customer_identifier
            self.auth_mode = auth_mode
            self.mandate_type = mandate_type
            self.corporate_config_id = corporate_config_id
            self.mandate_data = mandate_data
            self.notify_customer = notify_customer
            self.kwargs = kwargs

        def for_digio(self) -> DigioEnachCreateMandateCall.Request:
            return DigioEnachCreateMandateCall.Request(
                customer_identifier=self.customer_identifier,
                auth_mode=self.auth_mode,
                mandate_type=self.mandate_type,
                corporate_config_id=self.corporate_config_id,
                mandate_data=self.mandate_data,
                **self.kwargs
            )

        def to_dict(self) -> Dict[str, Any]:
            return {
                "customer_identifier": self.customer_identifier,
                "auth_mode": self.auth_mode.value,
                "mandate_type": self.mandate_type,
                "corporate_config_id": self.corporate_config_id,
                "mandate_data": self.mandate_data.to_dict(),
                "notify_customer": self.notify_customer
            }

    class Response:
        def __init__(
                self,
                id: str,
                mandate_id: str,
                state: CurrentStateOfMandate,
                type: MandateType,
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
        def from_digio(cls, response: DigioEnachCreateMandateCall.Response):
            return cls(
                id=response.id,
                mandate_id=response.mandate_id,
                state=response.state,
                type=response.type,
                bank_details=response.bank_details,
                created_at=response.created_at,
                mode=response.mode,
                service_provider_details=response.service_provider_details,
            )

        def to_dict(self) -> Dict[str, Any]:
            return {
                "id": self.id,
                "mandate_id": self.mandate_id,
                "state": self.state.value,
                "type": self.type.value,
                "bank_details": self.bank_details.to_dict(),
                "created_at": self.created_at.isoformat(),
                "mode": self.mode.value,
                "service_provider_details": self.service_provider_details.to_dict(),
            }
    
    def __init__(
        self,
        request: Request,
        response: Optional[Response],
        raw_response: Optional[dict],
        meta: CallMeta,
        info: CallInfo,
        provider: EnachProviders,
        helpers: ApiResponseHelpers
    ):
        default_meta = CallMeta(
            error_message="Enach API call failed",
            success_message="Enach API call executed successfully"
        )
        default_info = CallInfo(status_code=500)
        self.request = request
        self.response = response
        self.raw_response = raw_response
        self.meta = default_meta if meta is None else CallMeta.from_dict(
            MiscUtils.merge_nested_dicts(
                default_meta.to_dict(), meta.to_dict())
        )
        self.info = default_info if info is None else CallInfo.from_dict(
            MiscUtils.merge_nested_dicts(
                default_info.to_dict(), info.to_dict())
        )
        self.provider = provider
        self.helpers = ApiResponseHelpers() if helpers is None else helpers

    @classmethod
    def from_digio(cls,call: DigioEnachCreateMandateCall, response: DigioEnachCreateMandateCall.Response):
        return cls(
            request=call.request,
            response=EnachCreateMandateCall.Response.from_digio(call.response),
            raw_response=call.raw_response,
            meta=call.meta,
            info=call.info,
            provider=EnachProviders.DIGIO,
            helpers=call.helpers
        )

    def response_data(self, body_field_validations: List[BodyFieldValidation] = []) -> ResponseData:
            
            return ResponseData(
                request=DictWithConfig(
                    d=self.request.to_dict(),
                    config=DictConfig(
                        key_replacements=[
                            *BodyFieldValidation.get_replacements(body_field_validations)
                        ]
                    )
                ),
                features=DictWithConfig(
                    d=self.response.to_dict()
                ),
                raw_response=DictWithConfig(
                    d=self.raw_response
                ),
                helpers=self.helpers,
                vendor=self.provider.value
            )
    


class EnachGetMandateCall:
    class Request:
        def __init__(
            self,
            mandate_id: str
        ) -> None:
            self.mandate_id = mandate_id

        def for_digio(self) -> DigioEnachCreateMandateCall.Request:
            return DigioEnachCreateMandateCall.Request(
                mandate_id=self.mandate_id
            )
        
        def to_dict(self) -> Dict[str, str]:
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
        def from_digio(cls, response: DigioEnachGetMandateDetails.Response):
            return cls(
                id=response.id,
                mandate_id=response.mandate_id,
                state=response.state,
                type=response.type,
                bank_details=response.bank_details,
                mandate_details=response.mandate_details,
                umrn=response.umrn,
                created_at=response.created_at,
                updated_at=response.updated_at,
                mode=response.mode,
                service_provider_details=response.service_provider_details,
            )
        
        def to_dict(self) -> Dict[str, Any]:
            return {
                "id": self.id,
                "mandate_id": self.mandate_id,
                "state": self.state.value,
                "type": self.type.value,
                "bank_details": self.bank_details.to_dict(),
                "mandate_details": self.mandate_details.to_dict(),
                "umrn": self.umrn,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "mode": self.mode.value,
                "service_provider_details": self.service_provider_details.to_dict(),
            }
        
    def __init__(
        self,
        request: Request,
        response: Optional[Response],
        raw_response: Optional[dict],
        meta: CallMeta,
        info: CallInfo,
        provider: EnachProviders,
        helpers: ApiResponseHelpers
    ):
        default_meta = CallMeta(
            error_message="Enach get mandate API call failed",
            success_message="Enach get mandate API call executed successfully"
        )
        default_info = CallInfo(status_code=500)
        self.request = request
        self.response = response
        self.raw_response = raw_response
        self.meta = default_meta if meta is None else CallMeta.from_dict(
            MiscUtils.merge_nested_dicts(
                default_meta.to_dict(), meta.to_dict())
        )
        self.info = default_info if info is None else CallInfo.from_dict(
            MiscUtils.merge_nested_dicts(
                default_info.to_dict(), info.to_dict())
        )
        self.provider = provider
        self.helpers = ApiResponseHelpers() if helpers is None else helpers

    @classmethod
    def from_digio(cls, call: DigioEnachGetMandateDetails, response: DigioEnachGetMandateDetails.Response):
            return cls(
                request=call.request,
                response=EnachGetMandateCall.Response.from_digio(call.response),
                raw_response=call.raw_response,
                meta=call.meta,
                info=call.info,
                provider=EnachProviders.DIGIO,
                helpers=call.helpers
            )
        
    def response_data(self, body_field_validations: List[BodyFieldValidation] = []) -> ResponseData:
            return ResponseData(
                request=DictWithConfig(
                    d=self.request.to_dict(),
                    config=DictConfig(
                        key_replacements=[
                            *BodyFieldValidation.get_replacements(body_field_validations)
                        ]
                    )
                ),
                features=DictWithConfig(
                    d=self.response.to_dict()
                ),
                raw_response=DictWithConfig(
                    d=self.raw_response
                ),
                helpers=self.helpers,
                vendor=self.provider.value
            )
