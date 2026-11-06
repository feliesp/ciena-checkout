"""A Cart is a mapping from product name to one CartLine, plus the ways a cart can be invalid."""

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CartLine:
    """One product in the cart: its unit price (in whole cents) and how many units."""

    unit_price: Decimal
    quantity: int

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.quantity


Cart = Mapping[str, CartLine]


class CartError(ValueError):
    """The cart cannot be checked out."""


class EmptyCartError(CartError):
    """The cart has no lines."""


class InvalidCartLineError(CartError):
    """A line has a quantity below 1 or a negative unit price."""


def validate(cart: Cart) -> None:
    if not cart:
        raise EmptyCartError("The cart is empty.")
    for product, line in cart.items():
        if line.quantity < 1:
            raise InvalidCartLineError(
                f"{product}: quantity must be at least 1, got {line.quantity}."
            )
        if line.unit_price < 0:
            raise InvalidCartLineError(
                f"{product}: unit price cannot be negative, got {line.unit_price}."
            )
