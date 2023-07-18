class UserAlreadyExistsServiceException(Exception):
    pass


class UserNotFoundServiceException(Exception):
    pass


class FacilityAlreadyExistsServiceException(Exception):
    pass


class FacilityNotFoundServiceException(Exception):
    pass


class EmailPasswordRefreshAlreadyExistsException(Exception):
    pass


class EmailPasswordRefreshNotFoundException(Exception):
    pass


class EmailSubscriberAlreadyExistsException(Exception):
    pass


class EmailSubscriberNotFoundException(Exception):
    pass
