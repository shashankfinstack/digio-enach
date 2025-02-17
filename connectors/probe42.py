from __future__ import annotations
from flask import json
from helpers.finance.llp_basic_details import Probe42FinanceLlpBasicDetailsCall
from helpers.finance.company_search import Probe42FinanceCompanySearchCall
from helpers.error import Error
from helpers.common import CallInfo
from helpers.finance.company_basic_details import Probe42FinanceCompanyBasicDetailsCall
from helpers.finance.company_mca_update import Probe42FinanceCompanyMcaUpdateCall
from helpers.finance.llp_mca_update import Probe42FinanceLlpMcaUpdateCall
from helpers.finance.company_mca import Probe42FinanceCompanyMcaCall
from helpers.finance.llp_mca import Probe42FinanceLlpMcaCall
from helpers.error import Error, ErrorAdditionalInfo
from utils.probe42 import Probe42Utils
from utils.logger import request_logger, response_logger
from utils.misc import MiscUtils
import requests


class Probe42Connector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map probe42 {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )

    @staticmethod
    def finance_company_mca(request_body: Probe42FinanceCompanyMcaCall.Request) -> Probe42FinanceCompanyMcaCall:
        probe42_finance_company_mca_call = Probe42FinanceCompanyMcaCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_company_mca_call.context.request_context.url = probe42_finance_company_mca_call.context.request_context.url.format(
            request_body.cin_or_pan)
        if request_body.is_pan:
            probe42_finance_company_mca_call.context.request_context.url = probe42_finance_company_mca_call.context.request_context.url + "?identifier_type=PAN"
        response = probe42_finance_company_mca_call.context.call()
        probe42_finance_company_mca_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            probe42_finance_company_mca_call.raw_response = response.json()
            response_body = response.json()
            try:
                probe42_finance_company_mca_call.response = Probe42FinanceCompanyMcaCall.Response(
                    **response_body["data"])
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "company mca")
        else:
            response_error = response.json()
            probe42_finance_company_mca_call.meta.error_message = response_error.get(
                "message", probe42_finance_company_mca_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_company_mca_call)
        return probe42_finance_company_mca_call

    @staticmethod
    def finance_llp_mca(request_body: Probe42FinanceLlpMcaCall.Request) -> Probe42FinanceLlpMcaCall:
        probe42_finance_llp_mca_call = Probe42FinanceLlpMcaCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_llp_mca_call.context.request_context.url = probe42_finance_llp_mca_call.context.request_context.url.format(
            request_body.llpin_or_pan)
        if request_body.is_pan:
            probe42_finance_llp_mca_call.context.request_context.url = probe42_finance_llp_mca_call.context.request_context.url + "?identifier_type=PAN"
        response = probe42_finance_llp_mca_call.context.call()
        probe42_finance_llp_mca_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            probe42_finance_llp_mca_call.raw_response = response.json()
            response_body = response.json()
            try:
                probe42_finance_llp_mca_call.response = Probe42FinanceLlpMcaCall.Response(
                    **response_body["data"])
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "llp mca")
        else:
            response_error = response.json()
            probe42_finance_llp_mca_call.meta.error_message = response_error.get(
                "message", probe42_finance_llp_mca_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_llp_mca_call)
        return probe42_finance_llp_mca_call

    @staticmethod
    def company_basic_details(request_body: Probe42FinanceCompanyBasicDetailsCall.Request) -> Probe42FinanceCompanyBasicDetailsCall:
        probe42_finance_company_basic_details_call = Probe42FinanceCompanyBasicDetailsCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_company_basic_details_call.context.request_context.url = probe42_finance_company_basic_details_call.context.request_context.url.format(
            request_body.cin_or_pan)
        if request_body.is_pan:
            probe42_finance_company_basic_details_call.context.request_context.url = probe42_finance_company_basic_details_call.context.request_context.url + "?identifier_type=PAN"
        response = probe42_finance_company_basic_details_call.context.call()
        probe42_finance_company_basic_details_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            probe42_finance_company_basic_details_call.raw_response = response.json()
            response_body = response.json()
            try:
                probe42_finance_company_basic_details_call.response = Probe42FinanceCompanyBasicDetailsCall.Response(
                    **response_body["data"])
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "company basic details")
        else:
            response_error = response.json()
            probe42_finance_company_basic_details_call.meta.error_message = response_error.get(
                "message", probe42_finance_company_basic_details_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_company_basic_details_call)
        return probe42_finance_company_basic_details_call

    @staticmethod
    def llp_basic_details(request_body: Probe42FinanceLlpBasicDetailsCall.Request) -> Probe42FinanceLlpBasicDetailsCall:
        probe42_finance_llp_basic_details_call = Probe42FinanceLlpBasicDetailsCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_llp_basic_details_call.context.request_context.url = probe42_finance_llp_basic_details_call.context.request_context.url.format(
            request_body.llpin_or_pan)
        if request_body.is_pan:
            probe42_finance_llp_basic_details_call.context.request_context.url = probe42_finance_llp_basic_details_call.context.request_context.url + "?identifier_type=PAN"
        response = probe42_finance_llp_basic_details_call.context.call()
        probe42_finance_llp_basic_details_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            probe42_finance_llp_basic_details_call.raw_response = response.json()
            response_body = response.json()
            try:
                probe42_finance_llp_basic_details_call.response = Probe42FinanceLlpBasicDetailsCall.Response(
                    **response_body["data"])
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "llp basic details")
        else:
            response_error = response.json()
            probe42_finance_llp_basic_details_call.meta.error_message = response_error.get(
                "message", probe42_finance_llp_basic_details_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_llp_basic_details_call)
        return probe42_finance_llp_basic_details_call

    @staticmethod
    def company_search(request_body: Probe42FinanceCompanySearchCall.Request) -> Probe42FinanceCompanySearchCall:
        probe42_finance_company_search_call = Probe42FinanceCompanySearchCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_company_search_call.context.request_context.params = {
            "filters": json.dumps({"nameStartsWith": request_body.name_starts_with}),
            "limit": request_body.limit
        }
        response = probe42_finance_company_search_call.context.call()
        probe42_finance_company_search_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            response_body = response.json()
            probe42_finance_company_search_call.raw_response = response_body
            try:
                probe42_finance_company_search_call.response = Probe42FinanceCompanySearchCall.Response.from_raw_response(
                    response_body)
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "finance company search")
        else:
            response_error = response.json()
            probe42_finance_company_search_call.meta.error_message = response_error.get(
                "message", probe42_finance_company_search_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_company_search_call)
        return probe42_finance_company_search_call

    @staticmethod
    def company_mca_update(request_body: Probe42FinanceCompanyMcaUpdateCall.Request) -> Probe42FinanceCompanyMcaUpdateCall:
        probe42_finance_company_mca_update_call = Probe42FinanceCompanyMcaUpdateCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_company_mca_update_call.context.request_context.url = probe42_finance_company_mca_update_call.context.request_context.url.format(
            request_body.cin_or_pan)
        if request_body.is_pan:
            probe42_finance_company_mca_update_call.context.request_context.url = probe42_finance_company_mca_update_call.context.request_context.url + "?identifier_type=PAN"
        if request_body.postback_url is not None:
            probe42_finance_company_mca_update_call.context.request_context.url = probe42_finance_company_mca_update_call.context.request_context.url + \
                f"?postback_url={request_body.postback_url}"
        response = probe42_finance_company_mca_update_call.context.call()
        probe42_finance_company_mca_update_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            response_body = response.json()
            try:
                probe42_finance_company_mca_update_call.response = Probe42FinanceCompanyMcaUpdateCall.Response(
                    **response_body["data"])
            except:
                raise Probe42Connector.Errors.MAPPING_ERROR(
                    "company mca update")
        else:
            response_error = response.json()
            probe42_finance_company_mca_update_call.meta.error_message = response_error.get(
                "message", probe42_finance_company_mca_update_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_company_mca_update_call)
        return probe42_finance_company_mca_update_call

    @staticmethod
    def llp_mca_update(request_body: Probe42FinanceLlpMcaUpdateCall.Request) -> Probe42FinanceLlpMcaUpdateCall:
        probe42_finance_llp_mca_update_call = Probe42FinanceLlpMcaUpdateCall(
            response=None,
            request=request_body,
            info=CallInfo(status_code=500)
        )
        probe42_finance_llp_mca_update_call.context.request_context.url = probe42_finance_llp_mca_update_call.context.request_context.url.format(
            request_body.llpin_or_pan)
        if request_body.is_pan:
            probe42_finance_llp_mca_update_call.context.request_context.url = probe42_finance_llp_mca_update_call.context.request_context.url + "?identifier_type=PAN"
        if request_body.postback_url is not None:
            probe42_finance_llp_mca_update_call.context.request_context.url = probe42_finance_llp_mca_update_call.context.request_context.url + \
                f"?postback_url={request_body.postback_url}"
        response = probe42_finance_llp_mca_update_call.context.call()
        probe42_finance_llp_mca_update_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            response_body = response.json()
            try:
                probe42_finance_llp_mca_update_call.response = Probe42FinanceLlpMcaUpdateCall.Response(
                    **response_body["data"])
            except Exception:
                raise Probe42Connector.Errors.MAPPING_ERROR("llp mca update")
        else:
            response_error = response.json()
            probe42_finance_llp_mca_update_call.meta.error_message = response_error.get(
                "message", probe42_finance_llp_mca_update_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            probe42_finance_llp_mca_update_call)
        return probe42_finance_llp_mca_update_call

    @staticmethod
    def company_reference_document(cin_or_pan_number: str, doc_type: str, is_pan: bool):
        request_path = f"/companies/{cin_or_pan_number}/reference-document?type={doc_type}"
        if is_pan:
            request_path += "&identifier_type=PAN"
        request_url, request_method = Probe42Utils.get_post_url(
            request_path, is_file=True)
        request_url = request_url.replace('_pro', '_reports')
        request_headers = Probe42Utils.get_default_headers()
        request_body = None
        request_logger(str(request_url.strip()), request_method, request_headers,
                       request_body, None, None)
        api_response = requests.request(method=str(request_method),
                                        url=request_url, headers=request_headers)
        if api_response.status_code != 200:
            response_logger(response=api_response)
        success = api_response.status_code >= 200 and api_response.status_code < 300
        if not success:
            raise Error(
                msg=api_response.json().get("message"),
                status_code=api_response.status_code
            )
        if "Content-type" in api_response.headers and\
                api_response.headers["Content-type"] == "application/octet-stream":
            return (api_response.content, api_response.status_code)
        return (api_response.json(), api_response.status_code)

    @staticmethod
    def llps_reference_document(llpin_or_pan_number: str, doc_type: str, is_pan: bool):
        request_path = f"/llps/{llpin_or_pan_number}/reference-document?type={doc_type}"
        if is_pan:
            request_path += "&identifier_type=PAN"
        request_url, request_method = Probe42Utils.get_post_url(
            request_path, is_file=True)
        request_headers = Probe42Utils.get_default_headers()
        request_url = request_url.replace('_pro', '_reports')
        request_body = None
        request_logger(str(request_url.strip()), request_method, request_headers,
                       request_body, None, None)
        api_response = requests.request(method=str(request_method),
                                        url=request_url, headers=request_headers)
        if api_response.status_code != 200:
            response_logger(response=api_response)
        success = api_response.status_code >= 200 and api_response.status_code < 300
        if not success:
            raise Error(
                msg=api_response.json().get("message"),
                status_code=api_response.status_code
            )
        if "Content-type" in api_response.headers and\
                api_response.headers["Content-type"] == "application/octet-stream":
            return (api_response.content, api_response.status_code)
        return (api_response.json(), api_response.status_code)

    @staticmethod
    def company_reference_document_by_id(cin_or_pan_number: str, doc_id: str, is_pan: bool):
        request_path = f"/companies/{cin_or_pan_number}/reference-document-by-id?doc-id={doc_id}"
        if is_pan:
            request_path += "&identifier_type=PAN"
        request_url, request_method = Probe42Utils.get_post_url(
            request_path, is_file=True)
        request_url = request_url.replace('_pro', '_reports')
        request_headers = Probe42Utils.get_default_headers()
        request_body = None
        request_logger(str(request_url.strip()), request_method, request_headers,
                       request_body, None, None)
        api_response = requests.request(method=str(request_method),
                                        url=request_url, headers=request_headers)
        if api_response.status_code != 200:
            response_logger(response=api_response)
        success = api_response.status_code >= 200 and api_response.status_code < 300
        if not success:
            raise Error(
                msg=api_response.json().get("message"),
                status_code=api_response.status_code
            )
        if "Content-type" in api_response.headers and\
                api_response.headers["Content-type"] == "application/octet-stream":
            return (api_response.content, api_response.status_code)
        return (api_response.json(), api_response.status_code)

    @staticmethod
    def llps_reference_document_by_id(llpin_or_pan_number: str, doc_id: str, is_pan: bool):
        request_path = f"/llps/{llpin_or_pan_number}/reference-document-by-id?doc-id={doc_id}"
        if is_pan:
            request_path += "&identifier_type=PAN"
        request_url, request_method = Probe42Utils.get_post_url(
            request_path, is_file=True)
        request_url = request_url.replace('_pro', '_reports')
        request_headers = Probe42Utils.get_default_headers()
        request_body = None
        request_logger(str(request_url.strip()), request_method, request_headers,
                       request_body, None, None)
        api_response = requests.request(method=str(request_method),
                                        url=request_url, headers=request_headers)
        if api_response.status_code != 200:
            response_logger(response=api_response)
        success = api_response.status_code >= 200 and api_response.status_code < 300
        if not success:
            raise Error(
                msg=api_response.json().get("message"),
                status_code=api_response.status_code
            )
        if "Content-type" in api_response.headers and\
                api_response.headers["Content-type"] == "application/octet-stream":
            return (api_response.content, api_response.status_code)
        return (api_response.json(), api_response.status_code)
