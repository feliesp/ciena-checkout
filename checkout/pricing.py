"""checkout(): turn a Cart into a Receipt under a CheckoutPolicy."""

from dataclasses import dataclass
from decimal import Decimal

from checkout.cart import Cart, validate
from checkout.money import ZERO, percent_of, to_cents
from checkout.rules import BulkDiscount, DiscountLine, DiscountRule, PairDiscount

DEFAULT_RULES: tuple[DiscountRule, ...] = (BulkDiscount(), PairDiscount("Apple", "Banana"))


@dataclass(frozen=True)
class CheckoutPolicy:
    """Everything about pricing that is not the cart itself. Defaults are the brief's values."""

    tax_rate: Decimal = Decimal("8")
    shipping_charge: Decimal = Decimal("5.99")
    free_shipping_threshold: Decimal = Decimal("100.00")
    rules: tuple[DiscountRule, ...] = DEFAULT_RULES


DEFAULT_POLICY = CheckoutPolicy()


@dataclass(frozen=True)
class Receipt:
    """Every figure of a checkout, in cents. The lines always add up to the totals."""

    subtotal: Decimal
    discounts: tuple[DiscountLine, ...]
    total_discounts: Decimal
    discounted_subtotal: Decimal
    tax_rate: Decimal
    tax: Decimal
    shipping: Decimal
    grand_total: Decimal


def checkout(cart: Cart, policy: CheckoutPolicy = DEFAULT_POLICY) -> Receipt:
    """Price the cart.

    Rounding happens in exactly two places: each discount line (inside the rules) and the
    tax. Every other figure is a sum or difference of cent amounts, so the receipt adds up.
    """
    validate(cart)
    subtotal = to_cents(sum((line.total for line in cart.values()), ZERO))
    discounts = tuple(line for rule in policy.rules for line in rule.apply(cart))
    total_discounts = sum((line.amount for line in discounts), ZERO)
    discounted_subtotal = subtotal - total_discounts
    tax = to_cents(percent_of(discounted_subtotal, policy.tax_rate))
    free_shipping = discounted_subtotal > policy.free_shipping_threshold
    shipping = ZERO if free_shipping else policy.shipping_charge
    return Receipt(
        subtotal=subtotal,
        discounts=discounts,
        total_discounts=total_discounts,
        discounted_subtotal=discounted_subtotal,
        tax_rate=policy.tax_rate,
        tax=tax,
        shipping=shipping,
        grand_total=discounted_subtotal + tax + shipping,
    )
