from core.coinbase_requests_client import get_public_candles as client_get_public_candles
from . import mcp

@mcp.tool()
def get_public_candles(
    product_id: str,
    start_timestamp: str,
    end_timestamp: str,
    granularity: str
) -> dict:
    """
    Get historical candlestick data for a product from Coinbase Advanced Trade API (public endpoint).
    
    This is a public endpoint that doesn't require authentication and provides
    historical OHLCV (Open, High, Low, Close, Volume) candlestick data for trading analysis.
    
    Args:
        product_id: The trading pair identifier (e.g., "BTC-USD", "ETH-EUR")
        start_timestamp: The start time for candles in ISO 8601 format (e.g., "2023-01-01T00:00:00Z")
        end_timestamp: The end time for candles in ISO 8601 format (e.g., "2023-01-02T00:00:00Z")
        granularity: The time window for each candle. Valid options:
                    "UNKNOWN_GRANULARITY", "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE",
                    "THIRTY_MINUTE", "ONE_HOUR", "TWO_HOUR", "SIX_HOUR", "ONE_DAY"
    
    Returns:
        Dictionary containing candlestick data with OHLCV values
        
    Example:
        >>> get_public_candles("BTC-USD", "2024-01-01T00:00:00Z", "2024-01-02T00:00:00Z", "ONE_HOUR")
        {
            "status": "success",
            "message": "Public candle data retrieved successfully for BTC-USD",
            "product_id": "BTC-USD",
            "start_timestamp": "2024-01-01T00:00:00Z",
            "end_timestamp": "2024-01-02T00:00:00Z",
            "granularity": "ONE_HOUR",
            "candles_count": 24,
            "candles": [
                {
                    "start": "1704067200",
                    "low": "44800.50",
                    "high": "45200.75",
                    "open": "45000.00",
                    "close": "45100.25",
                    "volume": "123.456"
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
        
        if not start_timestamp or not isinstance(start_timestamp, str):
            return {
                "status": "error",
                "message": "Invalid start_timestamp parameter",
                "details": "start_timestamp must be a non-empty string in ISO 8601 format"
            }
        
        if not end_timestamp or not isinstance(end_timestamp, str):
            return {
                "status": "error",
                "message": "Invalid end_timestamp parameter",
                "details": "end_timestamp must be a non-empty string in ISO 8601 format"
            }
        
        # Validate granularity
        valid_granularities = [
            "UNKNOWN_GRANULARITY", "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE",
            "THIRTY_MINUTE", "ONE_HOUR", "TWO_HOUR", "SIX_HOUR", "ONE_DAY"
        ]
        if granularity not in valid_granularities:
            return {
                "status": "error",
                "message": "Invalid granularity parameter",
                "details": f"granularity must be one of: {', '.join(valid_granularities)}"
            }
        
        # Call the core client function
        result = client_get_public_candles(
            product_id=product_id,
            start=start_timestamp,
            end=end_timestamp,
            granularity=granularity
        )
        
        # Handle API errors
        if "error" in result:
            return {
                "status": "error",
                "message": f"API error: {result.get('error', 'Unknown error')}",
                "details": result.get("body", "No additional details"),
                "status_code": result.get("status_code")
            }
        
        candles = result.get("candles", [])
        
        return {
            "status": "success",
            "message": f"Public candle data retrieved successfully for {product_id}",
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
            "message": f"Failed to get public candles: {str(e)}",
            "details": "An unexpected error occurred while retrieving public candle data"
        } 