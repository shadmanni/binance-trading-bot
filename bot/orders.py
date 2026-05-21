from typing import Optional, Dict, Any

from bot.client    import BinanceFuturesClient, BinanceClientError
from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, ValidationError,
)
from bot.logging_config import setup_logger

logger = setup_logger("orders")


def place_order(
    client:     BinanceFuturesClient,
    symbol:     str,
    side:       str,
    order_type: str,
    quantity:   str,
    price:      Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    # --- Validate ---
    try:
        symbol     = validate_symbol(symbol)
        side       = validate_side(side)
        order_type = validate_order_type(order_type)
        qty        = validate_quantity(quantity)
        prc        = validate_price(price, order_type)
    except ValidationError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"\n❌  Validation Error: {exc}\n")
        return None

    # --- Summary ---
    print("\n" + "─" * 50)
    print("  ORDER REQUEST SUMMARY")
    print("─" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {qty}")
    if prc is not None:
        label = "Stop Price" if order_type == "STOP_MARKET" else "Price"
        print(f"  {label:<11}: {prc}")
    print("─" * 50 + "\n")

    logger.info(
        "Placing %s %s order | symbol=%s qty=%s price=%s",
        side, order_type, symbol, qty, prc
    )

    # --- Place ---
    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=qty,
            price=prc,
        )
    except BinanceClientError as exc:
        logger.error("API error placing order: %s", exc)
        print(f"❌  API Error ({exc.code}): {exc.message}\n")
        return None
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        print(f"❌  Unexpected error: {exc}\n")
        return None

    # --- Print response ---
    print("─" * 50)
    print("  ORDER RESPONSE")
    print("─" * 50)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Executed   : {response.get('executedQty', '0')} {response.get('symbol','')[:3]}")
    avg = response.get('avgPrice') or response.get('price', '0')
    print(f"  Avg Price  : {avg}")
    print(f"  Client OID : {response.get('clientOrderId', 'N/A')}")
    print("─" * 50)
    print("  ✅  Order placed successfully!\n")

    logger.info("Order placed successfully: orderId=%s status=%s", response.get('orderId'), response.get('status'))
    return response