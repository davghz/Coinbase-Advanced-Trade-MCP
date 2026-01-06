from tools import mcp
from core.coinbase_requests_client import get_market_trades as get_market_trades_api

@mcp.tool()
def get_market_trades(product_id: str, limit: int = 100) -> dict:
    """
    Get recent market trades for a product from Coinbase Advanced Trade API.
    
    This tool retrieves the most recent public trades for a specific trading pair,
    showing the actual transactions that have occurred on the market.
    
    Args:
        product_id: The product identifier (e.g., 'BTC-USD', 'ETH-EUR')
        limit: Number of trades to retrieve (default: 100, max: 1000)
    
    Returns:
        Dictionary containing recent market trades data
        
    Example:
        >>> get_market_trades("BTC-USD", 10)
        {
            "status": "success",
            "message": "Retrieved 10 market trades for BTC-USD",
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
        if not product_id:
            return {
                "status": "error",
                "message": "Product ID is required"
            }
            
        if limit > 1000:
            return {
                "status": "error",
                "message": "Limit cannot exceed 1000 trades per request",
                "provided_limit": limit
            }
        
        result = get_market_trades_api(product_id, limit)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve market trades: {result.get('error')}",
                "product_id": product_id,
                "details": result
            }
        
        trades = result.get("trades", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(trades)} market trades for {product_id}",
            "product_id": product_id,
            "limit": limit,
            "trades_count": len(trades),
            "trades": trades
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving market trades: {str(e)}",
            "product_id": product_id,
            "limit": limit
        } 