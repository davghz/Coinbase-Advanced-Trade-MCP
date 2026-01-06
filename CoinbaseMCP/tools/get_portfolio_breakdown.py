from tools import mcp
from core.coinbase_requests_client import get_portfolio_breakdown as get_portfolio_breakdown_api

@mcp.tool()
def get_portfolio_breakdown(portfolio_uuid: str) -> dict:
    """
    Get detailed breakdown of a specific portfolio from Coinbase Advanced Trade API.
    
    This tool retrieves comprehensive information about a portfolio including
    its assets, balances, and allocation breakdown.
    
    Args:
        portfolio_uuid: The UUID of the portfolio to retrieve
    
    Returns:
        Dictionary containing portfolio breakdown details
        
    Example:
        >>> get_portfolio_breakdown("abc123-def456-789")
        {
            "status": "success",
            "message": "Portfolio breakdown retrieved successfully",
            "portfolio_uuid": "abc123-def456-789",
            "breakdown": {
                "portfolio": {
                    "uuid": "abc123-def456-789",
                    "name": "Default",
                    "type": "DEFAULT"
                },
                "portfolio_balances": {
                    "total_balance": {"value": "10000.00", "currency": "USD"},
                    "total_futures_balance": {"value": "0.00", "currency": "USD"}
                },
                "spot_positions": [...],
                "perp_positions": [...]
            }
        }
    """
    try:
        if not portfolio_uuid:
            return {
                "status": "error",
                "message": "Portfolio UUID is required"
            }
        
        result = get_portfolio_breakdown_api(portfolio_uuid)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve portfolio breakdown: {result.get('error')}",
                "portfolio_uuid": portfolio_uuid,
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Portfolio breakdown retrieved successfully",
            "portfolio_uuid": portfolio_uuid,
            "breakdown": result.get("breakdown", result)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving portfolio breakdown: {str(e)}",
            "portfolio_uuid": portfolio_uuid
        }
