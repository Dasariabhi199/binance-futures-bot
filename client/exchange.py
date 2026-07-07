"""
Exchange interface.

Every exchange implementation must follow
this structure.

Examples:
- Binance Futures Testnet
- Mock Exchange
- Other Futures Exchanges
"""

from abc import ABC, abstractmethod

from models.order import (
    OrderRequest,
    OrderResponse,
)


class Exchange(ABC):
    """
    Abstract exchange base class.
    """


    @abstractmethod
    def place_order(
        self,
        order: OrderRequest
    ) -> OrderResponse:
        """
        Submit order to exchange.

        Must be implemented by every exchange.
        """

        pass



    @abstractmethod
    def get_balance(self) -> dict:
        """
        Return account balance.
        """

        pass



    @abstractmethod
    def get_positions(self) -> list:
        """
        Return open positions.
        """

        pass



    @abstractmethod
    def cancel_order(
        self,
        order_id: str
    ) -> bool:
        """
        Cancel existing order.
        """

        pass