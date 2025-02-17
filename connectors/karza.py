from typing import Any, Dict, Optional

import requests
from helpers.common import CallInfo, ResidenceAddress, KarzaInternalStatusCodeAuthentication, KarzaInternalStatusCodeOCR, KarzaInternalStatusCodeLiveliness, KarzaInternalStatusCodePhone
from helpers.error import Error, ErrorAdditionalInfo
from helpers.finance.bank_verification import KarzaBankAccountVerificationCall
from helpers.kyc.driver_license import KarzaKycDriverLicenseCall
from helpers.kyc.e_aadhaar import KarzaKycEAadhaarCall
from helpers.kyc.liveness import KarzaKycLivenessCall
from helpers.kyc.aadhaar_mobile_link import KarzaKycAadhaarMobileLinkCall
from helpers.kyc.facematch import KarzaKycFaceMatchCall, KycFaceMatchCall
from helpers.kyc.pan import KarzaKycPanCall
from helpers.kyc.pan_basic import KarzaBasicPanAuthenticationCall
from helpers.kyc.passport import KarzaPassportCall
from helpers.kyc.voter import KarzaKycVoterCall
from helpers.misc.name_match import KarzaMiscNameMatchCall
from helpers.ocr.driver_license import KarzaOcrDriverLicenseCall
from helpers.ocr.pan import KarzaOcrPanCall, OcrPanCall
from helpers.ocr.aadhaar import KarzaOcrAadhaarCall, OcrAadhaarCall
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

