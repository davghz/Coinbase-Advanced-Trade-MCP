from core.coinbase_requests_client import get_convert_trade as client_get_convert_trade
from . import mcp

@mcp.tool()
def get_convert_trade(
    trade_id: str,
    from_account: str,
    to_account: str
) -> dict:
    """
    Get convert trade details from Coinbase Advanced Trade API.
    
    This tool retrieves the details of a specific convert trade using the trade ID
    and account information. Useful for checking the status and details of conversions.
    
    Args:
        trade_id: The trade ID of the convert trade to retrieve
        from_account: Account ID that was converted from (source currency account UUID)
        to_account: Account ID that was converted to (destination currency account UUID)
    
    Returns:
        Dictionary containing convert trade details and status
        
    Example:
        >>> get_convert_trade("trade-completed-123", "abc123-btc-account", "def456-usd-account")
        {
            "status": "success",
            "message": "Convert trade details retrieved successfully",
            "trade_id": "trade-completed-123",
            "from_account": "abc123-btc-account",
            "to_account": "def456-usd-account",
            "trade": {
                "id": "trade-completed-123",
                "status": "COMPLETED",
                "from_currency": "BTC",
                "to_currency": "USD",
                "from_amount": "0.001",
                "to_amount": "45.23",
                "exchange_rate": "45230.00",
                "fee": "0.23",
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": "2024-01-15T10:30:05Z"
            }
        }
    """
    try:
        # Validate inputs
        if not trade_id or not isinstance(trade_id, str):
            return {
                "status": "error",
                "message": "Invalid trade_id parameter",
                "details": "trade_id must be a non-empty string"
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
        
        # Call the core client function
        result = client_get_convert_trade(
            trade_id=trade_id,
            from_account=from_account,
            to_account=to_account
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
            "message": "Convert trade details retrieved successfully",
            "trade_id": trade_id,
            "from_account": from_account,
            "to_account": to_account,
            "trade": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get convert trade: {str(e)}",
            "details": "An unexpected error occurred while retrieving convert trade details"
        } 