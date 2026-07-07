"""
Custom exception hierarchy for the trading bot.

All application-specific errors should inherit from
TradingBotException so they can be handled centrally.
"""


class TradingBotException(Exception):
    """
    Base exception for all trading bot errors.
    """

    def __init__(self, message: str, details: str | None = None):
        self.message = message
        self.details = details

        full_message = message

        if details:
            full_message += f" | Details: {details}"

        super().__init__(full_message)


class ConfigurationError(TradingBotException):
    """
    Raised when configuration is missing or invalid.
    """

    pass


class InvalidInputError(TradingBotException):
    """
    Raised when CLI input validation fails.
    """

    pass


class InvalidSymbolError(InvalidInputError):
    """
    Raised when trading symbol is invalid.
    """

    pass


class InvalidSideError(InvalidInputError):
    """
    Raised when BUY/SELL value is invalid.
    """

    pass


class InvalidOrderTypeError(InvalidInputError):
    """
    Raised when order type is invalid.
    """

    pass


class InvalidQuantityError(InvalidInputError):
    """
    Raised when order quantity is invalid.
    """

    pass


class InvalidPriceError(InvalidInputError):
    """
    Raised when limit order price is invalid.
    """

    pass


class ExchangeError(TradingBotException):
    """
    Base class for exchange-related errors.
    """

    pass


class AuthenticationError(ExchangeError):
    """
    Raised when API authentication fails.
    """

    pass


class APIError(ExchangeError):
    """
    Raised when exchange API returns an error.
    """

    def __init__(
        self,
        message: str,
        error_code: int | None = None,
        details: str | None = None,
    ):
        self.error_code = error_code

        if error_code:
            message = f"{message} (Code: {error_code})"

        super().__init__(message, details)


class NetworkError(ExchangeError):
    """
    Raised when network communication fails.
    """

    pass


class OrderError(TradingBotException):
    """
    Base order-related exception.
    """

    pass


class OrderPlacementError(OrderError):
    """
    Raised when order placement fails.
    """

    pass


class OrderCancellationError(OrderError):
    """
    Raised when order cancellation fails.
    """

    pass