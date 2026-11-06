from decimal import Decimal

import pytest

from checkout import CheckoutPolicy, checkout
from tests.support import assert_adds_up, single


@pytest.mark.parametrize(
    ("discounted_subtotal", "shipping"),
    [
        ("99.99", "5.99"),
        ("100.00", "5.99"),  # "exceeds" is strict: exactly 100 still pays shipping
        ("100.01", "0.00"),
    ],
)
def test_free_shipping_strictly_above_the_threshold(discounted_subtotal, shipping):
    receipt = checkout(single(discounted_subtotal))

    assert receipt.discounted_subtotal == Decimal(discounted_subtotal)
    assert receipt.shipping == Decimal(shipping)
    assert_adds_up(receipt)


def test_threshold_is_judged_after_discounts():
    # 110.00 before the bulk discount, 99.00 after it: not free.
    receipt = checkout(single("55.00", quantity=2))

    assert receipt.subtotal == Decimal("110.00")
    assert receipt.discounted_subtotal == Decimal("99.00")
    assert receipt.shipping == Decimal("5.99")
    assert_adds_up(receipt)


def test_shipping_charge_and_threshold_come_from_the_policy():
    policy = CheckoutPolicy(
        shipping_charge=Decimal("9.50"), free_shipping_threshold=Decimal("10.00")
    )

    assert checkout(single("10.00"), policy).shipping == Decimal("9.50")
    assert checkout(single("10.01"), policy).shipping == Decimal("0.00")
