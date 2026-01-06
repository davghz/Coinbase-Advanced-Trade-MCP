# Coinbase MCP Server

A Model Context Protocol (MCP) server for Coinbase Advanced Trade. Provides AI agents with 30+ tools for secure trading, portfolio management, and market analysis. Modular architecture with Pydantic type safety and efficient async execution. Ready for agentic workflows.

## Features

- **Account Management**: List accounts, get account details
- **Order Management**: Create, cancel, preview orders, list fills
- **Market Data**: Products, candles, order book, best bid/ask, market trades

## Prerequisites

- Python 3.10+
- Coinbase Advanced Trade API credentials (CDP API Key)

## Installation

1. **Extract the zip file:**
   ```bash
   unzip Coinbase-Advanced-Trade-MCP-main.zip
   cd Coinbase-Advanced-Trade-main
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API credentials** (see below)

## Getting Coinbase API Credentials

1. Go to [Coinbase Developer Platform](https://portal.cdp.coinbase.com/)

2. Sign in with your Coinbase account

3. Create a new API key:
   - Click "Create API Key"
   - Select "Advanced Trade API"
   - Choose permissions:
     - `view` - For read-only operations (accounts, products, orders)
     - `trade` - For creating/canceling orders
     - `transfer` - For moving funds between portfolios
   
4. **Important**: Select **Ed25519** as the key type (not ECDSA)

5. Download the JSON file containing your credentials

6. From the JSON file, you need:
   - `name` → This is your `COINBASE_KEY_ID`
   - `privateKey` → This is your `COINBASE_ED25519_KEY` (base64 encoded)

## Configuration

Create a `.env` file in the server directory:

```bash
# Coinbase API Credentials
COINBASE_KEY_ID=organizations/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/apiKeys/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
COINBASE_ED25519_KEY=your_base64_encoded_private_key_here
```

**Example** (with fake values):
```bash
COINBASE_KEY_ID=organizations/abc12345-1234-5678-9abc-def012345678/apiKeys/key12345-1234-5678-9abc-def012345678
COINBASE_ED25519_KEY=MC4CAQAwBQYDK2VwBCIEIGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## MCP Configuration

### For Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "atlas-coinbase": {
      "command": "python3",
      "args": ["/path/to/atlas-mcp-server/main_stdio.py"],
      "env": {},
      "disabled": false,
      "autoApprove": ["list_accounts", "list_products", "get_best_bid_ask"]
    }
  }
}
```

### For Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "atlas-coinbase": {
      "command": "python3",
      "args": ["/path/to/atlas-mcp-server/main_stdio.py"]
    }
  }
}
```

### For Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "atlas-coinbase": {
      "command": "python3",
      "args": ["/path/to/atlas-mcp-server/main_stdio.py"]
    }
  }
}
```

## Available Tools (34 total)

### Account Management
| Tool | Description |
|------|-------------|
| `list_accounts` | List all accounts with balances |
| `get_account` | Get specific account by currency |

### Order Management
| Tool | Description |
|------|-------------|
| `create_order` | Create buy/sell orders |
| `cancel_orders` | Cancel one or more orders |
| `list_orders` | List historical orders |
| `get_order` | Get order details by ID |
| `preview_order` | Preview order before placing |
| `get_historical_fills` | Get completed trades |
| `execute_twap_order` | Execute time-weighted average price order |

### Market Data
| Tool | Description |
|------|-------------|
| `list_products` | List all trading pairs |
| `get_product` | Get product details |
| `get_product_candles` | Get OHLCV candlestick data |
| `get_product_book` | Get order book |
| `get_best_bid_ask` | Get current bid/ask prices |
| `get_market_trades` | Get recent trades |

### Public Endpoints (No Auth Required)
| Tool | Description |
|------|-------------|
| `list_public_products` | List products (public) |
| `get_public_product` | Get product (public) |
| `get_public_candles` | Get candles (public) |
| `get_public_product_book` | Get order book (public) |
| `get_public_market_trades` | Get trades (public) |
| `get_server_time` | Get server time |

### Portfolio Management
| Tool | Description |
|------|-------------|
| `list_portfolios` | List all portfolios |
| `create_portfolio` | Create new portfolio |
| `get_portfolio_breakdown` | Get portfolio details |
| `edit_portfolio` | Rename portfolio |
| `delete_portfolio` | Delete portfolio |
| `move_portfolio_funds` | Transfer between portfolios |

### Payment Methods
| Tool | Description |
|------|-------------|
| `list_payment_methods` | List payment methods |
| `get_payment_method` | Get payment method details |

### Convert
| Tool | Description |
|------|-------------|
| `create_convert_quote` | Get conversion quote |
| `commit_convert_trade` | Execute conversion |
| `get_convert_trade` | Get conversion details |

### Other
| Tool | Description |
|------|-------------|
| `get_transactions_summary` | Get transaction summary |
| `get_api_key_permissions` | Check API key permissions |

## Testing

Test the server is working:

```bash
python3 -c "from tools import mcp; import asyncio; print(len(asyncio.run(mcp.get_tools())), 'tools loaded')"
```

Test API connection:

```bash
python3 -c "from core.coinbase_requests_client import get_server_time; print(get_server_time())"
```

## Troubleshooting

### "Invalid JWT" or "Unauthorized" errors
- Verify your `COINBASE_KEY_ID` matches exactly from the JSON file
- Ensure `COINBASE_ED25519_KEY` is the complete base64 string
- Check that you selected Ed25519 (not ECDSA) when creating the key

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.10+

### Tools not loading
- Check for import errors: `python3 -c "from tools import mcp"`
- Some optional tools may fail if dependencies aren't installed (this is OK)

## Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore`
- Use environment variables in production
- Limit API key permissions to only what you need

## License

MIT
