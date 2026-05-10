def validate_symbol(symbol: str) -> str:
    """Validates and normalizes the trading symbol."""
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty.")
    sym = symbol.strip().upper()
    if not sym.endswith("USDT"):
        raise ValueError("Symbol must end with USDT.")
    return sym

def validate_side(side: str) -> str:
    """Validates and normalizes the order side."""
    s = side.upper()
    if s not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL.")
    return s

def validate_order_type(order_type: str) -> str:
    """Validates and normalizes the order type."""
    t = order_type.upper()
    if t not in {"MARKET", "LIMIT", "STOP_LIMIT"}:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
    return t

def validate_quantity(quantity: float) -> float:
    """Validates the order quantity."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(price: float | None, order_type: str) -> float | None:
    """Validates the order price based on order type."""
    if order_type in {"LIMIT", "STOP_LIMIT"}:
        if price is None or price <= 0:
            raise ValueError("Price must be provided and > 0 for LIMIT or STOP_LIMIT orders.")
        return float(price)
    elif order_type == "MARKET":
        if price is not None:
            import logging
            logging.getLogger(__name__).warning("Price provided for MARKET order will be ignored.")
        return None
    return None

def validate_stop_price(stop_price: float | None, order_type: str) -> float | None:
    """Validates the stop price based on order type."""
    if order_type == "STOP_LIMIT":
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop price must be provided and > 0 for STOP_LIMIT orders.")
        return float(stop_price)
    else:
        if stop_price is not None:
            import logging
            logging.getLogger(__name__).warning("Stop price provided for non-STOP_LIMIT order will be ignored.")
        return None
