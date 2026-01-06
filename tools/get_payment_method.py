from tools import mcp
from core.coinbase_requests_client import get_payment_method as get_payment_method_api

@mcp.tool()
def get_payment_method(payment_method_id: str) -> dict:
    """
    Get a specific payment method from Coinbase Advanced Trade API.
    
    This tool retrieves detailed information about a specific payment method
    by its ID.
    
    Args:
        payment_method_id: The ID of the payment method to retrieve
    
    Returns:
        Dictionary containing payment method details
        
    Example:
        >>> get_payment_method("pm-abc123-def456")
        {
            "status": "success",
            "message": "Payment method retrieved successfully",
            "payment_method_id": "pm-abc123-def456",
            "payment_method": {
                "id": "pm-abc123-def456",
                "type": "ach_bank_account",
                "name": "Chase Checking ****1234",
                "currency": "USD",
                "verified": true,
                "allow_buy": true,
                "allow_sell": true,
                "allow_deposit": true,
                "allow_withdraw": true,
                "limits": {
                    "buy": [...],
                    "sell": [...],
                    "deposit": [...],
                    "withdraw": [...]
                }
            }
        }
    """
    try:
        if not payment_method_id:
            return {
                "status": "error",
                "message": "Payment method ID is required"
            }
        
        result = get_payment_method_api(payment_method_id)
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve payment method: {result.get('error')}",
                "payment_method_id": payment_method_id,
                "details": result
            }
        
        return {
            "status": "success",
            "message": "Payment method retrieved successfully",
            "payment_method_id": payment_method_id,
            "payment_method": result.get("payment_method", result)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving payment method: {str(e)}",
            "payment_method_id": payment_method_id
        }
