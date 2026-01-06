from typing import Optional
from core.coinbase_requests_client import get_transactions_summary as client_get_transactions_summary
from . import mcp

@mcp.tool()
def get_transactions_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_native_currency: Optional[str] = None,
    product_type: Optional[str] = None,
    contract_expiry_type: Optional[str] = None
) -> dict:
    """
    Get transactions summary from Coinbase Advanced Trade API.
    
    This tool retrieves a summary of transactions within a specified date range
    with various filtering options including currency, product type, and contract expiry.
    
    Args:
        start_date: Start date in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')
        end_date: End date in ISO 8601 format (e.g., '2024-01-31T23:59:59Z')
        user_native_currency: Filter by native currency (e.g., 'USD', 'EUR')
        product_type: Filter by product type (e.g., 'SPOT', 'FUTURE')
        contract_expiry_type: Filter by contract expiry type
    
    Returns:
        Dictionary containing transaction summary data
        
    Example:
        >>> get_transactions_summary("2024-01-01T00:00:00Z", "2024-01-31T23:59:59Z", "USD")
        {
            "status": "success",
            "message": "Transaction summary retrieved successfully",
            "filters": {
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
                "user_native_currency": "USD"
            },
            "summary": {
                "total_volume": "1234.56",
                "total_fees": "12.34",
                "buy_volume": "800.00",
                "sell_volume": "434.56",
                "advanced_trade_only_volume": "1234.56",
                "advanced_trade_only_fees": "12.34",
                "coinbase_pro_volume": "0.00",
                "coinbase_pro_fees": "0.00"
            }
        }
    """
    try:
        # Validate date format if provided
        if start_date and not isinstance(start_date, str):
            return {
                "status": "error",
                "message": "Invalid start_date parameter",
                "details": "start_date must be a string in ISO 8601 format"
            }
        
        if end_date and not isinstance(end_date, str):
            return {
                "status": "error",
                "message": "Invalid end_date parameter", 
                "details": "end_date must be a string in ISO 8601 format"
            }
        
        # Call the core client function
        result = client_get_transactions_summary(
            start_date=start_date,
            end_date=end_date,
            user_native_currency=user_native_currency,
            product_type=product_type,
            contract_expiry_type=contract_expiry_type
        )
        
        # Handle API errors
        if "error" in result:
            return {
                "status": "error",
                "message": f"API error: {result.get('error', 'Unknown error')}",
                "details": result.get("body", "No additional details"),
                "status_code": result.get("status_code")
            }
        
        # Build filters object for response
        filters = {}
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        if user_native_currency:
            filters["user_native_currency"] = user_native_currency
        if product_type:
            filters["product_type"] = product_type
        if contract_expiry_type:
            filters["contract_expiry_type"] = contract_expiry_type
        
        return {
            "status": "success",
            "message": "Transaction summary retrieved successfully",
            "filters": filters,
            "summary": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get transaction summary: {str(e)}",
            "details": "An unexpected error occurred while retrieving transaction summary"
        } 