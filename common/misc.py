from __future__ import annotations
from typing import Optional
from enum import Enum
from utils.misc import MiscUtils
from utils.logger import logger


class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
    TRANS = "T"

class IndianStates(Enum):
    AN = "Andaman & Nicobar Islands"
    AP = "Andhra Pradesh"
    AR = "Arunachal Pradesh"
    AS = "Assam"
    BR = "Bihar"
    CG = "Chattisgarh"
    CH = "Chandigarh"
    DD = "Daman & Diu"
    DL = "Delhi"
    DN = "Dadra & Nagar Haveli"
    GA = "Goa"
    GJ = "Gujarat"
    HP = "Himachal Pradesh"
    HR = "Haryana"
    JH = "Jharkhand"
    JK = "Jammu & Kashmir"
    KA = "Karnataka"
    KL = "Kerala"
    LD = "Lakshadweep"
    MH = "Maharashtra"
    ML = "Meghalaya"
    MN = "Manipur"
    MP = "Madhya Pradesh"
    MZ = "Mizoram"
    NL = "Nagaland"
    OR = "Orissa"
    PB = "Punjab"
    PY = "Pondicherry/Puducherry"
    RJ = "Rajasthan"
    SK = "Sikkim"
    TG = "Telangana"
    TN = "Tamil Nadu"
    TR = "Tripura"
    UL = "Uttaranchal/Uttarakhand"
    UP = "Uttar Pradesh"
    WB = "West Bengal"

    @staticmethod
    def guess(name: str) -> Optional[IndianStates]:
        if name is None:
            return None
        state_names = [member.value for member in IndianStates]
        max_score = 0
        selected_state_name = None
        for state_name in state_names:
            if name.lower() == state_name.lower():
                return MiscUtils.value_to_enum(state_name,IndianStates)
        for state_name in state_names:
            score,is_match =  MiscUtils.fuzzy(name.lower(),state_name.lower(),90)
            if score > max_score:
                max_score = score
                selected_state_name = state_name
        logger.info(f"\nIncoming State Name: '{name}'\nSelected State Name: {selected_state_name}")
        if selected_state_name is not None:
            return MiscUtils.value_to_enum(selected_state_name,IndianStates)
    

class MonthNames(Enum):
    January = "January"
    February = "February"
    March = "March"
    April = "April"
    May = "May"
    June = "June"
    July = "July"
    August = "August"
    September = "September"
    October = "October"
    November = "November"
    December = "December"


MonthNameToValue = {}
MonthNameToValue[MonthNames.January.value] = 10
MonthNameToValue[MonthNames.February.value] = 11
MonthNameToValue[MonthNames.March.value] = 12
MonthNameToValue[MonthNames.April.value] = 1
MonthNameToValue[MonthNames.May.value] = 2
MonthNameToValue[MonthNames.June.value] = 3
MonthNameToValue[MonthNames.July.value] = 4
MonthNameToValue[MonthNames.August.value] = 5
MonthNameToValue[MonthNames.September.value] = 6
MonthNameToValue[MonthNames.October.value] = 7
MonthNameToValue[MonthNames.November.value] = 8
MonthNameToValue[MonthNames.December.value] = 9

MonthValueToName = {}
MonthValueToName[10] = MonthNames.January.value
MonthValueToName[11] = MonthNames.February.value
MonthValueToName[12] = MonthNames.March.value
MonthValueToName[1] = MonthNames.April.value
MonthValueToName[2] = MonthNames.May.value
MonthValueToName[3] = MonthNames.June.value
MonthValueToName[4] = MonthNames.July.value
MonthValueToName[5] = MonthNames.August.value
MonthValueToName[6] = MonthNames.September.value
MonthValueToName[7] = MonthNames.October.value
MonthValueToName[8] = MonthNames.November.value
MonthValueToName[9] = MonthNames.December.value