from tools import mcp
from core.coinbase_requests_client import list_portfolios as list_portfolios_api

@mcp.tool()
def list_portfolios() -> dict:
    """
    List all portfolios from Coinbase Advanced Trade API.
    
    This tool retrieves all portfolios associated with your account,
    including the default portfolio and any custom portfolios you've created.
    
    Returns:
        Dictionary containing list of portfolios with their details
        
    Example:
        >>> list_portfolios()
        {
            "status": "success",
            "message": "Retrieved 2 portfolios",
            "portfolios": [
                {
                    "uuid": "abc123-def456-789",
                    "name": "Default",
                    "type": "DEFAULT",
                    "deleted": false
                },
                {
                    "uuid": "xyz789-abc123-456",
                    "name": "Trading Portfolio",
                    "type": "CONSUMER",
                    "deleted": false
                }
            ]
        }
    """
    try:
        result = list_portfolios_api()
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve portfolios: {result.get('error')}",
                "details": result
            }
        
        portfolios = result.get("portfolios", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(portfolios)} portfolios",
            "portfolios_count": len(portfolios),
            "portfolios": portfolios
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving portfolios: {str(e)}"
        }
