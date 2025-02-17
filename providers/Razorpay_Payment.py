from typing import Optional, List
from utils.misc import MiscUtils
from typing import Any, Union
from helpers.error import Error


class Customer:
    def __init__(
        self,
        contact: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,

    ) -> None:
        self.contact = contact
        self.email = email
        self.name = name

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        return cls(
            contact=MiscUtils.get_value_from_dict(
                data, "contact", none_accepted=True),
            email=MiscUtils.get_value_from_dict(
                data, "email", none_accepted=True),
            name=MiscUtils.get_value_from_dict(
                data, "name", none_accepted=True),
        )

    def to_dict(self):
        return {
            "contact": self.contact,
            "email": self.email,
            "name": self.name,
        }


class Notes:
    def __init__(
        self,
        policy_name: Optional[str] = None,

    ) -> None:
        self.policy_name = policy_name

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        return cls(
            policy_name=MiscUtils.get_value_from_dict(
                data, "policy_name", none_accepted=True)
        )

    def to_dict(self):
        return {
            "policy_name": self.policy_name
        }


class Notify:
    def __init__(
        self,
        email: Optional[bool] = None,
        sms: Optional[bool] = None,
        whatsapp: Optional[bool] = None

    ) -> None:

        self.email = email
        self.sms = sms
        self.whatsapp = whatsapp

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        return cls(
            email=MiscUtils.get_value_from_dict(
                data, "email", none_accepted=True),
            sms=MiscUtils.get_value_from_dict(data, "sms", none_accepted=True),
            whatsapp=MiscUtils.get_value_from_dict(
                data, "whatsapp", none_accepted=True),
        )

    def to_dict(self):
        return {

            "email": self.email,
            "sms": self.sms,
        }


