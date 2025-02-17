from typing import List
from flask import Blueprint

import decorators
from helpers.body_field_validation import BodyFieldValidation
from helpers.common.response_data import CallbackStatusEnum
from helpers.response import ApiResponse
from services.callback import CallbackService
from utils.response import ResponseUtils
from .finance import finance_view
from .kyc import kyc_view
from .okyc import okyc_view
from .asset import asset_view
from .esign import esign_view
from .enach import enach_view
from .message import message_view
from .utility_assessment import utility_assessment_view
from .ocr import ocr_view
from .misc import misc_view
from .callback import callback_view
from .razorpay import payment_view
from views.callback.resource.razorpay import payment_callback_view

root_view = Blueprint("root", __name__)


# Check Route
@root_view.get("/check")
def check_route():
    return "Finstack Features API - v1 : Working Fine"


root_view.register_blueprint(kyc_view, url_prefix="/kyc")
root_view.register_blueprint(okyc_view, url_prefix="/okyc")
root_view.register_blueprint(asset_view, url_prefix="/asset")
root_view.register_blueprint(finance_view, url_prefix="/finance")
root_view.register_blueprint(esign_view, url_prefix="/esign")
root_view.register_blueprint(enach_view, url_prefix="/enach")
root_view.register_blueprint(message_view, url_prefix="/message")
root_view.register_blueprint(
    utility_assessment_view, url_prefix="/utility_assessment")
root_view.register_blueprint(ocr_view, url_prefix="/ocr")
root_view.register_blueprint(misc_view, url_prefix="/misc")
root_view.register_blueprint(callback_view, url_prefix="/callback")
root_view.register_blueprint(payment_view, url_prefix="/payment")
# root_view.register_blueprint(payment_get_view, url_prefix="/payment")
root_view.register_blueprint(payment_callback_view, url_prefix="/razorpay_callback")



@root_view.post(
    "/callback_details"
)
@decorators.request_body_validators([
    BodyFieldValidation(
        name="callback_id",
        value_type=str,
        required=True,
        blank_allowed=False,
    ),
])
def retrieve_callback_details(
        request_body: dict,
        _: List[BodyFieldValidation],
):
    try:
        callback_id = request_body["callback_id"]
        callback_helper = CallbackService.get_one(callback_id)
        if callback_helper.status == CallbackStatusEnum.PENDING:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback is pending",
                    status_code=201,
                    data=callback_helper.response_data,
                )
            )
        elif callback_helper.status == CallbackStatusEnum.SUCCESS:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback is successful",
                    status_code=200,
                    data=callback_helper.response_data,
                )
            )
        else:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback failed",
                    status_code=400,
                    data=callback_helper.response_data,
                )
            )
    except Exception as error:
        return ResponseUtils.get_error_response(
            error,
        )


@root_view.post(
    "/<resource_solution>/<resource_enabler>/<resource_provider>/callback"
)
@decorators.request_body_validators([
    BodyFieldValidation(
        name="callback_id",
        value_type=str,
        required=True,
        blank_allowed=False,
    ),
])
def retrieve_callback_for_resource_details(
        request_body: dict,
        _: List[BodyFieldValidation],
        resource_solution: str,
        resource_enabler: str,
        resource_provider: str,
):
    try:
        callback_id = request_body["callback_id"]
        callback_helper = CallbackService.get_one(callback_id)
        if callback_helper.status == CallbackStatusEnum.PENDING:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback is pending",
                    status_code=201,
                    data=callback_helper.response_data,
                )
            )
        elif callback_helper.status == CallbackStatusEnum.SUCCESS:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback is successful",
                    status_code=200,
                    data=callback_helper.response_data,
                )
            )
        else:
            return ResponseUtils.get_api_response(
                ApiResponse(
                    msg="Callback failed",
                    status_code=400,
                    data=callback_helper.response_data,
                )
            )
    except Exception as error:
        return ResponseUtils.get_error_response(
            error,
        )
