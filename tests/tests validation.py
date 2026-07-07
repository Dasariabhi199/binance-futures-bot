"""
Tests for order input validation.
"""

import pytest

from services.validation import OrderValidator

from models.order import (
    OrderSide,
    OrderType,
)

from utils.exceptions import (
    InvalidQuantityError,
    InvalidSideError,
    InvalidOrderTypeError,
    InvalidPriceError,
)


def test_valid_market_order_creation():

    order = OrderValidator.create_order_request(

        symbol="BTCUSDT",

        side="BUY",

        order_type="MARKET",

        quantity="0.01"

    )


    assert order.symbol == "BTCUSDT"

    assert order.side == OrderSide.BUY

    assert order.order_type == OrderType.MARKET

    assert order.quantity == 0.01



def test_valid_limit_order_creation():

    order = OrderValidator.create_order_request(

        symbol="ETHUSDT",

        side="SELL",

        order_type="LIMIT",

        quantity="0.10",

        price="3500"

    )


    assert order.price == 3500

    assert order.side == OrderSide.SELL



def test_negative_quantity_fails():

    with pytest.raises(
        InvalidQuantityError
    ):

        OrderValidator.validate_quantity(
            "-5"
        )



def test_invalid_side_fails():

    with pytest.raises(
        InvalidSideError
    ):

        OrderValidator.validate_side(
            "HOLD"
        )



def test_invalid_order_type_fails():

    with pytest.raises(
        InvalidOrderTypeError
    ):

        OrderValidator.validate_order_type(
            "STOP"
        )



def test_limit_order_without_price_fails():

    with pytest.raises(
        InvalidPriceError
    ):

        OrderValidator.validate_price(

            None,

            OrderType.LIMIT

        )