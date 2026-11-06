# Checkout

Pricing a shopping cart: subtotal, discounts, tax, shipping and grand total.

## Language

**Product**:
A kind of thing that can be bought, identified by its name (Apple, Banana, Orange). The brief calls this an "item"; that word is avoided because the brief also uses it for a single unit.
_Avoid_: Item, SKU, type

**Unit**:
One piece of a Product. Three apples are three units of the Product Apple.
_Avoid_: Item, piece

**Cart Line**:
One Product in a Cart together with its unit price and quantity. A Cart has at most one Cart Line per Product. Quantity is at least 1 and the unit price is not negative.
_Avoid_: Item, line item, entry, row

**Cart**:
The set of Cart Lines being priced, keyed by Product name. A Cart with no Cart Lines is invalid and cannot be checked out.
_Avoid_: Basket, order

**Subtotal**:
The sum of every Cart Line's quantity times unit price, before any discount.
_Avoid_: Gross total, list total

**Discount Rule**:
A named pricing rule that looks at the whole Cart and reports zero or more Discount Lines. Rules are independent: each one is computed against the Subtotal prices, never against another rule's result.
_Avoid_: Promotion, offer, coupon

**Discount Line**:
One saving reported by one application of a Discount Rule: which rule, what it covered (one Product, or the Products in a Pair), how many units or Pairs it covered, and the amount saved, rounded to cents. The Bulk Discount reports one Discount Line per qualifying Product; the Pair Discount reports a single Discount Line for all Pairs.
_Avoid_: Discount entry, adjustment

**Bulk Discount**:
A Discount Rule: when a product's quantity is 2 or more, 10% off that product's entire line, not only the units beyond the first.
_Avoid_: Volume discount, quantity break

**Pair**:
One apple matched with one banana. A Cart holds as many Pairs as the smaller of its apple and banana quantities; unmatched units are not in a Pair.
_Avoid_: Bundle, combo

**Pair Discount**:
A Discount Rule: 5% off the unit price of every unit that is in a Pair, reported as one Discount Line covering all Pairs in the Cart.
_Avoid_: Bundle discount, combo deal

**Discounted Subtotal**:
The Subtotal minus the sum of all Discount Lines. It is the base for Tax and the figure that decides Free Shipping.
_Avoid_: Net subtotal, taxable amount

**Tax**:
8% of the Discounted Subtotal, rounded to cents. Shipping is not taxed.
_Avoid_: VAT, sales tax rate

**Shipping**:
A flat $5.99 charge, or $0.00 when Free Shipping applies.
_Avoid_: Delivery fee, postage

**Free Shipping**:
Shipping is waived when the Discounted Subtotal is strictly greater than $100.00. A Discounted Subtotal of exactly $100.00 still pays Shipping.
_Avoid_: Shipping discount (it is not a Discount Line)

**Grand Total**:
Discounted Subtotal plus Tax plus Shipping. Computed from the already-rounded figures, so the printed receipt adds up.
_Avoid_: Total, amount due
