from enum import Enum

class PanStatus(Enum):
    VALID = "valid"
    FAKE = "fake"
    DEACTIVATED = "deactivated"
    DELETED = "deleted"
    INVALID = "invalid"
    AMALGAMATION = "amalgamation"
    ACQUISITION = "acquisition"
    DEATH = "death"
    DISSOLUTION = "dissolution"
    LIQUIDATED = "liquidated"
    MERGER = "merger"
    PARTITION = "partition"
    SPLIT = "split"
    UNDER_LIQUIDATION = "under liquidation"
    INOPERATIVE = "inoperative"

class AadhaarSeedingStatus(Enum):
    SUCCESSFUL = "successful"
    UNSUCCESSFUL = "unsuccessful"
    NOT_SEEDED = "aadhaar is not seeded"
    NOT_APPLICABLE = "not applicable"

class TypeOfHolder(Enum):
    ASSOCIATION_OF_PERSONS = "association of persons (aop)"
    BODY_OF_INDIVIDUALS = "body of individuals (boi)"
    COMPANY = "company"
    FIRM = "firm"
    GOVERNMENT = "government"
    HINDU_UNDIVIDED_FAMILY = "huf (hindu undivided family)"
    LOCAL_AUTHORITY = "local authority"
    ARTIFICIAL_OR_JUDICIAL_PERSON = "artificial juridical person"
    INDIVIDUAL = "individual or person"
    TRUST = "trust"
    FIRM_LIMITED_LIABILITY_PARTNERSHIP = "firm/ limited liability partnership" 