from typing import Optional, Dict, Any
from core.coinbase_requests_client import preview_order as client_preview_order
from . import mcp

@mcp.tool()
def preview_order(
    product_id: str,
    side: str,
    order_configuration: Dict[str, Any],
    commission_rate: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Preview an order before placing it on Coinbase Advanced Trade API.
    
    This tool allows you to preview the details of an order including estimated
    fees, total cost, and other order parameters before actually placing the order.
    
    Args:
        product_id: The trading pair (e.g., 'BTC-USD', 'ETH-EUR')
        side: Order side - either 'BUY' or 'SELL'
        order_configuration: Order configuration object defining order type and parameters
        commission_rate: Optional commission rate override
    
    Returns:
        Dictionary containing order preview details including fees and totals
        
    Example order_configuration for limit order preview:
        {
            "limit_limit_gtc": {
                "base_size": "0.001",
                "limit_price": "30000.00"
            }
        }
        
    Example:
        >>> preview_order("BTC-USD", "BUY", {"limit_limit_gtc": {"base_size": "0.001", "limit_price": "30000.00"}})
        {
            "status": "success",
            "message": "Order preview generated successfully",
            "product_id": "BTC-USD",
            "side": "BUY",
            "preview": {
                "order_total": "30.03",
                "commission_total": "0.03",
                "errs": [],
                "warning": [],
                "quote_size": "30.00",
                "base_size": "0.001",
                "best_bid": "29950.00",
                "best_ask": "30050.00",
                "is_max": false
            }
        }
    """
    try:
        # Validate inputs
        if not product_id or not isinstance(product_id, str):
            return {
                "status": "error",
                "message": "Invalid product_id parameter",
                "details": "product_id must be a non-empty string"
            }
        
        if side.upper() not in ["BUY", "SELL"]:
            return {
                "status": "error", 
                "message": "Invalid side parameter",
                "details": "side must be either 'BUY' or 'SELL'"
            }
        
        if not order_configuration or not isinstance(order_configuration, dict):
            return {
                "status": "error",
                "message": "Invalid order_configuration parameter", 
                "details": "order_configuration must be a non-empty dictionary"
            }
        
        # Call the core client function
        result = client_preview_order(
            product_id=product_id,
            side=side,
            order_configuration=order_configuration,
            commission_rate=commission_rate
        )
        
        # Handle API errors
        if "error" in result:
            return {
                "status": "error",
                "message": f"API error: {result.get('error', 'Unknown error')}",
                "details": result.get("body", "No additional details"),
                "status_code": result.get("status_code")
            }
        
        return {
            "status": "success",
            "message": f"Order preview generated successfully for {product_id}",
            "product_id": product_id,
            "side": side.upper(),
            "preview": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to preview order: {str(e)}",
            "details": "An unexpected error occurred while previewing the order"
        } 