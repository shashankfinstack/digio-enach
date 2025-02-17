import logging
from helpers.common.providers.Razorpay_Payment import Payment
from helpers.error import Error, ErrorAdditionalInfo
from helpers.common import CallInfo, CallContext, AppContexts, RequestContext, HttpMethods
from typing import Optional
from utils.misc import MiscUtils
from helpers.payment.pg import RazorpayPaymentLink, RazorpayPaymentLinkCall
from utils.secret import SecretUtils


class RazorpayConnector:
    class Errors:
        @staticmethod
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )

    @staticmethod
    def create_payment_link(
        request_body: RazorpayPaymentLinkCall.Request
    ) -> RazorpayPaymentLink:
        razorpay_payment_call = RazorpayPaymentLinkCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        logging.info("Sending request to Razorpay: %s", request_body)

        try:
            post_response = razorpay_payment_call.context.call()
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Razorpay: %s", post_response.text)
        razorpay_payment_call.info.set_status_code(post_response.status_code)
        if (razorpay_payment_call.info.success):
            response_body: dict = post_response.json()
            razorpay_payment_call.response = Payment.PaymentLink(
                MiscUtils.get_value_from_dict(
                    response_body, "accept_partial", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "amount", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "amount_paid", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "callback_method", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "callback_url", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "cancelled_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "created_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "currency", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "customer", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "description", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "expire_by", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "expired_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "first_min_partial_amount", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "notes", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "notify", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "payments", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reference_id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reminder_enable", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reminders", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "short_url", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "status", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "updated_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "upi_link", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "user_id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "whatsapp_link", none_accepted=True)
            )

        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dict(
                post_response.json(), ["message"])
            razorpay_payment_call.meta.error_message = razorpay_payment_call.meta.error_message if (
                error_message is None) else error_message

        MiscUtils.raise_error_from_call(razorpay_payment_call)
        logging.info("Done processing Razorpay response")
        razorpay_call = RazorpayPaymentLink.from_razorpay(
            razorpay_payment_call
        )
        return razorpay_call

    @staticmethod
    def get_payment_links() -> dict:
        try:
            response = (
                f"{SecretUtils.SECRETS.RAZORPAY_BASE_URL}",

            )
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Razorpay: %s", response.text)
        return response.json()

    @staticmethod
    def get_payment_link_details(payment_link_id: str) -> RazorpayPaymentLinkCall:
        razorpay_call = RazorpayPaymentLinkCall(
            request=None,
            response=None,
            info=CallInfo(status_code=500)
        )
        url = f"{SecretUtils.SECRETS.RAZORPAY_BASE_URL}/payment_links/{payment_link_id}"
        logging.info("Fetching payment link details from ABC: %s", url)

        try:
            get_response = razorpay_call.context.call()
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from ABC: %s", get_response.text)
        razorpay_call.info.set_status_code(get_response.status_code)
        if razorpay_call.info.success:
            response_body: dict = get_response.json()
            try:
                razorpay_call.response = Payment.PaymentLink(
                    MiscUtils.get_value_from_dict(
                        response_body, "accept_partial"),
                    MiscUtils.get_value_from_dict(response_body, "amount"),
                    MiscUtils.get_value_from_dict(
                        response_body, "amount_paid"),
                    MiscUtils.get_value_from_dict(
                        response_body, "callback_method"),
                    MiscUtils.get_value_from_dict(
                        response_body, "callback_url"),
                    MiscUtils.get_value_from_dict(
                        response_body, "cancelled_at"),
                    MiscUtils.get_value_from_dict(response_body, "created_at"),
                    MiscUtils.get_value_from_dict(response_body, "currency"),
                    MiscUtils.get_value_from_dict(response_body, "customer"),
                    MiscUtils.get_value_from_dict(
                        response_body, "description"),
                    MiscUtils.get_value_from_dict(response_body, "expire_by"),
                    MiscUtils.get_value_from_dict(response_body, "expired_at"),
                    MiscUtils.get_value_from_dict(
                        response_body, "first_min_partial_amount"),
                    MiscUtils.get_value_from_dict(response_body, "id"),
                    MiscUtils.get_value_from_dict(response_body, "notes"),
                    MiscUtils.get_value_from_dict(response_body, "notify"),
                    MiscUtils.get_value_from_dict(
                        response_body, "payments", none_accepted=True),
                    MiscUtils.get_value_from_dict(
                        response_body, "reference_id"),
                    MiscUtils.get_value_from_dict(
                        response_body, "reminder_enable"),
                    MiscUtils.get_value_from_dict(response_body, "reminders"),
                    MiscUtils.get_value_from_dict(response_body, "short_url"),
                    MiscUtils.get_value_from_dict(response_body, "status"),
                    MiscUtils.get_value_from_dict(response_body, "updated_at"),
                    MiscUtils.get_value_from_dict(response_body, "upi_link"),
                    MiscUtils.get_value_from_dict(response_body, "user_id"),
                    MiscUtils.get_value_from_dict(
                        response_body, "whatsapp_link")
                )
            except Exception:
                raise RazorpayConnector.Errors.MAPPING_ERROR("razorpay call")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dict(
                get_response.json(), ["message"])
            razorpay_call.meta.error_message = razorpay_call.meta.error_message if (
                error_message is None) else error_message

        MiscUtils.raise_error_from_call(razorpay_call)
        logging.info("Done processing ABC response")
        return razorpay_call

    @staticmethod
    def notify_payment_link_by_sms(payment_link_id: str,request_body: RazorpayPaymentLinkCall.Request) -> dict:
        call_context = CallContext(
            base_url_var_name=SecretUtils.SECRETS.RAZORPAY_BASE_URL,
            request_contexts={
                    AppContexts.live: RequestContext(
                        method=HttpMethods.POST,
                        path=f"/v1/payment_links/{payment_link_id}/notify_by/sms",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": RazorpayPaymentLinkCall.get_auth_token(request_body.product),
                        },
                    ),
                    AppContexts.mock: RequestContext(
                        method=HttpMethods.POST,
                        path=f"{SecretUtils.SECRETS.RAZORPAY_BASE_URL}/payment_links/{payment_link_id}/notify_by/sms",
                    ),
                },
            mock_environments=[]
        )
        try:
            post_response = call_context.call()
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Razorpay: %s", post_response.text)

    @staticmethod
    def update_payment_link(payment_link_id: str, request_body: RazorpayPaymentLinkCall.Request) -> RazorpayPaymentLink:
        call_context = CallContext(
            base_url_var_name=SecretUtils.SECRETS.RAZORPAY_BASE_URL,
            request_contexts={
                    AppContexts.live: RequestContext(
                        method=HttpMethods.PATCH,
                        path=f"/v1/payment_links/{payment_link_id}",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": RazorpayPaymentLinkCall.get_auth_token(request_body.product),
                        },
                        json={
                            "expire_by": request_body.expire_by,
                        },
                    ),
                    AppContexts.mock: RequestContext(
                        method=HttpMethods.PATCH,
                        path=f"/payment/pg/razorpay/{payment_link_id}",
                        json={
                            "expire_by": request_body.expire_by,
                        },
                    ),
                },
            mock_environments=[]
        )
        razorpay_payment_call = RazorpayPaymentLinkCall(
                request=request_body,
                response=None,
                info=CallInfo(status_code=500),
                context=call_context
        )
        logging.info("Sending request to Razorpay: %s", request_body)

        try:
            post_response = razorpay_payment_call.context.call()
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Razorpay: %s", post_response.text)
        razorpay_payment_call.info.set_status_code(post_response.status_code)
        if (razorpay_payment_call.info.success):
            response_body: dict = post_response.json()
            razorpay_payment_call.response = Payment.PaymentLink(
                MiscUtils.get_value_from_dict(
                    response_body, "accept_partial", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "amount", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "amount_paid", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "callback_method", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "callback_url", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "cancelled_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "created_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "currency", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "customer", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "description", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "expire_by", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "expired_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "first_min_partial_amount", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "notes", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "notify", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "payments", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reference_id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reminder_enable", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "reminders", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "short_url", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "status", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "updated_at", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "upi_link", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "user_id", none_accepted=True),
                MiscUtils.get_value_from_dict(
                    response_body, "whatsapp_link", none_accepted=True)
            )

        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dict(
                post_response.json(), ["message"])
            razorpay_payment_call.meta.error_message = razorpay_payment_call.meta.error_message if (
                error_message is None) else error_message

        MiscUtils.raise_error_from_call(razorpay_payment_call)
        logging.info("Done processing Razorpay response")
        razorpay_call = RazorpayPaymentLink.from_razorpay(
            razorpay_payment_call
        )
        return razorpay_call

    @staticmethod
    def cancel_payment_link(payment_link_id: str) -> dict:
        try:
            response = (
                f"{SecretUtils.SECRETS.RAZORPAY_BASE_URL}/payment_links/{payment_link_id}/cancel"

            )

        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise RazorpayConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Razorpay: %s", response.text)
        return response.json()
