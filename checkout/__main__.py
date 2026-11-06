"""`python -m checkout` prints the receipt for the brief's example cart."""

from decimal import Decimal

from checkout import CartLine, checkout, format_receipt

EXAMPLE_CART = {
    "Apple": CartLine(unit_price=Decimal("1.50"), quantity=3),
    "Banana": CartLine(unit_price=Decimal("0.75"), quantity=2),
    "Orange": CartLine(unit_price=Decimal("2.00"), quantity=1),
}


def main() -> None:
    print(format_receipt(checkout(EXAMPLE_CART)))


if __name__ == "__main__":
    main()
