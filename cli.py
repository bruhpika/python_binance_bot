import os
import typer
import requests
from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price
)
from bot.orders import place_order as execute_order
from bot.client import BinanceClient, BinanceAPIError
from bot.logging_config import get_logger

logger = get_logger(__name__)
app = typer.Typer()

@app.command()
def place_order(
    symbol: str = typer.Argument(..., help="Symbol (e.g. BTCUSDT)"),
    side: str = typer.Argument(..., help="Side (BUY or SELL)"),
    order_type: str = typer.Argument(..., help="Order type (MARKET, LIMIT, STOP_LIMIT)"),
    quantity: float = typer.Argument(..., help="Quantity to trade"),
    price: float | None = typer.Option(None, "--price", help="Price for LIMIT or STOP_LIMIT orders"),
    stop_price: float | None = typer.Option(None, "--stop-price", help="Stop price for STOP_LIMIT orders")
):
    """
    Place a trade order on Binance Futures Testnet.
    """
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        typer.echo("Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set.", err=True)
        raise typer.Exit(code=1)

    try:
        symbol_val = validate_symbol(symbol)
        side_val = validate_side(side)
        order_type_val = validate_order_type(order_type)
        quantity_val = validate_quantity(quantity)
        price_val = validate_price(price, order_type_val)
        stop_price_val = validate_stop_price(stop_price, order_type_val)
    except ValueError as e:
        typer.echo(f"Validation error: {e}", err=True)
        raise typer.Exit(code=1)

    price_display = str(price_val) if price_val is not None else "N/A"
    stop_price_display = str(stop_price_val) if stop_price_val is not None else "N/A"
    
    summary = (
        "+-------------------------------------+\n"
        "|         ORDER REQUEST SUMMARY       |\n"
        "+-------------------------------------+\n"
        f"|  Symbol     : {str(symbol_val):<22}|\n"
        f"|  Side       : {str(side_val):<22}|\n"
        f"|  Type       : {str(order_type_val):<22}|\n"
        f"|  Quantity   : {str(quantity_val):<22}|\n"
        f"|  Price      : {price_display:<22}|\n"
        f"|  Stop Price : {stop_price_display:<22}|\n"
        "+-------------------------------------+"
    )
    typer.echo(summary)
    logger.info(f"Order request summary:\n{summary}")

    client = BinanceClient(api_key, api_secret)
    
    try:
        response = execute_order(
            client=client,
            symbol=symbol_val,
            side=side_val,
            order_type=order_type_val,
            quantity=quantity_val,
            price=price_val,
            stop_price=stop_price_val
        )
    except BinanceAPIError as e:
        typer.secho(f"Binance API Error [{e.code}]: {e.message}", fg=typer.colors.RED, err=True)
        logger.error(f"BinanceAPIError: {e}")
        raise typer.Exit(code=1)
    except requests.exceptions.RequestException as e:
        typer.secho(f"Network error: {e}", fg=typer.colors.RED, err=True)
        logger.error(f"RequestException: {e}")
        raise typer.Exit(code=1)

    logger.info(f"Order response: {response}")

    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    exec_qty = response.get("executedQty", "0.0")
    avg_price = response.get("avgPrice", "0.0")

    resp_summary = (
        "+-------------------------------------+\n"
        "|            ORDER RESPONSE           |\n"
        "+-------------------------------------+\n"
        f"|  Order ID   : {str(order_id):<22}|\n"
        f"|  Status     : {str(status):<22}|\n"
        f"|  Exec. Qty  : {str(exec_qty):<22}|\n"
        f"|  Avg Price  : {str(avg_price):<22}|\n"
        "+-------------------------------------+"
    )
    typer.echo(resp_summary)
    
    typer.secho("✓ Order placed successfully.", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
