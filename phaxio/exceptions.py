class PhaxioError(Exception):
    '''Base class for Phaxio-related errors'''

class AuthenticationError(PhaxioError):
    pass

class APIError(PhaxioError):
    pass

class ServerError(PhaxioError):
    pass