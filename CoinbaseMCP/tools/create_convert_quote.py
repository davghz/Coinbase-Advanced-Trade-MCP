from core.coinbase_requests_client import create_convert_quote as client_create_convert_quote
from . import mcp

@mcp.tool()
def create_convert_quote(
    from_account: str,
    to_account: str,
    amount: str
) -> dict:
    """
    Create a convert quote for currency conversion on Coinbase Advanced Trade API.
    
    This tool generates a quote for converting one currency to another, showing
    the exchange rate, fees, and estimated conversion amount before executing.
    
    Args:
        from_account: Account ID to convert from (source currency account UUID)
        to_account: Account ID to convert to (destination currency account UUID)
        amount: Amount to convert (string representation of decimal)
    
    Returns:
        Dictionary containing convert quote details including rates and fees
        
    Example:
        >>> create_convert_quote("abc123-btc-account", "def456-usd-account", "0.001")
        {
            "status": "success",
            "message": "Convert quote created successfully",
            "from_account": "abc123-btc-account",
            "to_account": "def456-usd-account",
            "amount": "0.001",
            "quote": {
                "trade_id": "quote-789xyz",
                "from_currency": "BTC",
                "to_currency": "USD",
                "from_amount": "0.001",
                "to_amount": "45.23",
                "exchange_rate": "45230.00",
                "fee": "0.23",
                "expires_at": "2024-01-15T10:35:00Z"
            }
        }
    """
    try:
        # Validate inputs
        if not from_account or not isinstance(from_account, str):
            return {
                "status": "error",
                "message": "Invalid from_account parameter",
                "details": "from_account must be a non-empty string (account UUID)"
            }
        
        if not to_account or not isinstance(to_account, str):
            return {
                "status": "error",
                "message": "Invalid to_account parameter",
                "details": "to_account must be a non-empty string (account UUID)"
            }
        
        if not amount or not isinstance(amount, str):
            return {
                "status": "error",
                "message": "Invalid amount parameter",
                "details": "amount must be a non-empty string representing a decimal number"
            }
        
        # Validate amount is a valid number
        try:
            float(amount)
        except ValueError:
            return {
                "status": "error",
                "message": "Invalid amount format",
                "details": "amount must be a valid decimal number string"
            }
        
        # Call the core client function
        result = client_create_convert_quote(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )
        
        # Handle API errors
        if "error" in result:
            return {
                "status": "error",
                "message": f"API error: {result.get('error', 'Unknown error')}",
                "details": result.get("body", "No additional details"),
                "status_code": result.get("status_code")
            }
        
        return {
            "status": "success",
            "message": "Convert quote created successfully",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "quote": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create convert quote: {str(e)}",
            "details": "An unexpected error occurred while creating convert quote"
        } 