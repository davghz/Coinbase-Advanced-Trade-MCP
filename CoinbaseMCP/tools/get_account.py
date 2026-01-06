from typing import Optional
from tools import mcp
from core.coinbase_requests_client import list_accounts as fetch_accounts

@mcp.tool()
def get_account(currency: Optional[str] = None) -> dict:
    """
    Get a specific account by currency symbol (e.g., BTC, USDC, ETH).
    
    This tool retrieves detailed information about a specific cryptocurrency or fiat
    account in your Coinbase portfolio. It searches through all accounts to find
    the one matching the specified currency symbol.
    
    Args:
        currency: Currency symbol to search for (e.g., 'BTC', 'USDC', 'ETH', 'USD')
                 Case-insensitive. Required parameter.
    
    Returns:
        Dictionary containing account details or error if not found
        
    Example:
        >>> get_account("BTC")
        {
            "uuid": "abc123-def456-789",
            "name": "Bitcoin Wallet",
            "currency": "BTC",
            "available_balance": {"value": "0.00001654", "currency": "BTC"},
            "hold": {"value": "0.0", "currency": "BTC"},
            "type": "ACCOUNT_TYPE_CRYPTO"
        }
    """
    if not currency:
        return {
            "error": "Currency parameter is required. Please specify a currency symbol (e.g., BTC, USDC, ETH)"
        }
    
    try:
        response = fetch_accounts()
        
        # Check for errors in response
        if "error" in response:
            return {
                "error": f"API Error: {response['error']}",
                "currency": currency.upper()
            }
        
        accounts = response.get("accounts", [])
        currency_upper = currency.upper()
        
        # Search for account with matching currency
        matching_accounts = [
            acct for acct in accounts 
            if acct.get("currency", "").upper() == currency_upper
        ]
        
        if not matching_accounts:
            return {
                "error": f"No account found for {currency_upper}. Available currencies: {', '.join(sorted(set(acct.get('currency', '') for acct in accounts)))}",
                "currency": currency_upper
            }
        
        # Return the first matching account (there should typically be only one per currency)
        account = matching_accounts[0]
        
        return {
            "uuid": account.get("uuid"),
            "name": account.get("name"),
            "currency": account.get("currency"),
            "available_balance": account.get("available_balance", {}),
            "hold": account.get("hold", {}),
            "type": account.get("type"),
            "created_at": account.get("created_at"),
            "updated_at": account.get("updated_at")
        }
        
    except Exception as e:
        return {
            "error": f"Failed to fetch account for {currency}: {str(e)}",
            "currency": currency.upper() if currency else None
        } 