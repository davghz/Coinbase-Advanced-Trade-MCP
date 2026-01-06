from core.coinbase_requests_client import commit_convert_trade as client_commit_convert_trade
from . import mcp

@mcp.tool()
def commit_convert_trade(
    trade_id: str,
    from_account: str,
    to_account: str,
    amount: str
) -> dict:
    """
    Commit a convert trade on Coinbase Advanced Trade API.
    
    This tool executes a currency conversion using a previously generated quote.
    The trade_id should come from a successful create_convert_quote call.
    
    Args:
        trade_id: The trade ID from the convert quote
        from_account: Account ID to convert from (source currency account UUID)
        to_account: Account ID to convert to (destination currency account UUID)
        amount: Amount to convert (string representation of decimal)
    
    Returns:
        Dictionary containing convert trade execution results
        
    Example:
        >>> commit_convert_trade("quote-789xyz", "abc123-btc-account", "def456-usd-account", "0.001")
        {
            "status": "success",
            "message": "Convert trade committed successfully",
            "trade_id": "quote-789xyz",
            "from_account": "abc123-btc-account",
            "to_account": "def456-usd-account",
            "amount": "0.001",
            "trade": {
                "id": "trade-completed-123",
                "status": "COMPLETED",
                "from_currency": "BTC",
                "to_currency": "USD",
                "from_amount": "0.001",
                "to_amount": "45.23",
                "exchange_rate": "45230.00",
                "fee": "0.23",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    """
    try:
        # Validate inputs
        if not trade_id or not isinstance(trade_id, str):
            return {
                "status": "error",
                "message": "Invalid trade_id parameter",
                "details": "trade_id must be a non-empty string from convert quote"
            }
        
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
        result = client_commit_convert_trade(
            trade_id=trade_id,
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
            "message": "Convert trade committed successfully",
            "trade_id": trade_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "trade": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to commit convert trade: {str(e)}",
            "details": "An unexpected error occurred while committing convert trade"
        } 