from decimal import Decimal

from checkout import CheckoutPolicy, DiscountLine, PairDiscount, checkout
from tests.support import assert_adds_up, cart, lines_of


def test_no_line_without_both_products():
    receipt = checkout(cart(Apple=2, Orange=1))

    assert lines_of(receipt, "Pair discount") == []
    assert_adds_up(receipt)


def test_one_pair_gets_five_percent_off_both_units():
    receipt = checkout(cart(Apple=1, Banana=1))

    # 5% of (1.50 + 0.75) = 0.1125 -> 0.11
    assert lines_of(receipt, "Pair discount") == [
        DiscountLine("Pair discount", "Apple + Banana", 1, Decimal("0.11"))
    ]
    assert_adds_up(receipt)


def test_pairs_are_the_smaller_quantity_and_leftovers_get_nothing():
    receipt = checkout(cart(Apple=3, Banana=2))

    # 2 pairs: 5% of 2 x (1.50 + 0.75) = 0.225 -> 0.23. The third apple is not in a pair.
    assert lines_of(receipt, "Pair discount") == [
        DiscountLine("Pair discount", "Apple + Banana", 2, Decimal("0.23"))
    ]
    assert_adds_up(receipt)


def test_pair_and_bulk_discounts_stack_on_the_same_units():
    receipt = checkout(cart(Apple=2, Banana=2))

    assert [line.rule for line in receipt.discounts] == [
        "Bulk discount",
        "Bulk discount",
        "Pair discount",
    ]
    # Pair is computed on list price, not on the bulk-discounted price.
    assert lines_of(receipt, "Pair discount")[0].amount == Decimal("0.23")
    assert_adds_up(receipt)


def test_pair_rule_can_pair_any_two_products():
    policy = CheckoutPolicy(rules=(PairDiscount("Orange", "Apple"),))

    receipt = checkout(cart(Apple=1, Orange=2), policy)

    # 5% of (2.00 + 1.50) = 0.175 -> 0.18
    assert receipt.discounts == (
        DiscountLine("Pair discount", "Orange + Apple", 1, Decimal("0.18")),
    )
    assert_adds_up(receipt)
