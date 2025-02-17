from __future__ import annotations
from typing import Optional
import requests
from helpers.identity_object import IdentityObject
from utils.misc import MiscUtils
from utils.logger import logger
from helpers.error import Error, ErrorAdditionalInfo
from utils.secret import SecretUtils
from helpers.common import CallInfo
from helpers.kyc.pan import KycPanCall, TransbnkKycPanCall
from helpers.finance.gstin import TransbnkFinanceGstinCall
from helpers.kyc.pan_nsdl import TransbnkKycPanNsdlCall

class TransbnkConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map transbnk {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                ),
            )
        
    @staticmethod
    def kyc_pan(request_body: TransbnkKycPanCall.Request) -> TransbnkKycPanCall:
        transbnk_kyc_pan_call = TransbnkKycPanCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = transbnk_kyc_pan_call.context.call()
        transbnk_kyc_pan_call.info.set_status_code(
            post_response.status_code)
        if transbnk_kyc_pan_call.info.success:
            transbnk_kyc_pan_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            code = response_body.get("code")
            if code == 400:
                result = response_body.get("result")
                raise Error(result.get("message"), 400)
            if code == 500:
                result = response_body.get("result")
                raise Error(result.get("error"), 500)
            internal_message = response_body.get("message")
            response_body_data = response_body.get("response")
            transbnk_kyc_pan_call.meta.success_message = internal_message
            try:
                if response_body_data is None:
                    transbnk_kyc_pan_call.response = TransbnkKycPanCall.Response(
                        {})
                else:
                    transbnk_kyc_pan_call.response = TransbnkKycPanCall.Response(
                        **response_body_data)
            except Exception:
                raise TransbnkConnector.Errors.MAPPING_ERROR("kyc pan")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            transbnk_kyc_pan_call.meta.error_message = transbnk_kyc_pan_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            transbnk_kyc_pan_call)
        return 
    
    @staticmethod
    def finance_gstin(request_body: TransbnkFinanceGstinCall.Request) -> TransbnkFinanceGstinCall:
        transbnk_finance_gstin_call = TransbnkFinanceGstinCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = transbnk_finance_gstin_call.context.call()
        transbnk_finance_gstin_call.info.set_status_code(
            post_response.status_code)
        if transbnk_finance_gstin_call.info.success:
            transbnk_finance_gstin_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            code = response_body.get("code")
            if code == 400:
                result = response_body.get("result")
                raise Error(result.get("message"), 400)
            internal_message = response_body.get("message")
            transbnk_finance_gstin_call.meta.success_message = internal_message
            try:
                transbnk_finance_gstin_call.response = (
                    TransbnkFinanceGstinCall.Response.from_raw_response(post_response.json())
                )
            except Exception:
                raise TransbnkConnector.Errors.MAPPING_ERROR("finance gstin")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            transbnk_finance_gstin_call.meta.error_message = transbnk_finance_gstin_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            transbnk_finance_gstin_call)
        return transbnk_finance_gstin_call
    
    @staticmethod
    def pan_nsdl(request_body: TransbnkKycPanNsdlCall.Request) -> TransbnkKycPanNsdlCall:
        transbnk_kyc_pan_nsdl_call = TransbnkKycPanNsdlCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        transbnk_kyc_pan_nsdl_call.context.request_context.json = {
            "Dob": request_body.dob,
            "PanNo": request_body.pan_number,
            "Name": request_body.name
        }
        post_response = transbnk_kyc_pan_nsdl_call.context.call()
        transbnk_kyc_pan_nsdl_call.info.set_status_code(
            post_response.status_code)
        if transbnk_kyc_pan_nsdl_call.info.success:
            transbnk_kyc_pan_nsdl_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            code = response_body.get("code")
            if code == 400:
                result = response_body.get("result")
                raise Error(result.get("message"), 400)
            if code == 500:
                result = response_body.get("result")
                raise Error(result.get("error"), 500)
            internal_message = response_body.get("message")
            response_body_data = response_body.get("response")
            transbnk_kyc_pan_nsdl_call.meta.success_message = internal_message
            try:
                if response_body_data is None:
                    transbnk_kyc_pan_nsdl_call.response = TransbnkKycPanNsdlCall.Response(
                        {})
                else:
                    transbnk_kyc_pan_nsdl_call.response = TransbnkKycPanNsdlCall.Response(
                        **response_body_data)
            except Exception:
                raise TransbnkConnector.Errors.MAPPING_ERROR("kyc pan nsdl")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"])
            transbnk_kyc_pan_nsdl_call.meta.error_message = transbnk_kyc_pan_nsdl_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            transbnk_kyc_pan_nsdl_call)
        return transbnk_kyc_pan_nsdl_call
    
