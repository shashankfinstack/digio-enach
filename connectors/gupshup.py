from typing import Optional
from helpers.message.phone import GupshupMessagePhoneCall
from helpers.common import CallInfo
from utils.misc import MiscUtils


class GupshupConnector:

    @staticmethod
    def message_phone(request_body: GupshupMessagePhoneCall.Request) -> GupshupMessagePhoneCall:
        gupshup_message_phone_call = GupshupMessagePhoneCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = gupshup_message_phone_call.context.call()
        gupshup_message_phone_call.info.set_status_code(
            post_response.status_code)
        if gupshup_message_phone_call.info.success:
            gupshup_message_phone_call.raw_response = post_response.text
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"])
            gupshup_message_phone_call.meta.error_message = gupshup_message_phone_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            gupshup_message_phone_call)
        return gupshup_message_phone_call
