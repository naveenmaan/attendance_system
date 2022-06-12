from validictory.validator import ValidationError


class WrongDateFormatError(ValidationError):
    """
    Validation error that refers to the wrong date format given
    """

    def __init__(self):
        message = "Wrong Date Format is given"
        super(WrongDateFormatError, self).__init__(message)


class WrongDateRangeError(ValidationError):
    """
    Validation error that refers to the wrong date range given
    """

    def __init__(self):
        message = "Wrong Date Range is given"
        super(WrongDateRangeError, self).__init__(message)


class DuplicateRequestError(ValidationError):
    """
    Validation error that refers to the duplicate leave request
    """

    def __init__(self):
        message = "Leave request already exist"
        super(DuplicateRequestError, self).__init__(message)


class InvalidRequestError(ValidationError):
    """
    Validation error that refers to the duplicate leave request
    """

    def __init__(self):
        message = "Given request id not valid"
        super(InvalidRequestError, self).__init__(message)
