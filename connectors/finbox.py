from helpers.finance.bankstatement import FinboxFinanceBankStatementUploadCall, FinboxFinanceBankStatementTransactionCall, FinboxFinanceBankStatementReportCall
from helpers.common import CallInfo
from helpers.error import Error, ErrorAdditionalInfo
from utils.misc import MiscUtils


class FinboxConnector:

    class Errors:
        @staticmethod
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map finbox {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )

    @staticmethod
    def upload_statement(request_body: FinboxFinanceBankStatementUploadCall.Request) -> FinboxFinanceBankStatementUploadCall:
        finbox_finance_bank_statement_upload_call = FinboxFinanceBankStatementUploadCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        finbox_finance_bank_statement_upload_call.context.request_context.data = {
            "file_url": finbox_finance_bank_statement_upload_call.request.bank_statement_url,
            "link_id": finbox_finance_bank_statement_upload_call.request.link_id,
            "pdf_password": finbox_finance_bank_statement_upload_call.request.pdf_password
        }
        response = finbox_finance_bank_statement_upload_call.context.call()
        finbox_finance_bank_statement_upload_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            response_body = response.json()
            try:
                finbox_finance_bank_statement_upload_call.response = FinboxFinanceBankStatementUploadCall.Response(
                    **response_body)
            except Exception:
                raise FinboxConnector.Errors.MAPPING_ERROR(
                    "bank statement upload")
        else:
            response_error = response.json()
            original_file_name_from_url = MiscUtils.original_file_name_from_url(finbox_finance_bank_statement_upload_call.request.bank_statement_url)
            custom_error_message = "(" + original_file_name_from_url + ") "  
            finbox_finance_bank_error_message = response_error.get(
                "message", finbox_finance_bank_statement_upload_call.meta.error_message)
            finbox_finance_bank_statement_upload_call.meta.error_message  = custom_error_message + finbox_finance_bank_error_message
        MiscUtils.raise_error_from_call(
            finbox_finance_bank_statement_upload_call)
        return finbox_finance_bank_statement_upload_call

    @staticmethod
    def get_entity_transactions(request_body: FinboxFinanceBankStatementTransactionCall.Request, entity_id: str) -> FinboxFinanceBankStatementTransactionCall:
        finbox_finance_bank_statement_transaction_call = FinboxFinanceBankStatementTransactionCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        finbox_finance_bank_statement_transaction_call.context.request_context.url = finbox_finance_bank_statement_transaction_call.context.request_context.url.format(
            entity_id)
        response = finbox_finance_bank_statement_transaction_call.context.call()
        finbox_finance_bank_statement_transaction_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            finbox_finance_bank_statement_transaction_call.raw_response = response.json()
            response_body = response.json()
            try:
                finbox_finance_bank_statement_transaction_call.response = FinboxFinanceBankStatementTransactionCall.Response(
                    **response_body)
            except Exception:
                raise FinboxConnector.Errors.MAPPING_ERROR(
                    "bank statement transaction")
        else:
            response_error = response.json()
            finbox_finance_bank_statement_transaction_call.meta.error_message = response_error.get(
                "message", finbox_finance_bank_statement_transaction_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            finbox_finance_bank_statement_transaction_call)
        return finbox_finance_bank_statement_transaction_call

    def get_entity_report(entity_id: str) -> FinboxFinanceBankStatementReportCall:
        finbox_finance_bank_statement_report_call = FinboxFinanceBankStatementReportCall(
            request={"entity_id": entity_id},
            response=None,
            info=CallInfo(status_code=500)
        )
        response = finbox_finance_bank_statement_report_call.context.call()
        finbox_finance_bank_statement_report_call.info.set_status_code(
            response.status_code)
        success = response.status_code >= 200 and response.status_code < 300
        if success:
            finbox_finance_bank_statement_report_call.raw_response = response.json()
            response_body = response.json()
            try:
                finbox_finance_bank_statement_report_call.response = FinboxFinanceBankStatementReportCall.Response(
                    **response_body)
            except Exception:
                raise FinboxConnector.Errors.MAPPING_ERROR(
                    "bank statement transaction")
        else:
            response_error = response.json()
            finbox_finance_bank_statement_report_call.meta.error_message = response_error.get(
                "message", finbox_finance_bank_statement_report_call.meta.error_message)
        MiscUtils.raise_error_from_call(
            finbox_finance_bank_statement_report_call)
        return finbox_finance_bank_statement_report_call
