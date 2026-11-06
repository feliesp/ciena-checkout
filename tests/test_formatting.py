from checkout import checkout, format_receipt
from checkout.__main__ import EXAMPLE_CART
from tests.support import single

EXPECTED = """\
Subtotal                                 $8.00
Discounts
  Bulk discount: Apple x3               -$0.45
  Bulk discount: Banana x2              -$0.15
  Pair discount: Apple + Banana x2      -$0.23
  Total discounts                       -$0.83
Discounted subtotal                      $7.17
Tax (8%)                                 $0.57
Shipping                                 $5.99
Grand total                             $13.73"""


def test_example_receipt_text():
    assert format_receipt(checkout(EXAMPLE_CART)) == EXPECTED


def test_free_shipping_and_no_discounts_are_spelled_out():
    text = format_receipt(checkout(single("150.00")))

    assert "  (none)" in text
    assert "Shipping (free)" in text
    assert text.splitlines()[-1].endswith("$162.00")
