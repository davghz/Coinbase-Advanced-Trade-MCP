from typing import Optional, List
from tools import mcp
from core.coinbase_requests_client import list_products as list_products_api

@mcp.tool()
def list_products(
    product_type: Optional[str] = None, 
    product_ids: Optional[List[str]] = None, 
    contract_expiry_type: Optional[str] = None
) -> dict:
    """
    List all available trading products from Coinbase Advanced Trade API.
    
    This tool retrieves information about all available trading pairs and products,
    with optional filtering by product type, specific product IDs, or contract expiry.
    
    Args:
        product_type: Optional filter by product type (e.g., 'SPOT', 'FUTURE')
        product_ids: Optional list of specific product IDs to retrieve
        contract_expiry_type: Optional filter by contract expiry type
    
    Returns:
        Dictionary containing products list with details about each trading pair
        
    Example:
        >>> list_products(product_type="SPOT")
        {
            "status": "success",
            "message": "Retrieved 150 products",
            "filters": {"product_type": "SPOT"},
            "products_count": 150,
            "products": [
                {
                    "product_id": "BTC-USD",
                    "price": "45000.00",
                    "price_percentage_change_24h": "2.5",
                    "volume_24h": "1234567.89",
                    "base_currency_id": "BTC",
                    "quote_currency_id": "USD",
                    ...
                }
            ]
        }
    """
    try:
        result = list_products_api(
            product_type=product_type,
            product_ids=product_ids,
            contract_expiry_type=contract_expiry_type
        )
        
        if "error" in result:
            return {
                "status": "error",
                "message": f"Failed to retrieve products: {result.get('error')}",
                "details": result
            }
        
        products = result.get("products", [])
        
        return {
            "status": "success",
            "message": f"Retrieved {len(products)} products",
            "filters": {
                "product_type": product_type,
                "product_ids": product_ids,
                "contract_expiry_type": contract_expiry_type
            },
            "products_count": len(products),
            "products": products
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving products: {str(e)}",
            "filters": {
                "product_type": product_type,
                "product_ids": product_ids,
                "contract_expiry_type": contract_expiry_type
            }
        } 