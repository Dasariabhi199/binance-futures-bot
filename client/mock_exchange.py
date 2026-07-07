"""
Mock Futures Exchange

A local simulation of Binance Futures Testnet.

Features:
- Market orders
- Limit orders
- Order history
- Balance tracking
- Position tracking
- Order cancellation
"""

import random
import time

from client.exchange import Exchange

from models.order import (
    OrderRequest,
    OrderResponse,
    OrderStatus,
)

from utils.logger import setup_logger

from utils.exceptions import (
    OrderPlacementError,
)


logger = setup_logger()


class MockExchange(Exchange):

    def __init__(self):

        self.balance = {
            "asset": "USDT",
            "available": 10000.0
        }

        self.orders = {}

        self.positions = []


        logger.info(
            "Mock Futures Exchange started"
        )


    # --------------------------------------------------
    # PLACE ORDER
    # --------------------------------------------------

    def place_order(
        self,
        order: OrderRequest
    ) -> OrderResponse:


        try:

            logger.info(
                "Received order request"
            )

            logger.info(
                order.summary()
            )


            time.sleep(1)


            order_id = str(
                random.randint(
                    100000,
                    999999
                )
            )


            if order.price:

                executed_price = order.price

            else:

                executed_price = round(
                    random.uniform(
                        95000,
                        110000
                    ),
                    2
                )


            response = OrderResponse(

                success=True,

                order_id=order_id,

                symbol=order.symbol,

                status=OrderStatus.FILLED,

                executed_quantity=
                order.quantity,

                average_price=
                executed_price,

                message=
                "Order filled successfully"

            )


            # Store order

            self.orders[order_id] = response



            # Create position

            position = {

                "order_id": order_id,

                "symbol": order.symbol,

                "side": order.side.value,

                "quantity": order.quantity,

                "entry_price": executed_price,

            }


            self.positions.append(
                position
            )


            # Simulate cost deduction

            trade_value = (
                order.quantity *
                executed_price
            )


            self.balance["available"] -= (
                trade_value * 0.01
            )


            logger.info(
                "Order executed"
            )


            logger.info(
                response.summary()
            )


            return response



        except Exception as error:


            logger.exception(
                "Order failed"
            )


            raise OrderPlacementError(
                "Unable to execute order",
                details=str(error)
            )



    # --------------------------------------------------
    # BALANCE
    # --------------------------------------------------

    def get_balance(self):


        logger.info(
            "Fetching account balance"
        )


        return self.balance



    # --------------------------------------------------
    # POSITIONS
    # --------------------------------------------------

    def get_positions(self):


        logger.info(
            "Fetching open positions"
        )


        return self.positions



    # --------------------------------------------------
    # CANCEL ORDER
    # --------------------------------------------------

    def cancel_order(
        self,
        order_id: str
    ):


        logger.info(
            f"Cancel request received: {order_id}"
        )


        if order_id not in self.orders:


            logger.warning(
                "Order not found"
            )


            return False



        del self.orders[order_id]


        self.positions = [

            position

            for position in self.positions

            if position["order_id"] != order_id

        ]


        logger.info(
            "Order cancelled successfully"
        )


        return True