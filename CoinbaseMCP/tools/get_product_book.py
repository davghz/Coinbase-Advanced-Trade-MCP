# tools/get_product_book.py

from typing import Optional
from tools import mcp
from core.coinbase_requests_client import get_product_book as get_product_book_api

@mcp.tool()
def get_product_book(product_id: str, limit: Optional[int] = None) -> dict:
    """
    Retrieves the order book (Level 2 data) for a given product ID from Coinbase.

    Args:
        product_id (str): The trading pair (e.g., "BTC-USD", "ETH-EUR").
        limit (Optional[int]): The number of bids and asks to return. 
                               If None, uses the API's default (currently 250). Min is 1, Max is 250.
    
    Returns:
        dict: A dictionary containing the order book data (typically 'bids' and 'asks' lists)
              or an error message.
    """
    try:
        if not product_id:
            return {
                "status": "error",
                "message": "Product ID is required"
            }
            
        if limit is not None and (limit < 1 or limit > 250):
            return {
                "status": "error",
                "message": "Limit must be between 1 and 250",
                "provided_limit": limit
            }
        
        result = get_product_book_api(product_id, limit)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve order book: {result.get('error')}",
                "product_id": product_id,
                "details": result
            }
        
        pricebook = result.get("pricebook", {})
        bids = pricebook.get("bids", [])
        asks = pricebook.get("asks", [])
        
        return {
            "status": "success",
            "message": f"Retrieved order book for {product_id}",
            "product_id": product_id,
            "limit": limit,
            "bids_count": len(bids),
            "asks_count": len(asks),
            "pricebook": pricebook
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving order book: {str(e)}",
            "product_id": product_id,
            "limit": limit
        }
