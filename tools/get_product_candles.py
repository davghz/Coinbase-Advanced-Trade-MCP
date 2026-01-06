# tools/get_product_candles.py

from typing import Optional # Included for consistency, though not strictly needed for this tool's signature
from tools import mcp
from core.coinbase_requests_client import get_candles as get_candles_api

@mcp.tool()
def get_product_candles(product_id: str, start_timestamp: str, end_timestamp: str, granularity: str) -> dict:
    """
    Retrieves historical candlestick data for a given product from Coinbase Advanced Trade API.

    Args:
        product_id (str): The trading pair identifier (e.g., "BTC-USD", "ETH-EUR").
        start_timestamp (str): The start time for the candles in ISO 8601 format (e.g., "2023-01-01T00:00:00Z").
        end_timestamp (str): The end time for the candles in ISO 8601 format (e.g., "2023-01-02T00:00:00Z").
        granularity (str): The time window for each candle. Valid options as per Coinbase API:
                           "UNKNOWN_GRANULARITY", "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE",
                           "THIRTY_MINUTE", "ONE_HOUR", "TWO_HOUR", "SIX_HOUR", "ONE_DAY".
    
    Returns:
        dict: A dictionary containing the candlestick data or an error message.
              On success, the response typically includes a 'candles' key with a list of candle data.
              Each candle data point usually includes: start time, low price, high price, open price, close price, and volume.
              On failure, returns a dictionary with an "error" key and details about the failure.
    """
    try:
        if not product_id:
            return {
                "status": "error",
                "message": "Product ID is required"
            }
            
        valid_granularities = [
            "UNKNOWN_GRANULARITY", "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE",
            "THIRTY_MINUTE", "ONE_HOUR", "TWO_HOUR", "SIX_HOUR", "ONE_DAY"
        ]
        
        if granularity not in valid_granularities:
            return {
                "status": "error",
                "message": f"Invalid granularity. Must be one of: {', '.join(valid_granularities)}",
                "provided_granularity": granularity
            }
        
        result = get_candles_api(product_id, start_timestamp, end_timestamp, granularity)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve candles: {result.get('error')}",
                "product_id": product_id,
                "details": result
            }
        
        candles = result.get("candles", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(candles)} candles for {product_id}",
            "product_id": product_id,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "granularity": granularity,
            "candles_count": len(candles),
            "candles": candles
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving candles: {str(e)}",
            "product_id": product_id,
            "granularity": granularity
        }
