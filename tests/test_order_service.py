"""
Tests for order service.
"""


from client.mock_exchange import MockExchange

from services.order_service import (
    OrderService,
)

from services.validation import (
    OrderValidator,
)


def test_market_order_execution():


    exchange = MockExchange()


    service = OrderService(
        exchange
    )


    order = OrderValidator.create_order_request(

        symbol="BTCUSDT",

        side="BUY",

        order_type="MARKET",

        quantity="0.01"

    )


    response = service.place_order(
        order
    )


    assert response.success is True

    assert response.symbol == "BTCUSDT"

    assert response.executed_quantity == 0.01



def test_limit_order_execution():


    exchange = MockExchange()


    service = OrderService(
        exchange
    )


    order = OrderValidator.create_order_request(

        symbol="ETHUSDT",

        side="SELL",

        order_type="LIMIT",

        quantity="0.10",

        price="3500"

    )


    response = service.place_order(
        order
    )


    assert response.success is True

    assert response.average_price == 3500



def test_cancel_order():


    exchange = MockExchange()


    service = OrderService(
        exchange
    )


    order = OrderValidator.create_order_request(

        symbol="BTCUSDT",

        side="BUY",

        order_type="MARKET",

        quantity="0.01"

    )


    response = service.place_order(
        order
    )


    result = service.cancel_order(
        response.order_id
    )


    assert result is True