class Payment:
    def __init__(
        self,
        amount: Optional[int] = None,
        method: Optional[str] = None,
        created_at: Optional[int] = None,
        payment_id: Optional[str] = None,
        plink_id: Optional[str] = None,
        status: Optional[str] = None,
        updated_at: Optional[int] = None,
        reference_id: Optional[str] = None,
        short_url: Optional[str] = None,
        reminder_enable: Optional[bool] = None,
        user_id: Optional[str] = None


    ) -> None:
        self.amount = amount
        self.method = method
        self.created_at = created_at
        self.payment_id = payment_id
        self.plink_id = plink_id
        self.status = status
        self.updated_at = updated_at
        self.reference_id = reference_id
        self.short_url = short_url
        self.reminder_enable = reminder_enable
        self.user_id = user_id

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        return cls(
            amount=cls.get_value_from_dict(data, "amount", none_accepted=True),
            created_at=cls.get_value_from_dict(
                data, "created_at", none_accepted=True),
            method=cls.get_value_from_dict(data, "method", none_accepted=True),
            payment_id=cls.get_value_from_dict(
                data, "payment_id", none_accepted=True),
            plink_id=cls.get_value_from_dict(
                data, "plink_id", none_accepted=True),
            status=cls.get_value_from_dict(data, "status", none_accepted=True),
            updated_at=cls.get_value_from_dict(
                data, "updated_at", none_accepted=True),
            reference_id=cls.get_value_from_dict(
                data, "reference_id", none_accepted=True),
            short_url=cls.get_value_from_dict(
                data, "short_url", none_accepted=True),
            reminder_enable=cls.get_value_from_dict(
                data, "reminder_enable", none_accepted=True),
            user_id=cls.get_value_from_dict(
                data, "user_id", none_accepted=True),

        )

    @staticmethod
    def get_value_from_dict(
        d: dict,
        keys: Union[str, List[str]],
        default: Any = None,
        none_accepted: bool = False,
        empty_accepted: bool = True,
    ):
        if isinstance(d, dict):
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key in d:
                    value = d[key]
                    if value is None and none_accepted == False:
                        raise Error(
                            msg=f"Could not extract '{key}' from dictionary", status_code=400
                        )
                    return (
                        MiscUtils.check_unknown_empty_value(value)
                        if empty_accepted is False
                        else value
                    )
            return default
        else:
            return None

    def to_dict(self):
        return {
            "amount": self.amount,
            "created_at": self.created_at,
            "method": self.method,
            "payment_id": self.payment_id,
            "plink_id": self.plink_id,
            "status": self.status,
            "updated_at": self.updated_at,
            "reference_id": self.reference_id,
            "short_url": self.short_url,
            "reminder_enable": self.reminder_enable,
            "user_id": self.user_id,
        }

    class PaymentLink:
        def __init__(
            self,
            accept_partial: Optional[bool],
            amount: Optional[int],
            amount_paid: Optional[int],
            callback_method: Optional[str],
            callback_url: Optional[str],
            cancelled_at: Optional[int],
            created_at: Optional[int],
            currency: Optional[str],
            customer: Optional[dict],
            description: Optional[str],
            expire_by: Optional[int],
            expired_at: Optional[int],
            first_min_partial_amount: Optional[int],
            id: Optional[str],
            notes: Optional[dict],
            notify: Optional[dict],
            payments: Optional[str],
            reference_id: Optional[str],
            reminder_enable: Optional[bool],
            reminders: Optional[list],
            short_url: Optional[str],
            status: Optional[str],
            updated_at: Optional[Optional[int]],
            upi_link: Optional[bool],
            user_id: Optional[str],
            whatsapp_link: Optional[bool],
        ) -> None:
            self.accept_partial = accept_partial
            self.amount = amount
            self.amount_paid = amount_paid
            self.callback_method = callback_method
            self.callback_url = callback_url
            self.cancelled_at = cancelled_at
            self.created_at = created_at
            self.currency = currency
            self.customer = customer
            self.description = description
            self.expire_by = expire_by
            self.expired_at = expired_at
            self.first_min_partial_amount = first_min_partial_amount
            self.id = id
            self.notes = notes
            self.notify = notify
            self.payments = payments
            self.reference_id = reference_id
            self.reminder_enable = reminder_enable
            self.reminders = reminders
            self.short_url = short_url
            self.status = status
            self.updated_at = updated_at
            self.upi_link = upi_link
            self.user_id = user_id
            self.whatsapp_link = whatsapp_link

        @classmethod
        def from_dict(cls, d: dict):
            return cls(
                accept_partial=MiscUtils.get_value_from_dict(
                    d, "accept_partial", none_accepted=True),
                amount=MiscUtils.get_value_from_dict(
                    d, "amount", none_accepted=True),
                amount_paid=MiscUtils.get_value_from_dict(
                    d, "amount_paid", none_accepted=True),
                callback_method=MiscUtils.get_value_from_dict(
                    d, "callback_method", none_accepted=True),
                callback_url=MiscUtils.get_value_from_dict(
                    d, "callback_url", none_accepted=True),
                cancelled_at=MiscUtils.get_value_from_dict(
                    d, "cancelled_at", none_accepted=True),
                created_at=MiscUtils.get_value_from_dict(
                    d, "created_at", none_accepted=True),
                currency=MiscUtils.get_value_from_dict(
                    d, "currency", none_accepted=True),
                customer=MiscUtils.get_value_from_dict(
                    d, "customer", none_accepted=True),
                description=MiscUtils.get_value_from_dict(
                    d, "description", none_accepted=True),
                expire_by=MiscUtils.get_value_from_dict(
                    d, "expire_by", none_accepted=True),
                expired_at=MiscUtils.get_value_from_dict(
                    d, "expired_at", none_accepted=True),
                first_min_partial_amount=MiscUtils.get_value_from_dict(
                    d, "first_min_partial_amount", none_accepted=True),
                id=MiscUtils.get_value_from_dict(d, "id", none_accepted=True),
                notes=MiscUtils.get_value_from_dict(
                    d, "notes", none_accepted=True),
                notify=MiscUtils.get_value_from_dict(
                    d, "notify", none_accepted=True),
                payments=MiscUtils.get_value_from_dict(
                    d, "payments", none_accepted=True),
                reference_id=MiscUtils.get_value_from_dict(
                    d, "reference_id", none_accepted=True),
                reminder_enable=MiscUtils.get_value_from_dict(
                    d, "reminder_enable", none_accepted=True),
                reminders=MiscUtils.get_value_from_dict(
                    d, "reminders", none_accepted=True),
                short_url=MiscUtils.get_value_from_dict(
                    d, "short_url", none_accepted=True),
                status=MiscUtils.get_value_from_dict(
                    d, "status", none_accepted=True),
                updated_at=MiscUtils.get_value_from_dict(
                    d, "updated_at", none_accepted=True),
                upi_link=MiscUtils.get_value_from_dict(
                    d, "upi_link", none_accepted=True),
                user_id=MiscUtils.get_value_from_dict(
                    d, "user_id", none_accepted=True),
                whatsapp_link=MiscUtils.get_value_from_dict(
                    d, "whatsapp_link", none_accepted=True),
            )

        def to_dict(self):
            return {
                "accept_partial": self.accept_partial,
                "amount": self.amount,
                "amount_paid": self.amount_paid,
                "callback_method": self.callback_method,
                "callback_url": self.callback_url,
                "cancelled_at": self.cancelled_at,
                "created_at": self.created_at,
                "currency": self.currency,
                "customer": self.customer,
                "description": self.description,
                "expire_by": self.expire_by,
                "expired_at": self.expired_at,
                "first_min_partial_amount": self.first_min_partial_amount,
                "id": self.id,
                "notes": self.notes,
                "notify": self.notify,
                "payments": self.payments,
                "reference_id": self.reference_id,
                "reminder_enable": self.reminder_enable,
                "reminders": self.reminders,
                "short_url": self.short_url,
                "status": self.status,
                "updated_at": self.updated_at,
                "upi_link": self.upi_link,
                "user_id": self.user_id,
                "whatsapp_link": self.whatsapp_link,
            }
