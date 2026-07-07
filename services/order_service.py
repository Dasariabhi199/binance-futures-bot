"""
Order Service

Acts as the bridge between the CLI
and the exchange implementation.
"""

from client.exchange import Exchange
from models.order import (
    OrderRequest,
    OrderResponse,
)

from utils.logger import setup_logger
from utils.exceptions import (
    OrderPlacementError,
)

logger = setup_logger()


class OrderService:
    """
    Handles all order operations.
    """

    def __init__(self, exchange: Exchange):

        self.exchange = exchange

        logger.info(
            "OrderService initialized."
        )

    def place_order(
        self,
        order: OrderRequest,
    ) -> OrderResponse:
        """
        Submit order through exchange.
        """

        logger.info(
            "Starting order placement..."
        )

        logger.info(
            order.summary()
        )

        try:

            response = self.exchange.place_order(
                order
            )

            logger.info(
                "Order completed successfully."
            )

            return response

        except Exception as error:

            logger.exception(
                "Order placement failed."
            )

            raise OrderPlacementError(
                "Failed to submit order.",
                details=str(error)
            )

    def get_balance(self):

        logger.info(
            "Requesting account balance..."
        )

        return self.exchange.get_balance()

    def get_positions(self):

        logger.info(
            "Requesting positions..."
        )

        return self.exchange.get_positions()

    def cancel_order(
        self,
        order_id: str,
    ) -> bool:

        logger.info(
            f"Cancel request: {order_id}"
        )

        return self.exchange.cancel_order(
            order_id
        )