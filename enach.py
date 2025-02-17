import datetime
from enum import Enum
from typing import List
from flask import Blueprint, request, jsonify
from utils.response import ResponseUtils
from decorators.request_validators import request_body_validators
from helpers.body_field_validation import BodyFieldValidation
from services.vendor import VendorService
from helpers.response import ApiResponse
from helpers.error import Error
from helpers.enach import EnachCreateMandateCall



enach_view = Blueprint('enach', __name__)

@enach_view.get("/check")
def check():
    return "E-NACH View - Service is up and running!"

# CREATE MANDATE
# right now the impl we have for enach is only for 1 provider "DIGIO" 
# @enach_view.post("/v3/client/mandate/create_form")
@enach_view.post("/create_mandate/<provider>")
@enach_view.post("/aadhaar/<provider>")
@request_body_validators(
    fields=[
        BodyFieldValidation(
            name="corporate_config_id",
            value_type=str,
            required=True
        ),
        BodyFieldValidation(
            name="customer_identifier",
            value_type=str,
            required=True
        ),
        BodyFieldValidation(
            name="notify_customer",
            value_type=bool,
            required=False,
            default=False
        ),
        # these below three should not be mandatory as they have default values
        BodyFieldValidation(
            name="auth_mode",
            value_type=str,
            required=False
        ),
        BodyFieldValidation(
            name="mandate_type",
            value_type=str,
            required=False
        ),
        BodyFieldValidation(
            name="generate_access_token",
            value_type=bool,
            required=False
        ),
        # MANDATE DATA FIELDS (make all fields as individual of mandate data)
        BodyFieldValidation(
            name="mandate_data",
            value_type=dict,
            required=True,
        ),
        
    ]
)
def enach_create_mandate_request(request_body:dict, body_field_validations: List[BodyFieldValidation], provider: str):
    try:
        vendor_service = VendorService.getServiceProvider(provider)
        enach_create_mandate_call: EnachCreateMandateCall = vendor_service.create_mandate_request(request_body)
        # Add callback response
        # DigioCallbackService.add_callback_with_response(
        #     enach_create_mandate_call.response_data()
        # )
        api_response = ApiResponse(
            data = enach_create_mandate_call.response_data(body_field_validations).to_dict(),
            msg = enach_create_mandate_call.meta.success_message,
            status_code = enach_create_mandate_call.info.status_code,
        )
        return ResponseUtils.get_api_response(api_response)
    
    except Exception as error:
        return ResponseUtils.get_error_response(error)
    


# GET E-NACH MANDATE DETAILS BY mandate_id
@enach_view.get("/get_mandate_by_id/<provider>/<mandate_id>")
def enach_get_mandate_request(provider:str, mandate_id:str):
    try:
        vendor_service = VendorService.getServiceProvider(provider)
        mandate_details = vendor_service.get_mandate_by_id(mandate_id)
    
        api_response = ApiResponse(
            data=mandate_details.response_data().to_dict(),
            msg="Mandate details fetched successfully",
            status_code=200,
        )
        return ResponseUtils.get_api_response(api_response)
    
    except Exception as error:
        return ResponseUtils.get_error_response(error)


# @enach_view.get("/get_mandate_by_id/<provider>")
# @request_body_validators(
#     fields=[
#         BodyFieldValidation(
#             name="mandate_id",
#             value_type=str,
#             required=True
#         )
#     ]
# )
# def enach_get_mandate_request(provider:str, mandate_id):
#     try:
#         vendor_service = VendorService.getServiceProvider(provider)
#         mandate_details = vendor_service.get_mandate_by_id(mandate_id)
    
#         api_response = ApiResponse(
#             data=mandate_details.to_dict(),
#             msg="Mandate details fetched successfully",
#             status_code=200,
#         )
#         return ResponseUtils.get_api_response(api_response)
    
#     except Exception as error:
#         return ResponseUtils.get_error_response(error)



# GET E-NACH MANDATE DETAILS BY CRN
# @enach_view.post("/get_mandate_by_crn/<provider>")
# @request_body_validators(
#     fields=[
#         BodyFieldValidation(
#             name="crn",
#             value_type=str,
#             required=True
#         )
#     ]
# )
# def enach_get_mandate_request(provider, crn):
#     try:
#         vendor_service = VendorService.getServiceProvider(provider)
#         if not vendor_service:
#             return ResponseUtils.get_error_response(f"Unsupported provider: {provider}")

#         # Fetch mandate details using the service provider
#         mandate_details = vendor_service.get_mandate_details_by_crn(crn)

#         if not mandate_details:
#             return ResponseUtils.get_error_response(f"Mandate with CRN {crn} not found")
#         api_response = ApiResponse(
#             msg="Successfully retrieved mandate details",
#             status_code=200,
#             data=mandate_details.to_dict(),
#         )
#         return ResponseUtils.get_api_response(api_response)

#     except ValueError as value_error:
#         return ResponseUtils.get_error_response(
#             error=f"Invalid value provided: {value_error}"
#         )
#     except Exception as error:
#         return ResponseUtils.get_error_response(
#             error=f"An error occurred while retrieving mandate details: {error}"
#         )



# CANCEL MANDATE REQUEST
# @enach_view.post("/mandate/cancel")
# @request_body_validators(
#     fields=[
#         BodyFieldValidation(name="umrn", value_type=str, required=False),
#         BodyFieldValidation(name="mandate_id", value_type=str, required=False),
#         BodyFieldValidation(name="reason", value_type=str, required=False)
#     ]
# )
# def cancel_mandate_request(request_data: CancelMandateRequest):
#     try:
#         if not request_data.umrn and not request_data.mandate_id:
#             raise ValueError("Either 'umrn' or 'mandate_id' must be provided.")

#         # Call the service to cancel the mandate
#         vendor_service = VendorService.getServiceProvider('DIGIO')
#         cancellation_response = vendor_service.cancel_mandate(request_data)

#         # Return API Response
#         api_response = ApiResponse(
#             data=cancellation_response.to_dict(),
#             msg="Mandate cancellation processed successfully",
#             status_code=200,
#         )
#         return ResponseUtils.get_api_response(api_response)
    
#     except Exception as error:
#         return ResponseUtils.get_error_response(error)