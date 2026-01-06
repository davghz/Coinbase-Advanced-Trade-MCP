from tools import mcp
from core.coinbase_requests_client import create_portfolio as create_portfolio_api

@mcp.tool()
def create_portfolio(name: str) -> dict:
    """
    Create a new portfolio on Coinbase Advanced Trade API.
    
    This tool creates a new portfolio with the specified name. Portfolios allow
    you to organize your assets and trading activity into separate groups.
    
    Args:
        name: The name for the new portfolio
    
    Returns:
        Dictionary containing the created portfolio details
        
    Example:
        >>> create_portfolio("My Trading Portfolio")
        {
            "status": "success",
            "message": "Portfolio created successfully",
            "portfolio": {
                "uuid": "xyz789-abc123-456",
                "name": "My Trading Portfolio",
                "type": "CONSUMER",
                "deleted": false
            }
        }
    """
    try:
        if not name or not name.strip():
            return {
                "status": "error",
                "message": "Portfolio name is required and cannot be empty"
            }
        
        result = create_portfolio_api(name.strip())
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to create portfolio: {result.get('error')}",
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Portfolio created successfully",
            "portfolio": result.get("portfolio", result)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating portfolio: {str(e)}",
            "name": name
        }
