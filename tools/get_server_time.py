from tools import mcp
from core.coinbase_requests_client import get_server_time as get_server_time_api

@mcp.tool()
def get_server_time() -> dict:
    """
    Get current server time from Coinbase Advanced Trade API.
    
    This tool retrieves the current server time in both Unix timestamp and ISO 8601 format.
    It's useful for synchronizing time-sensitive operations and ensuring accurate timestamps.
    This is a public endpoint that doesn't require authentication.
    
    Returns:
        Dictionary containing server time information
        
    Example:
        >>> get_server_time()
        {
            "status": "success", 
            "message": "Server time retrieved successfully",
            "server_time": {
                "iso": "2024-01-15T10:30:00Z",
                "epochSeconds": "1705316200",
                "epochMillis": "1705316200000"
            }
        }
    """
    try:
        result = get_server_time_api()
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve server time: {result.get('error')}",
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Server time retrieved successfully",
            "server_time": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving server time: {str(e)}"
        } 