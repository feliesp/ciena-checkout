"""Helpers shared by the tests: build carts with the brief's prices and check receipt invariants."""

from decimal import Decimal

from checkout import CartLine, DiscountLine, Receipt

PRICES = {"Apple": Decimal("1.50"), "Banana": Decimal("0.75"), "Orange": Decimal("2.00")}


def cart(**quantities: int) -> dict[str, CartLine]:
    """cart(Apple=3, Banana=2) -> a cart at the brief's prices."""
    return {product: CartLine(PRICES[product], qty) for product, qty in quantities.items()}


def single(price: str, quantity: int = 1, product: str = "Widget") -> dict[str, CartLine]:
    """A one-line cart for a product no rule knows about, to pin a chosen subtotal."""
    return {product: CartLine(Decimal(price), quantity)}


def lines_of(receipt: Receipt, rule: str) -> list[DiscountLine]:
    return [line for line in receipt.discounts if line.rule == rule]


def assert_adds_up(receipt: Receipt) -> None:
    """The invariant every receipt must satisfy: the printed figures sum to the printed totals."""
    assert sum(line.amount for line in receipt.discounts) == receipt.total_discounts
    assert receipt.subtotal - receipt.total_discounts == receipt.discounted_subtotal
    assert receipt.discounted_subtotal + receipt.tax + receipt.shipping == receipt.grand_total