class KarzaConnector:

    class Errors:
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map karza {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )


    @staticmethod
    def offline_aadhaar_initiate(
        karza_request: KarzaOkycAadhaarInitiateCall.Request,
    ) -> KarzaOkycAadhaarInitiateCall:
        karza_aadhaar_initiate_call = KarzaOkycAadhaarInitiateCall(
            request=karza_request, response=None
        )

        karza_aadhaar_initiate_call.context.request_context.json = {
            "aadhaarNo": karza_aadhaar_initiate_call.request.aadhaar_number,
            "consent": "Y",
        }

        karza_api_response = karza_aadhaar_initiate_call.context.call()

        karza_aadhaar_initiate_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_aadhaar_initiate_call.info.success:
            response_body = karza_api_response.json()
            karza_aadhaar_initiate_call.raw_response = response_body
            # internal status code from karza, refer api doc
            internal_status_code = response_body["statusCode"]
            if internal_status_code == 101:
                api_message = MiscUtils.get_value_from_dictionary(
                    response_body, ["result", "message"]
                )
                if api_message is None:
                    api_message = response_body["statusMessage"]

                if api_message == "OTP sent to registered mobile number":
                    karza_aadhaar_initiate_call.response = (
                        KarzaOkycAadhaarInitiateCall.Response(
                            request_id=response_body["requestId"]
                        )
                    )
                    karza_aadhaar_initiate_call.meta.success_message = api_message
                else:
                    karza_aadhaar_initiate_call.meta.error_message = api_message
                    karza_aadhaar_initiate_call.info.set_status_code(400)
            else:
                karza_aadhaar_initiate_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_aadhaar_initiate_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_aadhaar_initiate_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_aadhaar_initiate_call)

        return karza_aadhaar_initiate_call


    @staticmethod
    def offline_aadhaar_submit(
        karza_request: KarzaOkycAadhaarSubmitCall.Request,
    ) -> KarzaOkycAadhaarSubmitCall:
        karza_aadhaar_submit_call = KarzaOkycAadhaarSubmitCall(
            request=karza_request,
            response=None,
        )

        karza_aadhaar_submit_call.context.request_context.json = {
            "otp": karza_aadhaar_submit_call.request.otp,
            "aadhaarNo": karza_aadhaar_submit_call.request.aadhaar_number,
            "requestId": karza_aadhaar_submit_call.request.reference_id,
            "consent": "Y",
        }

        karza_api_response = karza_aadhaar_submit_call.context.call()
        karza_aadhaar_submit_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_aadhaar_submit_call.info.success:
            karza_aadhaar_submit_call.raw_response = karza_api_response.json()
            internal_status_code = karza_api_response.json()["statusCode"]
            if internal_status_code == 101:
                response_data = karza_api_response.json()["result"]
                address_data: dict = response_data["dataFromAadhaar"]["address"][
                    "splitAddress"
                ]
                address = ResidenceAddress(
                    house=address_data.get("houseNumber"),
                    street=address_data.get("street"),
                    landmark=address_data.get("landmark"),
                    pincode=address_data.get("pincode"),
                    post_office=address_data.get("postOffice"),
                    sub_district=address_data.get("subdistrict"),
                    district=address_data.get("district"),
                    country=address_data.get("country"),
                    state=address_data.get("state"),
                )

                aadhaar_data = response_data["dataFromAadhaar"]

                karza_aadhaar_submit_call.response = (
                    KarzaOkycAadhaarSubmitCall.Response(
                        address=address,
                        masked_aadhaar_number=aadhaar_data["maskedAadhaarNumber"],
                        name=aadhaar_data["name"],
                        dob=aadhaar_data["dob"],
                        gender=aadhaar_data["gender"],
                        mobile_hash=aadhaar_data["mobileHash"],
                        email_hash=aadhaar_data["emailHash"],
                        profile_image=aadhaar_data["image"],
                        aadhaar_xml_raw=aadhaar_data["file"],
                        share_code=response_data["shareCode"],
                    )
                )
            else:
                karza_aadhaar_submit_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_aadhaar_submit_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_aadhaar_submit_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_aadhaar_submit_call)

        return karza_aadhaar_submit_call

    @staticmethod
    def offline_phone_initiate(
        karza_request: KarzaOkycPhoneInitiateCall.Request,
    ) -> KarzaOkycPhoneInitiateCall:
        karza_phone_initiate_call = KarzaOkycPhoneInitiateCall(
            request=karza_request, response=None
        )

        karza_phone_initiate_call.context.request_context.json = {
            "mobile": karza_phone_initiate_call.request.mobile_number,
            "consent": "y",
        }

        karza_api_response = karza_phone_initiate_call.context.call()

        karza_phone_initiate_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_phone_initiate_call.info.success:
            response_body = karza_api_response.json()
            karza_phone_initiate_call.raw_response = response_body
            # internal status code from karza, refer api doc
            internal_status_code = int(response_body["status-code"])
            if internal_status_code == 101:
                api_message = MiscUtils.get_value_from_dictionary(
                    response_body, ["result", "message"]
                )
                if api_message is None:
                    api_message = response_body["statusMessage"]
                if api_message == "Otp has been sent to your mobile number":
                    karza_phone_initiate_call.response = (
                        KarzaOkycAadhaarInitiateCall.Response(
                            request_id=response_body["request_id"]
                        )
                    )
                    karza_phone_initiate_call.meta.success_message = api_message
                else:
                    karza_phone_initiate_call.meta.error_message = api_message
                    karza_phone_initiate_call.info.set_status_code(400)
            else:
                karza_phone_initiate_call.info.set_status_code(400)
                error_message = error_message = KarzaInternalStatusCodePhone.get(str(internal_status_code)) \
                        or KarzaInternalStatusCodeAuthentication.get(str(internal_status_code)) \
                        or "Unknown Vendor Status Code"
                karza_phone_initiate_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_phone_initiate_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_phone_initiate_call)

        return karza_phone_initiate_call

    @staticmethod
    def offline_phone_status(
        karza_request: KarzaOkycPhoneStatusCall.Request,
    ) -> KarzaOkycPhoneStatusCall:
        karza_phone_status_call = KarzaOkycPhoneStatusCall(
            request=karza_request,
            response=None,
        )
        karza_phone_status_call.context.request_context.json = {
            "otp": karza_phone_status_call.request.mobile_otp,
            "request_id": karza_phone_status_call.request.reference_id
        }
        karza_api_response = karza_phone_status_call.context.call()
        karza_phone_status_call.info.set_status_code(
            karza_api_response.status_code)
        if karza_phone_status_call.info.success:
            karza_phone_status_call.raw_response = karza_api_response.json()
            internal_status_code = int(karza_api_response.json()["status-code"])
            if internal_status_code == 101:
                response_data = karza_api_response.json()["result"]

                karza_phone_status_call.response = (
                    KarzaOkycPhoneStatusCall.Response(
                        sim_details=response_data["sim_details"],
                    )
                )
            else:
                karza_phone_status_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_phone_status_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_phone_status_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(karza_phone_status_call)
        return karza_phone_status_call


    @staticmethod
    def offline_phone_submit(
        karza_request: KarzaOkycPhoneStatusCall.Request,
    ) -> KarzaOkycPhoneSubmitCall:
        karza_phone_submit_call = KarzaOkycPhoneSubmitCall(
            request=karza_request,
            response=None,
        )
        karza_phone_submit_call.context.request_context.json = {
            "request_id": karza_phone_submit_call.request.reference_id,
        }

        karza_api_response = karza_phone_submit_call.context.call()
        karza_phone_submit_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_phone_submit_call.info.success:
            karza_phone_submit_call.raw_response = karza_api_response.json()
            internal_status_code = int(karza_api_response.json()["status-code"])
            if internal_status_code == 101:
                response_data = karza_api_response.json()["result"]
                karza_phone_submit_call.response = (
                    KarzaOkycPhoneSubmitCall.Response(
                        contact= MiscUtils.get_value_from_dict(response_data, "contact", none_accepted=True),
                        device=MiscUtils.get_value_from_dict(response_data, "device", none_accepted=True),
                        history=MiscUtils.get_value_from_dict(response_data, "history", none_accepted=True),
                        identity=MiscUtils.get_value_from_dict(response_data, "identity", none_accepted=True),
                        profile=MiscUtils.get_value_from_dict(response_data, "profile", none_accepted=True),
                        sim_details=MiscUtils.get_value_from_dict(response_data, "sim_details", none_accepted=True)
                    )
                )
            else:
                karza_phone_submit_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_phone_submit_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_phone_submit_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_phone_submit_call)

        return karza_phone_submit_call

    @staticmethod
    def basic_pan_authentication(
        request: KarzaBasicPanAuthenticationCall.Request,
    ) -> KarzaBasicPanAuthenticationCall:
        karza_pan_auth_call = KarzaBasicPanAuthenticationCall(
            request=request, response=None
        )

        karza_pan_auth_call.context.request_context.json = {
            "pan": karza_pan_auth_call.request.pan_number,
            "consent": "Y",
        }

        karza_api_response = karza_pan_auth_call.context.call()

        karza_pan_auth_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_pan_auth_call.info.success:
            karza_pan_auth_call.raw_response = karza_api_response.json()
            response_body = karza_api_response.json()
            internal_status_code = response_body.get("status-code")
            if internal_status_code == "101":
                karza_pan_auth_call.response = KarzaBasicPanAuthenticationCall.Response(
                    name=response_body["result"]["name"],
                    request_id=response_body["request_id"],
                )
            else:
                karza_pan_auth_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_pan_auth_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_pan_auth_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_pan_auth_call)
        return karza_pan_auth_call


    @staticmethod
    def kyc_driver_license(
        request: KarzaKycDriverLicenseCall.Request,
    ) -> KarzaKycDriverLicenseCall:
        karza_kyc_driver_license_call = KarzaKycDriverLicenseCall(
            request=request, response=None
        )

        karza_kyc_driver_license_call.context.request_context.json = {
            "dlNo": karza_kyc_driver_license_call.request.driver_license_no,
            "dob": karza_kyc_driver_license_call.request.date_of_birth,
            "consent": "Y",
        }

        post_response = karza_kyc_driver_license_call.context.call()
        karza_kyc_driver_license_call.info.set_status_code(
            post_response.status_code
        )

        if karza_kyc_driver_license_call.info.success:
            karza_kyc_driver_license_call.raw_response = post_response.json()
            response_body = post_response.json()
            internal_status_code = response_body["statusCode"]
            if internal_status_code == 101:
                try:
                    karza_kyc_driver_license_call.response = (
                        KarzaKycDriverLicenseCall.Response(
                            **response_body
                        )
                    )
                except:
                    raise KarzaConnector.Errors.MAPPING_ERROR(
                        "kyc driver license")
            else:
                karza_kyc_driver_license_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_kyc_driver_license_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_kyc_driver_license_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_kyc_driver_license_call)
        return karza_kyc_driver_license_call


    @staticmethod
    def finance_bank_verification(
        request: KarzaBankAccountVerificationCall.Request,
    ) -> KarzaBankAccountVerificationCall:
        karza_bank_account_verification_call = KarzaBankAccountVerificationCall(
            request=request, response=None
        )

        karza_bank_account_verification_call.context.request_context.json = {
            "ifsc": karza_bank_account_verification_call.request.IFSC,
            "accountNumber": karza_bank_account_verification_call.request.account_number,
            "consent": "Y",
        }

        karza_api_response = karza_bank_account_verification_call.context.call()
        karza_bank_account_verification_call.info.set_status_code(
            karza_api_response.status_code
        )

        if karza_bank_account_verification_call.info.success:
            karza_bank_account_verification_call.raw_response = karza_api_response.json()
            response_body = karza_api_response.json()
            internal_status_code = response_body["statusCode"]
            if internal_status_code == 101:
                response_data = response_body.get(
                    "result").get("data").get("source")
                if isinstance(response_data, list):
                    for entry in response_data:
                        if (
                            isinstance(entry, dict) and
                            entry.get("statusAsPerSource") == "VALID"
                        ):
                            try:
                                entry_data = entry.get("data")
                                karza_bank_account_verification_call.response = (
                                    KarzaBankAccountVerificationCall.Response(
                                        **entry_data
                                    )
                                )
                            except Exception as e:
                                raise KarzaConnector.Errors.MAPPING_ERROR(
                                    "finance bank verification"
                                )
                            break
                        else:
                            try:
                                entry_data = entry.get("data")
                                karza_bank_account_verification_call.meta.error_message = (
                                    entry_data["bankResponse"]
                                )
                                karza_bank_account_verification_call.info.set_status_code(
                                    400)
                            except Exception as e:
                                raise KarzaConnector.Errors.MAPPING_ERROR(
                                    "finance bank verification"
                                )
                            break
            elif "statusMessage" in response_body:
                karza_bank_account_verification_call.meta.error_message = (
                    response_body["statusMessage"]
                )
                karza_bank_account_verification_call.info.set_status_code(
                    400)
            else:
                karza_bank_account_verification_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_bank_account_verification_call.meta.error_message = error_message

        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_bank_account_verification_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_bank_account_verification_call)
        return karza_bank_account_verification_call


    @staticmethod
    def karza_electricity_bill(
        request: KarzaElectricityBillCall.Request,
    ) -> KarzaElectricityBillCall:
        karza_electricity_call = KarzaElectricityBillCall(
            request=request, response=None
        )

        karza_electricity_call.context.request_context.json = {
            "consent": "Y",
            "consumer_id": karza_electricity_call.request.consumer_id,
            "service_provider": karza_electricity_call.request.service_provider,
        }

        karza_api_response = karza_electricity_call.context.call()
        karza_electricity_call.info.set_status_code(
            karza_api_response.status_code)

        if karza_electricity_call.info.success:
            response_body = karza_api_response.json()
            karza_electricity_call.raw_response = response_body
            internal_status_code = response_body["status-code"]
            if internal_status_code == "101":
                response_data = response_body.get("result")
                karza_electricity_call.response = KarzaElectricityBillCall.Response(
                    address=response_data.get("address"),
                    amount_payable=response_data.get("amount_payable"),
                    bill_amount=response_data.get("bill_amount"),
                    bill_due_date=response_data.get("bill_due_date"),
                    bill_date=response_data.get("bill_date"),
                    bill_issue_date=response_data.get("bill_issue_date"),
                    bill_no=response_data.get("bill_no"),
                    consumer_name=response_data.get("consumer_name"),
                    consumer_number=response_data.get("consumer_number"),
                    email_address=response_data.get("email_address"),
                    mobile_number=response_data.get("mobile_number"),
                    total_amount=response_data.get("total_amount"),
                )
            else:
                karza_electricity_call.info.set_status_code(400)
                karza_electricity_call.meta.error_message = "Electricty bill api call failed due to third party vendor"
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_electricity_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_electricity_call)
        return karza_electricity_call


    @staticmethod
    def karza_LPG_authentication(
        request: KarzaLPGAuthenticationCall.Request,
    ) -> KarzaLPGAuthenticationCall:
        karza_lpg_call = KarzaLPGAuthenticationCall(
            request=request, response=None)

        karza_lpg_call.context.request_context.json = {
            "lpg_id": karza_lpg_call.request.lpg_id,
            "consent": "Y",
        }

        karza_api_response = karza_lpg_call.context.call()
        karza_lpg_call.info.set_status_code(karza_api_response.status_code)

        if karza_lpg_call.info.success:
            response_body = karza_api_response.json()
            karza_lpg_call.raw_response = response_body
            internal_status_code = response_body["status-code"]
            if internal_status_code == "101":
                response_data = response_body["result"]
                karza_lpg_call.response = KarzaLPGAuthenticationCall.Response(
                    status=response_data["status"],
                    approximate_subsidy_availed=response_data[
                        "ApproximateSubsidyAvailed"
                    ],
                    subsidized_refill_consumed=response_data[
                        "SubsidizedRefillConsumed"
                    ],
                    pin=response_data["pin"],
                    consumer_email=response_data["ConsumerEmail"],
                    distributor_code=response_data["DistributorCode"],
                    bank_name=response_data["BankName"],
                    IFSC_code=response_data["IFSCCode"],
                    city_town=response_data["city/town"],
                    aadhaar_number=response_data["AadhaarNo"],
                    consumer_contact=response_data["ConsumerContact"],
                    distributor_address=response_data["DistributorAddress"],
                    consumer_name=response_data["ConsumerName"],
                    consumer_number=response_data["ConsumerNo"],
                    distributor_name=response_data["DistributorName"],
                    bank_account_number=response_data["BankAccountNo"],
                    given_up_subsidy=response_data["GivenUpSubsidy"],
                    consumer_address=response_data["ConsumerAddress"],
                    last_booking_date=response_data["LastBookingDate"],
                    total_refill_consumed=response_data["TotalRefillConsumed"],
                )
            else:
                karza_lpg_call.info.set_status_code(400)
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                karza_api_response.json(), ["error"]
            )
            if error_message is not None:
                karza_lpg_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_lpg_call)
        return karza_lpg_call


    @staticmethod
    def passport_kyc(request: KarzaPassportCall.Request):
        karza_passport_call = KarzaPassportCall(request=request)
        request_body: Dict[str, Any] = {
            "consent": "y",
            "fileNo": request.passport_file_number,
            "dob": request.date_of_birth,
        }
        if request.passport_number:
            request_body["passportNo"] = request.passport_number
        if request.date_of_issue:
            request_body["doi"] = request.date_of_issue
        if request.name:
            request_body["name"] = request.name
        if request.case_id:
            request_body["clientData"] = {"caseId": request.case_id}
        karza_passport_call.context.request_context.json = request_body
        karza_passport_response = karza_passport_call.context.call()
        json_response = karza_passport_response.json()
        karza_passport_call.raw_response = json_response
        internal_status_code = json_response["statusCode"]
        if internal_status_code == 101:
            json_response_result = json_response["result"]
            karza_passport_call.response = KarzaPassportCall.Response(
                passport_number=json_response_result["passportNumber"]["passportNumberFromSource"],
                application_date=json_response_result["applicationDate"],
                issue_date=json_response_result["dateOfIssue"]["dispatchedOnFromSource"],
                surname=json_response_result["name"]["surnameFromPassport"],
                name=json_response_result["name"]["nameFromPassport"],
                type_of_application=json_response_result["typeOfApplication"],
            )
            karza_passport_call.info.set_status_code(200)
        else:
            karza_passport_call.info.set_status_code(400)
            error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
            karza_passport_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(karza_passport_call)
        return karza_passport_call


    @staticmethod
    def kyc_eaadhaar(request_body: KarzaKycEAadhaarCall.Request) -> KarzaKycEAadhaarCall:
        karza_kyc_eaadhaar_call = KarzaKycEAadhaarCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        karza_kyc_eaadhaar_call.context.request_context.json = {
            "url": karza_kyc_eaadhaar_call.request.eaadhaar_url,
            "maskAadhaar": karza_kyc_eaadhaar_call.request.mask_aadhaar,
            "hideAadhaar": karza_kyc_eaadhaar_call.request.hide_aadhaar
        }

        post_response = karza_kyc_eaadhaar_call.context.call()
        karza_kyc_eaadhaar_call.info.set_status_code(post_response.status_code)

        if karza_kyc_eaadhaar_call.info.success:
            karza_kyc_eaadhaar_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_kyc_eaadhaar_call.response = KarzaKycEAadhaarCall.Response(
                        **response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("kyc e-aadhaar")
            else:
                karza_kyc_eaadhaar_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_kyc_eaadhaar_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_kyc_eaadhaar_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_kyc_eaadhaar_call)
        return karza_kyc_eaadhaar_call


    @staticmethod
    def ocr_driver_license(request_body: KarzaOcrDriverLicenseCall.Request) -> KarzaOcrDriverLicenseCall:
        karza_ocr_driver_license_call = KarzaOcrDriverLicenseCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        karza_ocr_driver_license_call.context.request_context.json = {
            "url": karza_ocr_driver_license_call.request.driver_license_url,
            "docType": karza_ocr_driver_license_call.request.doc_type
        }

        post_response = karza_ocr_driver_license_call.context.call()
        karza_ocr_driver_license_call.info.set_status_code(
            post_response.status_code)

        if karza_ocr_driver_license_call.info.success:
            karza_ocr_driver_license_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_ocr_driver_license_call.response = KarzaOcrDriverLicenseCall.Response(
                        **response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("kyc e-aadhaar")
            else:
                karza_ocr_driver_license_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_ocr_driver_license_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_ocr_driver_license_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_ocr_driver_license_call)
        return karza_ocr_driver_license_call


    @staticmethod
    def voter_kyc(request: KarzaKycVoterCall.Request):
        karza_voter_call = KarzaKycVoterCall(request=request)
        request_body: Dict[str, Any] = {
            "consent": "y",
            "epicNo": request.epic_number,
        }
        if request.case_id:
            request_body["clientData"] = {"caseId": request.case_id}
        karza_voter_call.context.request_context.json = request_body
        karza_passport_response = karza_voter_call.context.call()
        json_response = karza_passport_response.json()
        karza_voter_call.raw_response = json_response
        internal_status_code = json_response["statusCode"]
        if internal_status_code == 101:
            json_response_result = json_response["result"]
            karza_voter_call.response = KarzaKycVoterCall.Response(
                name=json_response_result["name"],
                relative_name=json_response_result["rlnName"],
                relation_type=json_response_result["rlnType"],
                gender=json_response_result["gender"],
                district=json_response_result["district"],
                assembly_constituency_name=json_response_result["acName"],
                parlimentary_constituency_name=json_response_result["pcName"],
                state=json_response_result["state"],
                epic_number=json_response_result["epicNo"],
                dob=json_response_result["dob"],
                age=json_response_result["age"],
                part_number=json_response_result["partNo"],
                serial_number_of_part=json_response_result["slNoInPart"],
                pooling_booth_address=json_response_result["psName"],
                part_name=json_response_result["partName"],
                last_update=json_response_result["lastUpdate"],
                polling_booth_latitude_longitude=json_response_result["psLatLong"],
                section_number=json_response_result["sectionNo"],
                voter_id=json_response_result["id"],
                assembly_constituency_number=json_response_result["acNo"],
                state_code=json_response_result["stCode"],
                house_number=json_response_result["houseNo"],
                pincode=json_response_result["pin"]
            )
            karza_voter_call.info.set_status_code(200)
        else:
            karza_voter_call.info.set_status_code(400)
            error_message = KarzaInternalStatusCodeAuthentication.get(str(internal_status_code), "Unknown Vendor Status Code")
            karza_voter_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(karza_voter_call)
        return karza_voter_call


    @staticmethod
    def misc_name_match(request_body: KarzaMiscNameMatchCall.Request) -> KarzaMiscNameMatchCall:
        karza_misc_name_match_call = KarzaMiscNameMatchCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        karza_misc_name_match_call.context.request_context.json = {
            "name1": request_body.name_1,
            "name2": request_body.name_2,
            "type": "individual"
        }
        post_response = karza_misc_name_match_call.context.call()
        karza_misc_name_match_call.info.set_status_code(
            post_response.status_code)

        if karza_misc_name_match_call.info.success:
            karza_misc_name_match_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body: dict = post_response.json()
                try:
                    karza_misc_name_match_call.response = KarzaMiscNameMatchCall.Response(
                        **response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR(
                        "misc name match")
            else:
                karza_misc_name_match_call.info.set_status_code(400)
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_misc_name_match_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_misc_name_match_call)
        return karza_misc_name_match_call
    

    @staticmethod
    def ocr_voter(request_body: KarzaOcrVoterCall.Request, karza_ocr_voter_call: Optional[KarzaOcrVoterCall] = None) -> KarzaOcrVoterCall:
        karza_ocr_voter_call = KarzaOcrVoterCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        ) if karza_ocr_voter_call is None else karza_ocr_voter_call
        post_response = karza_ocr_voter_call.context.call()
        karza_ocr_voter_call.info.set_status_code(
            post_response.status_code)
        if karza_ocr_voter_call.info.success:
            karza_ocr_voter_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_ocr_voter_call.response = KarzaOcrVoterCall.Response.from_raw_response(
                        response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("ocr voter")
            else:
                karza_ocr_voter_call.info.set_status_code(400)
                karza_ocr_voter_call.meta.error_message = KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_ocr_voter_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_ocr_voter_call)
        return karza_ocr_voter_call
    

    @staticmethod
    def ocr_pan(request_body: KarzaOcrPanCall.Request)->KarzaOcrPanCall:
        karza_ocr_pan_call = KarzaOcrPanCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = karza_ocr_pan_call.context.call()
        karza_ocr_pan_call.info.set_status_code(
            post_response.status_code)
        if karza_ocr_pan_call.info.success:
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                karza_ocr_pan_call.raw_response = post_response.json()
                response_body = post_response.json()
                if "result" in post_response.json():
                    response_body = post_response.json()["result"]
                    if response_body is not None:
                        response_body = response_body.get("documents", []) 
                        if len(response_body) > 0 :
                                if response_body[0].get("documentType") != "PAN":
                                    karza_ocr_pan_call.info.set_status_code(400)
                                    karza_ocr_pan_call.meta.error_message = "Provided document is not PAN"
                                if response_body[0].get("ocrData"):
                                    response_body = response_body[0].get("ocrData")
                                try:
                                    karza_ocr_pan_call.response = KarzaOcrPanCall.Response(
                                            **response_body)
                                except Exception as error:
                                    raise KarzaConnector.Errors.MAPPING_ERROR("ocr pan")
                else:
                    error_message = MiscUtils.get_value_from_dictionary(
                    post_response.json(), ["error"]
                    )
                    if error_message is not None:
                        karza_ocr_pan_call.meta.error_message = error_message
            else:
                karza_ocr_pan_call.info.set_status_code(400)
                karza_ocr_pan_call.meta.error_message =  KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_ocr_pan_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(karza_ocr_pan_call)
        return karza_ocr_pan_call

    @staticmethod
    def kyc_pan(request_body: KarzaKycPanCall.Request) -> KarzaKycPanCall:
        karza_kyc_pan_call = KarzaKycPanCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = karza_kyc_pan_call.context.call()
        karza_kyc_pan_call.info.set_status_code(
            post_response.status_code)
        if karza_kyc_pan_call.info.success:
            karza_kyc_pan_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            internal_status_code = response_body["statusCode"]
            if internal_status_code == 101:
                response_body = response_body.get("result")
                try:
                    karza_kyc_pan_call.response = KarzaKycPanCall.Response(
                        **response_body)
                except Exception:
                    raise KarzaConnector.Errors.MAPPING_ERROR("kyc pan")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"])
            karza_kyc_pan_call.meta.error_message = karza_kyc_pan_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            karza_kyc_pan_call)
        return karza_kyc_pan_call
    
    @staticmethod
    def ocr_aadhaar(request_body: KarzaOcrAadhaarCall.Request)->KarzaOcrAadhaarCall:
        karza_ocr_aadhaar_call = KarzaOcrAadhaarCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = karza_ocr_aadhaar_call.context.call()
        karza_ocr_aadhaar_call.info.set_status_code(
            post_response.status_code)
        if karza_ocr_aadhaar_call.info.success:
            karza_ocr_aadhaar_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_ocr_aadhaar_call.response = KarzaOcrAadhaarCall.Response.from_raw_response(
                        response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("ocr aadhaar")
            else:
                karza_ocr_aadhaar_call.info.set_status_code(400)
                karza_ocr_aadhaar_call.meta.error_message =  KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_ocr_aadhaar_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(karza_ocr_aadhaar_call)
        return karza_ocr_aadhaar_call
    
    
    @staticmethod
    def kyc_liveness(request_body: KarzaKycLivenessCall.Request) -> KarzaKycLivenessCall:
        karza_kyc_liveness_call = KarzaKycLivenessCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        karza_kyc_liveness_call.context.request_context.json = {
            "url": karza_kyc_liveness_call.request.file_url,
        }

        post_response = karza_kyc_liveness_call.context.call()
        karza_kyc_liveness_call.info.set_status_code(post_response.status_code)

        if karza_kyc_liveness_call.info.success:
            karza_kyc_liveness_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_kyc_liveness_call.response = KarzaKycLivenessCall.Response(
                        **response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("kyc liveness")
            else:
                karza_kyc_liveness_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeLiveliness.get(str(internal_status_code)) \
                        or KarzaInternalStatusCodeAuthentication.get(str(internal_status_code)) \
                        or "Unknown Vendor Status Code"                
                karza_kyc_liveness_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_kyc_liveness_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_kyc_liveness_call)
        return karza_kyc_liveness_call

    @staticmethod
    def kyc_aadhaar_mobile_link(request_body: KarzaKycAadhaarMobileLinkCall.Request) -> KarzaKycAadhaarMobileLinkCall:
        karza_kyc_aadhaar_mobile_link_call = KarzaKycAadhaarMobileLinkCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        karza_kyc_aadhaar_mobile_link_call.context.request_context.json = {
            "mobile": karza_kyc_aadhaar_mobile_link_call.request.mobile_number,
            "aadhaar": karza_kyc_aadhaar_mobile_link_call.request.aadhaar_number,
            "consent": "Y"
        }

        post_response = karza_kyc_aadhaar_mobile_link_call.context.call()
        karza_kyc_aadhaar_mobile_link_call.info.set_status_code(post_response.status_code)

        if karza_kyc_aadhaar_mobile_link_call.info.success:
            karza_kyc_aadhaar_mobile_link_call.raw_response = post_response.json()
            internal_status_code = post_response.json()["statusCode"]
            if internal_status_code == 101:
                # Success
                response_body = post_response.json()
                try:
                    karza_kyc_aadhaar_mobile_link_call.response = KarzaKycAadhaarMobileLinkCall.Response(
                        **response_body)
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("kyc liveness")
            else:
                karza_kyc_aadhaar_mobile_link_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeOCR.get(str(internal_status_code), "Unknown Vendor Status Code")
                karza_kyc_aadhaar_mobile_link_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                karza_kyc_aadhaar_mobile_link_call.meta.error_message = error_message

        MiscUtils.raise_error_from_call(karza_kyc_aadhaar_mobile_link_call)
        return karza_kyc_aadhaar_mobile_link_call
    
    @staticmethod
    def kyc_face_match(request_body: KarzaKycFaceMatchCall) -> KarzaKycFaceMatchCall:
        kyc_face_match_call = KarzaKycFaceMatchCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        kyc_face_match_call.context.request_context.json = {
            "url1": kyc_face_match_call.request.url1,
            "url2": kyc_face_match_call.request.url2,
            "getNumberOfFaces": kyc_face_match_call.request.get_number_of_faces
        }
        post_response = kyc_face_match_call.context.call()
        kyc_face_match_call.info.set_status_code(post_response.status_code)

        if kyc_face_match_call.info.success:
            kyc_face_match_call.raw_response = post_response.json()
            internal_status_code = post_response.json().get("statusCode")
            
            if internal_status_code == 101:
                response_body = post_response.json()
                response_body = response_body.get('result')
                try:
                    kyc_face_match_call.response = KarzaKycFaceMatchCall.Response(
                        **response_body
                    )
                except Exception as error:
                    raise KarzaConnector.Errors.MAPPING_ERROR("face match response mapping")
            else:
                kyc_face_match_call.info.set_status_code(400)
                error_message = KarzaInternalStatusCodeOCR.get(
                    str(internal_status_code), "Unknown Vendor Status Code"
                )
                kyc_face_match_call.meta.error_message = error_message
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error"]
            )
            if error_message is not None:
                kyc_face_match_call.meta.error_message = error_message
        MiscUtils.raise_error_from_call(kyc_face_match_call)
        return kyc_face_match_call

