from typing import Optional
from tools import mcp
from core.coinbase_requests_client import get_historical_fills as fetch_historical_fills

@mcp.tool()
def get_historical_fills(product_id: Optional[str] = None, limit: int = 5) -> dict:
    """
    Fetch historical fills (completed trades) from Coinbase Advanced Trade API.
    
    This tool retrieves your recent trading activity across all products or filtered by a specific product.
    Historical fills show completed trades with details like price, size, fees, and timestamps.
    
    Args:
        product_id: Optional product symbol to filter fills (e.g., 'BTC-USD', 'ETH-USD')
        limit: Number of fills to retrieve (default: 5, max: 100)
    
    Returns:
        Dictionary containing the fills data with product_id and fills array
        
    Example:
        >>> get_historical_fills("BTC-USD", 10)
        {
            "product_id": "BTC-USD",
            "fills_count": 3,
            "fills": [
                {
                    "entry_id": "12345-abcd-6789",
                    "trade_id": "54321",
                    "order_id": "order-abc123",
                    "trade_time": "2024-01-15T10:30:00Z",
                    "product_id": "BTC-USD",
                    "price": "45000.50",
                    "size": "0.001",
                    "side": "BUY",
                    "commission": "0.45",
                    "trade_type": "FILL"
                }
            ]
        }
    """
    try:
        # Ensure limit is within acceptable range
        safe_limit = min(max(1, limit), 100)
        
        # Use the core function to fetch fills
        response = fetch_historical_fills(
            product_id=product_id.upper() if product_id else None,
            limit=safe_limit
        )
        
        # Check for errors in response
        if "error" in response:
            return {
                "error": f"API Error: {response['error']}",
                "product_id": product_id or "ALL",
                "fills_count": 0,
                "fills": []
            }
        
        # Extract fills from response
        fills = response.get("fills", [])
        
        return {
            "product_id": product_id or "ALL",
            "fills_count": len(fills),
            "fills": fills
        }
        
    except Exception as e:
        return {
            "error": f"Failed to fetch historical fills: {str(e)}",
            "product_id": product_id or "ALL",
            "fills_count": 0,
            "fills": []
        }
