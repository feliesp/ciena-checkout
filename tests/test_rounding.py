from decimal import Decimal

from checkout import checkout
from tests.support import assert_adds_up, cart, single


def test_discount_line_on_a_half_cent_rounds_up():
    # 3 bananas: 10% of 2.25 = 0.225. Half-up gives 0.23; banker's rounding would give 0.22.
    receipt = checkout(cart(Banana=3))

    assert receipt.discounts[0].amount == Decimal("0.23")
    assert_adds_up(receipt)


def test_tax_rounds_down():
    # 8% of 7.17 = 0.5736
    assert checkout(single("7.17")).tax == Decimal("0.57")


def test_tax_rounds_up():
    # 8% of 0.95 = 0.076
    assert checkout(single("0.95")).tax == Decimal("0.08")


def test_every_figure_is_in_whole_cents():
    receipt = checkout(cart(Apple=3, Banana=2, Orange=1))

    figures = [
        receipt.subtotal,
        receipt.total_discounts,
        receipt.discounted_subtotal,
        receipt.tax,
        receipt.shipping,
        receipt.grand_total,
        *(line.amount for line in receipt.discounts),
    ]
    assert all(figure.as_tuple().exponent == -2 for figure in figures)


def test_totals_are_sums_of_the_rounded_lines_not_rounded_sums():
    # Exact discounts total 0.825 and exact discounted subtotal is 7.175, which would round to
    # 7.18. The receipt instead carries 8.00 - 0.83 = 7.17 so that its lines add up.
    receipt = checkout(cart(Apple=3, Banana=2, Orange=1))

    assert receipt.total_discounts == Decimal("0.83")
    assert receipt.discounted_subtotal == Decimal("7.17")
    assert_adds_up(receipt)
