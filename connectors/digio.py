import logging
from typing import Optional
from helpers.error import Error, ErrorAdditionalInfo
from helpers.esign.aadhaar.providers.digio import DigioEsignAadharCall, SigningPartyHelper, DigioMergeTemplateCall, DigioGetDocumentDetailsCall
from helpers.enach.providers.digio import (
    DigioEnachCreateMandateCall, DigioEnachGetMandateDetails, DigioEnachGetMandateDetailsByCRN, DigioEnachCancelExistingMandate
)
from helpers.common import (
    CallContext,
    CallInfo,
    CallMeta,
    RequestContext,
    AppContexts,
    HttpMethods,
)
import utils.logger
from utils.secret import SecretUtils
from utils.misc import MiscUtils
import requests

class DigioConnector:
    class Errors:
        @staticmethod
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map digio {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                ),
            )

    @staticmethod
    def create_mandate_request(request_body: DigioEnachCreateMandateCall.Request) -> DigioEnachCreateMandateCall:
        enach_create_call = DigioEnachCreateMandateCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        
        post_response = enach_create_call.context.call()
       
        enach_create_call.info.set_status_code(
            post_response.status_code
        )
        if enach_create_call.info.success:
            enach_create_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            try:
                enach_create_call.response = (
                    DigioEnachCreateMandateCall.Response.from_dict(response_body)
                )
                print(enach_create_call.response.__dict__)
            except Exception:
                raise DigioConnector.Errors.MAPPING_ERROR("Create Mandate")

        else:
            error_message = Optional[str] = post_response.json().get("message")
            enach_create_call.meta.error_message = (
                enach_create_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(enach_create_call)
        return enach_create_call
    
        
    
    @staticmethod
    def get_mandate_details_by_id(request_body: DigioEnachGetMandateDetails.Request) -> DigioEnachGetMandateDetails:
        enach_get_call = DigioEnachGetMandateDetails(
            request=request_body, 
            response=None, 
            info=CallInfo(status_code=500)
        )

        post_response = enach_get_call.context.call()
        enach_get_call.info.set_status_code(
            post_response.status_code
        )
        
        if enach_get_call.info.success:
            enach_get_call.raw_response = post_response.json()
            response_body: dict = post_response.json()
            try:
                enach_get_call.response = (
                    DigioEnachGetMandateDetails.Response.from_dict(response_body)
                )
            except Exception:
                raise DigioConnector.Errors.MAPPING_ERROR("Get Mandate Details")
            
        else:
            error_message = Optional[str] = post_response.json().get("message")
            enach_get_call.meta.error_message = (
                enach_get_call.meta.error_message
                if error_message is None
                else error_message
            )
        MiscUtils.raise_error_from_call(enach_get_call)
        return enach_get_call
    

    @staticmethod
    def generate_or_create_sign_request(request_body:DigioEsignAadharCall.Request, path:str):
        if request_body.templates is None:
            request_body = request_body.to_dict()
            del request_body["templates"]
        else:
            request_body = request_body.to_dict()
        digio_call = DigioEsignAadharCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500),
            context=(
                CallContext(
                    base_url_var_name= SecretUtils.SECRETS.DIGIO_TEMPLATE_BASE_URL,
                    request_contexts={
                        AppContexts.live: RequestContext(
                            method=HttpMethods.POST,
                            path=f"{path}",
                            headers={
                                "Content-Type":"application/json",
                                "Authorization": SecretUtils.get_secret_value(
                                SecretUtils.SECRETS.DIGIO_AUTHENTICATION_TOKEN
                            )
                            },
                            json=request_body
                        ),
                        AppContexts.mock: RequestContext(
                            method=HttpMethods.POST,
                            path=f"{path}",
                            headers={
                                "Content-Type":"application/json",
                                "Authorization":SecretUtils.get_secret_value(
                                SecretUtils.SECRETS.DIGIO_AUTHENTICATION_TOKEN
                            )
                            },
                            json=request_body
                        )
                    },
                    mock_environments=[]
                )
            )
        )
        try:
            response = digio_call.context.call()
        except Exception as error:
            raise DigioConnector.Errors.MAPPING_ERROR("Call to Digio Failed")
        digio_call.info.set_status_code(response.status_code)
        if digio_call.info.success:
            response_body = response.json()
            digio_call.response = DigioEsignAadharCall.Response(
                id=MiscUtils.get_value_from_dict(response_body, "id", none_accepted=False),
                is_agreement=MiscUtils.get_value_from_dict(response_body, "is_agreement", none_accepted=True),
                agreement_type=MiscUtils.get_value_from_dict(response_body, "agreement_type", none_accepted=False),
                agreement_status=MiscUtils.get_value_from_dict(response_body,"agreement_status", none_accepted=True),
                file_name=MiscUtils.get_value_from_dict(response_body, "file_name", none_accepted=False),
                created_at=MiscUtils.get_value_from_dict(response_body,"created_at", none_accepted=True),
                no_of_pages=MiscUtils.get_value_from_dict(response_body,"no_of_pages", none_accepted=True),
                signing_parties=[SigningPartyHelper(**signer) for signer in MiscUtils.get_value_from_dict(response_body, "signing_parties", none_accepted=True, default=[])],
                sign_request_details=MiscUtils.get_value_from_dict(response_body, "sign_request_details", none_accepted=True),
                channel=MiscUtils.get_value_from_dict(response_body, "channel",  none_accepted=True),
                self_signed=MiscUtils.get_value_from_dict(response_body, "self_signed", none_accepted=True),
                self_sign_type=MiscUtils.get_value_from_dict(response_body, "self_sign_type", none_accepted=True),
                self_sign_mode=MiscUtils.get_value_from_dict(response_body, "self_sign_mode", none_accepted=True),
                other_doc_details=MiscUtils.get_value_from_dict(response_body, "other_doc_details", none_accepted=True),
                access_token=MiscUtils.get_value_from_dict(response_body, "access_token", none_accepted=True),
                attached_estamp_details=MiscUtils.get_value_from_dict(response_body, "attached_estamp_details", none_accepted=True)
            )
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                response.json(), "message")
            digio_call.meta.error_message = digio_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(digio_call)
        return digio_call
        
    @staticmethod
    def merge_templates(request_body:DigioMergeTemplateCall.Request):
        digio_merge_template_call = DigioMergeTemplateCall(request=request_body)
        try:
            response = digio_merge_template_call.context.call()
        except Exception as error:
            raise DigioConnector.Errors.MAPPING_ERROR("Call to Digio Failed")
        digio_merge_template_call.info.set_status_code(response.status_code)
        
        if digio_merge_template_call.info.success:
            digio_merge_template_call.response = response.content
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                    response.json(),"message")
            digio_merge_template_call.meta.error_message = digio_merge_template_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(digio_merge_template_call)
        return digio_merge_template_call
    
    def get_document_details(request_body:DigioGetDocumentDetailsCall.Request):
        digio_call = DigioGetDocumentDetailsCall(request=request_body)
        try:
            response = digio_call.context.call()
        except Exception as error:
            raise DigioConnector.Errors.MAPPING_ERROR("Call to Digio Failed")
        digio_call.info.set_status_code(response.status_code)
        if digio_call.info.success:
            response_body = response.json()
            digio_call.response = DigioEsignAadharCall.Response(
                id=MiscUtils.get_value_from_dict(response_body, "id", none_accepted=False),
                is_agreement=MiscUtils.get_value_from_dict(response_body, "is_agreement", none_accepted=True),
                agreement_type=MiscUtils.get_value_from_dict(response_body, "agreement_type", none_accepted=False),
                agreement_status=MiscUtils.get_value_from_dict(response_body,"agreement_status", none_accepted=True),
                file_name=MiscUtils.get_value_from_dict(response_body, "file_name", none_accepted=False),
                created_at=MiscUtils.get_value_from_dict(response_body,"created_at", none_accepted=True),
                no_of_pages=MiscUtils.get_value_from_dict(response_body,"no_of_pages", none_accepted=True),
                signing_parties=[SigningPartyHelper.from_dict(signer) for signer in MiscUtils.get_value_from_dict(response_body, "signing_parties", none_accepted=True, default=[])],
                sign_request_details=MiscUtils.get_value_from_dict(response_body, "sign_request_details", none_accepted=True),
                channel=MiscUtils.get_value_from_dict(response_body, "channel",  none_accepted=True),
                self_signed=MiscUtils.get_value_from_dict(response_body, "self_signed", none_accepted=True),
                self_sign_type=MiscUtils.get_value_from_dict(response_body, "self_sign_type", none_accepted=True),
                self_sign_mode=MiscUtils.get_value_from_dict(response_body, "self_sign_mode", none_accepted=True),
                other_doc_details=MiscUtils.get_value_from_dict(response_body, "other_doc_details", none_accepted=True),
                access_token=MiscUtils.get_value_from_dict(response_body, "access_token", none_accepted=True),
                attached_estamp_details=MiscUtils.get_value_from_dict(response_body, "attached_estamp_details", none_accepted=True)
            )
        else:
            error_message = MiscUtils.get_value_from_dictionary(
                    response.json(), "message")
            digio_call.meta.error_message = digio_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(digio_call)
        return digio_call