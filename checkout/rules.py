"""Discount rules. Each rule looks at the whole cart and reports the discount lines it earns.

Rules are independent: every rule computes its saving against the list price, never against
another rule's result. Each reported amount is already rounded to cents.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from checkout.cart import Cart
from checkout.money import percent_of, to_cents


@dataclass(frozen=True)
class DiscountLine:
    """One saving: which rule, what it covered, how many units or pairs, and the amount."""

    rule: str
    applies_to: str
    quantity: int
    amount: Decimal


class DiscountRule(Protocol):
    @property
    def name(self) -> str: ...

    def apply(self, cart: Cart) -> list[DiscountLine]: ...


@dataclass(frozen=True)
class BulkDiscount:
    """`percent` off the whole line of any product bought `min_quantity` times or more."""

    percent: Decimal = Decimal("10")
    min_quantity: int = 2
    name: str = "Bulk discount"

    def apply(self, cart: Cart) -> list[DiscountLine]:
        return [
            DiscountLine(
                rule=self.name,
                applies_to=product,
                quantity=line.quantity,
                amount=to_cents(percent_of(line.total, self.percent)),
            )
            for product, line in cart.items()
            if line.quantity >= self.min_quantity
        ]


@dataclass(frozen=True)
class PairDiscount:
    """`percent` off every unit that is in a pair of one `first` and one `second`.

    The cart holds as many pairs as the smaller of the two quantities. Unmatched units
    get nothing. All pairs are reported as a single line.
    """

    first: str
    second: str
    percent: Decimal = Decimal("5")
    name: str = "Pair discount"

    def apply(self, cart: Cart) -> list[DiscountLine]:
        first, second = cart.get(self.first), cart.get(self.second)
        if first is None or second is None:
            return []
        pairs = min(first.quantity, second.quantity)
        pair_price = first.unit_price + second.unit_price
        return [
            DiscountLine(
                rule=self.name,
                applies_to=f"{self.first} + {self.second}",
                quantity=pairs,
                amount=to_cents(percent_of(pair_price * pairs, self.percent)),
            )
        ]
