from tools import mcp
from core.coinbase_requests_client import get_product as get_product_api

@mcp.tool()
def get_product(product_id: str) -> dict:
    """
    Get detailed information about a specific trading product from Coinbase Advanced Trade API.
    
    This tool retrieves comprehensive details about a specific trading pair including
    price, volume, market data, trading parameters, and product configuration.
    
    Args:
        product_id: The product identifier (e.g., 'BTC-USD', 'ETH-EUR', 'DOGE-USDT')
    
    Returns:
        Dictionary containing detailed product information
        
    Example:
        >>> get_product("BTC-USD")
        {
            "status": "success",
            "message": "Product BTC-USD retrieved successfully",
            "product_id": "BTC-USD",
            "product": {
                "product_id": "BTC-USD",
                "price": "45000.00",
                "price_percentage_change_24h": "2.5",
                "volume_24h": "1234567.89",
                "volume_percentage_change_24h": "5.2",
                "base_increment": "0.00000001",
                "quote_increment": "0.01",
                "quote_min_size": "1.00",
                "quote_max_size": "1000000.00",
                "base_min_size": "0.00001",
                "base_max_size": "100.00",
                "base_name": "Bitcoin",
                "quote_name": "US Dollar",
                "watched": false,
                "is_disabled": false,
                "new": false,
                "status": "online",
                "cancel_only": false,
                "limit_only": false,
                "post_only": false,
                "trading_disabled": false,
                "auction_mode": false,
                "product_type": "SPOT",
                "quote_currency_id": "USD",
                "base_currency_id": "BTC",
                ...
            }
        }
    """
    try:
        if not product_id:
            return {
                "status": "error",
                "message": "Product ID is required"
            }
        
        result = get_product_api(product_id)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve product: {result.get('error')}",
                "product_id": product_id,
                "details": result
            }
        
        return {
            "status": "success",
            "message": f"Product {product_id} retrieved successfully",
            "product_id": product_id,
            "product": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving product: {str(e)}",
            "product_id": product_id
        } 