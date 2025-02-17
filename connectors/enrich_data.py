import logging
from helpers.error import Error, ErrorAdditionalInfo
from helpers.common import CallInfo
from typing import Optional
from utils.misc import MiscUtils
import utils
import json
from helpers.kyc.others.providers import EnrichDataCall,EnrichDataOthersCall

class EnrichDataConnector:

    class Errors:
        @staticmethod
        def MAPPING_ERROR(name: str):
            return Error(
                msg=f"Could not map enrich data {name} response to finstack response",
                status_code=500,
                additional_info=ErrorAdditionalInfo(
                    error_name="FINSTACK_MAPPING_ERROR",
                )
            )

    @staticmethod
    def enrich_data_call(request_body:EnrichDataCall.Request) -> EnrichDataCall:
        enrich_data_call = EnrichDataCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        logging.info("Sending request to Enrich Data: %s", request_body)
        enrich_data_call.context.request_context.json = {
            "phone": enrich_data_call.request.phone,
            "email": enrich_data_call.request.email,
            "name": enrich_data_call.request.name,
            "pincode": enrich_data_call.request.pincode,
        }
        try:
            post_response = enrich_data_call.context.call()
        except Exception as e:
            logging.error("Error during API call: %s", str(e))
            raise EnrichDataConnector.Errors.MAPPING_ERROR("API call")

        logging.info("Received response from Enrich Data: %s", post_response.text)
        enrich_data_call.info.set_status_code(post_response.status_code)
        if enrich_data_call.info.success:
            response_body: dict = post_response.json()
            try:
                enrich_data_call.response = EnrichDataCall.Response(
                     MiscUtils.get_value_from_dict(response_body, "digitalIdentityScore"),
                     MiscUtils.get_value_from_dict(response_body, "phoneNameDIScore"),
                     MiscUtils.get_value_from_dict(response_body, "spendPropensity"),
                     MiscUtils.get_value_from_dict(response_body, "digitalFootprint"),
                     MiscUtils.get_value_from_dict(response_body, "ecomFootprint"),
                     MiscUtils.get_value_from_dict(response_body, "fcomFootprint"),
                     MiscUtils.get_value_from_dict(response_body, "qcomFootprint"),
                     MiscUtils.get_value_from_dict(response_body, "travelFootprint"),
                     MiscUtils.get_value_from_dict(response_body, "ottUser"),
                     MiscUtils.get_value_from_dict(response_body, "postpaidFlag"),
                     MiscUtils.get_value_from_dict(response_body, "fintechApproved"),
                     MiscUtils.get_value_from_dict(response_body, "dmatAccount"),
                     MiscUtils.get_value_from_dict(response_body, "upiVPACount"),
                     MiscUtils.get_value_from_dict(response_body, "hasMutualFund"),
                     MiscUtils.get_value_from_dict(response_body, "hasCreditCard"),
                     MiscUtils.get_value_from_dict(response_body, "ageBand"),
                     MiscUtils.get_value_from_dict(response_body, "tier"),
                     MiscUtils.get_value_from_dict(response_body, "zone"),
                     MiscUtils.get_value_from_dict(response_body, "gender"),
                     MiscUtils.get_value_from_dict(response_body, "nameMatchScore"),
                     MiscUtils.get_value_from_dict(response_body, "phoneFirstSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "emailFirstSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "phoneEmailFirstSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "phoneEmailLastSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "phoneNameFirstSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "phoneNameLastSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "emailNameFirstSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "emailNameLastSeenYear"),
                     MiscUtils.get_value_from_dict(response_body, "occupation"),
                     MiscUtils.get_value_from_dict(response_body, "language"),
                     MiscUtils.get_value_from_dict(response_body, "businessNameFound"),
                     MiscUtils.get_value_from_dict(response_body, "businessOwner"),
                     MiscUtils.get_value_from_dict(response_body, "phone"),
                     MiscUtils.get_value_from_dict(response_body, "name"),
                     MiscUtils.get_value_from_dict(response_body, "email"),
                     MiscUtils.get_value_from_dict(response_body, "pincode")
                )
            except Exception:
                raise EnrichDataConnector.Errors.MAPPING_ERROR("enrich data call")
        else:
            error_message: Optional[str] = MiscUtils.get_value_from_dict(post_response.json(), ["message"])
            enrich_data_call.meta.error_message = enrich_data_call.meta.error_message if error_message is None else error_message

        MiscUtils.raise_error_from_call(enrich_data_call)
        logging.info("Done processing Enrich Data response")
        return enrich_data_call