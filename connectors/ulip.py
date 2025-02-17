from helpers.finance.ewaybill import FinanceEwaybillCall
from helpers.finance.ewaybill.providers.ulip import FinanceEwaybillUlipCall
from helpers.finance.mca_basic import UlipFinanceMcaBasicCall
from helpers.finance.fastag import UlipFinanceFastagCall
from utils.secret import SecretUtils
from utils.logger import logger
import requests
from utils.misc import MiscUtils
from helpers.common import DEFAULT_ULIP_LOGIN_HEADERS
import json
from typing import Optional
from helpers.error import Error, ErrorAdditionalInfo


class UlipConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map ulip {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                ),
            )

    @staticmethod
    def finance_ewaybill(ewb_number: str):
        request = FinanceEwaybillUlipCall.Request(ewb_number)
        ulip_finance_ewaybill_call = FinanceEwaybillUlipCall(request=request)
        raw_response = ulip_finance_ewaybill_call.context.call()
        ulip_finance_ewaybill_call.info.set_status_code(raw_response.status_code)
        if ulip_finance_ewaybill_call.info.success:
            try:
                response_body = raw_response.json()
                ulip_finance_ewaybill_call.raw_response = raw_response.json()
                ulip_finance_ewaybill_call.response = (
                    FinanceEwaybillUlipCall.Response.from_dict(raw_response.json())
                )
            except Exception:
                raise UlipConnector.Errors.MAPPING_ERROR("finance ewaybill")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                raw_response.json(), ["message"]
            )
            ulip_finance_ewaybill_call.meta.error_message = (
                ulip_finance_ewaybill_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(ulip_finance_ewaybill_call)
        return FinanceEwaybillCall.from_ulip(ulip_finance_ewaybill_call)

    def get_login_response():
        try:
            ulip_login_credentials = {
                "username": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.ULIP_USERNAME
                ),
                "password": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.ULIP_PASSWORD
                ),
            }
            json_ulip_login_credentials = json.dumps(ulip_login_credentials)
            request_url = f"{SecretUtils.get_secret_value(SecretUtils.SECRETS.ULIP_BASE_URL)}/v1.0.0/user/login"
            ulip_headers = DEFAULT_ULIP_LOGIN_HEADERS
            logger.info(
                f"Request URL: {request_url}\nRequest Body: {json_ulip_login_credentials}\nRequest Headers: {ulip_headers}"
            )
            post_response = requests.post(
                url=request_url, data=json_ulip_login_credentials, headers=ulip_headers
            )
            login_object = post_response.json()
            return login_object
        except Exception as e:
            logger.error("ulip login error", e)
            return None

    @staticmethod
    def finance_mca_basic(
        request_body: UlipFinanceMcaBasicCall.Request,
    ) -> UlipFinanceMcaBasicCall:
        finance_mca_basic_call = UlipFinanceMcaBasicCall(
            request=request_body, response=None
        )
        post_response = finance_mca_basic_call.context.call()
        finance_mca_basic_call.info.set_status_code(post_response.status_code)
        if finance_mca_basic_call.info.success:
            try:
                response_body = post_response.json()
                finance_mca_basic_call.raw_response = post_response.json()
                # Setting the relavent part of the response object to be the response_body
                logger.info(f"Json Response: {response_body}")
                if (
                    int(response_body.get("code", 0)) >= 200
                    and int(response_body.get("code", 0)) < 300
                ):
                    if (
                        response_body.get("response") is not None
                        and len(response_body.get("response")) > 0
                    ):
                        response_dict: dict = response_body.get("response")[0]
                        if response_dict.get("responseStatus") == "SUCCESS":
                            finance_mca_basic_call.response = (
                                UlipFinanceMcaBasicCall.Response(
                                    **response_dict.get("response")
                                )
                            )
                        else:
                            finance_mca_basic_call.meta.error_message = (
                                response_dict.get("response")["error_description"]
                            )
                            MiscUtils.raise_error_from_call(finance_mca_basic_call)
                else:
                    finance_mca_basic_call.meta.error_message = response_body.get(
                        "message"
                    )
                    MiscUtils.raise_error_from_call(finance_mca_basic_call)
            except Exception:
                raise UlipConnector.Errors.MAPPING_ERROR("finance mca basic")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"]
            )
            finance_mca_basic_call.meta.error_message = (
                finance_mca_basic_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(finance_mca_basic_call)
        return finance_mca_basic_call

    @staticmethod
    def finance_fastag(
        request_body: UlipFinanceFastagCall.Request,
    ) -> UlipFinanceFastagCall:
        finance_fastag_call = UlipFinanceFastagCall(request=request_body, response=None)
        post_response = finance_fastag_call.context.call()
        finance_fastag_call.info.set_status_code(post_response.status_code)
        if finance_fastag_call.info.success:
            try:
                response_body = post_response.json()
                finance_fastag_call.raw_response = post_response.json()
                # Setting the relavent part of the response object to be the response_body
                logger.info(f"Json Response: {response_body}")
                if (
                    int(response_body.get("code", 0)) >= 200
                    and int(response_body.get("code", 0)) < 300
                ):
                    if (
                        response_body.get("response") is not None
                        and len(response_body.get("response")) > 0
                    ):
                        response_dict: dict = response_body.get("response")[0]
                        if response_dict.get("responseStatus") == "SUCCESS":
                            if(MiscUtils.get_value_from_dictionary(response_dict, ["response","vehicle", "errCode"])=="740"):
                                error_message: Optional[str] = "Vehicle number does not exist in FASTAG system"
                                finance_fastag_call.meta.success_message = (
                                    finance_fastag_call.meta.success_message
                                    if error_message is None
                                    else error_message
                                )
                            finance_fastag_call.response = (
                                UlipFinanceFastagCall.Response(
                                    **response_dict.get("response")
                                )
                            )
                else:
                    finance_fastag_call.meta.error_message = response_body.get(
                        "message"
                    )
                    MiscUtils.raise_error_from_call(finance_fastag_call)
            except Exception:
                raise UlipConnector.Errors.MAPPING_ERROR("finance mca basic")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["message"]
            )
            finance_fastag_call.meta.error_message = (
                finance_fastag_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(finance_fastag_call)
        return finance_fastag_call
