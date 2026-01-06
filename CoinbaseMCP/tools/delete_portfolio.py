from tools import mcp
from core.coinbase_requests_client import delete_portfolio as delete_portfolio_api

@mcp.tool()
def delete_portfolio(portfolio_uuid: str) -> dict:
    """
    Delete a portfolio on Coinbase Advanced Trade API.
    
    This tool deletes an existing portfolio. You must have trade permissions
    for the portfolio. Note: You cannot delete the default portfolio.
    
    Args:
        portfolio_uuid: UUID of the portfolio to delete
    
    Returns:
        Dictionary containing the deletion result
        
    Example:
        >>> delete_portfolio("abc123-def456-789")
        {
            "status": "success",
            "message": "Portfolio deleted successfully",
            "portfolio_uuid": "abc123-def456-789"
        }
    """
    try:
        if not portfolio_uuid:
            return {
                "status": "error",
                "message": "Portfolio UUID is required"
            }
        
        result = delete_portfolio_api(portfolio_uuid)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to delete portfolio: {result.get('error')}",
                "portfolio_uuid": portfolio_uuid,
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Portfolio deleted successfully",
            "portfolio_uuid": portfolio_uuid,
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting portfolio: {str(e)}",
            "portfolio_uuid": portfolio_uuid
        }
