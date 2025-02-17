from datetime import date
from enum import Enum
from typing import TypedDict


class BankTransaction:
    def __init__(
        self,
        type: str,
        note: str,
        amount: float,
        balance: float,
        date: date,
        channel: str,
        category: str,
        description: str,
    ):
        self.type = type
        self.note = note
        self.amount = amount
        self.balance = balance
        self.date = date
        self.channel = channel
        self.category = category
        self.description = description

    def to_dict(self, for_db: bool = False):
        return {
            "type": self.type.upper(),
            "note": self.note,
            "amount": self.amount,
            "balance": self.balance,
            "date": self.date.isoformat() if for_db is False and isinstance(self.date, date) else self.date,
            "channel": self.channel,
            "category": self.category,
            "description": self.description,
        }
    

class StatementPeriod(TypedDict):
    from_date: date
    to_date: date


class AmountWithDate(TypedDict):
    amount: float
    date: date
