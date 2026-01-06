from typing import Optional, Dict, Any
from tools import mcp
from core.coinbase_requests_client import create_order as create_order_api

@mcp.tool()
def create_order(
    client_order_id: str, 
    product_id: str, 
    side: str, 
    order_configuration: Dict[str, Any],
    retail_portfolio_id: Optional[str] = None
) -> dict:
    """
    Create an order on Coinbase Advanced Trade API.
    
    This tool creates buy or sell orders with various order types including market orders,
    limit orders, stop orders, and more complex order configurations.
    
    Args:
        client_order_id: Unique client-generated order ID (UUID format recommended)
        product_id: The trading pair (e.g., 'BTC-USD', 'ETH-EUR')
        side: Order side - either 'BUY' or 'SELL'
        order_configuration: Order configuration object defining order type and parameters
        retail_portfolio_id: Optional retail portfolio ID for the order
    
    Returns:
        Dictionary containing order creation response with order details
        
    Example order_configuration for market order:
        {
            "market_market_ioc": {
                "quote_size": "10.00"  # Buy $10 worth
            }
        }
        
    Example order_configuration for limit order:
        {
            "limit_limit_gtc": {
                "base_size": "0.001",   # Buy 0.001 BTC
                "limit_price": "30000.00"
            }
        }
    """
    try:
        result = create_order_api(
            client_order_id=client_order_id,
            product_id=product_id,
            side=side,
            order_configuration=order_configuration,
            retail_portfolio_id=retail_portfolio_id
        )
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to create order: {result.get('error')}",
                "details": result
            }
        
        return {
            "status": "success", 
            "message": f"Order created successfully for {product_id}",
            "order_data": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating order: {str(e)}",
            "client_order_id": client_order_id,
            "product_id": product_id
        } 