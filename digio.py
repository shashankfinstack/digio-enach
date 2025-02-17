from connectors.digio import DigioConnector
from helpers.esign.aadhaar.providers.digio import DigioEsignAadharCall, SignerHelper, TemplatesHelper, SignCoordinatesManager, SignatureVerificationHelper, SignTypeEnum, DigioMergeTemplateCall, DigioGetDocumentDetailsCall, DisplayOnPageEnum
from helpers.esign.aadhaar import EsignAadhaarCall
from repositories.esign import EsignRepository
from helpers.common.response_data import ResponseCallbackHelper, CallbackStatusEnum, ResponseData
from helpers.error import Error
from helpers.digio_callback import DigioCallbackHelper
import utils
import requests
from helpers.enach import EnachCreateMandateCall, EnachGetMandateCall
from requests.auth import HTTPBasicAuth
import base64
import datetime
from helpers.enach.providers.digio import AuthMode, BankDetails, DigioEnachCreateMandateCall,DigioEnachGetMandateDetails , MandateData, Frequency, MandateType, ServiceProviderDetails
from .document import DocumentService
import utils.misc
class DigioService:
    
    @staticmethod
    def create_mandate_request(request_body:dict):
        if request_body.get("corporate_config_id") is None:
            raise Error("Corporate config id is mandatory to create a mandate request")

        mandate_request_body = EnachCreateMandateCall.Request(**request_body)
        digio_mandate_request: DigioEnachCreateMandateCall = DigioConnector.create_mandate_request(
            mandate_request_body.for_digio()
        )
        # digio_mandate_response: EnachCreateMandateCall = EnachCreateMandateCall.from_digio(
        #     mandate_request_body, digio_mandate_request
        # )
        digio_mandate_response: EnachCreateMandateCall = EnachCreateMandateCall.from_digio(
            digio_mandate_request,  mandate_request_body,
        )
        return digio_mandate_response
    
    
    @staticmethod
    def get_mandate_by_id(mandate_id: str):
        if not mandate_id:
            raise Error("Mandate ID is mandatory to fetch mandate details")
        
        mandate_request_body = EnachGetMandateCall.Request(mandate_id)
        digio_mandate_request: DigioEnachGetMandateDetails = DigioConnector.get_mandate_details_by_id()

        return digio_mandate_request

    # @staticmethod
    # def cancel_mandate(cancel_request: CancelMandateRequest) -> dict:
    #     # Determine which identifier to use (UMRN or Mandate ID)
    #     if cancel_request.umrn:
    #         # Call the Digi connector to cancel mandate using UMRN
    #         return DigioConnector.cancel_mandate_by_umrn(cancel_request.umrn, cancel_request.reason)
    #     elif cancel_request.mandate_id:
    #         # Call the Digi connector to cancel mandate using Mandate ID
    #         return DigioConnector.cancel_mandate_by_mandate_id(cancel_request.mandate_id, cancel_request.reason)

    @staticmethod
    def genrate_document(request_body:dict):
        if request_body.get("document_url") is None and request_body.get("templates") is None:
            raise Error("Either 'templates' or 'document_url' must be provided to create a sign request.")
        
        is_template_mode = utils.misc.MiscUtils.get_value_from_dict(request_body, "templates", none_accepted=True) is not None

        signers = [
            SignerHelper(**signer) 
            for signer in utils.misc.MiscUtils.get_value_from_dict(request_body, "signers", none_accepted=False)
        ]
        sign_coordinates = None if utils.misc.MiscUtils.get_value_from_dict(request_body, "sign_coordinates", none_accepted=True) is None else SignCoordinatesManager(
            utils.misc.MiscUtils.get_value_from_dict(request_body, "sign_coordinates", none_accepted=True)
        )

        templates = None
        file_data = None
        if is_template_mode:
            templates = [
                TemplatesHelper(**template) 
                for template in utils.misc.MiscUtils.get_value_from_dict(request_body, "templates", none_accepted=False)
            ]
        else:
            document_url = utils.misc.MiscUtils.get_value_from_dict(request_body, "document_url", none_accepted=False)
            if not isinstance(document_url, str):
                raise Error("'document_url' must be a string for uploading a PDF.")
            file_data = pdf_to_base64(document_url)
        
        signature_verification = utils.misc.MiscUtils.get_value_from_dict(request_body, "signature_verification", none_accepted=True)
        if signature_verification is not None:
            signature_verification = SignatureVerificationHelper(**signature_verification)
        
        signature_type = utils.misc.MiscUtils.get_value_from_dict(request_body, "signature_type", none_accepted=True)
        if signature_type is not None:
            signature_type = utils.misc.MiscUtils.value_to_enum(signature_type, SignTypeEnum)
        
        digio_request_body = DigioEsignAadharCall.Request(
            signers=signers,
            file_name=utils.misc.MiscUtils.get_value_from_dict(request_body, "file_name", none_accepted=False),
            templates=templates,
            sign_coordinates=sign_coordinates,
            signature_verification=signature_verification,
            signature_type=signature_type,
            expire_in_days=utils.misc.MiscUtils.get_value_from_dict(request_body, "expire_in_days", none_accepted=True),
            send_sign_link=utils.misc.MiscUtils.get_value_from_dict(request_body, "send_sign_link", none_accepted=True),
            notify_signers=utils.misc.MiscUtils.get_value_from_dict(request_body, "notify_signers", none_accepted=True),
            display_on_page=utils.misc.MiscUtils.value_to_enum(utils.misc.MiscUtils.get_value_from_dict(request_body, "display_on_page", none_accepted=True, default="all"), DisplayOnPageEnum),
            generate_access_token=utils.misc.MiscUtils.get_value_from_dict(request_body, "generate_access_token", none_accepted=True),
            customer_notification_mode=utils.misc.MiscUtils.get_value_from_dict(request_body, "customer_notification_mode", none_accepted=True),
            sequential=utils.misc.MiscUtils.get_value_from_dict(request_body, "sequential", none_accepted=True),
            file_data=file_data,
            signatory=utils.misc.MiscUtils.get_value_from_dict(request_body, "signatory", none_accepted=True),
            will_self_sign=utils.misc.MiscUtils.get_value_from_dict(request_body, "will_self_sign", none_accepted=True),
        )
        
        path = "/template/multi_templates/create_sign_request" if is_template_mode else "/document/uploadpdf"
        
        digio_call = DigioConnector.generate_or_create_sign_request(digio_request_body, path=path)
        
        return digio_call
    
    def merge_tempates(request_body:list):
        templates = [ TemplatesHelper.from_dict(template) for template in utils.misc.MiscUtils.get_value_from_dict(request_body, "templates", none_accepted=False)]
        request = DigioMergeTemplateCall.Request(templates=templates)
        digio_call = DigioConnector.merge_templates(request)
        digio_call.response = DocumentService.upload(digio_call.response,"pdf")
        return digio_call.response

    def get_document_details(document_id:str):
        request = DigioGetDocumentDetailsCall.Request(document_id=document_id)
        digio_call:DigioGetDocumentDetailsCall = DigioConnector.get_document_details(request)
        return digio_call.response.to_dict()

