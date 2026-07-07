"""
Order data models.

This module defines the structures used throughout
the trading application.

The same models will work for:
- Mock Exchange
- Binance Futures Testnet
- Other exchanges
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional


class OrderSide(str, Enum):
    """
    Supported order sides.
    """

    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """
    Supported futures order types.
    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, Enum):
    """
    Possible order states.
    """

    NEW = "NEW"
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


@dataclass
class OrderRequest:
    """
    Represents a user's order request.

    This object is created from CLI input
    and passed to the order service.
    """

    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None

    created_at: datetime = field(
        default_factory=datetime.now
    )

    def is_market_order(self) -> bool:
        """
        Check whether order is market type.
        """

        return self.order_type == OrderType.MARKET


    def is_limit_order(self) -> bool:
        """
        Check whether order is limit type.
        """

        return self.order_type == OrderType.LIMIT


    def summary(self) -> str:
        """
        Human-readable order summary.
        """

        details = [
            "========== ORDER REQUEST ==========",
            f"Symbol      : {self.symbol}",
            f"Side        : {self.side.value}",
            f"Type        : {self.order_type.value}",
            f"Quantity    : {self.quantity}",
        ]

        if self.price:
            details.append(
                f"Price       : {self.price}"
            )

        details.append(
            f"Created     : {self.created_at}"
        )

        details.append(
            "=================================="
        )

        return "\n".join(details)


@dataclass
class OrderResponse:
    """
    Represents exchange response after
    submitting an order.
    """

    success: bool

    order_id: Optional[str] = None

    symbol: Optional[str] = None

    status: OrderStatus = OrderStatus.NEW

    executed_quantity: float = 0.0

    average_price: float = 0.0

    message: str = ""

    created_at: datetime = field(
        default_factory=datetime.now
    )


    def summary(self) -> str:
        """
        Format exchange response.
        """

        result = [
            "========== ORDER RESPONSE ==========",
            f"Success          : {self.success}",
            f"Order ID         : {self.order_id}",
            f"Symbol           : {self.symbol}",
            f"Status           : {self.status.value}",
            f"Executed Qty     : {self.executed_quantity}",
            f"Average Price    : {self.average_price}",
        ]

        if self.message:
            result.append(
                f"Message          : {self.message}"
            )

        result.append(
            "===================================="
        )

        return "\n".join(result)