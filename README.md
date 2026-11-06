# Ciena checkout

Prices a shopping cart: subtotal, discount breakdown, tax, shipping and grand total.

Domain vocabulary is in [GLOSSARY.md](GLOSSARY.md).

## Running it

You need Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync                     # install pytest and ruff
uv run python -m checkout   # price the example cart from the brief
uv run pytest               # 27 tests
uv run ruff check .         # lint
```

Without uv: `python -m checkout` and `python -m pytest` work from this folder with any
Python 3.13 that has pytest installed. The package itself has no dependencies.

## The example cart

Apple x3 at $1.50, Banana x2 at $0.75, Orange x1 at $2.00:

```
Subtotal                                 $8.00
Discounts
  Bulk discount: Apple x3               -$0.45
  Bulk discount: Banana x2              -$0.15
  Pair discount: Apple + Banana x2      -$0.23
  Total discounts                       -$0.83
Discounted subtotal                      $7.17
Tax (8%)                                 $0.57
Shipping                                 $5.99
Grand total                             $13.73
```

## Using it from code

```python
from decimal import Decimal
from checkout import CartLine, checkout, format_receipt

cart = {"Apple": CartLine(unit_price=Decimal("1.50"), quantity=3)}
receipt = checkout(cart)          # a Receipt: Decimals in cents plus the discount lines
print(receipt.grand_total)        # Decimal('10.36')
print(format_receipt(receipt))    # the text above
```

Rates, the shipping charge, the free-shipping threshold and the list of discount rules live
in a `CheckoutPolicy`. The defaults are the brief's values; pass your own to change them:

```python
from checkout import BulkDiscount, CheckoutPolicy, PairDiscount

policy = CheckoutPolicy(
    free_shipping_threshold=Decimal("50.00"),
    rules=(BulkDiscount(), PairDiscount("Apple", "Banana"), PairDiscount("Orange", "Apple")),
)
receipt = checkout(cart, policy)
```

## Assumptions

Where the brief is ambiguous I chose the following. Each one is pinned by a test.

1. **Discounts stack independently.** Each rule is computed on the list price and the savings
   are summed. The pair discount is 5% of $1.50, not 5% of the already bulk-discounted $1.35.
   The result does not depend on the order of the rules.
2. **Pairs are the smaller of the apple and banana quantities.** Three apples and two bananas
   make two pairs; the third apple gets no pair discount.
3. **The bulk discount covers the whole line** once the quantity reaches 2, not only the units
   beyond the first.
4. **Free shipping needs the discounted subtotal to be strictly above $100.00.** Exactly
   $100.00 still pays shipping. The threshold is judged after discounts and before tax.
5. **Tax is 8% of the discounted subtotal.** Shipping is not taxed.
6. **Rounding.** Money is `Decimal`, never `float`. Each discount line is computed exactly and
   then rounded to cents, half up ($0.225 becomes $0.23). Tax is rounded once the same way.
   Every other figure is a sum or difference of those cent amounts, so the receipt always adds
   up: total discounts is the sum of the lines, discounted subtotal is subtotal minus total
   discounts, and grand total is discounted subtotal plus tax plus shipping. The pair discount
   is reported as a single line for all pairs rather than one per product, because each
   rounded line is a place where a half cent can be lost. For the example cart, unrounded
   arithmetic gives $13.739; the receipt shows $13.73 because the lines it prints sum to that.
7. **Prices are whole cents.** A unit price of $0.00 is allowed (a free sample). A negative
   price, a quantity below 1, or an empty cart raise a `CartError`, which is a `ValueError`.

## Design

**The cart carries its prices.** A cart is a plain mapping from product name to a
`CartLine(unit_price, quantity)`, with no separate catalog. This mirrors how a quote line
snapshots its price, and the mapping gives one line per product for free, so the rules never
have to merge duplicate lines.

**Discount rules are a list of small objects.** A rule is anything with a `name` and an
`apply(cart) -> list[DiscountLine]` method, declared as a `Protocol`. `BulkDiscount` and
`PairDiscount` are frozen dataclasses holding their percentages, and the pair rule takes the
two product names so pairing other products is a one-line change. Adding a third rule means
writing one class and adding it to the policy. Free shipping is not a discount rule: it
produces no discount line and it reads the discounted subtotal, which only exists after the
rules have run.

**One policy object instead of constants.** `CheckoutPolicy` groups the tax rate, shipping
charge, free-shipping threshold and rule list. Tests exercise other thresholds by passing a
policy, not by patching module globals, and a new rate does not change the `checkout`
signature.

**Arithmetic, then text.** `checkout()` returns a frozen `Receipt` of Decimals and knows nothing
about formatting. `format_receipt()` is the only module with dollar signs and column widths,
and `python -m checkout` prints the example cart. Tests assert on numbers rather than parsing
strings, and a frontend could consume the `Receipt` as JSON instead of scraping text.

**Layout.**

```
checkout/
  cart.py        CartLine, Cart, validation and the CartError hierarchy
  rules.py       DiscountLine, the DiscountRule protocol, BulkDiscount, PairDiscount
  pricing.py     CheckoutPolicy, Receipt and checkout()
  formatting.py  format_receipt()
  money.py       to_cents() and percent_of(): the only rounding and percentage code
  __main__.py    the example cart
tests/           one file per concern: bulk, pair, shipping, validation, rounding,
                 the example cart and formatting
```

## Testing approach

Tests go through `checkout()` and the `Receipt` it returns, never through the rule objects,
so the internals can be refactored without touching them. Each rule has a case where it does
not apply (no line at all, never a $0.00 line), one where it applies once and one where it
applies several times. Shipping is tested at $99.99, $100.00 and $100.01. Rounding has its own
file, including the half-cent case that separates half-up from banker's rounding. Every test
that produces a receipt also asserts that its lines sum to its totals.

## AI usage

I used Claude Code as a pair: first to interrogate the brief and settle the ambiguities above
before any code existed, then to write the tests and implementation against those decisions.
The design choices and the reasoning behind them are mine, and every behaviour is pinned by a
test I reviewed.
