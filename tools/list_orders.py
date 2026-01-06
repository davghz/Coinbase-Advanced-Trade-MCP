from typing import Optional
from tools import mcp
from core.coinbase_requests_client import list_orders as list_orders_api

@mcp.tool()
def list_orders(
    product_id: Optional[str] = None, 
    order_status: Optional[str] = None, 
    limit: int = 100, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> dict:
    """
    List historical orders with optional filtering from Coinbase Advanced Trade API.
    
    This tool retrieves your order history with various filtering options including
    product, status, date range, and pagination controls.
    
    Args:
        product_id: Optional product to filter orders (e.g., 'BTC-USD', 'ETH-EUR')
        order_status: Optional status filter ('OPEN', 'FILLED', 'CANCELLED', 'EXPIRED', 'FAILED')
        limit: Number of orders to retrieve (default: 100, max: 1000)
        start_date: Start date in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')
        end_date: End date in ISO 8601 format (e.g., '2024-01-31T23:59:59Z')
    
    Returns:
        Dictionary containing orders list with filtering parameters and order details
        
    Example:
        >>> list_orders(product_id="BTC-USD", order_status="FILLED", limit=10)
        {
            "status": "success",
            "filters": {...},
            "orders": [...],
            "orders_count": 10
        }
    """
    try:
        # Validate parameters
        if limit > 1000:
            return {
                "status": "error",
                "message": "Limit cannot exceed 1000 orders per request",
                "provided_limit": limit
            }
            
        valid_statuses = ['OPEN', 'FILLED', 'CANCELLED', 'EXPIRED', 'FAILED']
        if order_status and order_status.upper() not in valid_statuses:
            return {
                "status": "error",
                "message": f"Invalid order status. Must be one of: {', '.join(valid_statuses)}",
                "provided_status": order_status
            }
        
        result = list_orders_api(
            product_id=product_id,
            order_status=order_status,
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve orders: {result.get('error')}",
                "details": result
            }
        
        orders = result.get("orders", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(orders)} orders",
            "filters": {
                "product_id": product_id,
                "order_status": order_status,
                "limit": limit,
                "start_date": start_date,
                "end_date": end_date
            },
            "orders_count": len(orders),
            "orders": orders
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving orders: {str(e)}",
            "filters": {
                "product_id": product_id,
                "order_status": order_status,
                "limit": limit
            }
        } 