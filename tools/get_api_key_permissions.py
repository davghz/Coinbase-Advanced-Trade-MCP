from tools import mcp
from core.coinbase_requests_client import get_api_key_permissions as get_api_key_permissions_api

@mcp.tool()
def get_api_key_permissions() -> dict:
    """
    Get API key permissions from Coinbase Advanced Trade API.
    
    This tool retrieves the permissions and capabilities associated with the current API key,
    showing what actions are allowed (view, trade, transfer) and any restrictions.
    
    Returns:
        Dictionary containing API key permissions and capabilities
        
    Example:
        >>> get_api_key_permissions()
        {
            "status": "success",
            "message": "API key permissions retrieved successfully",
            "permissions": {
                "can_view": true,
                "can_trade": true,
                "can_transfer": false,
                "portfolio_id": "abc123-def456-789",
                "portfolio_uuid": "abc123-def456-789",
                "user_id": "user123",
                "restrictions": []
            }
        }
    """
    try:
        result = get_api_key_permissions_api()
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve API key permissions: {result.get('error')}",
                "details": result
            }
        
        return {
            "status": "success",
            "message": "API key permissions retrieved successfully",
            "permissions": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving API key permissions: {str(e)}"
        } 