def pdf_to_base64(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        pdf_content = response.content

        base64_encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

        return base64_encoded_pdf

    except requests.exceptions.RequestException as e:
        raise f"Error fetching the PDF: {e}"

       
class DigioCallbackService:
    @staticmethod
    def update_failure_callback_with_response(
            response_callback: ResponseCallbackHelper
    ):
        callback_helper = EsignRepository.get_one(response_callback.id)
        if not callback_helper:
            raise Error("Callback does not exist", 400)
        callback_helper.response_data = None
        callback_helper.status = response_callback.status
        return EsignRepository.update(
            callback_helper._id,
            callback_helper.to_dict(for_db=True),
        )

    @staticmethod
    def add_callback_with_response(response_data: ResponseData):
        response_callback = response_data.callback
        if not response_callback:
            raise Error(
                "Callback details not found, unable to initiate callback!",
                400
            )
        callback_helper = DigioCallbackHelper(
            _id=response_callback.id,
            status=response_callback.status,
            response_data=response_data.to_dict() if response_data else None,
        )
        return EsignRepository.add(
            callback_helper
        )

    @staticmethod
    def update_callback_with_response(response_data: ResponseData):
        response_callback = response_data.callback
        if not response_callback:
            raise Error(
                "Callback details not found, unable to initiate callback!",
                400
            )
        callback_helper = EsignRepository.get_one(response_callback.id)
        if not callback_helper:
            raise Error("Callback does not exist", 400)
        callback_helper.response_data = response_data.to_dict()
        callback_helper._id = response_callback.id
        callback_helper.status = response_callback.status
        return EsignRepository.update(
            callback_helper._id,
            callback_helper.to_dict(for_db=True)
        )

    @staticmethod
    def get_one(callback_id: str):
        callback_helper = EsignRepository.get_one(callback_id)
        # if not callback_helper:
        #     raise Error("Callback Does not exist!", 400)
        return callback_helper
 