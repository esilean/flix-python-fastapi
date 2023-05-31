from fastapi.responses import JSONResponse

class BaseErrorResponse(Exception):
    def __init__(self, status: int, errors: dict, headers: dict = {}) -> None:
        self.__status = status
        self.__errors = errors
        self.__headers = headers
    
    def gen_error_response(self) -> JSONResponse:
        content: dict = {}
        if self.__errors:
            content = self.__errors

        return JSONResponse(
            status_code=self.__status,
            content=content,
            headers=self.__headers
        )
    
class BadRequest(BaseErrorResponse):
    def __init__(self, errors: dict, headers: dict = {}) -> None:
        super(BadRequest, self).__init__(400, errors, headers)

class NotFound(BaseErrorResponse):
    def __init__(self, errors: dict, headers: dict = {}) -> None:
        super(NotFound, self).__init__(404, errors, headers)

class InternalError(BaseErrorResponse):
    def __init__(self, errors: dict, headers: dict = {}) -> None:
        super(InternalError, self).__init__(500, errors, headers)

class Unauthorized(BaseErrorResponse):
    def __init__(self, errors: dict, headers: dict = {}) -> None:
        super(Unauthorized, self).__init__(401, errors, headers)

class Forbidden(BaseErrorResponse):
    def __init__(self, errors: dict, headers: dict = {}) -> None:
        super(Forbidden, self).__init__(403, errors, headers)