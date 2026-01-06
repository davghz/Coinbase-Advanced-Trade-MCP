from core.coinbase_requests_client import get_public_market_trades as client_get_public_market_trades
from . import mcp

@mcp.tool()
def get_public_market_trades(
    product_id: str,
    limit: int = 100
) -> dict:
    """
    Get recent market trades for a product from Coinbase Advanced Trade API (public endpoint).
    
    This is a public endpoint that doesn't require authentication and provides
    the most recent public trades for a specific trading pair, showing actual
    transactions that have occurred on the market.
    
    Args:
        product_id: The product identifier (e.g., 'BTC-USD', 'ETH-EUR')
        limit: Number of trades to retrieve (default: 100, max: 1000)
    
    Returns:
        Dictionary containing recent market trades data
        
    Example:
        >>> get_public_market_trades("BTC-USD", 10)
        {
            "status": "success",
            "message": "Retrieved 10 public market trades for BTC-USD",
            "product_id": "BTC-USD",
            "limit": 10,
            "trades": [
                {
                    "trade_id": "12345",
                    "product_id": "BTC-USD",
                    "price": "45000.50",
                    "size": "0.001",
                    "time": "2024-01-15T10:30:00Z",
                    "side": "buy",
                    "bid": "44999.00",
                    "ask": "45001.00"
                },
                ...
            ]
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
        
        if not isinstance(limit, int) or limit < 1 or limit > 1000:
            return {
                "status": "error",
                "message": "Invalid limit parameter",
                "details": "limit must be an integer between 1 and 1000"
            }
        
        # Call the core client function
        result = client_get_public_market_trades(
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
        
        trades = result.get("trades", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(trades)} public market trades for {product_id}",
            "product_id": product_id,
            "limit": limit,
            "trades": trades
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get public market trades: {str(e)}",
            "details": "An unexpected error occurred while retrieving public market trades"
        } 