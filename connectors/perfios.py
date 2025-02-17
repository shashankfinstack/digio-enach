from typing import Dict, List, Optional
from helpers.error import Error
from helpers.finance.bankstatement_perfios.providers.perfios import PerfiosBankStatementPerfiosCall
from helpers.finance.bankstatement_transaction.providers.perfios import \
    PerfiosBankStatementTransactionCall
from utils.perfios import PerfiosUtils
import json


class PerfiosConnector:
    @staticmethod
    def bankstatement_retrieve(
            call: PerfiosBankStatementPerfiosCall
    ):
        perfios_date = PerfiosUtils.get_date()
        payload = ""
        url = call.context.request_context.url
        if not url:
            raise Error("Perfios url not found", 400)
        host = PerfiosUtils.get_host(url)
        path = f"{call.context.request_context.path}"
        signature = PerfiosUtils.get_signature(
            "GET",
            path,
            payload,
            host,
            perfios_date
        ).decode()
        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
            "Host": host,
            "X-Perfios-Algorithm": PerfiosUtils.PERFIOS_ALGO,
            "X-Perfios-Content-Sha256": PerfiosUtils.calculate_checksum(payload),
            "X-Perfios-Date": perfios_date,
            "X-Perfios-Signature": signature,
            "X-Perfios-Signed-Headers": PerfiosUtils.SIGNED_HEADERS,
        }
        call.context.request_context.headers = headers
        response = call.context.call()
        response_json = response.json()
        call.raw_response = {"response": response_json}
        if "error" in response_json and response_json["error"] is not None:
            error = response_json["error"]
            error_message_details: Optional[List[Dict[str, str]]] = error.get(
                "details"
            )
            error_message_concated: Optional[str] = ""
            if error_message_details:
                for error_message_detail in error_message_details:
                    error_message = error_message_detail.get("message")
                    if error_message:
                        error_message_concated = f"{error_message_concated}; {error_message}"
            else:
                error_message_concated = error.get("message")
            call_error_message = call.meta.error_message\
                if call.meta.error_message else ""
            raise Error(
                error_message_concated
                if error_message_concated else call_error_message,
                response.status_code,
            )
        call_response = PerfiosBankStatementPerfiosCall.Response.from_dict(
            response_json
        )
        call.response = call_response
        call.info.set_status_code(response.status_code)
        if not call.response:
            raise Error(
                call.meta.error_message if call.meta.error_message else "",
                400
            )
        else:
            return call

    @staticmethod
    def bankstatement_transaction(
            call: PerfiosBankStatementTransactionCall
    ) -> PerfiosBankStatementTransactionCall:
        perfios_date = PerfiosUtils.get_date()
        perfios_date = "20191125T123214Z"
        payload = call.request.to_dict()
        url = call.context.request_context.url
        if not url:
            raise Error("Perfios url not found", 400)
        host = PerfiosUtils.get_host(url)
        signature = PerfiosUtils.get_signature(
            "POST",
            f"{call.context.request_context.path}",
            payload,
            host,
            perfios_date
        ).decode()

        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
            "Host": host,
            "X-Perfios-Algorithm": PerfiosUtils.PERFIOS_ALGO,
            "X-Perfios-Content-Sha256": PerfiosUtils.calculate_checksum(
                json.dumps(payload)
            ),
            "X-Perfios-Date": perfios_date,
            "X-Perfios-Signature": signature,
            "X-Perfios-Signed-Headers": PerfiosUtils.SIGNED_HEADERS,
        }

        call.context.request_context.headers = headers
        response = call.context.call()
        response_json = response.json()
        call.raw_response = response_json
        if "error" in response_json and response_json["error"] is not None:
            error = response_json["error"]
            error_message_details: Optional[List[Dict[str, str]]] = error.get(
                "details"
            )
            error_message_concated: Optional[str] = ""
            if error_message_details:
                for error_message_detail in error_message_details:
                    error_message = error_message_detail.get("message")
                    if error_message:
                        if len(error_message_concated) > 0:
                            error_message_concated = f"{error_message_concated}; {error_message}"
                        else:
                            error_message_concated = error_message
            else:
                error_message_concated = error.get("message")
            call_error_message = call.meta.error_message\
                if call.meta.error_message else ""
            raise Error(
                error_message_concated
                if error_message_concated else call_error_message,
                response.status_code,
            )
        call_response = PerfiosBankStatementTransactionCall.Response.from_dict(
            response_json, call.request.txn_id
        )

        call.response = call_response
        if not call.response:
            raise Error(
                call.meta.error_message if call.meta.error_message else "",
                400
            )
        else:
            return call
