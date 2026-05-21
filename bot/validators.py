from typing import Optional

VALID_SYMBOLS = None   # None = accept anything; set a list to restrict
VALID_SIDES   = {"BUY", "SELL"}
VALID_TYPES   = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(ValueError):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    if VALID_SYMBOLS and s not in VALID_SYMBOLS:
        raise ValidationError(f"Unknown symbol '{s}'. Expected one of {VALID_SYMBOLS}.")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Side must be BUY or SELL, got '{side}'.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_TYPES:
        raise ValidationError(f"Order type must be one of {VALID_TYPES}, got '{order_type}'.")
    return t


def validate_quantity(qty: str) -> float:
    try:
        val = float(qty)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity must be a number, got '{qty}'.")
    if val <= 0:
        raise ValidationError(f"Quantity must be > 0, got {val}.")
    return val


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            val = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Price must be a number, got '{price}'.")
        if val <= 0:
            raise ValidationError(f"Price must be > 0, got {val}.")
        return val
    if order_type == "STOP_MARKET":
        if price is None:
            raise ValidationError("Stop price is required for STOP_MARKET orders.")
        try:
            val = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Stop price must be a number, got '{price}'.")
        if val <= 0:
            raise ValidationError(f"Stop price must be > 0, got {val}.")
        return val
    return None  # MARKET orders don't need a price