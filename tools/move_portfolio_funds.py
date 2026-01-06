from tools import mcp
from core.coinbase_requests_client import move_portfolio_funds as move_portfolio_funds_api

@mcp.tool()
def move_portfolio_funds(
    source_portfolio_uuid: str,
    target_portfolio_uuid: str,
    currency: str,
    value: str
) -> dict:
    """
    Move funds between portfolios on Coinbase Advanced Trade API.
    
    This tool transfers funds from one portfolio to another. You must have
    transfer permissions for the source portfolio.
    
    Args:
        source_portfolio_uuid: UUID of the source portfolio
        target_portfolio_uuid: UUID of the target portfolio
        currency: Currency to transfer (e.g., 'USD', 'BTC', 'ETH')
        value: Amount to transfer as a string (e.g., '100.00')
    
    Returns:
        Dictionary containing the transfer result
        
    Example:
        >>> move_portfolio_funds(
        ...     "abc123-source-uuid",
        ...     "xyz789-target-uuid",
        ...     "USD",
        ...     "500.00"
        ... )
        {
            "status": "success",
            "message": "Funds moved successfully",
            "source_portfolio_uuid": "abc123-source-uuid",
            "target_portfolio_uuid": "xyz789-target-uuid",
            "funds": {"currency": "USD", "value": "500.00"}
        }
    """
    try:
        if not source_portfolio_uuid:
            return {
                "status": "error",
                "message": "Source portfolio UUID is required"
            }
        
        if not target_portfolio_uuid:
            return {
                "status": "error",
                "message": "Target portfolio UUID is required"
            }
        
        if not currency:
            return {
                "status": "error",
                "message": "Currency is required"
            }
        
        if not value:
            return {
                "status": "error",
                "message": "Value is required"
            }
        
        funds = {
            "value": value,
            "currency": currency.upper()
        }
        
        result = move_portfolio_funds_api(funds, source_portfolio_uuid, target_portfolio_uuid)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to move funds: {result.get('error')}",
                "source_portfolio_uuid": source_portfolio_uuid,
                "target_portfolio_uuid": target_portfolio_uuid,
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Funds moved successfully",
            "source_portfolio_uuid": source_portfolio_uuid,
            "target_portfolio_uuid": target_portfolio_uuid,
            "funds": funds,
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error moving funds: {str(e)}",
            "source_portfolio_uuid": source_portfolio_uuid,
            "target_portfolio_uuid": target_portfolio_uuid
        }
