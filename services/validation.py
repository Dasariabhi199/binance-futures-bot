"""
Order input validation module.

Responsible for validating:
- Trading symbol
- Order side
- Order type
- Quantity
- Price

This layer prevents bad requests from
reaching the exchange API.
"""

import re

from models.order import (
    OrderSide,
    OrderType,
    OrderRequest,
)

from utils.exceptions import (
    InvalidSymbolError,
    InvalidSideError,
    InvalidOrderTypeError,
    InvalidQuantityError,
    InvalidPriceError,
)


class OrderValidator:
    """
    Handles all order validation rules.
    """


    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate futures trading symbol.

        Examples:
            BTCUSDT  ✓
            ETHUSDT  ✓
            btcusdt  ✓ converted

        Invalid:
            BTC
            BTC-USDT
            empty value
        """

        if not symbol:
            raise InvalidSymbolError(
                "Symbol cannot be empty"
            )


        symbol = symbol.upper().strip()


        pattern = r"^[A-Z0-9]{5,20}$"


        if not re.match(pattern, symbol):
            raise InvalidSymbolError(
                f"Invalid trading symbol: {symbol}"
            )


        return symbol



    @staticmethod
    def validate_side(side: str) -> OrderSide:
        """
        Validate BUY or SELL.
        """

        if not side:
            raise InvalidSideError(
                "Side cannot be empty"
            )


        side = side.upper().strip()


        try:
            return OrderSide(side)

        except ValueError:

            raise InvalidSideError(
                f"Invalid side '{side}'. "
                "Allowed: BUY, SELL"
            )



    @staticmethod
    def validate_order_type(
        order_type: str
    ) -> OrderType:
        """
        Validate MARKET or LIMIT.
        """

        if not order_type:
            raise InvalidOrderTypeError(
                "Order type cannot be empty"
            )


        order_type = (
            order_type
            .upper()
            .strip()
        )


        try:
            return OrderType(order_type)


        except ValueError:

            raise InvalidOrderTypeError(
                f"Invalid order type '{order_type}'. "
                "Allowed: MARKET, LIMIT"
            )



    @staticmethod
    def validate_quantity(
        quantity: str | float
    ) -> float:
        """
        Validate order quantity.

        Must be:
        - numeric
        - greater than zero
        """

        try:

            quantity = float(quantity)


        except ValueError:

            raise InvalidQuantityError(
                "Quantity must be numeric"
            )


        if quantity <= 0:

            raise InvalidQuantityError(
                "Quantity must be greater than zero"
            )


        return quantity



    @staticmethod
    def validate_price(
        price: str | float | None,
        order_type: OrderType
    ) -> float | None:
        """
        Validate price.

        Market orders do not require price.
        Limit orders require valid price.
        """


        if order_type == OrderType.MARKET:

            return None



        if price is None or price == "":

            raise InvalidPriceError(
                "Limit order requires price"
            )



        try:

            price = float(price)


        except ValueError:

            raise InvalidPriceError(
                "Price must be numeric"
            )


        if price <= 0:

            raise InvalidPriceError(
                "Price must be greater than zero"
            )


        return price



    @classmethod
    def create_order_request(
        cls,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str | float,
        price: str | float | None = None,
    ) -> OrderRequest:
        """
        Complete validation pipeline.

        Converts raw CLI input into
        a validated OrderRequest object.
        """


        validated_symbol = (
            cls.validate_symbol(symbol)
        )


        validated_side = (
            cls.validate_side(side)
        )


        validated_type = (
            cls.validate_order_type(order_type)
        )


        validated_quantity = (
            cls.validate_quantity(quantity)
        )


        validated_price = (
            cls.validate_price(
                price,
                validated_type
            )
        )



        return OrderRequest(
            symbol=validated_symbol,
            side=validated_side,
            order_type=validated_type,
            quantity=validated_quantity,
            price=validated_price,
        )