from tools import mcp
from core.coinbase_requests_client import list_payment_methods as list_payment_methods_api

@mcp.tool()
def list_payment_methods() -> dict:
    """
    List all payment methods from Coinbase Advanced Trade API.
    
    This tool retrieves all payment methods associated with your account,
    including bank accounts, cards, and other funding sources.
    
    Returns:
        Dictionary containing list of payment methods
        
    Example:
        >>> list_payment_methods()
        {
            "status": "success",
            "message": "Retrieved 2 payment methods",
            "payment_methods": [
                {
                    "id": "pm-abc123-def456",
                    "type": "ach_bank_account",
                    "name": "Chase Checking ****1234",
                    "currency": "USD",
                    "verified": true,
                    "allow_buy": true,
                    "allow_sell": true,
                    "allow_deposit": true,
                    "allow_withdraw": true
                },
                {
                    "id": "pm-xyz789-abc123",
                    "type": "card",
                    "name": "Visa ****5678",
                    "currency": "USD",
                    "verified": true,
                    "allow_buy": true,
                    "allow_sell": false,
                    "allow_deposit": false,
                    "allow_withdraw": false
                }
            ]
        }
    """
    try:
        result = list_payment_methods_api()
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve payment methods: {result.get('error')}",
                "details": result
            }
        
        payment_methods = result.get("payment_methods", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(payment_methods)} payment methods",
            "payment_methods_count": len(payment_methods),
            "payment_methods": payment_methods
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving payment methods: {str(e)}"
        }
