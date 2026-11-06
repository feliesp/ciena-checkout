from decimal import Decimal

from checkout import DiscountLine, checkout
from checkout.__main__ import EXAMPLE_CART
from tests.support import assert_adds_up


def test_the_example_cart_from_the_brief():
    receipt = checkout(EXAMPLE_CART)

    assert receipt.subtotal == Decimal("8.00")
    assert receipt.discounts == (
        DiscountLine("Bulk discount", "Apple", 3, Decimal("0.45")),
        DiscountLine("Bulk discount", "Banana", 2, Decimal("0.15")),
        DiscountLine("Pair discount", "Apple + Banana", 2, Decimal("0.23")),
    )
    assert receipt.total_discounts == Decimal("0.83")
    assert receipt.discounted_subtotal == Decimal("7.17")
    assert receipt.tax == Decimal("0.57")
    assert receipt.shipping == Decimal("5.99")
    assert receipt.grand_total == Decimal("13.73")
    assert_adds_up(receipt)
