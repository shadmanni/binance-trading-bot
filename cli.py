#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot – CLI entry point
"""

import argparse
import os
import sys

from bot.client         import BinanceFuturesClient
from bot.orders         import place_order
from bot.logging_config import setup_logger

logger = setup_logger("cli")

BANNER = r"""
╔══════════════════════════════════════════════════╗
║      Binance Futures Testnet  –  Trading Bot     ║
╚══════════════════════════════════════════════════╝
"""


def get_credentials():
    api_key    = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("⚠️  API credentials not found in environment variables.")
        api_key    = input("  Enter your Binance Testnet API Key    : ").strip()
        api_secret = input("  Enter your Binance Testnet API Secret : ").strip()

    if not api_key or not api_secret:
        print("❌  API credentials are required. Exiting.")
        sys.exit(1)

    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python cli.py",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,  choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument(
        "--type",     required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        dest="order_type",
        help="Order type"
    )
    parser.add_argument("--qty",      required=True,  help="Order quantity")
    parser.add_argument("--price",    required=False, default=None,
                        help="Limit price (required for LIMIT); stop price for STOP_MARKET")
    return parser


def main():
    print(BANNER)
    parser = build_parser()
    args   = parser.parse_args()

    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key, api_secret)

    logger.info(
        "CLI invoked: symbol=%s side=%s type=%s qty=%s price=%s",
        args.symbol, args.side, args.order_type, args.qty, args.price
    )

    place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.qty,
        price=args.price,
    )


if __name__ == "__main__":
    main()