# Binance Futures Trading Bot

A robust command-line trading bot for the Binance Futures Testnet executing MARKET, LIMIT, and STOP_LIMIT orders.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![License MIT](https://img.shields.io/badge/License-MIT-green)
![Status Testnet](https://img.shields.io/badge/Status-Testnet-orange)
![Vibe Coded](https://img.shields.io/badge/Vibe-Coded-blueviolet)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Binance Testnet API Key Setup](#binance-testnet-api-key-setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Logging](#logging)
- [How This Was Built — Multi-Agent AI Pipeline](#-how-this-was-built--multi-agent-ai-pipeline)
- [Assumptions & Notes](#assumptions--notes)
- [License](#license)

## Overview

This bot provides a command-line interface to place trades on the Binance Futures Testnet. It supports robust validation and secure execution of MARKET, LIMIT, and STOP_LIMIT orders. Built with Python, it is designed for testing algorithmic strategies or manual trades without risking real capital.

## Features

- MARKET/LIMIT/STOP_LIMIT orders
- Typer CLI
- HMAC-SHA256 signing
- Rotating file logging
- Input validation
- Error handling
- Vibe Coded

## Prerequisites

- Python 3.10 or higher
- A Binance Futures Testnet account
- Testnet API Key and Secret

## Binance Testnet API Key Setup

Step 1: Go to <https://testnet.binancefuture.com>
Step 2: Click "Log In" → register with email or GitHub
Step 3: After login, click your avatar → "API Management" → "Create API"
Step 4: Copy the API Key and Secret Key shown — the Secret is shown ONCE
Step 5: Testnet keys have no IP restrictions needed; no need to whitelist

## Installation

```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
pip install -r requirements.txt
```

## Configuration

Export environment variables (do NOT hardcode):

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

Note for Windows (PowerShell):

```powershell
$env:BINANCE_API_KEY="your_testnet_api_key"
$env:BINANCE_API_SECRET="your_testnet_api_secret"
```

## Usage

```
Usage: python cli.py [OPTIONS] SYMBOL SIDE ORDER_TYPE QUANTITY

  Place a trade order on Binance Futures Testnet.

Arguments:
  SYMBOL      Symbol (e.g. BTCUSDT)  [required]
  SIDE        Side (BUY or SELL)  [required]
  ORDER_TYPE  Order type (MARKET, LIMIT, STOP_LIMIT)  [required]
  QUANTITY    Quantity to trade  [required]

Options:
  --price FLOAT       Price for LIMIT or STOP_LIMIT orders
  --stop-price FLOAT  Stop price for STOP_LIMIT orders
  --help              Show this message and exit.
```

### Example 1 — MARKET order

```bash
python cli.py BTCUSDT BUY MARKET 0.001
```

Expected Output:

```
┌─────────────────────────────────────┐
│         ORDER REQUEST SUMMARY       │
├─────────────────────────────────────┤
│  Symbol     : BTCUSDT               │
│  Side       : BUY                   │
│  Type       : MARKET                │
│  Quantity   : 0.001                 │
│  Price      : N/A                   │
│  Stop Price : N/A                   │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│            ORDER RESPONSE           │
├─────────────────────────────────────┤
│  Order ID   : 3412567890            │
│  Status     : FILLED                │
│  Exec. Qty  : 0.001                 │
│  Avg Price  : 34000.00              │
└─────────────────────────────────────┘
✓ Order placed successfully.
```

### Example 2 — LIMIT order

```bash
python cli.py BTCUSDT SELL LIMIT 0.001 --price 35000.0
```

Expected Output:

```
┌─────────────────────────────────────┐
│         ORDER REQUEST SUMMARY       │
├─────────────────────────────────────┤
│  Symbol     : BTCUSDT               │
│  Side       : SELL                  │
│  Type       : LIMIT                 │
│  Quantity   : 0.001                 │
│  Price      : 35000.0               │
│  Stop Price : N/A                   │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│            ORDER RESPONSE           │
├─────────────────────────────────────┤
│  Order ID   : 3412567891            │
│  Status     : NEW                   │
│  Exec. Qty  : 0.0                   │
│  Avg Price  : 0.0                   │
└─────────────────────────────────────┘
✓ Order placed successfully.
```

### Example 3 — STOP_LIMIT order (bonus)

```bash
python cli.py BTCUSDT SELL STOP_LIMIT 0.001 --price 34500.0 --stop-price 35000.0
```

Expected Output:

```
┌─────────────────────────────────────┐
│         ORDER REQUEST SUMMARY       │
├─────────────────────────────────────┤
│  Symbol     : BTCUSDT               │
│  Side       : SELL                  │
│  Type       : STOP_LIMIT            │
│  Quantity   : 0.001                 │
│  Price      : 34500.0               │
│  Stop Price : 35000.0               │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│            ORDER RESPONSE           │
├─────────────────────────────────────┤
│  Order ID   : 3412567892            │
│  Status     : NEW                   │
│  Exec. Qty  : 0.0                   │
│  Avg Price  : 0.0                   │
└─────────────────────────────────────┘
✓ Order placed successfully.
```

## Project Structure

```text
trading_bot/
├── cli.py               # Typer CLI entrypoint
├── bot/                 # Core bot package
│   ├── __init__.py      # Package exports
│   ├── client.py        # BinanceClient and HMAC-SHA256 signing
│   ├── orders.py        # High-level order logic 
│   ├── validators.py    # Input validation rules
│   └── logging_config.py# Rotating file logging setup
├── requirements.txt     # Pinned Python dependencies
└── README.md            # This documentation file
```

## Logging

The bot records trading activity to the log file located at `logs/trading_bot.log`. It uses a rotation policy that limits files to 5MB and keeps up to 3 backups. The log format includes timestamps, log level, module name, and messages.

It logs requests, responses, and errors.
Example log lines:

```text
2025-01-15 14:23:01,482 | INFO | client | Placing order: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': '0.001'}
2025-01-15 14:23:02,103 | INFO | client | Response: {'orderId': 3412567890, 'status': 'FILLED', 'executedQty': '0.001', 'avgPrice': '34000.00'}
2025-01-15 14:23:02,150 | ERROR | client | Binance API error: code=-2011, msg=Unknown order sent.
```

## How This Was Built — Multi-Agent AI Pipeline

This project was built using a Blackboard Architecture, where multiple specialised AI agents collaborate exclusively through a shared coordination document (`blackboard.md`). This approach enforces strict isolation and prevents uncoordinated agent interactions, ensuring predictable and verifiable development.

```text
  [Orchestrator]
        │ (Defines Tasks)
        ▼
  [Blackboard] ◀── [Agent 2: Core Coder]
        ▲      ◀── [Agent 3: CLI Coder]
        │      ◀── [Agent 4: Docs + Runner]
        └──────◀── [Agent 5: Verifier]
```

- **Agent 1 — Orchestrator**: Designed the implementation plan, defined the blackboard schema, and assigned scoped tasks without writing application code.
- **Agent 2 — Core Coder**: Implemented the foundational `bot/` package, including the Binance API client, HMAC-SHA256 signing, validation rules, and logging.
- **Agent 3 — CLI Coder**: Built the Typer-based command-line interface, securely wiring user inputs to the core execution logic via environment variables.
- **Agent 4 — Docs + Runner**: Authored the project documentation and executed live testnet trades to capture verifiable order logs.
- **Agent 5 — Verifier**: Audited all agent outputs against a 51-point checklist to guarantee protocol compliance, security, and functional completeness.

This architecture demonstrates the effectiveness of a strict two-write protocol to maintain a clear separation of concerns, resulting in highly reproducible and verifiable software outputs.

## Assumptions & Notes

- Testnet only; do not use production API keys
- Quantity/price precision depends on symbol; BTCUSDT testnet accepts 0.001 BTC minimum
- STOP_LIMIT uses Binance STOP order type internally on testnet

## License

MIT
