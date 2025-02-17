from typing import Optional
from helpers.common.call import CallInfo
from helpers.error import Error, ErrorAdditionalInfo
from helpers.okyc.aadhaar.providers.decentro import OkycAadhaarDecentroInitiateCall, OkycAadhaarDecentroSubmitCall
from utils.misc import MiscUtils
from typing import Tuple, Optional
from helpers.error import Error, ErrorAdditionalInfo
from utils.misc import MiscUtils
from helpers.common import CallInfo
from helpers.finance.gstin import DecentroFinanceGstinCall
from helpers.kyc.driver_license import DecentroKycDriverLicenseCall
from helpers.kyc.pan import DecentroKycPanCall
import uuid


class DecentroConnector:

    class Errors:
        @staticmethod
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map decentro {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                ),
            )

    @staticmethod
    def offline_aadhaar_initiate(
        request_body: OkycAadhaarDecentroInitiateCall.Request,
    ) -> OkycAadhaarDecentroInitiateCall:
        decentro_okyc_aadhaar_initiate_call = OkycAadhaarDecentroInitiateCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        post_response = decentro_okyc_aadhaar_initiate_call.context.call()
        decentro_okyc_aadhaar_initiate_call.info.set_status_code(
            post_response.status_code
        )
        if decentro_okyc_aadhaar_initiate_call.info.success:
            decentro_okyc_aadhaar_initiate_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            try:
                decentro_okyc_aadhaar_initiate_call.response = (
                    OkycAadhaarDecentroInitiateCall.Response.from_dict(
                        response_body,
                        request_body.aadhaar_number,
                    )
                )
            except Exception:
                raise DecentroConnector.Errors.MAPPING_ERROR(
                    "okyc aadhaar intiate")
        else:
            error_message: Optional[str] = post_response.json().get("message")
            decentro_okyc_aadhaar_initiate_call.meta.error_message = (
                decentro_okyc_aadhaar_initiate_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(decentro_okyc_aadhaar_initiate_call)
        return decentro_okyc_aadhaar_initiate_call

    @staticmethod
    def offline_aadhaar_submit(
        request_body: OkycAadhaarDecentroSubmitCall.Request,
    ) -> OkycAadhaarDecentroSubmitCall:
        decentro_okyc_aadhaar_submit_call = OkycAadhaarDecentroSubmitCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        post_response = decentro_okyc_aadhaar_submit_call.context.call()
        response_body = post_response.json()
        # Check internal status code
        internal_status_code = response_body.get("statusCode")
        if internal_status_code is not None and internal_status_code != 200:
            decentro_okyc_aadhaar_submit_call.info.set_status_code(
                internal_status_code)
            decentro_okyc_aadhaar_submit_call.meta.error_message = response_body.get(
                "message"
            )
        final_status_code = (
            internal_status_code
            if post_response.status_code == 200 and internal_status_code is not None
            else post_response.status_code
        )
        decentro_okyc_aadhaar_submit_call.info.set_status_code(
            final_status_code)
        if decentro_okyc_aadhaar_submit_call.info.success is True:
            decentro_okyc_aadhaar_submit_call.raw_response = post_response.json()
            response_data_body: dict = post_response.json()
            if decentro_okyc_aadhaar_submit_call.info.success is True:
                try:
                    decentro_okyc_aadhaar_submit_call.response = (
                        OkycAadhaarDecentroSubmitCall.Response.from_dict(
                            response_data_body)
                    )
                except Exception:
                    raise DecentroConnector.Errors.MAPPING_ERROR(
                        "okyc aadhaar submit")
        else:
            error_message: Optional[str] = post_response.json().get("message")
            decentro_okyc_aadhaar_submit_call.meta.error_message = (
                decentro_okyc_aadhaar_submit_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(decentro_okyc_aadhaar_submit_call)
        return decentro_okyc_aadhaar_submit_call

    @staticmethod
    def finance_gstin(request_body: DecentroFinanceGstinCall.Request) -> DecentroFinanceGstinCall:
        decentro_finance_gstin_call = DecentroFinanceGstinCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        decentro_finance_gstin_call.context.request_context.json = {
            "consent": "Y",
            "consent_purpose": "For GSTIN_DETAILED information",
            "reference_id": str(uuid.uuid4()),
            "document_type": "GSTIN_DETAILED",
            "id_number": request_body.gstin_number if request_body.gstin_number is not None else None
        }
        post_response = decentro_finance_gstin_call.context.call()
        decentro_finance_gstin_call.info.set_status_code(
            post_response.status_code)
        if decentro_finance_gstin_call.info.success:
            decentro_finance_gstin_call.raw_response = post_response.json()
            try:
                decentro_finance_gstin_call.response = (
                    DecentroFinanceGstinCall.Response.from_raw_response(
                        post_response.json()
                    )
                )
            except Exception:
                raise DecentroConnector.Errors.MAPPING_ERROR("finance gstin")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            decentro_finance_gstin_call.meta.error_message = decentro_finance_gstin_call.meta.error_message if error_message is None else error_message
        return decentro_finance_gstin_call
    
    def kyc_driver_license(request_body: DecentroKycDriverLicenseCall.Request) -> DecentroKycDriverLicenseCall:
        decentro_kyc_driver_license_call = DecentroKycDriverLicenseCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        decentro_kyc_driver_license_call.context.request_context.json = {
            "consent" : "Y",
            "consent_purpose": "For DRIVER LICENSE information",
            "reference_id": str(uuid.uuid4()),
            "document_type": "DRIVING_LICENSE",
            "dob": str(request_body.date_of_birth),
            "id_number": request_body.driver_license_no if request_body.driver_license_no is not None else None
        }
        post_response = decentro_kyc_driver_license_call.context.call()
        decentro_kyc_driver_license_call.info.set_status_code(
            post_response.status_code)
        if decentro_kyc_driver_license_call.info.success:
            decentro_kyc_driver_license_call.raw_response = post_response.json()
            try:
                decentro_kyc_driver_license_call.response = (
                    DecentroKycDriverLicenseCall.Response.from_raw_response(
                        post_response.json()
                    )
                )
            except Exception:
                raise DecentroConnector.Errors.MAPPING_ERROR("kyc driver license")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            decentro_kyc_driver_license_call.meta.error_message = decentro_kyc_driver_license_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            decentro_kyc_driver_license_call)
        return decentro_kyc_driver_license_call
    
    def kyc_pan(request_body: DecentroKycPanCall.Request) -> DecentroKycPanCall:
        decentro_kyc_driver_license_call = DecentroKycPanCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        decentro_kyc_driver_license_call.context.request_context.json = {
            "consent" : request_body.consent if request_body.consent and request_body.consent is not None else "Y",
            "consent_purpose": "For PAN DETAILED information",
            "reference_id": str(uuid.uuid4()),
            "document_type": "PAN_DETAILED",
            "id_number": request_body.pan_number if request_body.pan_number is not None else None
        }
        post_response = decentro_kyc_driver_license_call.context.call()
        decentro_kyc_driver_license_call.info.set_status_code(
            post_response.status_code)
        if decentro_kyc_driver_license_call.info.success:
            if MiscUtils.get_value_from_dict(post_response.json(),['kycStatus']) == "FAILURE":
                error = MiscUtils.get_value_from_dict(post_response.json(), ['error'])
                raise Error(MiscUtils.get_value_from_dict(error, "message"), 500)
            decentro_kyc_driver_license_call.raw_response = post_response.json()
            try:
                decentro_kyc_driver_license_call.response = (
                    DecentroKycPanCall.Response.from_raw_response(
                        post_response.json()
                    )
                )
            except Exception:
                raise DecentroConnector.Errors.MAPPING_ERROR("kyc pan")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            decentro_kyc_driver_license_call.meta.error_message = decentro_kyc_driver_license_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            decentro_kyc_driver_license_call)
        return decentro_kyc_driver_license_call

