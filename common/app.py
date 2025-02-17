from enum import Enum


class AppEnvironments(Enum):
    development = "development"
    staging = "staging"
    sandbox = "sandbox"
    production = "production"
    preprod = "preprod"


class AppContexts(Enum):
    mock = "mock"
    live = "live"
