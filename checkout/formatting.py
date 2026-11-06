"""Render a Receipt as text. The only module that knows about dollar signs and columns."""

from decimal import Decimal

from checkout.pricing import Receipt

LABEL_WIDTH = 36
AMOUNT_WIDTH = 10


def _row(label: str, amount: Decimal, sign: str = "") -> str:
    return f"{label:<{LABEL_WIDTH}}{sign + '$' + str(amount):>{AMOUNT_WIDTH}}"


def format_receipt(receipt: Receipt) -> str:
    rows = [_row("Subtotal", receipt.subtotal), "Discounts"]
    for line in receipt.discounts:
        rows.append(_row(f"  {line.rule}: {line.applies_to} x{line.quantity}", line.amount, "-"))
    if not receipt.discounts:
        rows.append("  (none)")
    rows.append(_row("  Total discounts", receipt.total_discounts, "-"))
    rows.append(_row("Discounted subtotal", receipt.discounted_subtotal))
    rows.append(_row(f"Tax ({receipt.tax_rate}%)", receipt.tax))
    shipping_label = "Shipping (free)" if receipt.shipping == 0 else "Shipping"
    rows.append(_row(shipping_label, receipt.shipping))
    rows.append(_row("Grand total", receipt.grand_total))
    return "\n".join(rows)
