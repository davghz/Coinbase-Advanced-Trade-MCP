from typing import List
from tools import mcp
from core.coinbase_requests_client import cancel_orders as cancel_orders_api

@mcp.tool()
def cancel_orders(order_ids: List[str]) -> dict:
    """
    Cancel multiple orders at once using Coinbase Advanced Trade API.
    
    This tool allows you to cancel one or more orders by providing their order IDs.
    It's useful for bulk order cancellation or canceling specific orders.
    
    Args:
        order_ids: List of order IDs to cancel (maximum 100 orders per request)
    
    Returns:
        Dictionary containing cancellation results and status for each order
        
    Example:
        >>> cancel_orders(["order-123", "order-456"])
        {
            "status": "success",
            "message": "Cancelled 2 orders successfully",
            "results": {...}
        }
    """
    try:
        if not order_ids:
            return {
                "status": "error",
                "message": "No order IDs provided for cancellation"
            }
            
        if len(order_ids) > 100:
            return {
                "status": "error", 
                "message": "Too many orders specified. Maximum 100 orders per request.",
                "provided_count": len(order_ids)
            }
        
        result = cancel_orders_api(order_ids)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to cancel orders: {result.get('error')}",
                "details": result,
                "order_ids": order_ids
            }
        
        return {
            "status": "success",
            "message": f"Attempted to cancel {len(order_ids)} orders",
            "order_ids": order_ids,
            "results": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error canceling orders: {str(e)}",
            "order_ids": order_ids
        } 