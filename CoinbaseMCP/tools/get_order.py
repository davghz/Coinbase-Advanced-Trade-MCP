from tools import mcp
from core.coinbase_requests_client import get_order as get_order_api

@mcp.tool()
def get_order(order_id: str) -> dict:
    """
    Get details of a specific order by order ID from Coinbase Advanced Trade API.
    
    This tool retrieves comprehensive information about a single order including
    its status, filled amount, fees, timestamps, and order configuration.
    
    Args:
        order_id: The unique order ID to retrieve details for
    
    Returns:
        Dictionary containing detailed order information
        
    Example:
        >>> get_order("abc123-def456-789")
        {
            "status": "success",
            "message": "Order retrieved successfully",
            "order": {
                "order_id": "abc123-def456-789",
                "product_id": "BTC-USD",
                "side": "BUY",
                "order_configuration": {...},
                "status": "FILLED",
                ...
            }
        }
    """
    try:
        if not order_id:
            return {
                "status": "error",
                "message": "Order ID is required"
            }
        
        result = get_order_api(order_id)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve order: {result.get('error')}",
                "order_id": order_id,
                "details": result
            }
        
        return {
            "status": "success",
            "message": f"Order {order_id} retrieved successfully",
            "order_id": order_id,
            "order": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving order: {str(e)}",
            "order_id": order_id
        } 