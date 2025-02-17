from typing import Optional, List

class AwsEmailContent:
    def __init__(
        self,
        subject: Optional[str] = None,
        text: Optional[str] = None,
        html: Optional[str] = None
    ) -> None:
        self.subject = "" if subject is None else subject
        self.text = "" if text is None else text
        self.html = "" if html is None else html
        
    def for_aws(self) -> dict:
        return {
            "Simple": {
                'Subject': {
                    'Data': self.subject
                },
                'Body': {
                    'Text': {
                        'Data': self.text
                    },
                    'Html': {
                        'Data': self.html
                    }
                }
            }
        }


class AwsSendEmailDestinations:
    def __init__(
        self,
        to: List[str] = None,
        cc: List[str] = None,
        bcc: List[str] = None
    ) -> None:
        self.to = [] if to is None else to
        self.cc = [] if cc is None else cc 
        self.bcc = [] if bcc is None else bcc 


    def for_aws(self) -> dict:
        return {
                "ToAddresses": self.to,
                'CcAddresses': self.cc,
                'BccAddresses': self.bcc
            }