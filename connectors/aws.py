import boto3
from helpers.common import CallInfo
from helpers.message.email import AwsMessageEmailSendCall,AwsMessageEmailIdentityCreateCall,AwsMessageEmailIdentityGetCall
from utils.misc import MiscUtils
from utils.secret import SecretUtils
from botocore.exceptions import ClientError


class AwsConnector:
    AWS_EMAIL_ACCESS_KEY = SecretUtils.get_secret_value(SecretUtils.SECRETS.AWS_EMAIL_ACCESS_KEY)
    AWS_EMAIL_SECRET_KEY = SecretUtils.get_secret_value(SecretUtils.SECRETS.AWS_EMAIL_SECRET_KEY)

    if AWS_EMAIL_ACCESS_KEY is not None and AWS_EMAIL_SECRET_KEY is not None:
        AWS_SESV2_CLIENT = boto3.client('sesv2', aws_access_key_id=AWS_EMAIL_ACCESS_KEY, aws_secret_access_key=AWS_EMAIL_SECRET_KEY)
    else:
        AWS_SESV2_CLIENT = boto3.client('sesv2')



    @staticmethod
    def send_email(request_body: AwsMessageEmailSendCall.Request) -> AwsMessageEmailSendCall:
        aws_message_email_send_call = AwsMessageEmailSendCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        try:
            response = AwsConnector.AWS_SESV2_CLIENT.send_email(
                FromEmailAddress=request_body.sender,
                Destination=request_body.destinations.for_aws(),
                Content=request_body.content.for_aws()
            )
            aws_message_email_send_call.raw_response = response
        except ClientError as error:
            response = error.response
            error_message = MiscUtils.get_value_from_dictionary(response,["Error","Message"])
            aws_message_email_send_call.meta.error_message = aws_message_email_send_call.meta.error_message if error_message is None else error_message
        aws_message_email_send_call.info.set_status_code(status_code=MiscUtils.get_value_from_dictionary(response,["ResponseMetadata","HTTPStatusCode"]))
        MiscUtils.raise_error_from_call(
            aws_message_email_send_call)
        return aws_message_email_send_call
    
    @staticmethod
    def identity_create(request_body: AwsMessageEmailIdentityCreateCall.Request) -> AwsMessageEmailIdentityCreateCall:
        aws_message_email_identity_create_call = AwsMessageEmailIdentityCreateCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        try:
            response = AwsConnector.AWS_SESV2_CLIENT.create_email_identity(
                EmailIdentity=request_body.email
            )
            aws_message_email_identity_create_call.raw_response = response
        except ClientError as error:
            response = error.response
            error_message = MiscUtils.get_value_from_dictionary(response,["Error","Message"])
            aws_message_email_identity_create_call.meta.error_message = aws_message_email_identity_create_call.meta.error_message if error_message is None else error_message
        aws_message_email_identity_create_call.info.set_status_code(status_code=MiscUtils.get_value_from_dictionary(response,["ResponseMetadata","HTTPStatusCode"]))
        MiscUtils.raise_error_from_call(
            aws_message_email_identity_create_call)
        return aws_message_email_identity_create_call
    
    @staticmethod
    def identity_get(request_body: AwsMessageEmailIdentityGetCall.Request) -> AwsMessageEmailIdentityGetCall:
        aws_message_email_identity_get_call = AwsMessageEmailIdentityGetCall(
            request=request_body,
            response=None,
            info=CallInfo(status_code=500)
        )
        try:
            response = AwsConnector.AWS_SESV2_CLIENT.get_email_identity(
                EmailIdentity=request_body.email
            )
            aws_message_email_identity_get_call.raw_response = response
        except ClientError as error:
            response = error.response
            error_message = MiscUtils.get_value_from_dictionary(response,["Error","Message"])
            aws_message_email_identity_get_call.meta.error_message = aws_message_email_identity_get_call.meta.error_message if error_message is None else error_message
        aws_message_email_identity_get_call.info.set_status_code(status_code=MiscUtils.get_value_from_dictionary(response,["ResponseMetadata","HTTPStatusCode"]))
        MiscUtils.raise_error_from_call(
            aws_message_email_identity_get_call)
        return aws_message_email_identity_get_call