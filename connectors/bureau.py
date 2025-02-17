from typing import Any, Dict, Optional

import requests
from helpers.common import CallInfo, ResidenceAddress, KarzaInternalStatusCodeAuthentication, KarzaInternalStatusCodeOCR, KarzaInternalStatusCodeLiveliness, KarzaInternalStatusCodePhone
from helpers.error import Error, ErrorAdditionalInfo
from helpers.finance.bank_verification import KarzaBankAccountVerificationCall
from helpers.kyc.driver_license import BureauKycDriverLicenseCall
from helpers.kyc.e_aadhaar import KarzaKycEAadhaarCall
from helpers.kyc.liveness import KarzaKycLivenessCall
from helpers.kyc.aadhaar_mobile_link import KarzaKycAadhaarMobileLinkCall
from helpers.kyc.facematch import KarzaKycFaceMatchCall, KycFaceMatchCall
from helpers.kyc.pan import KarzaKycPanCall
from helpers.kyc.pan_basic import KarzaBasicPanAuthenticationCall
from helpers.kyc.passport import KarzaPassportCall
from helpers.kyc.voter import KarzaKycVoterCall, BureauKycVoterCall
from helpers.misc.name_match import KarzaMiscNameMatchCall
from helpers.ocr.driver_license import KarzaOcrDriverLicenseCall
from helpers.ocr.pan import BureauOcrPanCall, OcrPanCall
from helpers.ocr.aadhaar import KarzaOcrAadhaarCall, OcrAadhaarCall, BureauOcrAadhaarCall
from helpers.ocr.passport import OcrPassportCall, BureauOcrPassportCall
from helpers.ocr.voter import BureauOcrVoterCall
from helpers.asset.vehicle import BureauAssetVehicleCall
from helpers.ocr.voter import KarzaOcrVoterCall
from helpers.okyc.aadhaar import (KarzaOkycAadhaarInitiateCall,
                                  KarzaOkycAadhaarSubmitCall)
from helpers.okyc.phone import (KarzaOkycPhoneInitiateCall,
                                  KarzaOkycPhoneSubmitCall, KarzaOkycPhoneStatusCall)
from helpers.utility_assessment.electricity_bill import \
    KarzaElectricityBillCall
from helpers.utility_assessment.LPG import KarzaLPGAuthenticationCall
from utils.misc import MiscUtils
from helpers.common import KarzaDocumentType

class BureauConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map bureau {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )


    @staticmethod
    def ocr_aadhaar(request_body: BureauOcrAadhaarCall.Request)->BureauOcrAadhaarCall:
        bureau_ocr_aadhaar_call = BureauOcrAadhaarCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_ocr_aadhaar_call.context.request_context.json = {
            "docType" : "aadhaar",
            "countryCode" : "IND",
            "frontUrl" : request_body.frontUrl,
            "backUrl": request_body.backUrl,
        }
        post_response = bureau_ocr_aadhaar_call.context.call()
        bureau_ocr_aadhaar_call.info.set_status_code(
            post_response.status_code)
        if bureau_ocr_aadhaar_call.info.success:
            bureau_ocr_aadhaar_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_ocr_aadhaar_call.response = BureauOcrAadhaarCall.Response(
                        **response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("ocr aadhaar")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_ocr_aadhaar_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_ocr_aadhaar_call)
        return bureau_ocr_aadhaar_call
    

    @staticmethod
    def ocr_pan(request_body: BureauOcrPanCall.Request) -> BureauOcrPanCall:
        bureau_ocr_pan_call = BureauOcrPanCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_ocr_pan_call.context.request_context.json = {
            "docType" : "pan",
            "countryCode" : "IND",
            "frontUrl" : request_body.pan_image_url,
        }
        post_response = bureau_ocr_pan_call.context.call()
        bureau_ocr_pan_call.info.set_status_code(
            post_response.status_code)
        if bureau_ocr_pan_call.info.success:
            bureau_ocr_pan_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_ocr_pan_call.response = BureauOcrPanCall.Response(**response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("ocr pan")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_ocr_pan_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_ocr_pan_call)
        return bureau_ocr_pan_call
    
    @staticmethod
    def kyc_voter(request_body: BureauKycVoterCall.Request) -> BureauKycVoterCall:
        bureau_kyc_voter_call = BureauKycVoterCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_kyc_voter_call.context.request_context.json = {
            "epicNumber" : request_body.epic_number
        }
        post_response = bureau_kyc_voter_call.context.call()
        bureau_kyc_voter_call.info.set_status_code(
            post_response.status_code)
        if bureau_kyc_voter_call.info.success:
            bureau_kyc_voter_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_kyc_voter_call.response = BureauKycVoterCall.Response(**response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("kyc voter")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_kyc_voter_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_kyc_voter_call)
        return bureau_kyc_voter_call
    
    @staticmethod
    def ocr_voter(request_body: BureauOcrVoterCall.Request) -> BureauOcrVoterCall:
        bureau_ocr_voter_call = BureauOcrVoterCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_ocr_voter_call.context.request_context.json = {
            "docType" : "voter",
            "countryCode" : "IND",
            "frontUrl" : request_body.voter_front_url,
            "backUrl" : request_body.voter_back_url
        }
        post_response = bureau_ocr_voter_call.context.call()
        bureau_ocr_voter_call.info.set_status_code(
            post_response.status_code)
        if bureau_ocr_voter_call.info.success:
            bureau_ocr_voter_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_ocr_voter_call.response = BureauOcrVoterCall.Response(**response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("ocr voter")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_ocr_voter_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_ocr_voter_call)
        return bureau_ocr_voter_call
    
    @staticmethod
    def ocr_passport(request_body: BureauOcrPassportCall.Request) -> BureauOcrPassportCall:
        bureau_ocr_passport_call = BureauOcrPassportCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_ocr_passport_call.context.request_context.json = {
            "docType" : "passport",
            "countryCode" : "IND",
            "frontUrl" : request_body.front_image_url,
            "backUrl" : request_body.back_image_url
        }
        post_response = bureau_ocr_passport_call.context.call()
        bureau_ocr_passport_call.info.set_status_code(
            post_response.status_code)
        if bureau_ocr_passport_call.info.success:
            bureau_ocr_passport_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_ocr_passport_call.response = BureauOcrPassportCall.Response(**response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("ocr voter")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_ocr_passport_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_ocr_passport_call)
        return bureau_ocr_passport_call
    
    @staticmethod
    def kyc_driver_license(request_body: BureauKycDriverLicenseCall.Request) -> BureauKycDriverLicenseCall:
        bureau_kyc_driver_license_call = BureauKycDriverLicenseCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        bureau_kyc_driver_license_call.context.request_context.json = {
            "docNumber" : request_body.driver_license_no,
            "dob": request_body.date_of_birth
        }
        post_response = bureau_kyc_driver_license_call.context.call()
        bureau_kyc_driver_license_call.info.set_status_code(
            post_response.status_code)
        if bureau_kyc_driver_license_call.info.success:
            bureau_kyc_driver_license_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_kyc_driver_license_call.response = BureauKycDriverLicenseCall.Response.from_raw_response(response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("kyc driver license")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_kyc_driver_license_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_kyc_driver_license_call)
        return bureau_kyc_driver_license_call
    
    @staticmethod
    def asset_vehicle(request_body: BureauAssetVehicleCall.Request) -> BureauAssetVehicleCall:
        bureau_asset_vehicle_call = BureauAssetVehicleCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = bureau_asset_vehicle_call.context.call()
        bureau_asset_vehicle_call.info.set_status_code(
            post_response.status_code)
        if bureau_asset_vehicle_call.info.success:
            bureau_asset_vehicle_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 200:
                # Success
                response_body = post_response.json()
                try:
                    bureau_asset_vehicle_call.response = BureauAssetVehicleCall.Response(**response_body)
                except Exception as error:
                    raise BureauConnector.Errors.MAPPING_ERROR("asset vehicle")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error","description"]
            )
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "message"])
            if MiscUtils.return_null_if_empty(error_message) is None:
                error_message = MiscUtils.get_value_from_dictionary(post_response.json(), ["error", "errorCode"])
            if error_message is not None:
                bureau_asset_vehicle_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(bureau_asset_vehicle_call)
        return bureau_asset_vehicle_call