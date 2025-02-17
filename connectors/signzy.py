from __future__ import annotations
from typing import Optional
import requests
from helpers.identity_object import IdentityObject
from utils.signzy import SignzyUtils
from utils.misc import MiscUtils
from utils.logger import logger
from helpers.error import Error, ErrorAdditionalInfo
from utils.secret import SecretUtils
from helpers.okyc.aadhaar import (
    SignzyOkycAadhaarInitiateCall,
    SignzyOkycAadhaarSubmitCall,
)
from helpers.finance.bankstatement import SignzyFinanceBankStatementCall
from helpers.finance.gstin import SignzyFinanceGstinCall
from helpers.kyc.pan import SignzyKycPanCall
from helpers.kyc.driver_license import SignzyKycDriverLicenseCall
from helpers.kyc.aadhaar import SignzyKycAadhaarCall
from helpers.ocr.passport import SignzyOcrPassportCall
from helpers.ocr.pan import SignzyOcrPanCall
from helpers.kyc.voter import SignzyKycVoterCall
from helpers.asset.vehicle import SignzyAssetVehicleCall
from helpers.esign.aadhaar import SignzyEsignAadhaarCall
from helpers.common import CallInfo

VERIFY_AADHAAR_ASYNC_TASK = "verifyAadhaarAsyncId"
EXTRACT_AADHAAR_TASK = "autoRecognition"
VEHICLE_DETAILED_SEARCH_TASK = "detailedSearch"
VEHICLE_BASIC_SEARCH_TASK = "basicSearch"


class SignzyConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map signzy {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                ),
            )

    @staticmethod
    def kyc_aadhaar(
        request_body: SignzyKycAadhaarCall.Request,
        identity_id: str,
        identity_access_token: str,
    ) -> SignzyKycAadhaarCall:
        signzy_kyc_aadhaar_call = SignzyKycAadhaarCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_kyc_aadhaar_call.context.request_context.json = {
            "service": "Identity",
            "itemId": identity_id,
            "task": "autoRecognition",
            "accessToken": identity_access_token,
            "essentials": {},
        }
        post_response = signzy_kyc_aadhaar_call.context.call()
        signzy_kyc_aadhaar_call.info.set_status_code(post_response.status_code)
        if signzy_kyc_aadhaar_call.info.success:
            try:
                signzy_kyc_aadhaar_call.raw_response = post_response.json()
                response_body = post_response.json()
                response_body = MiscUtils.get_value_from_dictionary(
                    response_body, ["response", "result", "summary"]
                )
                # Setting the relavent part of the response object to be the response_body
                if response_body is None:
                    raise Error(msg="No data from source", status_code=500)
                del response_body["dateOfBirth"]
                signzy_kyc_aadhaar_call.response = SignzyKycAadhaarCall.Response(
                    **response_body
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("kyc aadhaar")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_kyc_aadhaar_call.meta.error_message = (
                signzy_kyc_aadhaar_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_kyc_aadhaar_call)
        return signzy_kyc_aadhaar_call

    @staticmethod
    def ocr_passport(
        request_body: SignzyOcrPassportCall.Request,
        identity_id: str,
        identity_access_token: str,
    ) -> SignzyOcrPassportCall:
        signzy_ocr_passport_call = SignzyOcrPassportCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_ocr_passport_call.context.request_context.json = {
            "service": "Identity",
            "itemId": identity_id,
            "task": "autoRecognition",
            "accessToken": identity_access_token,
            "essentials": {},
        }
        post_response = signzy_ocr_passport_call.context.call()
        signzy_ocr_passport_call.info.set_status_code(post_response.status_code)
        if signzy_ocr_passport_call.info.success:
            try:
                signzy_ocr_passport_call.raw_response = post_response.json()
                response_body = post_response.json()
                response_body = MiscUtils.get_value_from_dictionary(
                    response_body, ["response", "result", "summary"]
                )
                # Setting the relavent part of the response object to be the response_body
                if response_body is None:
                    raise Error(msg="No data from source", status_code=500)
                logger.info(f"Json Response: {response_body}")
                signzy_ocr_passport_call.response = SignzyOcrPassportCall.Response(
                    **response_body
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("ocr passport")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_ocr_passport_call.meta.error_message = (
                signzy_ocr_passport_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_ocr_passport_call)
        return signzy_ocr_passport_call

    @staticmethod
    def ocr_pan(
        request_body: SignzyOcrPanCall.Request,
        identity_id: str,
        identity_access_token: str,
    ) -> SignzyOcrPanCall:
        signzy_ocr_pan_call = SignzyOcrPanCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_ocr_pan_call.context.request_context.json = {
            "service": "Identity",
            "itemId": identity_id,
            "task": "autoRecognition",
            "accessToken": identity_access_token,
            "essentials": {},
        }
        post_response = signzy_ocr_pan_call.context.call()
        signzy_ocr_pan_call.info.set_status_code(post_response.status_code)
        if signzy_ocr_pan_call.info.success:
            try:
                signzy_ocr_pan_call.raw_response = post_response.json()
                response_body = post_response.json()
                response_body = MiscUtils.get_value_from_dictionary(
                    response_body, ["response", "result", "summary"]
                )
                # Setting the relavent part of the response object to be the response_body
                if response_body is None:
                    raise Error(msg="No data from source", status_code=500)
                logger.info(f"Json Response: {response_body}")
                signzy_ocr_pan_call.response = SignzyOcrPanCall.Response(
                    **response_body
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("ocr pan")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_ocr_pan_call.meta.error_message = (
                signzy_ocr_pan_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_ocr_pan_call)
        return signzy_ocr_pan_call

    @staticmethod
    def get_identity_object(document_type: str, images: list = []):
        """Gets the identity object from signzy"""
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        SIGNZY_DEFAULT_BASE_URL = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_DEFAULT_BASE_URL
        )
        request_url = f"{SIGNZY_DEFAULT_BASE_URL}/api/v2/patrons/{SIGNZY_PATREON_ID}/identities"
        headers = SignzyUtils.get_default_header()
        request_body = SignzyUtils.get_identity_request_body(
            document_type=document_type,
            images=images,
        )
        logger.info(
            f"Request URL: {request_url}\nRequest Body: {request_body}\nRequest Headers: {headers}"
        )
        post_response = requests.post(
            url=request_url, headers=headers, data=request_body
        )
        logger.info(f"Json Response: {post_response.json()}")
        response_body = post_response.json()
        if "error" in response_body.keys() and response_body["error"]:
            return IdentityObject(
                document_type=document_type,
                id=None,
                access_token=None,
                image_urls=None,
            )
        identity_object = IdentityObject(
            document_type=document_type,
            id=response_body["id"],
            access_token=response_body["accessToken"],
            image_urls=images,
        )
        return identity_object

    @staticmethod
    def get_login_response():
        try:
            signzy_login_credentials = {
                "username": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_USERNAME
                ),
                "password": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_PASSWORD
                ),
            }
            request_url = SignzyUtils.get_url("patrons/login")
            logger.info(
                f"Request URL: {request_url}\nRequest Body: {signzy_login_credentials}\nRequest Headers: {{}}"
            )
            post_response = requests.post(
                url=request_url, data=signzy_login_credentials, headers={}
            )
            logger.info(f"Json Response: {post_response.json()}")
            login_object = post_response.json()
            return login_object
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def get_esign_login_response():
        try:
            signzy_login_credentials = {
                "username": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_ESIGN_USERNAME
                ),
                "password": SecretUtils.get_secret_value(
                    SecretUtils.SECRETS.SIGNZY_ESIGN_PASSWORD
                ),
            }
            request_url = SignzyUtils.get_esign_url("login")
            logger.info(
                f"Request URL: {request_url}\nRequest Body: {signzy_login_credentials}\nRequest Headers: {{}}"
            )
            post_response = requests.post(
                url=request_url, data=signzy_login_credentials, headers={}
            )
            logger.info(f"Json Response: {post_response.json()}")
            login_object = post_response.json()
            return login_object
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def vehicle_detailed(
        request_body: SignzyAssetVehicleCall.Request,
    ) -> SignzyAssetVehicleCall:
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        signzy_asset_vehicle_call = SignzyAssetVehicleCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_asset_vehicle_call.context.request_context.url = (
            signzy_asset_vehicle_call.context.request_context.url.format(
                SIGNZY_PATREON_ID
            )
        )
        signzy_asset_vehicle_call.context.request_context.json = {
            "task": "detailedSearch",
            "essentials": {"vehicleNumber": request_body.vehicle_number},
        }
        post_response = signzy_asset_vehicle_call.context.call()
        signzy_asset_vehicle_call.info.set_status_code(post_response.status_code)
        if signzy_asset_vehicle_call.info.success:
            signzy_asset_vehicle_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["result"]
            try:
                signzy_asset_vehicle_call.response = (
                    SignzyAssetVehicleCall.Response.from_raw_response(response_body)
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("asset vehicle")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_asset_vehicle_call.meta.error_message = (
                signzy_asset_vehicle_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_asset_vehicle_call)
        return signzy_asset_vehicle_call

    @staticmethod
    def extract_bank_statement(
        request_body: SignzyFinanceBankStatementCall.Request,
    ) -> SignzyFinanceBankStatementCall:
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        signzy_finance_bank_statement_call = SignzyFinanceBankStatementCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_finance_bank_statement_call.context.request_context.url = (
            signzy_finance_bank_statement_call.context.request_context.url.format(
                SIGNZY_PATREON_ID
            )
        )
        post_response = signzy_finance_bank_statement_call.context.call()
        signzy_finance_bank_statement_call.info.set_status_code(
            post_response.status_code
        )
        if signzy_finance_bank_statement_call.info.success:
            signzy_finance_bank_statement_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["result"]
            try:
                signzy_finance_bank_statement_call.response = (
                    SignzyFinanceBankStatementCall.Response(**response_body)
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("bank statement")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_finance_bank_statement_call.meta.error_message = (
                signzy_finance_bank_statement_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_finance_bank_statement_call)
        return signzy_finance_bank_statement_call

    @staticmethod
    def kyc_pan(request_body: SignzyKycPanCall.Request) -> SignzyKycPanCall:
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        signzy_kyc_pan_call = SignzyKycPanCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_kyc_pan_call.context.request_context.url = (
            signzy_kyc_pan_call.context.request_context.url.format(SIGNZY_PATREON_ID)
        )
        signzy_kyc_pan_call.context.request_context.json = {
            "task": ["1"],
            "essentials": {
                "number": signzy_kyc_pan_call.request.pan_number,
            },
        }
        post_response = signzy_kyc_pan_call.context.call()
        signzy_kyc_pan_call.info.set_status_code(post_response.status_code)
        if signzy_kyc_pan_call.info.success:
            signzy_kyc_pan_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["result"]
            try:
                signzy_kyc_pan_call.response = SignzyKycPanCall.Response(
                    **response_body
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("kyc pan")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_kyc_pan_call.meta.error_message = (
                signzy_kyc_pan_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_kyc_pan_call)
        return signzy_kyc_pan_call

    @staticmethod
    def finance_gstin(
        request_body: SignzyFinanceGstinCall.Request,
    ) -> SignzyFinanceGstinCall:
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        signzy_finance_gstin_call = SignzyFinanceGstinCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_finance_gstin_call.context.request_context.url = (
            signzy_finance_gstin_call.context.request_context.url.format(
                SIGNZY_PATREON_ID
            )
        )
        post_response = signzy_finance_gstin_call.context.call()
        signzy_finance_gstin_call.info.set_status_code(post_response.status_code)
        if signzy_finance_gstin_call.info.success:
            signzy_finance_gstin_call.raw_response = post_response.json()
            try:
                signzy_finance_gstin_call.response = (
                    SignzyFinanceGstinCall.Response.from_raw_response(
                        post_response.json()
                    )
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("finance gstin")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_finance_gstin_call.meta.error_message = (
                signzy_finance_gstin_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_finance_gstin_call)
        return signzy_finance_gstin_call

    def esign_aadhaar(
        request_body: SignzyEsignAadhaarCall.Request,
    ) -> SignzyEsignAadhaarCall:
        SIGNZY_ESIGN_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_ESIGN_PATREON_ID
        )
        signzy_esign_aadhaar_call = SignzyEsignAadhaarCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_esign_aadhaar_call.context.request_context.url = (
            signzy_esign_aadhaar_call.context.request_context.url.format(
                SIGNZY_ESIGN_PATREON_ID
            )
        )
        signzy_esign_aadhaar_call.context.request_context.json = {
            "task": "url",
            "inputFile": request_body.document_url,
            "name": request_body.options.name,
            "signatureType": "aadhaaresign",
            "provider": request_body.options.provider.value,
            "callbackUrl": request_body.options.callback_url,
            "signatures": [
                {
                    "pageNo": signature.page_nos,
                    "signaturePosition": [
                        position.value for position in signature.positions
                    ],
                    "height": signature.height,
                    "width": signature.width,
                    "x-coordinate": signature.x_coordinates,
                    "y-coordinate": signature.y_coordinates,
                }
                for signature in request_body.options.signatures
            ],
        }
        if request_body.options.redirect_url:
            signzy_esign_aadhaar_call.context.request_context.json["redirectUrl"] = (
                request_body.options.redirect_url
            )
        if request_body.options.multi_pages:
            signzy_esign_aadhaar_call.context.request_context.json["multiPages"] = (
                request_body.options.multi_pages
            )
        if request_body.options.page_number:
            signzy_esign_aadhaar_call.context.request_context.json["pageNo"] = (
                request_body.options.page_number
            )
        post_response = signzy_esign_aadhaar_call.context.call()
        signzy_esign_aadhaar_call.info.set_status_code(post_response.status_code)
        if signzy_esign_aadhaar_call.info.success:
            signzy_esign_aadhaar_call.raw_response = post_response.json()
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_esign_aadhaar_call.meta.error_message = (
                signzy_esign_aadhaar_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_esign_aadhaar_call)
        return signzy_esign_aadhaar_call

    def offline_aadhaar_initiate(
        request_body: SignzyOkycAadhaarInitiateCall.Request,
    ) -> SignzyOkycAadhaarInitiateCall:
        signzy_okyc_aadhaar_initiate_call = SignzyOkycAadhaarInitiateCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_okyc_aadhaar_initiate_call.context.request_context.json = {
            "aadhaarNumber": request_body.aadhaar_number
        }
        post_response = signzy_okyc_aadhaar_initiate_call.context.call()
        signzy_okyc_aadhaar_initiate_call.info.set_status_code(
            post_response.status_code
        )
        if signzy_okyc_aadhaar_initiate_call.info.success:
            signzy_okyc_aadhaar_initiate_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["data"]
            try:
                signzy_okyc_aadhaar_initiate_call.response = (
                    SignzyOkycAadhaarInitiateCall.Response(**response_body)
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("okyc aadhaar intiate")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_okyc_aadhaar_initiate_call.meta.error_message = (
                signzy_okyc_aadhaar_initiate_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_okyc_aadhaar_initiate_call)
        return signzy_okyc_aadhaar_initiate_call

    def offline_aadhaar_submit(
        request_body: SignzyOkycAadhaarSubmitCall.Request,
    ) -> SignzyOkycAadhaarSubmitCall:
        signzy_okyc_aadhaar_submit_call = SignzyOkycAadhaarSubmitCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_okyc_aadhaar_submit_call.context.request_context.json = {
            "requestId": request_body.reference_id,
            "otp": request_body.aadhaar_otp,
        }
        post_response = signzy_okyc_aadhaar_submit_call.context.call()
        response_body = post_response.json()
        # Check internal status code
        internal_status_code = response_body.get("statusCode")
        if internal_status_code is not None and internal_status_code != 200:
            signzy_okyc_aadhaar_submit_call.info.set_status_code(internal_status_code)
            signzy_okyc_aadhaar_submit_call.meta.error_message = response_body.get(
                "message"
            )
        final_status_code = (
            internal_status_code
            if post_response.status_code == 200 and internal_status_code is not None
            else post_response.status_code
        )
        signzy_okyc_aadhaar_submit_call.info.set_status_code(final_status_code)
        if signzy_okyc_aadhaar_submit_call.info.success is True:
            signzy_okyc_aadhaar_submit_call.raw_response = post_response.json()
            response_data_body: dict = post_response.json()["data"]
            if signzy_okyc_aadhaar_submit_call.info.success is True:
                try:
                    signzy_okyc_aadhaar_submit_call.response = (
                        SignzyOkycAadhaarSubmitCall.Response(**response_data_body)
                    )
                except Exception:
                    raise SignzyConnector.Errors.MAPPING_ERROR("okyc aadhaar submit")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_okyc_aadhaar_submit_call.meta.error_message = (
                signzy_okyc_aadhaar_submit_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_okyc_aadhaar_submit_call)
        return signzy_okyc_aadhaar_submit_call

    def kyc_voter(request_body: SignzyKycVoterCall.Request) -> SignzyKycVoterCall:
        SIGNZY_PATREON_ID = SecretUtils.get_secret_value(
            SecretUtils.SECRETS.SIGNZY_PATREON_ID
        )
        signzy_kyc_voter_call = SignzyKycVoterCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_kyc_voter_call.context.request_context.url = (
            signzy_kyc_voter_call.context.request_context.url.format(SIGNZY_PATREON_ID)
        )
        signzy_kyc_voter_call.context.request_context.json = {
            "essentials": {
                "epicNumber": signzy_kyc_voter_call.request.epic_number,
            }
        }
        post_response = signzy_kyc_voter_call.context.call()
        signzy_kyc_voter_call.info.set_status_code(post_response.status_code)
        if signzy_kyc_voter_call.info.success:
            signzy_kyc_voter_call.raw_response = post_response.json()
            response_body: dict = post_response.json()["result"]
            try:
                response_body["epic_number"] = post_response.json()["essentials"].get(
                    "epicNumber"
                )
                signzy_kyc_voter_call.response = SignzyKycVoterCall.Response(
                    **response_body
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("kyc voter")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_kyc_voter_call.meta.error_message = (
                signzy_kyc_voter_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_kyc_voter_call)
        return signzy_kyc_voter_call

    def kyc_driver_license(
        request_body: SignzyKycDriverLicenseCall.Request,
        identity_id: str,
        identity_access_token: str,
    ) -> SignzyKycDriverLicenseCall:
        signzy_kyc_driver_license_call = SignzyKycDriverLicenseCall(
            request=request_body, response=None, info=CallInfo(status_code=500)
        )
        signzy_kyc_driver_license_call.context.request_context.json = {
            "service": "Identity",
            "itemId": identity_id,
            "task": "fetch",
            "accessToken": identity_access_token,
            "essentials": {
                "number": signzy_kyc_driver_license_call.request.number,
                "dob": (
                    MiscUtils.parse_date_to_format(
                        signzy_kyc_driver_license_call.request.dob
                    )
                    if signzy_kyc_driver_license_call.request.dob
                    else None
                ),
            },
        }
        post_response = signzy_kyc_driver_license_call.context.call()
        signzy_kyc_driver_license_call.info.set_status_code(post_response.status_code)
        if signzy_kyc_driver_license_call.info.success:
            try:
                signzy_kyc_driver_license_call.raw_response = post_response.json()
                response_body = post_response.json()
                response_body = MiscUtils.get_value_from_dictionary(
                    response_body, ["response", "result"]
                )
                # Setting the relavent part of the response object to be the response_body
                if response_body is None:
                    raise Error(msg="No data from source", status_code=500)
                logger.info(f"Json Response: {response_body}")
                signzy_kyc_driver_license_call.response = (
                    SignzyKycDriverLicenseCall.Response(**response_body)
                )
            except Exception:
                raise SignzyConnector.Errors.MAPPING_ERROR("kyc driver license")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"]
            )
            signzy_kyc_driver_license_call.meta.error_message = (
                signzy_kyc_driver_license_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(signzy_kyc_driver_license_call)
        return signzy_kyc_driver_license_call
