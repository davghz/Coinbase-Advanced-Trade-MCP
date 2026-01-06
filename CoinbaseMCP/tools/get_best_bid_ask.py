from typing import List
from tools import mcp
from core.coinbase_requests_client import get_best_bid_ask as get_best_bid_ask_api

@mcp.tool()
def get_best_bid_ask(product_ids: List[str]) -> dict:
    """
    Get best bid and ask prices for specified products from Coinbase Advanced Trade API.
    
    This tool retrieves the current best bid (highest buy price) and best ask (lowest sell price)
    for one or more trading products. This is useful for getting current market spreads and prices.
    
    Args:
        product_ids: List of product identifiers to get bid/ask for (e.g., ['BTC-USD', 'ETH-USD'])
                    Maximum 100 products per request
    
    Returns:
        Dictionary containing bid/ask data for each requested product
        
    Example:
        >>> get_best_bid_ask(["BTC-USD", "ETH-USD"])
        {
            "status": "success",
            "message": "Retrieved bid/ask for 2 products",
            "product_ids": ["BTC-USD", "ETH-USD"],
            "pricebooks": [
                {
                    "product_id": "BTC-USD",
                    "bids": [{"price": "44950.00", "size": "0.1"}],
                    "asks": [{"price": "45050.00", "size": "0.15"}],
                    "time": "2024-01-15T10:30:00Z"
                },
                {
                    "product_id": "ETH-USD", 
                    "bids": [{"price": "2950.00", "size": "2.5"}],
                    "asks": [{"price": "2955.00", "size": "1.8"}],
                    "time": "2024-01-15T10:30:00Z"
                }
            ]
        }
    """
    try:
        if not product_ids:
            return {
                "status": "error",
                "message": "At least one product ID is required"
            }
            
        if len(product_ids) > 100:
            return {
                "status": "error",
                "message": "Too many products specified. Maximum 100 products per request.",
                "provided_count": len(product_ids)
            }
        
        result = get_best_bid_ask_api(product_ids)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve bid/ask: {result.get('error')}",
                "product_ids": product_ids,
                "details": result
            }
        
        pricebooks = result.get("pricebooks", [])
        
        return {
            "status": "success",
            "message": f"Retrieved bid/ask for {len(product_ids)} products",
            "product_ids": product_ids,
            "pricebooks": pricebooks
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving bid/ask: {str(e)}",
            "product_ids": product_ids
        } 