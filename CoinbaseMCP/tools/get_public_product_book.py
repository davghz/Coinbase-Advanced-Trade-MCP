from typing import Optional
from core.coinbase_requests_client import get_public_product_book as client_get_public_product_book
from . import mcp

@mcp.tool()
def get_public_product_book(
    product_id: str,
    limit: Optional[int] = None
) -> dict:
    """
    Get public order book (Level 2 data) for a product from Coinbase Advanced Trade API.
    
    This is a public endpoint that doesn't require authentication and provides
    real-time order book data including bids and asks with prices and sizes.
    
    Args:
        product_id: The trading pair (e.g., 'BTC-USD', 'ETH-EUR')
        limit: Number of bids and asks to return (min: 1, max: 250, default: 250)
    
    Returns:
        Dictionary containing order book data with bids and asks
        
    Example:
        >>> get_public_product_book("BTC-USD", 10)
        {
            "status": "success",
            "message": "Public order book retrieved successfully for BTC-USD",
            "product_id": "BTC-USD",
            "limit": 10,
            "order_book": {
                "pricebook": {
                    "product_id": "BTC-USD",
                    "bids": [
                        {"price": "44950.00", "size": "0.1"},
                        {"price": "44949.50", "size": "0.05"}
                    ],
                    "asks": [
                        {"price": "45050.00", "size": "0.15"},
                        {"price": "45050.50", "size": "0.08"}
                    ],
                    "time": "2024-01-15T10:30:00Z"
                }
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
        
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 250:
                return {
                    "status": "error",
                    "message": "Invalid limit parameter",
                    "details": "limit must be an integer between 1 and 250"
                }
        
        # Call the core client function
        result = client_get_public_product_book(
            product_id=product_id,
            limit=limit
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
            "message": f"Public order book retrieved successfully for {product_id}",
            "product_id": product_id,
            "limit": limit,
            "order_book": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get public order book: {str(e)}",
            "details": "An unexpected error occurred while retrieving public order book"
        } 