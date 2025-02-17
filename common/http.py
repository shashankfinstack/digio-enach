from enum import Enum


class HttpMethods(Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class RequestPathAndMethod:
    def __init__(
        self,
        path: str,
        method: HttpMethods
    ) -> None:
        self.path = path
        self.method = method

    def to_dict(self, for_db: bool = False):
        return {
            "path": self.path,
            "method": self.method.value
        }


class RequestOptions:
    def __init__(
        self,
        mock: RequestPathAndMethod,
        real: RequestPathAndMethod
    ) -> None:
        self.mock = mock
        self.real = real

    def to_dict(self, for_db: bool = False):
        return {
            "mock": self.mock.to_dict(for_db),
            "real": self.real.to_dict(for_db)
        }
