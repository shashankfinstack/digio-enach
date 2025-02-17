from helpers.message.phone import SmartpingMessagePhoneCall
from helpers.common import CallInfo
from utils.misc import MiscUtils
from typing import Optional

class SmartpingConnector:
    
    @staticmethod
    def message_phone(request_body: SmartpingMessagePhoneCall.Request) -> SmartpingMessagePhoneCall:
        smartping_message_phone_call = SmartpingMessagePhoneCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        post_response = smartping_message_phone_call.context.call()
        smartping_message_phone_call.info.set_status_code(
            post_response.status_code)
        if smartping_message_phone_call.info.success:
            smartping_message_phone_call.raw_response = post_response.json()
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dictionary(
                post_response.json(), ["error", "message"])
            smartping_message_phone_call.meta.error_message = smartping_message_phone_call.meta.error_message if error_message is None else error_message
        MiscUtils.raise_error_from_call(
            smartping_message_phone_call)
        return smartping_message_phone_call
