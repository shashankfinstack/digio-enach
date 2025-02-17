
import requests
from typing import Optional
from helpers.okyc.aadhaar import PichainOkycAadhaarInitiateCall, PichainOkycAadhaarSubmitCall
from helpers.common import CallInfo
from utils.misc import MiscUtils
from helpers.error import Error, ErrorAdditionalInfo


class PichainConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map pichain {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )

    def offline_aadhaar_initiate(request_body: PichainOkycAadhaarInitiateCall.Request) -> PichainOkycAadhaarInitiateCall:
        pichain_okyc_aadhaar_initiate_call = PichainOkycAadhaarInitiateCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        pichain_okyc_aadhaar_initiate_call.context.request_context.json = {
            "aadhaar_no": pichain_okyc_aadhaar_initiate_call.request.aadhaar_number
        }
        post_response = pichain_okyc_aadhaar_initiate_call.context.call()
        pichain_okyc_aadhaar_initiate_call.info.set_status_code(
            post_response.status_code)
        if pichain_okyc_aadhaar_initiate_call.info.success:
            pichain_okyc_aadhaar_initiate_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            try:
                pichain_okyc_aadhaar_initiate_call.response = PichainOkycAadhaarInitiateCall.Response(
                    **response_body)
            except Exception:
                raise PichainConnector.Errors.MAPPING_ERROR("okyc aadhaar intiate")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"])
            pichain_okyc_aadhaar_initiate_call.meta.error_message = pichain_okyc_aadhaar_initiate_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            pichain_okyc_aadhaar_initiate_call)
        return pichain_okyc_aadhaar_initiate_call

    def offline_aadhaar_submit(request_body: PichainOkycAadhaarSubmitCall.Request) -> PichainOkycAadhaarSubmitCall:
        pichain_okyc_aadhaar_submit_call = PichainOkycAadhaarSubmitCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        pichain_okyc_aadhaar_submit_call.context.request_context.json = {
             "aadhaar_otp": pichain_okyc_aadhaar_submit_call.request.aadhaar_otp,
            "reference_id": request_body.reference_id
        }
        post_response = pichain_okyc_aadhaar_submit_call.context.call()
        pichain_okyc_aadhaar_submit_call.info.set_status_code(
            post_response.status_code)
        if pichain_okyc_aadhaar_submit_call.info.success:
            pichain_okyc_aadhaar_submit_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["data"]
            try:
                pichain_okyc_aadhaar_submit_call.response = PichainOkycAadhaarSubmitCall.Response(
                    **response_body)
            except Exception:
                raise PichainConnector.Errors.MAPPING_ERROR("okyc aadhaar submit")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"])
            pichain_okyc_aadhaar_submit_call.meta.error_message = pichain_okyc_aadhaar_submit_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            pichain_okyc_aadhaar_submit_call)
        return pichain_okyc_aadhaar_submit_call