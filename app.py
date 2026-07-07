from client.mock_exchange import MockExchange

from services.order_service import OrderService

from cli import TradingCLI


def main():

    exchange = MockExchange()

    service = OrderService(exchange)

    application = TradingCLI(service)

    application.start()


if __name__ == "__main__":

    main()