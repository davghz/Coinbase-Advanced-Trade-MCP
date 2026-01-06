from typing import Optional
from tools import mcp
from core.coinbase_requests_client import list_accounts as fetch_accounts

@mcp.tool()
def list_accounts(currency: Optional[str] = None) -> dict:
    """
    List all accounts (portfolio overview) or filter by currency symbol.
    
    This tool provides access to your Coinbase portfolio, showing all available accounts
    with their balances, currencies, and account details. You can optionally filter
    to show only accounts for a specific currency.
    
    Args:
        currency: Optional currency symbol to filter accounts (e.g., 'BTC', 'USD', 'ETH')
    
    Returns:
        Dictionary containing currency filter and balances array with account details
        
    Example:
        >>> list_accounts()
        {
            "currency": "ALL",
            "accounts_count": 5,
            "balances": [
                {
                    "uuid": "abc123-def456-789",
                    "name": "Bitcoin Wallet",
                    "currency": "BTC",
                    "available_balance": {"value": "0.001", "currency": "BTC"},
                    "hold": {"value": "0.0", "currency": "BTC"}
                }
            ]
        }
    """
    try:
        response = fetch_accounts()
        
        # Check for errors in response
        if "error" in response:
            return {
                "error": f"API Error: {response['error']}",
                "currency": currency or "ALL",
                "accounts_count": 0,
                "balances": []
            }
        
        accounts = response.get("accounts", [])
        
        # Filter by currency if specified
        if currency:
            currency_upper = currency.upper()
            filtered_accounts = [
                acct for acct in accounts 
                if acct.get("currency", "").upper() == currency_upper
            ]
            result = filtered_accounts
        else:
            result = accounts

        return {
            "currency": currency or "ALL",
            "accounts_count": len(result),
            "balances": result
        }

    except Exception as e:
        return {
            "error": f"Failed to fetch accounts: {str(e)}",
            "currency": currency or "ALL",
            "accounts_count": 0,
            "balances": []
        } 