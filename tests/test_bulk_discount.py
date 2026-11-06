from decimal import Decimal

from checkout import DiscountLine, checkout
from tests.support import assert_adds_up, cart, lines_of


def test_no_line_when_every_product_is_bought_once():
    receipt = checkout(cart(Apple=1, Banana=1, Orange=1))

    assert lines_of(receipt, "Bulk discount") == []
    assert_adds_up(receipt)


def test_ten_percent_off_the_whole_line_from_two_units():
    receipt = checkout(cart(Apple=2))

    assert lines_of(receipt, "Bulk discount") == [
        DiscountLine("Bulk discount", "Apple", 2, Decimal("0.30"))
    ]
    assert_adds_up(receipt)


def test_one_line_per_qualifying_product_only():
    receipt = checkout(cart(Apple=3, Banana=2, Orange=1))

    assert lines_of(receipt, "Bulk discount") == [
        DiscountLine("Bulk discount", "Apple", 3, Decimal("0.45")),
        DiscountLine("Bulk discount", "Banana", 2, Decimal("0.15")),
    ]
    assert_adds_up(receipt)
