from core.coinbase_requests_client import get_public_product as client_get_public_product
from . import mcp

@mcp.tool()
def get_public_product(
    product_id: str
) -> dict:
    """
    Get detailed information about a specific trading product from Coinbase Advanced Trade API (public endpoint).
    
    This is a public endpoint that doesn't require authentication and provides
    comprehensive details about a specific trading pair including price, volume,
    market data, and product configuration.
    
    Args:
        product_id: The product identifier (e.g., 'BTC-USD', 'ETH-EUR', 'DOGE-USDT')
    
    Returns:
        Dictionary containing detailed product information
        
    Example:
        >>> get_public_product("BTC-USD")
        {
            "status": "success",
            "message": "Public product BTC-USD retrieved successfully",
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
                "status": "online",
                "product_type": "SPOT",
                "quote_currency_id": "USD",
                "base_currency_id": "BTC",
                ...
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
        
        # Call the core client function
        result = client_get_public_product(product_id=product_id)
        
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
            "message": f"Public product {product_id} retrieved successfully",
            "product_id": product_id,
            "product": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get public product: {str(e)}",
            "details": "An unexpected error occurred while retrieving public product details"
        } 