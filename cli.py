"""
Trading Bot Command Line Interface

Provides an interactive menu for:
1. Place Order
2. View Balance
3. View Positions
4. Cancel Order
5. Exit
"""

from colorama import Fore, Style, init

from services.validation import OrderValidator
from utils.exceptions import (
    InvalidInputError,
    OrderPlacementError,
)

init(autoreset=True)


class TradingCLI:

    def __init__(self, order_service):

        self.order_service = order_service

    # -----------------------------------------------------

    def print_header(self):

        print("\n")
        print("=" * 65)
        print("          BINANCE FUTURES TESTNET TRADING BOT")
        print("=" * 65)

    # -----------------------------------------------------

    def print_menu(self):

        print("\nChoose an option\n")

        print("1. Place Order")

        print("2. View Balance")

        print("3. View Positions")

        print("4. Cancel Order")

        print("5. Exit")

    # -----------------------------------------------------

    def place_order(self):

        try:

            print("\nPlace New Order\n")

            symbol = input("Symbol : ")

            side = input("Side (BUY/SELL): ")

            order_type = input("Order Type (MARKET/LIMIT): ")

            quantity = input("Quantity : ")

            price = None

            if order_type.upper() == "LIMIT":

                price = input("Price : ")

            order = OrderValidator.create_order_request(

                symbol=symbol,

                side=side,

                order_type=order_type,

                quantity=quantity,

                price=price,

            )

            print()

            print(Fore.CYAN)

            print(order.summary())

            response = self.order_service.place_order(order)

            print()

            print(Fore.GREEN)

            print(response.summary())

        except InvalidInputError as error:

            print(Fore.RED)

            print(error)

        except OrderPlacementError as error:

            print(Fore.RED)

            print(error)

        except Exception as error:

            print(Fore.RED)

            print(error)

    # -----------------------------------------------------

    def view_balance(self):

        print()

        balance = self.order_service.get_balance()

        print(Fore.YELLOW)

        print("=" * 40)

        print("ACCOUNT BALANCE")

        print("=" * 40)

        print(f"Asset      : {balance['asset']}")

        print(f"Available  : {balance['available']}")

    # -----------------------------------------------------

    def view_positions(self):

        positions = self.order_service.get_positions()

        print()

        print("=" * 40)

        print("OPEN POSITIONS")

        print("=" * 40)

        if not positions:

            print("No Open Positions")

            return

        for position in positions:

            print(position)

    # -----------------------------------------------------

    def cancel_order(self):

        order_id = input("\nOrder ID : ")

        status = self.order_service.cancel_order(order_id)

        print()

        if status:

            print(Fore.GREEN)

            print("Order cancelled successfully.")

        else:

            print(Fore.RED)

            print("Order not found.")

    # -----------------------------------------------------

    def start(self):

        while True:

            self.print_header()

            self.print_menu()

            choice = input("\nEnter Choice : ")

            if choice == "1":

                self.place_order()

            elif choice == "2":

                self.view_balance()

            elif choice == "3":

                self.view_positions()

            elif choice == "4":

                self.cancel_order()

            elif choice == "5":

                print()

                print("Good Bye!")

                break

            else:

                print()

                print(Fore.RED)

                print("Invalid Choice")

            input("\nPress ENTER to continue...")