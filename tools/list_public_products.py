from typing import Optional, List
from core.coinbase_requests_client import list_public_products as client_list_public_products
from . import mcp

@mcp.tool()
def list_public_products(
    product_type: Optional[str] = None,
    product_ids: Optional[List[str]] = None
) -> dict:
    """
    List all available trading products from Coinbase Advanced Trade API (public endpoint).
    
    This is a public endpoint that doesn't require authentication and provides
    information about all available trading pairs and products with market data.
    
    Args:
        product_type: Optional filter by product type (e.g., 'SPOT', 'FUTURE')
        product_ids: Optional list of specific product IDs to retrieve
    
    Returns:
        Dictionary containing products list with details about each trading pair
        
    Example:
        >>> list_public_products(product_type="SPOT")
        {
            "status": "success",
            "message": "Retrieved 150 public products",
            "filters": {"product_type": "SPOT"},
            "products_count": 150,
            "products": [
                {
                    "product_id": "BTC-USD",
                    "price": "45000.00",
                    "price_percentage_change_24h": "2.5",
                    "volume_24h": "1234567.89",
                    "base_currency_id": "BTC",
                    "quote_currency_id": "USD",
                    "base_name": "Bitcoin",
                    "quote_name": "US Dollar",
                    "status": "online",
                    "product_type": "SPOT",
                    ...
                }
            ]
        }
    """
    try:
        # Validate product_type if provided
        if product_type is not None and not isinstance(product_type, str):
            return {
                "status": "error",
                "message": "Invalid product_type parameter",
                "details": "product_type must be a string if provided"
            }
        
        # Validate product_ids if provided
        if product_ids is not None:
            if not isinstance(product_ids, list) or not all(isinstance(pid, str) for pid in product_ids):
                return {
                    "status": "error",
                    "message": "Invalid product_ids parameter",
                    "details": "product_ids must be a list of strings if provided"
                }
        
        # Call the core client function
        result = client_list_public_products(
            product_type=product_type,
            product_ids=product_ids
        )
        
        # Handle API errors
        if "error" in result:
            return {
                "status": "error",
                "message": f"API error: {result.get('error', 'Unknown error')}",
                "details": result.get("body", "No additional details"),
                "status_code": result.get("status_code")
            }
        
        # Build filters object
        filters = {}
        if product_type:
            filters["product_type"] = product_type
        if product_ids:
            filters["product_ids"] = product_ids
        
        products = result.get("products", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(products)} public products",
            "filters": filters,
            "products_count": len(products),
            "products": products
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list public products: {str(e)}",
            "details": "An unexpected error occurred while retrieving public products"
        } 