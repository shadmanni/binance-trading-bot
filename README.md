# Binance Futures Testnet – Trading Bot

A clean, modular Python CLI bot for placing orders on the Binance USDT-M Futures Demo/Testnet environment.

---

# Project Structure

```text
binance-trading-bot/
├── bot/
│   ├── client.py          # Binance REST API wrapper (signing + requests)
│   ├── orders.py          # Order placement logic + formatted console output
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Structured logging (file + colored console)
├── logs/
│   └── trading_bot.log    # Auto-created on first run
├── .env                   # Environment variables (not committed)
├── .gitignore
├── cli.py                 # CLI entry point
├── requirements.txt
└── README.md
```

---

# Features

- Place MARKET orders
- Place LIMIT orders
- Place STOP_MARKET orders
- Signed Binance Futures API requests
- Structured logging
- Input validation
- Modular reusable architecture
- CLI interface using argparse
- Environment variable support via `.env`

---

# Setup

## 1. Generate Binance Futures Demo API Keys

1. Visit:

   https://testnet.binancefuture.com

2. Log in and open the Futures Demo dashboard

3. Go to API Management → Create API

4. Copy:
   - API Key
   - Secret Key

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_secret_key_here
```

---

# How to Run

## Place a MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

---

## Place a LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 50000
```

---

## Place a STOP_MARKET Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.001 --price 48000
```

---

## View CLI Help

```bash
python cli.py --help
```

---

# Example Output

```text
╔══════════════════════════════════════════════════╗
║      Binance Futures Testnet – Trading Bot      ║
╚══════════════════════════════════════════════════╝

INFO     CLI invoked: symbol=BTCUSDT side=BUY type=MARKET qty=0.001

──────────────────────────────────────────────────
  ORDER REQUEST SUMMARY
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
──────────────────────────────────────────────────

──────────────────────────────────────────────────
  ORDER RESPONSE
──────────────────────────────────────────────────
  Order ID   : 13172684998
  Status     : NEW
  Symbol     : BTCUSDT
  Executed   : 0.0000 BTC
  Avg Price  : 0.00
  Client OID : ayFYSkhKux9Hz9arzKBIgX
──────────────────────────────────────────────────

✅ Order placed successfully!
```

---

# Logging

All activity is written to:

```text
logs/trading_bot.log
```

Includes:
- API requests and responses
- Order execution details
- Validation errors
- Binance API errors
- Network exceptions

---

# Assumptions

- Uses Binance USDT-M Futures Demo/Testnet only
- Uses REST API requests via `requests`
- LIMIT orders use `GTC` by default
- STOP_MARKET uses `--price` as stop trigger price
- Each CLI execution places a single order
- No persistent database/state management

---

# Requirements

- Python 3.8+
- requests
- python-dotenv
- colorlog

---

# Security Notes

- API keys are loaded from `.env`
- `.env` is excluded via `.gitignore`
- Secret keys should never be committed to GitHub

---

# API Endpoint

```text
https://demo-fapi.binance.com
```