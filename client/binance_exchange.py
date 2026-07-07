"""
Binance Futures Testnet Exchange

Implements the Exchange interface.
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException

from client.exchange import Exchange

from models.order import (
    OrderRequest,
    OrderResponse,
    OrderStatus,
)

from utils.logger import setup_logger
from utils.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
)

logger = setup_logger()


class BinanceExchange(Exchange):

    def __init__(
        self,
        api_key: str,
        api_secret: str,
    ):

        try:

            self.client = Client(
                api_key,
                api_secret,
                testnet=True
            )

            logger.info(
                "Connected to Binance Futures Testnet."
            )

        except Exception as error:

            logger.exception("Authentication failed.")

            raise AuthenticationError(
                "Unable to authenticate.",
                details=str(error)
            )

    def place_order(
        self,
        order: OrderRequest
    ) -> OrderResponse:

        try:

            params = {

                "symbol": order.symbol,

                "side": order.side.value,

                "type": order.order_type.value,

                "quantity": order.quantity,

            }

            if order.price:

                params["price"] = order.price

                params["timeInForce"] = "GTC"

            result = self.client.futures_create_order(
                **params
            )

            return OrderResponse(

                success=True,

                order_id=str(result["orderId"]),

                symbol=result["symbol"],

                status=OrderStatus.NEW,

                executed_quantity=float(
                    result.get(
                        "executedQty",
                        0
                    )
                ),

                average_price=float(
                    result.get(
                        "avgPrice",
                        0
                    )
                ),

                message="Order submitted successfully"

            )

        except BinanceAPIException as error:

            logger.exception("Binance API error.")

            raise APIError(
                error.message,
                error_code=error.status_code
            )

        except Exception as error:

            logger.exception("Network error.")

            raise NetworkError(
                str(error)
            )

    def get_balance(self):

        return self.client.futures_account_balance()

    def get_positions(self):

        return self.client.futures_position_information()

    def cancel_order(
        self,
        order_id: str
    ):

        return self.client.futures_cancel_order(
            orderId=order_id
        )