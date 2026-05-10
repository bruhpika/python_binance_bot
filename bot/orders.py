from .client import BinanceClient
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price, validate_stop_price

def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None
) -> dict:
    """Validates parameters and places an order via the client."""
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    stop_price = validate_stop_price(stop_price, order_type)
    
    params = {
        "symbol": symbol,
        "side": side,
        "quantity": str(quantity)
    }
    
    if order_type == "MARKET":
        params["type"] = "MARKET"
    elif order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT order")
        params["type"] = "LIMIT"
        params["price"] = str(price)
        params["timeInForce"] = "GTC"
    elif order_type == "STOP_LIMIT":
        if price is None or stop_price is None:
            raise ValueError("Price and Stop Price are required for STOP_LIMIT order")
        params["type"] = "STOP"
        params["price"] = str(price)
        params["stopPrice"] = str(stop_price)
        params["timeInForce"] = "GTC"
    else:
        raise ValueError(f"Unrecognised order type: {order_type}")
        
    return client.place_order(params)
