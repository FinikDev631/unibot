class UniBotError(Exception):
    pass


class BotAPIError(UniBotError):
    def __init__(self, method, description="", error_code=None, parameters=None, response=None):
        self.method = method
        self.description = description
        self.error_code = error_code
        self.parameters = parameters
        self.response = response
        message = description or "Bot API request failed"
        if error_code is not None:
            message = f"{message} (HTTP/API code: {error_code})"
        super().__init__(message)


class NetworkError(UniBotError):
    pass


class InvalidProviderError(UniBotError):
    pass
