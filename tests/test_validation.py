from decimal import Decimal

import pytest

from checkout import CartError, CartLine, EmptyCartError, InvalidCartLineError, checkout
from tests.support import assert_adds_up


def test_empty_cart_is_refused():
    with pytest.raises(EmptyCartError):
        checkout({})


@pytest.mark.parametrize("quantity", [0, -1])
def test_quantity_below_one_is_refused(quantity):
    with pytest.raises(InvalidCartLineError, match="Apple: quantity"):
        checkout({"Apple": CartLine(Decimal("1.50"), quantity)})


def test_negative_unit_price_is_refused():
    with pytest.raises(InvalidCartLineError, match="Apple: unit price"):
        checkout({"Apple": CartLine(Decimal("-1.50"), 1)})


def test_zero_unit_price_is_allowed():
    receipt = checkout({"Sample": CartLine(Decimal("0.00"), 1)})

    assert receipt.grand_total == Decimal("5.99")
    assert_adds_up(receipt)


def test_every_cart_error_is_a_value_error():
    with pytest.raises(CartError):
        checkout({})
    assert issubclass(CartError, ValueError)
