from tools import mcp
from core.coinbase_requests_client import edit_portfolio as edit_portfolio_api

@mcp.tool()
def edit_portfolio(portfolio_uuid: str, name: str) -> dict:
    """
    Edit a portfolio's name on Coinbase Advanced Trade API.
    
    This tool updates the name of an existing portfolio. You must have
    trade permissions for the portfolio.
    
    Args:
        portfolio_uuid: UUID of the portfolio to edit
        name: New name for the portfolio
    
    Returns:
        Dictionary containing the updated portfolio details
        
    Example:
        >>> edit_portfolio("abc123-def456-789", "My Updated Portfolio")
        {
            "status": "success",
            "message": "Portfolio updated successfully",
            "portfolio": {
                "uuid": "abc123-def456-789",
                "name": "My Updated Portfolio",
                "type": "CONSUMER",
                "deleted": false
            }
        }
    """
    try:
        if not portfolio_uuid:
            return {
                "status": "error",
                "message": "Portfolio UUID is required"
            }
        
        if not name or not name.strip():
            return {
                "status": "error",
                "message": "Portfolio name is required and cannot be empty"
            }
        
        result = edit_portfolio_api(portfolio_uuid, name.strip())
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to edit portfolio: {result.get('error')}",
                "portfolio_uuid": portfolio_uuid,
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Portfolio updated successfully",
            "portfolio": result.get("portfolio", result)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error editing portfolio: {str(e)}",
            "portfolio_uuid": portfolio_uuid
        }
