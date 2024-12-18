from abc import ABC
from enum import StrEnum, unique

from fastapi import HTTPException


@unique
class ErrorCode(StrEnum):  
    NONE = "NONE"
    INVALID_ENUM = "INVALID_ENUM"
    INVALID_PROPERTY = "INVALID_PROPERTY"


class BaseError(HTTPException, ABC):
    def __init__(self, status_code: int, detail: str, code):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class Internal(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(500, detail, code)


class BadRequest(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(400, detail, code)


class Unauthorized(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(401, detail, code)


class Forbidden(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(403, detail, code)


class NotFound(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(404, detail, code)


class Conflict(BaseError):
    def __init__(self, detail: str, code: ErrorCode = ErrorCode.NONE):
        super().__init__(409, detail, code)
