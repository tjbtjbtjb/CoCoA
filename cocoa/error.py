
class CocoaError(Exception):
    """Base class for exceptions in CoCoa."""
    pass

    
class CocoaKeyError(CocoaError):
    """Exception raised for errors in used key option.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class CocoaDbError(CocoaError):
    """Exception raised for database errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class CocoaWhereError(CocoaError):
    """Exception raised for location errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
