class Error(Exception):
    # Base class for exceptions in this library
    pass

class WigleError(Error):
    """Exception raised because WiGLE server returned an error

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
