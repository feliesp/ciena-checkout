"""Money is a Decimal. These helpers are the only two places that round or take percentages."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ZERO = Decimal("0.00")


def to_cents(amount: Decimal) -> Decimal:
    """Round to the nearest cent, halves up: 0.225 becomes 0.23."""
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def percent_of(amount: Decimal, percent: Decimal) -> Decimal:
    """Exact, unrounded `percent`% of `amount`."""
    return amount * percent / 100
