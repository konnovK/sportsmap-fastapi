from fastapi import HTTPException


class UserAlreadyExistsServiceException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=409,
            detail={"message": msg}
        )


class UserNotFoundServiceException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=400,
            detail={"message": msg}
        )


class FacilityAlreadyExistsServiceException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=409,
            detail={"message": msg}
        )


class FacilityNotFoundServiceException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=400,
            detail={"message": msg}
        )


class EmailPasswordRefreshAlreadyExistsException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=409,
            detail={"message": msg}
        )


class EmailPasswordRefreshNotFoundException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=400,
            detail={"message": msg}
        )


class EmailSubscriberAlreadyExistsException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=409,
            detail={"message": msg}
        )


class EmailSubscriberNotFoundException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=400,
            detail={"message": msg}
        )


class PhotoNotFoundServiceException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=400,
            detail={"message": msg}
        )
